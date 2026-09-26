#!/usr/bin/env python3
"""FUNN(ScTasks 正式版) vs FUNNKR(伪装 ntkrnlmp 的 KR 版) 行为差异核验：
任务标记集 / 控件名集 / 表单类 / 驱动与服务标识 / 浏览器篡改路径。
"""
import pathlib
import re

ENG = pathlib.Path('/root/dev/OpenSysprep/work/engines')
PAIRS = [('FUNN', 'FUNNKR'), ('FUNNX64', 'FUNNKRX64')]


def strs(b, minlen=6):
    a = {m.group().decode('latin1') for m in re.finditer(rb'[\x20-\x7e]{%d,}' % minlen, b)}
    w = b.decode('utf-16-le', 'ignore')
    u = {m.group() for m in re.finditer(r'[\u0020-\uffff]{%d,}' % minlen, w)
         if sum(c.isprintable() for c in m.group()) > len(m.group()) * 0.9}
    return a | u


PATTERNS = {
    'Sysprep 标记': re.compile(r'Sysprep\.[A-Za-z_]+'),
    'Cb_ 控件': re.compile(r'\bCb_[A-Za-z0-9_]+'),
    'Btn_ 控件': re.compile(r'\bBtn_[A-Za-z0-9_]+'),
    'optimize_ 项': re.compile(r'\boptimize_[A-Za-z0-9_]+'),
    '表单类': re.compile(r'\bT[A-Z][A-Za-z0-9_]{2,}Form\b'),
    '驱动/服务名': re.compile(r'\b(?:Scufd|scdrv|ScfudDevice|ForceDelete|MiniDriverInstall|DriverMessage)\b'),
    '目录/注册表': re.compile(r'(?:System32\\drivers|CurrentControlSet\\Services\\[\w\- ]+|RunOnce|SetupComplete)'),
    '浏览器路径': re.compile(r'(?:newtabx\.com|sejai\.com|Secure Preferences|Local State|User Data\\[\w\\]*)'),
}


def sets_of(b):
    S = strs(b)
    out = {}
    for name, pat in PATTERNS.items():
        hits = set()
        for s in S:
            hits |= set(pat.findall(s))
        out[name] = hits
    return out, S


data = {}
for n in ('FUNN', 'FUNNX64', 'FUNNKR', 'FUNNKRX64'):
    data[n] = sets_of((ENG / n).read_bytes())

for a, b_ in PAIRS:
    sa, Sa = data[a]
    sb, Sb = data[b_]
    print('=' * 92)
    print(f'### {a}  vs  {b_}')
    for k in PATTERNS:
        oa, ob = sa[k] - sb[k], sb[k] - sa[k]
        ca = sa[k] & sb[k]
        print(f'\n-- {k}: 共有 {len(ca)} | 仅{a} {len(oa)} | 仅{b_} {len(ob)}')
        if oa & sa[k] or ob:
            if oa:
                print(f'   仅 {a}: {sorted(oa)[:40]}')
            if ob:
                print(f'   仅 {b_}: {sorted(ob)[:40]}')

print('\n' + '=' * 92)
print('### 驱动/服务相关字符串上下文（各模块）')
for n in ('FUNN', 'FUNNKR', 'FUNNKRX64', 'FUNMKRX64'):
    b = (ENG / n).read_bytes()
    print(f'\n-- {n}:')
    seen = set()
    for pat in (rb'System32\\drivers', rb'MiniDriverInstall', rb'DriverMessage', rb'Scufd', rb'scdrv', rb'ForceDelete'):
        for m in list(re.finditer(re.escape(pat), b))[:3]:
            h = m.start()
            ctx = b[max(0, h - 60):h + 70]
            s = '·'.join(x.decode('latin1') for x in re.findall(rb'[\x20-\x7e]{4,}', ctx))
            key = (pat, s[:60])
            if key in seen:
                continue
            seen.add(key)
            print(f'     [{pat.decode()}] {s[:150]}')
