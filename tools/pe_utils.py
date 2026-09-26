#!/usr/bin/env python3
"""Minimal PE utilities: sections, off<->va, ref search (for 32-bit & 64-bit)."""
import struct, pathlib

class PE:
    def __init__(self, path):
        self.path = pathlib.Path(path)
        self.b = self.path.read_bytes()
        e = struct.unpack_from('<I', self.b, 0x3c)[0]
        assert self.b[e:e+4] == b'PE\0\0', 'not PE'
        nsec = struct.unpack_from('<H', self.b, e+6)[0]
        optsz = struct.unpack_from('<H', self.b, e+20)[0]
        self.opt = e + 24
        self.magic = struct.unpack_from('<H', self.b, self.opt)[0]  # 0x10b / 0x20b
        self.is64 = self.magic == 0x20b
        if self.is64:
            self.imagebase = struct.unpack_from('<Q', self.b, self.opt+24)[0]
        else:
            self.imagebase = struct.unpack_from('<I', self.b, self.opt+28)[0]
        self.sections = []
        for i in range(nsec):
            o = e + 24 + optsz + i*40
            name = self.b[o:o+8].rstrip(b'\0').decode('latin1')
            vsize, vaddr, rsize, rptr = struct.unpack_from('<IIII', self.b, o+8)
            ch = struct.unpack_from('<I', self.b, o+36)[0]
            self.sections.append(dict(name=name, vsize=vsize, vaddr=vaddr,
                                      rsize=rsize, rptr=rptr, ch=ch))

    def off2va(self, off):
        for s in self.sections:
            if s['rptr'] <= off < s['rptr'] + max(s['rsize'], 1) + 0x10000:
                r = off - s['rptr']
                if r < max(s['vsize'], s['rsize']):
                    return self.imagebase + s['vaddr'] + r
        raise ValueError(f'off {off:#x} not in any section')

    def va2off(self, va):
        r = va - self.imagebase
        for s in self.sections:
            if s['vaddr'] <= r < s['vaddr'] + max(s['vsize'], s['rsize']):
                return s['rptr'] + (r - s['vaddr'])
        raise ValueError(f'va {va:#x} not in any section')

    def code_sections(self):
        return [s for s in self.sections if s['ch'] & 0x20000000]  # IMAGE_SCN_CNT_CODE

    def find_refs(self, va, limit=64):
        pat = struct.pack('<I', va)
        out = []
        for s in self.code_sections():
            data = self.b[s['rptr']:s['rptr'] + min(s['rsize'], s['vsize'])]
            start = 0
            while True:
                i = data.find(pat, start)
                if i < 0:
                    break
                off = s['rptr'] + i
                out.append((s['name'], off, self.off2va(off)))
                start = i + 1
                if len(out) >= limit:
                    return out
        return out

    def find_all(self, needle, limit=64):
        out = []
        start = 0
        while True:
            i = self.b.find(needle, start)
            if i < 0:
                break
            out.append(i)
            start = i + 1
            if len(out) >= limit:
                break
        return out
