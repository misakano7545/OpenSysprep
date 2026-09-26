#!/usr/bin/env python3
"""从 objdump 反汇编构建「函数图 + 字面量交叉引用」索引（只读，不执行样本）。

思路：不装反编译器，用两份已有数据叉乘
  ① objdump 反汇编里的 call/jmp 目标 + (bad) 数据区   → 函数边界
  ② 镜像里的 UTF-16 字面量（Delphi 2009+ 字符串常量）在 .text 里的绝对引用 → 函数 → 用了哪个路径/注册表/API
理由：Delphi 把 API 名和路径都存成 UTF-16 常量，代码用绝对地址引用（实测 3,750/9,503 命中），
     所以「谁调用了 DeviceIoControl / 谁写了这条注册表」可以直接查表，不需要伪代码。

用法: xref.py <Scpt.unpacked.exe> <Scpt.text.asm> <输出目录>
产物: functions.tsv、literal-xref.tsv
"""
import bisect
import pathlib
import re
import struct
import sys

import pefile

LINE = re.compile(r'^\s+([0-9a-f]+):\t(.*)$')
CALLTGT = re.compile(r'(?:call|jmp)\s+(?:DWORD PTR ds:)?0x([0-9a-f]+)')
CATEGORY = [
    ('注册表', re.compile(r'HKEY_|SYSTEM\\\\CurrentControlSet|SOFTWARE\\\\')),
    ('URL', re.compile(r'^https?://', re.I)),
    ('路径', re.compile(r'\\\\|\.(?:exe|dll|sys|sc|ini|inf|dat|png|bmp|jpg|ico)$', re.I)),
    ('API', re.compile(r'^[A-Z][A-Za-z0-9_]{4,40}(?:W|A|Ex|ExW|ExA)?$')),
]


def load(exe):
    pe = pefile.PE(str(exe), fast_load=True)
    raw = exe.read_bytes()
    ib = pe.OPTIONAL_HEADER.ImageBase
    t = [s for s in pe.sections if s.Name.startswith(b'.text')][0]
    return pe, raw, ib, t, raw[t.PointerToRawData:t.PointerToRawData + t.SizeOfRawData]


def literals(raw, ib, secs):
    """UTF-16LE 字面量 → VA（取每个字面量第一次出现的位置）"""
    out = {}
    for m in re.finditer(rb'(?:[\x20-\x7e]\x00){6,}', raw):
        off = m.start()
        for s in secs:
            if s.PointerToRawData <= off < s.PointerToRawData + s.SizeOfRawData:
                va = ib + s.VirtualAddress + (off - s.PointerToRawData)
                out.setdefault(va, m.group().decode('utf-16-le'))
                break
    return out


def classify(s):
    for name, pat in CATEGORY:
        if pat.search(s):
            return name
    return '其他'


def main(exe, asm, outdir):
    pe, raw, ib, tsec, code = load(exe)
    code0 = ib + tsec.VirtualAddress
    code_end = code0 + len(code)

    # ① 函数边界：**call 目标**（jmp 多为尾调用/数据误码，会把函数数灌到 10 万级）；剔除落在 (bad) 数据区里的
    targets, calls, bad = set(), [], []
    for line in open(asm, errors='replace'):
        m = LINE.match(line)
        if not m:
            continue
        a = int(m.group(1), 16)
        body = m.group(2)
        if body.startswith('(bad)'):
            bad.append(a)
            continue
        if body.startswith('call'):
            c = CALLTGT.search(body)
            if c:
                targets.add(int(c.group(1), 16))
                calls.append((a, int(c.group(1), 16)))
    badset = set(bad)
    starts = sorted(x for x in targets if code0 <= x < code_end and x not in badset)
    starts += [code0]                                  # 段首也算一个入口（可能不在 call 目标里）

    def owner(addr):
        i = bisect.bisect_right(starts, addr) - 1
        return starts[i] if i >= 0 else None

    caller_cnt = {}
    callee_cnt = {}
    for site, tgt in calls:
        o = owner(site)
        if o is not None:
            caller_cnt[o] = caller_cnt.get(o, 0) + 1
        if code0 <= tgt < code_end:
            callee_cnt[tgt] = callee_cnt.get(tgt, 0) + 1

    od = pathlib.Path(outdir)
    od.mkdir(parents=True, exist_ok=True)
    with (od / 'functions.tsv').open('w') as f:
        f.write('start\tend\tsize\tcall_sites\tin_calls\n')
        for i, s in enumerate(starts):
            e = starts[i + 1] if i + 1 < len(starts) else code_end
            f.write(f'{s:#010x}\t{e:#010x}\t{e-s}\t{caller_cnt.get(s,0)}\t{callee_cnt.get(s,0)}\n')

    # ② 字面量 → 引用它的代码地址 → 所在函数
    lits = literals(raw, ib, pe.sections)
    va2lit = dict(lits)          # 字面量可以在任何节区：Delphi 把常量字符串也放在 .text 里
    refs = []
    mv = memoryview(code)
    for i in range(len(code) - 4):
        v = struct.unpack_from('<I', mv, i)[0]
        if v in va2lit:
            refs.append((v, code0 + i))
    with (od / 'literal-xref.tsv').open('w') as f:
        f.write('函数\t字面量VA\t引用地址\t类别\t字面量\n')
        seen = set()
        for va, ref in sorted(refs, key=lambda r: (owner(r[1]) or 0, r[0])):
            lit = va2lit[va]
            o = owner(ref)
            if (o, va) in seen:
                continue
            seen.add((o, va))
            f.write(f'{o:#010x}\t{va:#010x}\t{ref:#010x}\t{classify(lit)}\t{lit[:120]}\n')

    # 自检：逻辑坏了这里会先炸
    assert starts and all(code0 <= s < code_end for s in starts), '函数起点越界'
    assert len(starts) > 1000, f'函数数异常: {len(starts)}'
    assert refs, '字面量 xref 为空（模型不成立）'
    api_refs = [r for r in refs if classify(va2lit[r[0]]) == 'API']
    assert api_refs, 'API 字面量 xref 为空'
    print(f'函数 {len(starts)}  字面量引用 {len(refs)}（API 类 {len(api_refs)}）  → {od}')


if __name__ == '__main__':
    main(pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]), pathlib.Path(sys.argv[3]))
