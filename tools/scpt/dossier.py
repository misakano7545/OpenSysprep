#!/usr/bin/env python3
"""SCPT 全模块 dossier 生成器：对 work/engines 下每个模块产出身份/结构/导入/资源/特征字符串。

输出:
  work/analysis/dossier.json
  docs/analysis/module-dossiers.md   （人工校订前的自动稿；定性结论在 module-map.md）
"""
import hashlib
import json
import pathlib
import re
import struct

import pefile

ROOT = pathlib.Path('/root/dev/OpenSysprep')
ENG = ROOT / 'work/engines'
OUTD = ROOT / 'work/analysis'
DOCD = ROOT / 'docs/analysis'

RT = {1: 'CURSOR', 2: 'BITMAP', 3: 'ICON', 4: 'MENU', 5: 'DIALOG', 6: 'STRING', 7: 'FONTDIR',
      8: 'FONT', 9: 'ACCELERATOR', 10: 'RCDATA', 11: 'MESSAGETABLE', 12: 'GROUP_CURSOR',
      14: 'GROUP_ICON', 16: 'VERSION', 17: 'DLGINCLUDE', 19: 'PLUGPLAY', 20: 'VXD',
      21: 'ANICURSOR', 22: 'ANIICON', 23: 'HTML', 24: 'MANIFEST'}

CATS = {
    '浏览器篡改': ['newtabx', 'sejai', 'hao_pg', '90013418', 'prefs_enclave', 'Secure Preferences', 'BLBeacon', 'setedge', 'broscfg'],
    '浏览器': ['Internet Explorer', 'Chromium', 'chrome', 'msedge', 'iexplore', 'User Data', 'homepage', 'startup_urls', '收藏夹'],
    'sysprep': ['sysprep', 'generalize', 'oobe', 'unattend', 'Panther', 'setupcl', 'setupcomplete'],
    '驱动': ['pnputil', 'dism.exe', 'DriverStore', 'SRS', 'scdrv', 'Scufd', 'ForceDelete', 'MiniDriverInstall', '.sys'],
    '部署': ['ScTasks', 'ScDeploy', 'Scdata', 'RunOnce', 'Deploy', 'tasklist'],
    '用户配置': ['ForensiT', 'DefProf', 'NTUSER.DAT', 'SCRUNTEMP'],
    '压缩': ['Igor Pavlov', '7-Zip', '7z.exe', '7z.dll', 'AbZipper', 'aria2', 'xunlei', '迅雷'],
    'ACL': ['SetACL', 'Helge Klein', 'EditSecurity', 'AUTHZ'],
    'OEM': ['OEM'],
    '任务栏': ['taskbar', '任务栏'],
    '网络': ['netsh', 'ipconfig', 'rasdial', '宽带连接'],
    '总裁系': ['Sysceo', '系统总裁', 'scpt'],
    '伪装': ['ntkrnlmp', 'NT Kernel & System', 'Microsoft Time-Stamp', 'ntkrnlup'],
    '虚拟机': ['VMware', 'VirtualBox', '虚拟机'],
    '推广': ['AppBox', '软件魔盒', 'union', '计费', 'Mbox'],
}

FILEINFO_KEYS = ['CompanyName', 'FileDescription', 'FileVersion', 'InternalName', 'LegalCopyright',
                 'OriginalFilename', 'ProductName', 'ProductVersion', 'Comments']


def version_info(b):
    """从原始字节解析 VS_VERSIONINFO。

    注意: String 结构是 wLength/wValueLength/wType + szKey, 因此按 NUL 切分后
    **键名会粘上前一个字段的尾部字节**（如 'L\\x16\\x01CompanyName'）；必须用后缀匹配，
    否则永远解析不出任何字段（旧版 full_inventory.py 即因此全表为空）。
    """
    i = b.find('VS_VERSION_INFO'.encode('utf-16-le'))
    if i < 0:
        return {}
    w = b[i:i + 8192].decode('utf-16-le', 'ignore')
    toks = [t.strip() for t in w.split('\x00') if t.strip()]
    out = {}
    for j, t in enumerate(toks):
        if j + 1 >= len(toks):
            break
        for k in FILEINFO_KEYS:
            if t.endswith(k) and not any(toks[j + 1].endswith(k2) for k2 in FILEINFO_KEYS):
                out.setdefault(k, toks[j + 1])
    return out



