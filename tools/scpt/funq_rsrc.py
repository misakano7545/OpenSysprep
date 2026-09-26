#!/usr/bin/env python3
"""手工走 FUNQ 脱壳产物的资源目录（RVA == 文件偏移），检查每条资源数据是否完好。"""
import pathlib
import struct
import sys

P = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else '/tmp/funq_out/Scpt.unpacked.exe')
b = P.read_bytes()
RSRC = 0x322000
HI = 0x80000000
MASK = 0x7FFFFFFF

u16 = lambda o: struct.unpack_from('<H', b, o)[0]
u32 = lambda o: struct.unpack_from('<I', b, o)[0]


def name_at(off):
    n = u16(off)
    return b[off + 2:off + 2 + 2 * n].decode('utf-16-le', 'ignore')


rows = []


def walk(diroff, depth, path):
    n = u16(diroff + 12)
    m = u16(diroff + 14)
    for i in range(n + m):
        e = diroff + 16 + i * 8
        nm, ofs = u32(e), u32(e + 4)
        lab = name_at(RSRC + (nm - HI)) if nm >= HI else str(nm)
        if ofs >= HI:
            walk(RSRC + (ofs - HI), depth + 1, path + [lab])
        else:
            de = RSRC + ofs
            rva, size, cp, _ = struct.unpack_from('<IIII', b, de)
            rows.append((path + [lab], rva, size))


walk(RSRC, 0, [])
print(f'共 {len(rows)} 条资源数据；文件大小 {len(b)}')
print(f"{'类型':10s} {'名称':16s} {'RVA':>10s} {'size':>8s}  头部20字节")
for p, rva, size in rows:
    t = p[0] if p else '?'
    nm = p[1] if len(p) > 1 else ''
    inside = 'IN' if rva + size <= len(b) else 'OUT!'
    head = b[rva:rva + 20] if rva < len(b) else b''
    print(f'{t:10s} {nm:16s} {rva:#10x} {size:8d} {inside} {head!r}')
