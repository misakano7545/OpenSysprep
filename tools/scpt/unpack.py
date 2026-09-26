#!/usr/bin/env python3
"""Static ASPack (2.12 / 2.42 / other) unpacker.

Port of ClamAV libclamav/aspack.c (Copyright (C) 2013-2026 Cisco Systems, Inc.,
2007-2013 Sourcefire, Inc., authors Luciano Giuseppe 'Pnluck', Alberto Wu;
GPLv2) to Python. No code from the sample is executed: pure data decompression.
"""
import json
import pathlib
import struct
import sys

import pefile

M32 = 0xFFFFFFFF
OFF = {
    # version: (blocks, str_init_mlt, comp_block, wrkbuf, oep)
    "212": (0x57C, 0x70E, 0x6D6, 0x148, 0x39B),
    "other": (0x5D8, 0x76A, 0x732, 0x13A, 0x401),
    "242": (0x5E4, 0x776, 0x73E, 0x148, 0x40D),
}
EPBUFF = {"212": 0x3B9, "other": 0x41F, "242": 0x42B}
EP_SIG = b"\x60\xe8\x03\x00\x00\x00\xe9\xeb"
EP_TAIL = b"\x68\x00\x00\x00\x00\xc3"


def u32(b, o):
    return struct.unpack_from("<I", b, o)[0]


def w32(b, o, v):
    struct.pack_into("<I", b, o, v & M32)


def shr(x, n):
    """x86-style shift: count is masked to 5 bits."""
    return (x & M32) >> (n & 31)


def rol(x, n):
    n &= 31
    x &= M32
    return ((x << n) | (x >> (32 - n))) & M32 if n else x


class Fatal(Exception):
    pass


class CapHit(Exception):
    """Raised when a capped trial decompression exceeds the cap without error."""


class Stream:
    def __init__(self):
        self.bitpos = 0
        self.hash = 0x10000
        self.init_array = [0] * 58
        self.dh = [
            {"starts": [0] * 721, "ends": bytearray(0x100), "size": 721},
            {"starts": [0] * 28, "ends": bytearray(0x100), "size": 28},
            {"starts": [0] * 8, "ends": bytearray(0x100), "size": 8},
            {"starts": [0] * 19, "ends": bytearray(0x100), "size": 19},
        ]
        self.input = b""
        self.inpos = 0
        self.ilen = 0
        self.decrypt_dict = bytearray(0x1800)
        self.decarray3 = [[0] * 24 for _ in range(4)]
        self.decarray4 = [[0] * 24 for _ in range(4)]
        self.dict_ok = 0
        self.array2 = bytearray(758)
        self.array1 = bytearray(19)
        self._prog_next = 0x1000000

    def readstream(self):
        while self.bitpos >= 8:
            if self.inpos >= self.ilen:
                return False
            self.hash = ((self.hash << 8) | self.input[self.inpos]) & M32
            self.inpos += 1
            self.bitpos -= 8
        return True


def getdec(st, which):
    d3 = st.decarray3[which]
    d4 = st.decarray4[which]
    if not st.readstream():
        return None
    ret = shr(st.hash, 8 - st.bitpos) & 0xFFFE00
    if ret < d3[8]:
        if (ret >> 16) >= 0x100:
            return None
        pos = st.dh[which]["ends"][ret >> 16]
        if not pos or pos >= 24:
            return None
    elif ret < d3[10]:
        pos = 9 if ret < d3[9] else 10
    elif ret < d3[11]:
        pos = 11
    elif ret < d3[12]:
        pos = 12
    elif ret < d3[13]:
        pos = 13
    elif ret < d3[14]:
        pos = 14
    else:
        pos = 15

    st.bitpos += pos
    ret = (shr((ret - d3[pos - 1]) & M32, 24 - pos) + d4[pos]) & M32
    if ret >= st.dh[which]["size"]:
        return None
    return st.dh[which]["starts"][ret]


