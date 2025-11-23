#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
silva 138.2 dada2 format to SINTAX format for usearch
制作人：lwzhao
制作时间：2025-11-23
版本：1.0
注意：使用该脚本转换格式后，在使用usearch进行物种注释时仍会有个别警告，可以忽略
警告事例
“WARNING: g:Eubacterium has parents f:Eubacteriaceae (kept) and f:Lachnospiraceae (discarded)”
"""

import sys
import re

def print_help():
    print("""
用法：
    python sintax_uCG001_final.py <input.fasta> [output.fasta]
    python sintax_uCG001_final.py -h

特性：
    • 精准处理：仅 "UCG-001" → 上一级名 UCG-001（带空格）
    • 不处理 UCG-002、UCG-003 等任何其他编号
    • 彻底清除 Incertae_Sedis / unidentified / uncultured / endosymbionts
    • 缺失层级 → 上一级_X
    • 种缺失 → 属_sp
""")
    sys.exit(0)

if len(sys.argv) == 1 or sys.argv[1] in ("-h", "--help", "-help"):
    print_help()

input_fa  = sys.argv[1] if len(sys.argv) > 1 else "input.fasta"
output_fa = sys.argv[2] if len(sys.argv) > 2 else "sintax_uCG001_perfect.fa"
rank_map = ["k", "p", "c", "o", "f", "g", "s"]

# 要替换为 _X 的脏词（不区分大小写）
BAD_WORDS_X = [
    "incertae_sedis", "unidentified", "unknown", "unknown_family",
    "uncultured", "unclassified", "metagenome", "environmental", "candidate"
]

def clean_name(s):
    if not s:
        return None
    s = re.sub(r"^[kpcofgs]__\s*", "", s, flags=re.IGNORECASE)
    s = s.strip()
    s = re.sub(r"\s+", "_", s)
    s = re.sub(r"[^\w\-]", "", s)
    s = re.sub(r"^[-_]+|[-_]+$", "", s)
    return s if s else None

def is_bad_word(name):
    if not name:
        return False
    return any(bad in name.lower() for bad in BAD_WORDS_X)

def convert_header(header, idx):
    taxa_str = re.sub(r";\s*tax=.*$", "", header.strip(), flags=re.IGNORECASE)
    parts = [p.strip() for p in taxa_str.split(";") if p.strip()]

    raw_levels = [None] * 7
    for i, part in enumerate(parts[:7]):
        raw_levels[i] = clean_name(part)

    last_valid = "Root"           # 上一级真实有效名字
    final_levels = []

    for i in range(7):
        raw_name = raw_levels[i]

        if raw_name is not None:
            # 精准规则：仅当严格等于 "UCG-001" 时替换（区分大小写）
            if raw_name == "UCG-001":
                current = f"{last_valid} UCG-001"

            # endosymbionts 处理
            elif "endosymbiont" in raw_name.lower():
                current = f"{last_valid}_endosymbionts"

            # 脏词处理
            elif is_bad_word(raw_name):
                current = f"{last_valid}_X"

            # 正常有效名字
            else:
                current = raw_name
                last_valid = current
        else:
            # 层级缺失
            current = f"{last_valid}_X"

        final_levels.append(current)

    genus = final_levels[5]

    # 构建最终 tax=
    items = []
    for i in range(7):
        rank = rank_map[i]
        name = final_levels[i]

        if i == 6:  # 种水平
            if raw_levels[6] is not None and raw_levels[6] != "UCG-001" and not is_bad_word(raw_levels[6]) and "endosymbiont" not in raw_levels[6].lower():
                items.append(f"s:{genus}_{raw_levels[6]}")
            else:
                items.append(f"s:{genus}_sp")
        else:
            items.append(f"{rank}:{name}")

    tax = ",".join(items)
    return f">Ref{idx};tax={tax};"

# ==================== 主程序 ====================
print(f"正在执行精准 UCG-001 处理: {input_fa} → {output_fa}")

count = 0
with open(input_fa, "r", encoding="utf-8") as fin, \
     open(output_fa, "w", encoding="utf-8") as fout:
    for line in fin:
        line = line.rstrip("\n\r")
        if line.startswith(">"):
            count += 1
            new_header = convert_header(line[1:], count)
            fout.write(new_header + "\n")
        else:
            fout.write(line + "\n")

print("="*95)
print(f"精准清洗完成！共处理 {count} 条序列")
print(f"输出文件: {output_fa}")
print("="*95)