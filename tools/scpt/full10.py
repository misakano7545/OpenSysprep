#!/usr/bin/env python3
"""Decompress the .rsrc ASPack stream (block 10) and verify reconstructed resources."""
import pathlib
import re
import struct
import sys

sys.path.insert(0, ".")
import unpack  # noqa: E402

W = pathlib.Path(".")
img = bytearray((W / "image_unpacked.bin").read_bytes())
ep = 0x5C1A000  # logical: ep-1 was 0x5c1a000; stream offsets are section-relative to it
oep_ep = 0x5C19FFF + 1  # not used; keeping explicit below

# rebuild stream state exactly like unaspack does
EP = 0x5C1A000  # ep = vep-1 = 0x5c1a000 -> wait: vep=0x5c1a001, ep=0x5c1a000
EP = 0x5C1A000
OFF = unpack.OFF["242"]
ssize = len(img)
blocks_off, sim_off, comp_off, wrk_off, oep_off = OFF

BLOCK_RVA = 0x647E8C
BLOCK_SIZE = 0x55D1774


def make_stream():
    st = unpack.Stream()
    st.hash = 0x10000
    j = 0
    for i in range(58):
        st.init_array[i] = j
        if EP + i + sim_off < ssize:
            j += 1 << img[EP + i + sim_off]
    return st


stuff_off = EP + comp_off

print("== probe (cap 8MB) ==", flush=True)
st = make_stream()
buf = bytearray(BLOCK_SIZE + 0x10E)
buf[0:BLOCK_SIZE] = img[BLOCK_RVA:BLOCK_RVA + BLOCK_SIZE]
st.input = buf
st.ilen = len(buf)
st.inpos = 0
scratch = bytearray(8_200_000)
try:
    ok = unpack.decomp_block(st, BLOCK_SIZE, img, stuff_off, scratch, 0, cap=8_000_000)
    print("probe result:", ok)
    print("head:", bytes(scratch[:64]).hex())
    if not ok:
        sys.exit("probe failed - stream not valid")
except unpack.CapHit:
    print("probe: valid stream past 8MB cap")
    print("head:", bytes(scratch[:64]).hex())

print("== full decompression ==", flush=True)
st2 = make_stream()
st2.input = buf
st2.ilen = len(buf)
st2.inpos = 0
out = bytearray(img)  # copy; write directly at BLOCK_RVA
try:
    ok = unpack.decomp_block(st2, BLOCK_SIZE, img, stuff_off, out, BLOCK_RVA, progress=True)
except unpack.CapHit:
    sys.exit("unexpected cap")

print("full result:", ok, flush=True)
if not ok:
    sys.exit("full decompression failed")

(W / "image_full.bin").write_bytes(out)
print("saved image_full.bin", hex(len(out)))

# ---- verification ----
def at(rva, n=48):
    return bytes(out[rva:rva + n])


print("\nreconstructed landmark checks:")
checks = [
    ("TMAINFORM", 0x52D00C0, b"TPF0"),
    ("TAPPMSGFORM", 0x52D00C0, b"TPF0"),
    ("MLSKINREGISTERHINT", 0x52B7194, None),
    ("LANGS/SCCHS", 0x51E3E2C, None),
    ("string table 6/4039", 0x52A7A8C, None),
    ("FUNA", 0x647E8C, None),
    ("PUBCE", 0x3E41744, None),
]
for name, rva, sig in checks:
    h = at(rva, 32)
    m = "OK" if (sig and h.startswith(sig)) else ("?" if sig else "")
    print(f"  {name:22s} @{hex(rva)} {m} {h.hex()}")
    print("      ascii:", repr(h[:32]))

print("\nTMAINFORM head+64:", at(0x52D00C0, 96).hex())
print("is TPF0 at TMAINFORM?", at(0x52D00C0, 4) == b"TPF0")
print("TMFUN head:", at(0x52D11F0, 48).hex())
print("TMLSKINRESDM head:", at(0x5311934, 48).hex())
print("SCCHS head:", at(0x51E3E2C, 64).hex())

# MZ scan in reconstructed region
region = bytes(out[0x647E8C:0x5C1A000])
print("\nMZ count in region:", len(list(re.finditer(rb"MZ", region))))
mt = [(m.start() + 0x647E8C, region[m.start():m.start() + 64]) for m in re.finditer(rb"MZ", region)]
print("first MZ offsets:", [hex(o) for o, _ in mt[:20]])
for o, b in mt[:6]:
    print(hex(o), b.hex())

print("PK count:", len(list(re.finditer(rb"PK\x03\x04", region))))
print("SCAN_FULL_DONE")