def build_decrypt_array(st, array, which):
    dh = st.dh[which]
    d3 = st.decarray3[which]
    d4 = st.decarray4[which]
    bus = [0] * 18
    dic = [0] * 18
    for i in range(dh["size"]):
        v = array[i]
        if v > 17:
            return False
        bus[v] += 1

    d3[0] = d4[0] = 0
    total = 0
    counter = 23
    i = 0
    endoff = 0
    while counter >= 9:
        total = (total + (bus[i + 1] << counter)) & M32
        if total > 0x1000000:
            return False
        d3[i + 1] = total
        dic[i + 1] = bus[i] + dic[i]
        d4[i + 1] = dic[i + 1]
        if counter >= 0x10:
            old = endoff
            endoff = shr(d3[i + 1], 0x10)
            if endoff < old:
                return False
            remaining = endoff - old
            if remaining > 0:
                if old + remaining > 0x100:
                    return False
                dh["ends"][old:old + remaining] = bytes([i + 1]) * remaining
        i += 1
        counter -= 1

    if total != 0x1000000:
        return False

    for i in range(dh["size"]):
        v = array[i]
        if v:
            if v > 17:
                return False
            if dic[v] >= dh["size"]:
                return False
            dh["starts"][dic[v]] = i
            dic[v] += 1
    return True


def getbits(st, num):
    if not st.readstream():
        return None
    v = shr(shr(st.hash, 8 - st.bitpos) & 0xFFFFFF, 24 - num)
    st.bitpos += num
    return v


def build_decrypt_dictionaries(st):
    v = getbits(st, 1)
    if v is None:
        st.decrypt_dict[0:0x2F5] = b"\x00" * 0x2F5
        return False
    if v == 0:
        st.decrypt_dict[0:0x2F5] = b"\x00" * 0x2F5

    for c in range(19):
        b = getbits(st, 4)
        if b is None:
            return False
        st.array1[c] = b
    if not build_decrypt_array(st, st.array1, 3):
        return False

    counter = 0
    while counter < 757:
        r = getdec(st, 3)
        if r is None:
            return False
        if r >= 16:
            if r != 16:
                if r == 17:
                    add = getbits(st, 3)
                    r = None if add is None else 3 + add
                else:
                    add = getbits(st, 7)
                    r = None if add is None else 11 + add
                if r is None:
                    return False
                while r:
                    if counter >= 757:
                        break
                    st.array2[1 + counter] = 0
                    counter += 1
                    r -= 1
            else:
                add = getbits(st, 2)
                if add is None:
                    return False
                r = 3 + add
                while r:
                    if counter >= 757:
                        break
                    st.array2[1 + counter] = st.array2[counter]
                    counter += 1
                    r -= 1
        else:
            st.array2[1 + counter] = (st.decrypt_dict[counter] + r) & 0xF
            counter += 1

    if not build_decrypt_array(st, st.array2[1:], 0):
        return False
    if not build_decrypt_array(st, st.array2[722:], 1):
        return False
    if not build_decrypt_array(st, st.array2[750:], 2):
        return False

    st.dict_ok = 0
    for c in range(8):
        if st.array2[750 + c] != 3:
            st.dict_ok = 1
            break

    st.decrypt_dict[0:757] = st.array2[1:758]
    return True


