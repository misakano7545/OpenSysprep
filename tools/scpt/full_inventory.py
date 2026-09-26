#!/usr/bin/env python3
"""SCPT 全量模块盘点：逐个模块提取身份信息 + 类别关键词命中 + 加壳状态。

输入:
  - work/engines/                       (已解包/原样的模块文件)
  - ../scpt-analysis/02-resources/DATA/<NAME>/2052  (原始,可能带壳)

输出:
  - work/analysis/full_inventory.json
  - work/analysis/full_inventory.md
"""
import json
import pathlib
import re
import subprocess

BASE = pathlib.Path('/root/dev/OpenSysprep')
ENG = BASE / 'work/engines'
ORIG = pathlib.Path('/root/dev/scpt-analysis/02-resources/DATA')
OUTD = BASE / 'work/analysis'

CATS = {
    '浏览器篡改': ['newtabx', 'sejai', 'hao_pg', '90013418', 'prefs_enclave', 'Secure Preferences', 'BLBeacon'],
    '浏览器': ['Internet Explorer', 'Chromium', 'User Data', 'homepage', 'startup_urls'],
    'sysprep': ['sysprep', 'generalize', 'oobe', 'unattend', 'Panther', 'setupcl'],
    '驱动': ['pnputil', 'dism.exe', 'DriverStore', 'SRS'],
    '部署': ['ScTasks', 'ScDeploy', 'Scdata', 'RunOnce', 'Deploy'],
    '用户配置': ['ForensiT', 'DefProf', 'NTUSER.DAT', 'SCRUNTEMP'],
    '压缩': ['Igor Pavlov', '7-Zip', '7z.exe', '7z.dll'],
    'ACL': ['SetACL', 'Helge Klein'],
    'OEM': ['OEM'],
    '任务栏': ['taskbar', '任务栏'],
    '网络': ['netsh', 'ipconfig'],
    '总裁系': ['Sysceo', '系统总裁', 'scpt'],
    'Delphi': ['Borland', 'Embarcadero', 'DVCLAL'],
    '虚拟机': ['VMware', 'VirtualBox', '虚拟机'],
    '安全软件': ['杀毒', '安全软件', 'Defender'],
}

VKEYS = ['CompanyName', 'FileDescription', 'FileVersion', 'InternalName',
         'LegalCopyright', 'OriginalFilename', 'ProductName', 'ProductVersion', 'Comments']


def file_type(p: pathlib.Path) -> str:
    return subprocess.run(['file', '-b', str(p)], capture_output=True, text=True).stdout.strip()


def version_info(b: bytes) -> dict:
    mag = 'VS_VERSION_INFO'.encode('utf-16-le')
    i = b.find(mag)
    if i < 0:
        return {}
    w = b[i:i + 8192].decode('utf-16-le', 'ignore')
    toks = [t.strip() for t in w.split('\x00')]
    toks = [t for t in toks if t]
    out = {}
    for j, t in enumerate(toks):
        if t in VKEYS and j + 1 < len(toks) and toks[j + 1] not in VKEYS:
            out[t] = toks[j + 1]
    return out


def scan_cats(b: bytes) -> dict:
    low = b.lower()
    res = {}
    for cat, kws in CATS.items():
        n = 0
        for kw in kws:
            ka = kw.lower().encode('latin1', 'ignore')
            ku = kw.lower().encode('utf-16-le', 'ignore')
            if ka:
                n += low.count(ka)
            if ku and ku != ka:
                n += low.count(ku)
        if n:
            res[cat] = n
    return res


def main():
    rows = []
    files = [f for f in sorted(ENG.iterdir()) if f.is_file()
             and not f.name.endswith('.unp')
             and f.name not in ('funn_unpacked.exe', 'funnkrx64_unpacked.exe')]
    for f in files:
        b = f.read_bytes()
        name = f.name
        orig = ORIG / name.replace('_embed.raw', '')
        packed = ''
        op = orig / '2052'
        if op.is_file():
            ob = op.read_bytes()
            if b'UPX!' in ob[:4000] or b'UPX!' in ob:
                packed = 'UPX(原包)'
        v = version_info(b)
        cats = scan_cats(b)
        rows.append({
            'name': name,
            'size': len(b),
            'type': file_type(f),
            'packed': packed,
            'version': v,
            'cats': cats,
        })
        print(f"{name:18s} {len(b):>10} {packed:10s} {v.get('CompanyName','-')[:28]:28s} {sorted(cats.keys())}")

    (OUTD / 'full_inventory.json').write_text(
        json.dumps(rows, ensure_ascii=False, indent=1), encoding='utf-8')

    lines = ['# SCPT 全模块盘点（自动扫描原始输出）', '',
             '| 模块 | 大小 | 类型 | 加壳 | CompanyName | FileDescription | ProductName | InternalName | OriginalFilename | 类别命中 |',
             '|---|---:|---|---|---|---|---|---|---|---|']
    for r in rows:
        v = r['version']
        cells = [
            r['name'], f"{r['size']}", r['type'][:38], r['packed'] or '-',
            v.get('CompanyName', '-'), v.get('FileDescription', '-'),
            v.get('ProductName', '-'), v.get('InternalName', '-'),
            v.get('OriginalFilename', '-'),
            ', '.join(f'{k}×{n}' for k, n in sorted(r['cats'].items())),
        ]
        lines.append('| ' + ' | '.join(c.replace('|', '/') for c in cells) + ' |')
    (OUTD / 'full_inventory.md').write_text('\n'.join(lines), encoding='utf-8')
    print(f"\n== 输出: {OUTD/'full_inventory.json'} / full_inventory.md  ({len(rows)} 个模块)")


if __name__ == '__main__':
    main()
