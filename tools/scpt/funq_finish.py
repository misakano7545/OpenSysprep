#!/usr/bin/env python3
"""FUNQ 完整脱壳收尾：ASPack 块解压 + 修正 .rsrc 真实范围（尾部资源原样存放在壳区）+ 重建 PE。

关键点：ASPack 把 .rsrc 的压缩块解压到 [0x322d78, 0x3EEA00)，
而尾部资源（图标 / 版本信息 / 清单）以**原样字节**存放在 .aspack 段的地址范围内
（RVA 0x3f0448 起），所以重建时必须保留 [0x3EEA00, 0x406000) 这段原始字节，
并让 .rsrc 的 VirtualSize 覆盖到 .adata 起点。
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import pefile  # noqa: E402
import unpack  # noqa: E402

SRC = pathlib.Path('/root/dev/OpenSysprep/work/engines/FUNQ')
OUT = pathlib.Path('/root/dev/OpenSysprep/work/engines/FUNQ.unpacked.exe')

raw = SRC.read_bytes()
pe = pefile.PE(data=raw, fast_load=True)
vep = pe.OPTIONAL_HEADER.AddressOfEntryPoint
ep_file = pe.get_offset_from_rva(vep)
ver = unpack.detect(raw, len(raw), ep_file)
ep = vep - 1

sects = [{'name': s.Name.rstrip(b'\x00').decode('latin1'), 'vsz': s.Misc_VirtualSize,
          'rva': s.VirtualAddress, 'rsz': s.SizeOfRawData,
          'raw': s.PointerToRawData} for s in pe.sections]
ssize = max(s['rva'] + s['vsz'] for s in sects)
img = bytearray(ssize)
for s in sects:
    if s['rsz']:
        img[s['rva']:s['rva'] + s['rsz']] = raw[s['raw']:s['raw'] + s['rsz']]

log = []
failed, oep = unpack.unaspack(img, ssize, ep, ver, log)
ok = sum(1 for b in log if b.get('status') == 'ok')
print(f'ASPack {ver}: blocks ok={ok}/{len(log)}, failed={failed}, oep={oep:#x}')

rsrc = next(s for s in sects if s['name'] == '.rsrc')
adata = next(s for s in sects if s['name'] == '.adata')
rsrc['vsz'] = adata['rva'] - rsrc['rva']      # 覆盖到 .adata 起点（含尾部原始资源）
keep = [s for s in sects if s['name'] not in ('.aspack', '.adata')]

unpack.rebuild(raw[:pe.OPTIONAL_HEADER.SizeOfHeaders], img, keep, oep, OUT)
print('rebuilt:', OUT, OUT.stat().st_size)