def decrypt(st, stuff, stuff_off, size, out, out_off, cap=None, progress=False):
    counter = 0
    hist = [0, 0, 0, 0]
    while counter < size:
        if progress and counter >= st._prog_next:
            print(f"    ... {counter >> 20} MB / {size >> 20} MB", flush=True)
            st._prog_next = counter + 0x1000000
        if cap is not None and counter >= cap:
            raise CapHit()
        gen = getdec(st, 0)
        if gen is None:
            return False
        if gen < 256:
            out[out_off + counter] = gen
            counter += 1
            continue
        if gen >= 720:
            if not build_decrypt_dictionaries(st):
                return False
            continue

        backbytes = (gen - 256) >> 3
        backsize = ((gen - 256) & 7) + 2
        if (backsize - 2) == 7:
            g2 = getdec(st, 1)
            if g2 is None or g2 >= 0x56:
                return False
            hlp = stuff[stuff_off + g2 + 0x1C]
            if not st.readstream():
                return False
            backsize += stuff[stuff_off + g2] + shr(shr(st.hash, 8 - st.bitpos) & 0xFFFFFF, 0x18 - hlp)
            st.bitpos += hlp

        useold = st.init_array[backbytes]
        gen = stuff[stuff_off + backbytes + 0x38]
        if not st.dict_ok or gen < 3:
            if not st.readstream():
                return False
            useold += shr(shr(st.hash, 8 - st.bitpos) & 0xFFFFFF, 24 - gen)
            st.bitpos += gen
        else:
            gen -= 3
            if not st.readstream():
                return False
            useold += shr(shr(st.hash, 8 - st.bitpos) & 0xFFFFFF, 24 - gen) * 8
            st.bitpos += gen
            t = getdec(st, 2)
            if t is None:
                return False
            useold += t

        if useold < 3:
            backbytes = hist[useold]
            if useold != 0:
                hist[useold] = hist[0]
                hist[0] = backbytes
        else:
            hist[2] = hist[1]
            hist[1] = hist[0]
            hist[0] = backbytes = useold - 3

        backbytes += 1
        if not backbytes or backbytes > counter or backsize > size - counter:
            return False
        for _ in range(backsize):
            out[out_off + counter] = out[out_off + counter - backbytes]
            counter += 1
    return True


def decomp_block(st, size, stuff, stuff_off, out, out_off, cap=None, progress=False):
    for i in range(4):
        st.decarray3[i] = [0] * 24
        st.decarray4[i] = [0] * 24
    st.decrypt_dict[0:757] = b"\x00" * 757
    st.bitpos = 0x20
    if not build_decrypt_dictionaries(st):
        return False
    return decrypt(st, stuff, stuff_off, size, out, out_off, cap=cap, progress=progress)


def detect(image, fsize, ep_file):
    if ep_file + 8 > fsize or image[ep_file:ep_file + 8] != EP_SIG:
        raise Fatal("entry stub signature mismatch (not ASPack, or damaged)")
    for ver in ("212", "other", "242"):
        o = ep_file + EPBUFF[ver]
        if o + 6 <= fsize and image[o:o + 6] == EP_TAIL:
            return ver
    raise Fatal("unknown ASPack version: no EP-buffer marker found")


def unaspack(img, ssize, ep, ver, log, verbose=False):
    import time
    blocks_off, sim_off, comp_off, wrk_off, oep_off = OFF[ver]
    st = Stream()
    st.hash = 0x10000

    j = 0
    for i in range(58):
        st.init_array[i] = j
        if ep + i + sim_off < ssize:
            j += 1 << img[ep + i + sim_off]

    stuff_off = ep + comp_off
    wrk_marker = img[ep + wrk_off]

    pos = ep + blocks_off
    blocks = []
    stage = 0  # mirrors C's reused `i`
    while pos + 8 <= ssize:
        block_rva = u32(img, pos)
        block_size = u32(img, pos + 4)
        if not block_rva or block_rva + block_size > ssize:
            break
        log.append({"block_rva": block_rva, "block_size": block_size})
        t0 = time.time()

        buf = bytearray(block_size + 0x10E)
        buf[0:block_size] = img[block_rva:block_rva + block_size]
        st.input = buf
        st.ilen = len(buf)
        st.inpos = 0

        if not decomp_block(st, block_size, img, stuff_off, img, block_rva):
            log[-1]["status"] = "decomp_failed"
            if verbose:
                print(f"  block {len(log) - 1}: rva={hex(block_rva)} size={hex(block_size)} FAILED", flush=True)
            break
        log[-1]["status"] = "ok"
        if verbose:
            print(f"  block {len(log) - 1}: rva={hex(block_rva)} size={hex(block_size)} ok "
                  f"({time.time() - t0:.1f}s)", flush=True)

        if stage == 0 and block_size > 7:  # first section j/c unrolling
            while stage < block_size - 6:
                if img[block_rva + stage] in (0xE8, 0xE9):
                    if img[block_rva + stage + 1] == wrk_marker:
                        target = rol(u32(img, block_rva + stage + 1) & 0xFFFFFF00, 0x18)
                        w32(img, block_rva + stage + 1, target - stage)
                        stage += 4
                stage += 1

        if ver == "212":
            pos += 8
        else:
            pos += 12
            bs = u32(img, pos + 4)
            while ((bs + 0x10E) & M32) == 0:
                pos += 12
                bs = u32(img, pos + 4)

    failed = u32(img, ep + blocks_off) != 0
    oep = u32(img, ep + oep_off)
    return failed, oep


