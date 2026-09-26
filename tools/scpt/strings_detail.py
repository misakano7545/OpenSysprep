#!/usr/bin/env python3
"""剩余模块的区分性字符串（过滤噪声，只留路径/注册表/命令/中文短语）。

输出: work/analysis/strings_detail.md
"""
import pathlib
import re

ENG = pathlib.Path('/root/dev/OpenSysprep/work/engines')
OUT = pathlib.Path('/root/dev/OpenSysprep/work/analysis/strings_detail.md')

TARGETS = ['FUNB', 'FUNC', 'FUND', 'FUNE', 'FUNF', 'FUNFX64', 'FUNG', 'FUNGX64',
           'FUNO', 'FUNP', 'FUNR', 'FUNT', 'FUNU', 'FUNX', 'FUNY', 'FUNZ',
           'PUBCA', 'PUBCB', 'PUBCC', 'PUBCD', 'PUBCE', 'PUBCF', 'PUBCG', 'PUBCH', 'PUBCI']

NOISE = ('kernel32', 'user32', 'gdi32', 'advapi32', 'ole32', 'oleaut32', 'msvcrt',
         'comctl32', 'shell32', 'shlwapi', 'winspool', 'cfgmgr32', 'setupapi',
         'delphi', 'embarcadero', 'borland', 'codegear', 'system.pas', 'vcl.',
         'system.', 'winapi.', 'tform', 'tbutton', 'tlabel', 'tpanel', 'tbitmap',
         'this program cannot', 'program must be run', '.rsrc', '.reloc', '.idata',
         '.rdata', '.data', '.text', '.itext', '.didata', '.edata', 'rich',
         'null', 'stringfileinfo', 'varfileinfo', 'translation')


def keep(s: str) -> bool:
    low = s.lower()
    if any(n in low for n in NOISE):
        return False
    if len(s) < 5:
        return False
    # 路径 / 注册表 / 命令 / 中文
    if any(t in s for t in ('\\', '/', 'HKLM', 'HKCU', 'SOFTWARE', 'Microsoft\\',
                            '.exe', '.dll', '.ini', '.inf', '.sys', '.bat', '.cmd',
                            '.reg', '.txt', '.jpg', '.bmp', '.ico', '.cab', '.msi')):
        return True
    if re.search(r'[\u4e00-\u9fff]', s):
        return True
    if re.match(r'^[A-Za-z][A-Za-z0-9 _\-\.]{8,}$', s):
        return True
    return False


def extract(b: bytes):
    out = []
    for m in re.finditer(rb'[\x20-\x7e]{5,160}', b):
        s = m.group().decode('latin1')
        if keep(s):
            out.append(s.strip())
    for m in re.finditer(rb'(?:[\x20-\x7e]\x00){5,160}', b):
        s = m.group().decode('utf-16-le', 'ignore').strip()
        if keep(s):
            out.append(s)
    # 去重保序
    seen, res = set(), []
    for s in out:
        if s not in seen:
            seen.add(s)
            res.append(s)
    return res


def main():
    lines = ['# 剩余模块区分性字符串（原始输出）', '']
    for name in TARGETS:
        f = ENG / name
        if not f.is_file():
            continue
        b = f.read_bytes()
        strs = extract(b)
        lines.append(f'## {name}  ({len(b)} bytes, {len(strs)} 条)')
        lines += [f'  {s[:150]}' for s in strs[:60]]
        lines.append('')
        print(f'{name:10s} {len(strs):5d} 条  ' + ' | '.join(strs[:3])[:100])
    OUT.write_text('\n'.join(lines), encoding='utf-8')
    print(f'\n输出: {OUT}')


if __name__ == '__main__':
    main()
