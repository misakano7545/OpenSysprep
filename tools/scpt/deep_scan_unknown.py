#!/usr/bin/env python3
"""深挖未知模块：FUNA/FUNH/FUNI/FUNQ/FUNV/PUBCH/PUBCI + 三个 FUNN 内嵌组件。

输出每个模块的：类型、版本信息、区分性字符串（前 40 条）。
"""
import pathlib
import re
import subprocess

BASE = pathlib.Path('/root/dev/OpenSysprep')
ENG = BASE / 'work/engines'
AN = BASE / 'work/analysis'

TARGETS = ['FUNA', 'FUNH', 'FUNI', 'FUNQ', 'FUNV', 'PUBCH', 'PUBCI',
           'FUNA_embed.raw', 'FUNB_embed.raw', 'FUNC_embed.raw']


def printable_strings(b, minlen=6, limit=40):
    out = []
    # ASCII
    for m in re.finditer(rb'[\x20-\x7e]{%d,120}' % minlen, b):
        out.append(('A', m.group().decode('latin1')))
    # UTF-16LE (含中文)
    for m in re.finditer(rb'(?:[\x20-\x7e]\x00|[\x00-\xff][\x4e-\x9f]){%d,120}' % minlen, b):
        try:
            s = m.group().decode('utf-16-le', 'ignore')
        except Exception:
            continue
        s = s.strip()
        if len(s) >= minlen:
            out.append(('U', s))
    return out


def noise(s):
    bad = ('KERNEL32', 'USER32', 'GDI32', 'ADVAPI32', 'OLE32', 'OLEAUT32',
           'msvcrt', 'comctl32', 'shell32', 'shlwapi', 'version.dll', 'winspool',
           'CFG', 'SYSTEM\\CurrentControlSet', 'TForm', 'TButton', 'TLabel',
           'Delphi', 'Embarcadero', 'CodeGear', 'Borland', 'System.pas',
           'System.', 'Vcl.', 'Winapi.', 'Unit', '.rsrc', '!This program',
           'Rich', 'PELauncher', 'PAGEx', 'EXCEPT')
    return any(k.lower() in s.lower() for k in bad)


def main():
    lines = ['# SCPT 未知模块深挖（原始输出）', '']
    for name in TARGETS:
        f = ENG / name
        if not f.is_file():
            lines.append(f'## {name}\n\n(文件不存在)\n')
            continue
        b = f.read_bytes()
        t = subprocess.run(['file', '-b', str(f)], capture_output=True, text=True).stdout.strip()
        lines.append(f'## {name}  ({len(b)} bytes)')
        lines.append(f'- 类型: {t}')
        # 可读文本文件直接打印前 60 行
        if 'INFormation' in t or name in ('FUNA', 'FUNI'):
            try:
                txt = b.decode('utf-16-le', 'ignore')
                if txt.count('\x00') > len(txt) * 0.3:
                    txt = b.decode('latin1')
            except Exception:
                txt = b.decode('latin1', 'ignore')
            keep = [l.strip() for l in re.split(r'[\r\n]+', txt) if l.strip()]
            lines.append('- 文本内容（前 60 行）:')
            lines += [f'  {l[:150]}' for l in keep[:60]]
        else:
            strs = printable_strings(b)
            seen, keep = set(), []
            for kind, s in strs:
                if noise(s) or s in seen:
                    continue
                seen.add(s)
                keep.append((kind, s))
                if len(keep) >= 40:
                    break
            lines.append('- 区分性字符串:')
            lines += [f'  [{k}] {s[:130]}' for k, s in keep]
        lines.append('')
        print(f'{name}: {t} | strings={len(keep)}')
    (AN / 'unknown_modules.md').write_text('\n'.join(lines), encoding='utf-8')
    print(f'\n输出: {AN/"unknown_modules.md"}')


if __name__ == '__main__':
    main()