def strings_of(b, minlen=6):
    a = {m.group().decode() for m in re.finditer(rb'[\x20-\x7e]{%d,}' % minlen, b)}
    w = b.decode('utf-16-le', 'ignore')
    u = {m.group() for m in re.finditer(r'[\u0020-\uffff]{%d,}' % minlen, w)
         if sum(c.isprintable() for c in m.group()) > len(m.group()) * 0.9}
    return a | u


def classified(strs):
    out = {}
    for cat, kws in CATS.items():
        hits = sorted({s for s in strs if any(k.lower() in s.lower() for k in kws)})
        if hits:
            out[cat] = hits
    return out


def analyse(path):
    b = path.read_bytes()
    d = dict(name=path.name, size=len(b),
             sha256=hashlib.sha256(b).hexdigest(), raw_mz=b[:2] == b'MZ')
    try:
        pe = pefile.PE(str(path), fast_load=True)
        pe.parse_data_directories(directories=[
            pefile.DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_IMPORT'],
            pefile.DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_EXPORT'],
            pefile.DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_RESOURCE']])
        d['machine'] = f"{pe.FILE_HEADER.Machine:#x}"
        d['arch'] = {0x14c: 'x86', 0x8664: 'x64'}.get(pe.FILE_HEADER.Machine, hex(pe.FILE_HEADER.Machine))
        d['subsystem'] = pe.OPTIONAL_HEADER.Subsystem
        d['ts'] = pe.FILE_HEADER.TimeDateStamp
        d['sections'] = [[s.Name.rstrip(b'\0').decode('latin1'), s.Misc_VirtualSize, s.SizeOfRawData]
                         for s in pe.sections]
        d['packed'] = any(s[0].startswith('UPX') for s in d['sections'])
        d['version'] = version_info(b)
        d['imports'] = {}
        for e in getattr(pe, 'DIRECTORY_ENTRY_IMPORT', []):
            fns = [(i.name.decode('utf-8', 'replace') if i.name else f'#{i.ordinal}') for i in e.imports]
            d['imports'][e.dll.decode('utf-8', 'replace')] = sorted(set(fns))
        d['exports'] = sorted({(x.name.decode('utf-8', 'replace') if x.name else f'#{x.ordinal}')
                               for x in getattr(getattr(pe, 'DIRECTORY_ENTRY_EXPORT', None), 'symbols', [])})
        res = {}
        names = {}
        try:
            for t in pe.DIRECTORY_ENTRY_RESOURCE.entries:
                tid = t.name.decode() if t.name else (RT.get(t.id, str(t.id)))
                kids = getattr(t.directory, 'entries', []) or []
                res[tid] = len(kids)
                if tid in ('RCDATA', 'DATA'):
                    names[tid] = sorted((k.name.decode('utf-8', 'replace') if k.name else f'#{k.id}')
                                        for k in kids)
        except Exception as ex:
            d['resource_error'] = str(ex)
        d['resources'] = res
        d['resource_names'] = names
        d['entrypoint'] = f"{pe.OPTIONAL_HEADER.AddressOfEntryPoint:#x}"
        pe.close()
    except Exception as ex:
        d['pe_error'] = str(ex)
    S = strings_of(b)
    d['n_strings'] = len(S)
    cls = classified(S)
    d['hits'] = {k: len(v) for k, v in cls.items()}
    d['hit_samples'] = {k: v[:6] for k, v in cls.items()}
    d['pdb'] = sorted({m for m in S if m.lower().endswith('.pdb')})[:8]
    d['dllnames'] = sorted({m for m in S if re.fullmatch(r'[\w\-\.]{3,32}\.(dll|DLL)', m)})[:20]
    d['urls'] = sorted({m for m in S if m.startswith('http')})[:5]
    return d


def main():
    mods = []
    for p in sorted(ENG.iterdir()):
        if not p.is_file() or p.name.endswith(('.unp', '.raw', '.bin')) or p.name.endswith('.unpacked.exe'):
            continue
        mods.append(analyse(p))
    (OUTD / 'dossier.json').write_text(json.dumps(mods, ensure_ascii=False, indent=1), encoding='utf-8')

    L = ['# SCPT 全模块 dossier（自动生成）', '',
         f'> 输入：`work/engines/`（{len(mods)} 个文件：模块 + 内嵌组件 + 主程序脱壳副本）。',
         '> 版本信息/导入/资源由 pefile 解析；字符串为 ASCII + UTF-16 双编码提取。',
         '> 本文件是**原始证据稿**；功能定性与 Rust 方案见 `docs/analysis/module-map.md`。', '']
    L += ['## 汇总表', '',
          '| 模块 | 大小 | 架构 | 版本信息(CompanyName / FileDescription) | 导入DLL | 资源类型 | 关键词命中 |',
          '|---|---:|---|---|---:|---|---|']
    for m in mods:
        v = m.get('version', {})
        ident = ' / '.join(x for x in (v.get('CompanyName'), v.get('FileDescription'), v.get('ProductName')) if x) or '-'
        L.append('| `{}` | {:,} | {} | {} | {} | {} | {} |'.format(
            m['name'], m['size'], m.get('arch', '-'), ident[:60],
            len(m.get('imports', {})),
            ','.join(f'{k}×{n}' for k, n in sorted(m.get('resources', {}).items())) or '-',
            ', '.join(f'{k}×{n}' for k, n in sorted(m.get('hits', {}).items())) or '-'))
    L.append('')
    for m in mods:
        L.append(f"### `{m['name']}`")
        L.append(f"- 大小 `{m['size']:,}` · sha256 `{m['sha256'][:16]}…` · 架构 `{m.get('arch','-')}`"
                 f" · 子系统 `{m.get('subsystem','-')}` · 入口 `{m.get('entrypoint','-')}` · 时间戳 `{m.get('ts','-')}`")
        v = m.get('version', {})
        if v:
            L.append('- 版本信息: ' + ' · '.join(f'{k}=`{x}`' for k, x in v.items() if k != 'FileVersionRaw')[:400])
        else:
            L.append('- 版本信息: 无')
        L.append(f"- 节区({len(m.get('sections', []))}): " + ', '.join(f"`{n}`" for n, _, _ in m.get('sections', [])))
        im = m.get('imports', {})
        L.append(f"- 导入({len(im)} DLL): " + ', '.join(f"`{k}`({len(vv)})" for k, vv in sorted(im.items()))[:600])
        if m.get('exports'):
            L.append(f"- 导出({len(m['exports'])}): " + ', '.join(f'`{x}`' for x in m['exports'][:20]))
        res = m.get('resources', {})
        if res:
            L.append('- 资源: ' + ', '.join(f'{k}×{n}' for k, n in sorted(res.items())))
        for k, vs in m.get('resource_names', {}).items():
            L.append(f"- {k} 条目({len(vs)}): " + ', '.join(f'`{x}`' for x in vs[:30]))
        if m.get('pdb'):
            L.append('- PDB: ' + ', '.join(f'`{x}`' for x in m['pdb']))
        if m.get('dllnames'):
            L.append('- 内含 DLL 名: ' + ', '.join(f'`{x}`' for x in m['dllnames'][:14]))
        if m.get('urls'):
            L.append('- URL: ' + ', '.join(f'`{x}`' for x in m['urls']))
        L.append(f"- 字符串总数 `{m.get('n_strings','-')}`；关键词命中: "
                 + (', '.join(f'{k}×{n}' for k, n in sorted(m.get('hits', {}).items())) or '无'))
        for k, vs in m.get('hit_samples', {}).items():
            L.append(f"  - {k}: " + ' | '.join(f'`{s[:70]}`' for s in vs[:4]))
        L.append('')
    (DOCD / 'module-dossiers.md').write_text('\n'.join(L), encoding='utf-8')
    print(f"写成 {OUTD/'dossier.json'} 与 {DOCD/'module-dossiers.md'}（{len(mods)} 模块）")


if __name__ == '__main__':
    main()
