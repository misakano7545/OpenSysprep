#!/bin/sh
# 主程序全量反汇编（只读，不执行样本）。用法: tools/scpt/disasm.sh <Scpt.unpacked.exe> <输出目录>
set -eu
EXE=${1:?用法: disasm.sh <Scpt.unpacked.exe> <输出目录>}
OUT=${2:-.}
mkdir -p "$OUT"
objdump -D -M intel --no-show-raw-insn -j .text  "$EXE" > "$OUT/Scpt.text.asm"
objdump -D -M intel --no-show-raw-insn -j .itext "$EXE" > "$OUT/Scpt.itext.asm"
wc -l "$OUT/Scpt.text.asm" "$OUT/Scpt.itext.asm"
