#!/usr/bin/env python3
"""FUNN 家族（ScTasks 部署引擎）四变体对比：
版本信息 / 架构 / 导入 / 资源 / 字符串差集 / 篡改标识与伪装标识。
"""
import pathlib
import re
import subprocess
import sys
import tempfile

import pefile

ENG = pathlib.Path('/root/dev/OpenSysprep/work/engines')
ORIG = pathlib.Path('/root/dev/scpt-analysis/02-resources/DATA')
FAM = ['FUNN', 'FUNNX64', 'FUNNKR', 'FUNNKRX64']
VKEYS = ['CompanyName', 'FileDescription', 'FileVersion', 'InternalName',
         'LegalCopyright', 'OriginalFilename', 'ProductName', 'ProductVersion', 'Comments']
TAMPER = ['newtabx', 'sejai', 'hao_pg', '90013418', 'prefs_enclave', 'Secure Preferences', 'BLBeacon', 'setedge']
DISGUISE = ['ntkrnlmp', 'NT Kernel & System', 'Microsoft Corporation', 'Windows Operating System']
INTEREST = ['browser', 'chrome', 'edge', 'iexplore', 'newtab', 'homepage', '主页', '首页', '收藏夹',
            'scdrv', 'scufd', 'ntkrnl', 'kernel', 'driver', 'sysprep', '部署', '任务', '锁', '权限',
            'sysceo', 'union', '联盟', 'tcp', 'dns', 'ip', 'netsh', 'reg add', 'schtasks', 'runonce',
            'oem', 'taskbar', 'defprof', 'ntuser']


def strings_of(b, minlen=6):
    out = set()
    for m in re.finditer(rb'[\x20-\x7e]{%d,}' % minlen, b):
        out.add(m.group().decode())
    try:
        w = b.decode('utf-16-le', 'ignore')
        for m in re.finditer(r'[\u0020-\uffff]{%d,}' % minlen, w):
            s = m.group()
            if sum(c.isprintable() for c in s) > len(s) * 0.9:
                out.add(s)
    except Exception:
        pass
    return out


def ver_info(path):
    b = path.read_bytes()
    i = b.find('VS_VERSION_INFO'.encode('utf-16-le'))
    if i < 0:
        return {}
    w = b[i:i + 8192].decode('utf-16-le', 'ignore')
    toks = [t.strip() for t in w.split('\x00') if t.strip()]
    out = {}
    for j, t in enumerate(toks):
        if t in VKEYS and j + 1 < len(toks) and toks[j + 1] not in VKEYS:
            out.setdefault(t, toks[j + 1])
    return out


rows = {}
for name in FAM:
    p = ENG / name
    b = p.read_bytes()
    pe = pefile.PE(str(p), fast_load=True)
    pe.parse_data_directories(directories=[
        pefile.DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_IMPORT'],
        pefile.DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_RESOURCE']])
    imps = {}
    for e in getattr(pe, 'DIRECTORY_ENTRY_IMPORT', []):
        fns = set()
        for imp in e.imports:
            fns.add(imp.name.decode() if imp.name else f'#{imp.ordinal}')
        imps[e.dll.decode()] = fns
    res = {}
    try:
        for t in pe.DIRECTORY_ENTRY_RESOURCE.entries:
            res[str(t.name or t.id)] = sum(len(getattr(n, 'directory', None).entries)
                                           if hasattr(n, 'directory') and n.directory else 1
                                           for n in (getattr(t.directory, 'entries', []) or [])
                                           )
    except Exception:
        pass
    S = strings_of(b)
    rows[name] = dict(size=len(b), ver=ver_info(p), machine=f'{pe.FILE_HEADER.Machine:#x}',
                      sub=pe.OPTIONAL_HEADER.Subsystem, ts=pe.FILE_HEADER.TimeDateStamp,
                      secs=[(s.Name.rstrip(b'\0').decode(), s.Misc_VirtualSize) for s in pe.sections],
                      imports={k: sorted(v) for k, v in imps.items()}, res=res,
                      strings=S, sections=list(pe.sections))
    pe.close()

print('=' * 100)
for name in FAM:
    r = rows[name]
    v = r['ver']
    print(f"\n### {name}  {r['size']:,}B  machine={r['machine']} sub={r['sub']} ts={r['ts']} ({r['ts']})")
    for k in VKEYS:
        if v.get(k):
            print(f"    {k:18s}= {v[k]}")
    print(f"    节区: {', '.join(n for n, _ in r['secs'])}")
    print(f"    导入 DLL({len(r['imports'])}): {', '.join(sorted(r['imports']))}")
    print(f"    资源类型: {r['res']}")
    low = str(r['ver']).lower()
    print(f"    伪装标识: {[d for d in DISGUISE if d.lower() in low]}")
    raw = (ENG / name).read_bytes().lower()
    print(f"    篡改标识: {[t for t in TAMPER if t.lower().encode() in raw or t.lower().encode('utf-16-le') in raw]}")

print('\n' + '=' * 100)
print('### 字符串差集（同一架构内比较）')
for a, b_ in (('FUNN', 'FUNNKR'), ('FUNNX64', 'FUNNKRX64')):
    sa, sb = rows[a]['strings'], rows[b_]['strings']
    only_a, only_b, common = sa - sb, sb - sa, sa & sb
    print(f"\n--- {a}({len(sa)}) vs {b_}({len(sb)}): 共有={len(common)} 仅{a}={len(only_a)} 仅{b_}={len(only_b)}")
    for lab, st in ((f'仅 {a}', only_a), (f'仅 {b_}', only_b)):
        hits = sorted({s for s in st if any(k in s.lower() for k in INTEREST)})
        print(f"   {lab} 关键命中 {len(hits)}:")
        for s in hits[:45]:
            print('      ', s[:110])
print('\n### 导入差异（x86 内）')
ia, ib = rows['FUNN']['imports'], rows['FUNNKR']['imports']
print('  DLL 差:', set(ia) - set(ib), set(ib) - set(ia))
for d in sorted(set(ia) & set(ib)):
    oa, ob = set(ia[d]) - set(ib[d]), set(ib[d]) - set(ia[d])
    if oa or ob:
        print(f'  {d}: 仅FUNN={sorted(oa)[:12]}  仅FUNNKR={sorted(ob)[:12]}')
