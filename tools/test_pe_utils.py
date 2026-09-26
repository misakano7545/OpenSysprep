"""tools/pe_utils.py 的自检（CI 运行）。"""
import os
import pathlib
import struct
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import pe_utils


def build_min_pe():
    """最小 PE32：1 个 .text 节（VA 0x1000 / 文件 0x200 / 0x200 字节），ImageBase 0x400000。"""
    b = bytearray(0x400)
    b[0:2] = b"MZ"
    struct.pack_into("<I", b, 0x3C, 0x40)
    e = 0x40
    b[e:e + 4] = b"PE\0\0"
    struct.pack_into("<H", b, e + 4, 0x14C)    # Machine: i386
    struct.pack_into("<H", b, e + 6, 1)        # NumberOfSections
    struct.pack_into("<H", b, e + 20, 0xE0)    # SizeOfOptionalHeader
    opt = e + 24
    struct.pack_into("<H", b, opt, 0x10B)      # magic PE32
    struct.pack_into("<I", b, opt + 28, 0x400000)  # ImageBase
    sec = opt + 0xE0
    b[sec:sec + 8] = b".text\0\0\0"
    struct.pack_into("<IIII", b, sec + 8, 0x100, 0x1000, 0x200, 0x200)
    struct.pack_into("<I", b, sec + 36, 0x60000020)  # CNT_CODE|EXECUTE|READ
    struct.pack_into("<I", b, 0x204, 0x401234)       # .text 内一个 32 位引用
    return bytes(b)


class TestPE(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".bin")
        tmp.write(build_min_pe())
        tmp.close()
        self.addCleanup(os.unlink, tmp.name)
        self.pe = pe_utils.PE(tmp.name)

    def test_sections(self):
        self.assertEqual(self.pe.sections[0]["name"], ".text")
        self.assertFalse(self.pe.is64)
        self.assertEqual(self.pe.imagebase, 0x400000)

    def test_va_roundtrip(self):
        self.assertEqual(self.pe.off2va(0x200), 0x401000)
        self.assertEqual(self.pe.va2off(0x401000), 0x200)

    def test_find_refs(self):
        refs = self.pe.find_refs(0x401234)
        self.assertTrue(any(off == 0x204 for _, off, _ in refs), refs)


if __name__ == "__main__":
    unittest.main()
