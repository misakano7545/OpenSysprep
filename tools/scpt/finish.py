#!/usr/bin/env python3
"""Final build: image_best (with .aspack-area resources), rebuilt exe, full resource dump."""
import json
import pathlib
import re
import struct
import sys

sys.path.insert(0, ".")
import pefile  # noqa: E402
import unpack  # noqa: E402

W = pathlib.Path(".")
raw = (W / "Scpt.exe").read_bytes()
img = bytearray((W / "image_full.bin").read_bytes())
oep = int((W / "unpack_oep.txt").read_text().strip(), 16)
pe = pefile.PE(data=raw, fast_load=True)

# 1) patch .aspack raw region (stub + manifest + version + icons) into rva space
asp = next(s for s in pe.sections if s.Name.startswith(b".aspack"))
asp_rva, asp_off, asp_rsz = asp.VirtualAddress, asp.PointerToRawData, asp.SizeOfRawData
img[asp_rva:asp_rva + asp_rsz] = raw[asp_off:asp_off + asp_rsz]
(W / "image_best.bin").write_bytes(img)
print("image_best saved; .aspack raw patched at", hex(asp_rva), "size", hex(asp_rsz))

# verify icon/manifest landmarks in rva space now
print("manifest@0x5c1b890:", bytes(img[0x5C1B890:0x5C1B898]))
print("MAINICON@0x5c1c0d0:", bytes(img[0x5C1C0D0:0x5C1C0D8]).hex())

# 2) rebuild exe
sects = []
for s in pe.sections:
    sects.append(dict(name=s.Name.rstrip(b"\x00").decode("latin-1"), vsz=s.Misc_VirtualSize,
                      rva=s.VirtualAddress, rsz=s.SizeOfRawData, raw=s.PointerToRawData))
keep = [s for s in sects if not s["name"].startswith((".aspack", ".adata"))]
# extend .rsrc to also cover the icon/manifest/version tail that the packer
# relocated into the .aspack section area (original .rsrc ended at its own end)
rsrc_end = asp_rva + asp_rsz
rsrc_end = ((rsrc_end + 0xFFF) // 0x1000) * 0x1000
for s in keep:
    if s["name"] == ".rsrc":
        s["vsz"] = rsrc_end - s["rva"]
print("rsrc extended:", hex(sects[-3]["rva"]), "->", hex(rsrc_end))

rebuilt = unpack.rebuild(raw[:pe.OPTIONAL_HEADER.SizeOfHeaders], img, keep, oep, W / "Scpt.unpacked.exe")
print("rebuilt:", rebuilt, rebuilt.stat().st_size)

# fix SizeOfImage in rebuilt header to cover everything
pe2 = pefile.PE(str(rebuilt), fast_load=True)
simg = pe2.OPTIONAL_HEADER.SizeOfImage
need = max(s["rva"] + s["vsz"] for s in keep)
align = pe2.OPTIONAL_HEADER.SectionAlignment
new_simg = ((need + align - 1) // align) * align
if new_simg > simg:
    b = bytearray(rebuilt.read_bytes())
    e_lfanew = struct.unpack_from("<I", b, 0x3C)[0]
    opt = e_lfanew + 24
    struct.pack_into("<I", b, opt + 56, new_simg)
    rebuilt.write_bytes(b)
    print("SizeOfImage fixed:", hex(simg), "->", hex(new_simg))

# 3) extract all resources from rebuilt exe
pe3 = pefile.PE(str(rebuilt))
resdir = W / "out_res"
resdir.mkdir(exist_ok=True)
count = 0
manifest = []
def walk(entries, path):
    global count
    for e in entries:
        label = e.name or str(e.id)
        try:
            label = label.decode("ascii") if isinstance(label, bytes) else str(label)
        except Exception:
            label = str(label)
        if hasattr(e, "directory"):
            walk(e.directory.entries, path + [label])
        else:
            d = e.data.struct
            data = pe3.get_data(d.OffsetToData, d.Size)
            safe = "/".join(path + [label]).replace("\\", "_")
            dst = resdir / safe
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_bytes(data)
            count += 1
            manifest.append({"path": safe, "rva": d.OffsetToData, "size": d.Size, "got": len(data),
                             "head": data[:16].hex()})
walk(pe3.DIRECTORY_ENTRY_RESOURCE.entries, [])
(W / "out_res_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1))
print("resources extracted:", count)

heads = {m["path"]: m for m in manifest}
for p in ("DATA/FUNA", "10/TAPPMSGFORM", "10/TMFFUN", "LANGS/SCCHS", "24/1", "16/1", "14/MAINICON"):
    m = heads.get(p)
    if m:
        print(f"  {p:18s} {m['size']:>9d} got={m['got']:>9d} head={m['head']}")

mzs = [m for m in manifest if m["head"].startswith("4d5a")]
pks = [m for m in manifest if m["head"].startswith("504b")]
print("MZ resources:", [(m["path"], m["size"]) for m in mzs])
print("PK resources:", [(m["path"], m["size"]) for m in pks])

tm = heads.get("10/TAPPMSGFORM")
if tm:
    b = (resdir / "10/TAPPMSGFORM").read_bytes()
    print("TAPPMSGFORM TPF0?", b[:4] == b"TPF0", b[:16].hex())
print("FINISH_DONE")