def rebuild(orig_header, img, sections, oep, out_path):
    hdr = bytearray(orig_header)
    nsec = len(sections)
    pe_off = struct.unpack_from("<I", hdr, 0x3C)[0]
    struct.pack_into("<H", hdr, pe_off + 6, nsec)
    opt = pe_off + 24
    # 修正：SizeOfOptionalHeader 在 COFF 头 pe_off+20，而不是 OptionalHeader 的 Magic（opt+0）
    size_opt = struct.unpack_from("<H", hdr, pe_off + 20)[0]
    struct.pack_into("<I", hdr, opt + 16, oep)  # AddressOfEntryPoint
    sec_off = opt + size_opt
    for i, s in enumerate(sections):
        e = sec_off + i * 40
        struct.pack_into("<I", hdr, e + 8, s["vsz"])   # VirtualSize
        struct.pack_into("<I", hdr, e + 12, s["rva"])  # VirtualAddress
        struct.pack_into("<I", hdr, e + 16, s["vsz"])  # SizeOfRawData
        struct.pack_into("<I", hdr, e + 20, s["rva"])  # PointerToRawData
    for i in range(nsec, nsec + 2):
        hdr[sec_off + i * 40: sec_off + (i + 1) * 40] = b"\x00" * 40

    size = max(s["rva"] + s["vsz"] for s in sections)
    size = max(size, len(hdr))
    out = bytearray(size)
    out[0:len(hdr)] = hdr
    for s in sections:
        out[s["rva"]: s["rva"] + s["vsz"]] = img[s["rva"]: s["rva"] + s["vsz"]]
    out_path.write_bytes(out)
    return out_path


def main():
    src = pathlib.Path(sys.argv[1])
    outdir = pathlib.Path(sys.argv[2])
    outdir.mkdir(parents=True, exist_ok=True)
    raw = src.read_bytes()
    pe = pefile.PE(data=raw, fast_load=True)
    vep = pe.OPTIONAL_HEADER.AddressOfEntryPoint
    ep_file = pe.get_offset_from_rva(vep)
    ver = detect(raw, len(raw), ep_file)
    ep = vep - 1

    sects = []
    for s in pe.sections:
        sects.append({
            "name": s.Name.rstrip(b"\x00").decode("latin-1"),
            "vsz": s.Misc_VirtualSize,
            "rva": s.VirtualAddress,
            "rsz": s.SizeOfRawData,
            "raw": s.PointerToRawData,
        })
    ssize = max(s["rva"] + s["vsz"] for s in sects)
    img = bytearray(ssize)
    for s in sects:
        if s["rsz"]:
            img[s["rva"]:s["rva"] + s["rsz"]] = raw[s["raw"]:s["raw"] + s["rsz"]]

    log = []
    failed, oep = unaspack(img, ssize, ep, ver, log)

    report = {
        "input": str(src),
        "aspack_version": ver,
        "entry_rva": hex(vep),
        "ep_used": hex(ep),
        "image_size": ssize,
        "blocks": log,
        "unpack_failed": failed,
        "oep": hex(oep),
    }
    (outdir / "unpack.json").write_text(json.dumps(report, indent=2))
    (outdir / "image.bin").write_bytes(img)
    nsec = len(sects) - 2 if sects[-1]["rsz"] == 0 and ep == sects[-2]["rva"] else len(sects)
    pe2 = rebuild(raw[:pe.OPTIONAL_HEADER.SizeOfHeaders], img, sects[:nsec], oep,
                  outdir / "Scpt.unpacked.exe")
    print(json.dumps({k: v for k, v in report.items() if k != "blocks"}, indent=2))
    print("blocks:", len(log), "ok:", sum(1 for b in log if b.get("status") == "ok"))
    print("total_decompressed:", hex(sum(b["block_size"] for b in log)))
    print("rebuilt:", pe2, pe2.stat().st_size)


if __name__ == "__main__":
    main()
