#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
切配阶段 4 自检：核对材料骨架的脚注与引文。

用法：
    python check_footnotes.py 骨架.md [引用汇编.md]

检查项：
  1. 每个 [^n] 引用有定义，每个定义被引用。
  2. 脚注编号按首次出现顺序连续（1, 2, 3 …）。
  3. 「同上书」「同上」不出现在第 1 条脚注。
  4. 连接句（非引文、非脚注的正文行）里的禁用词。
  5. 若给了汇编：骨架里每条引文能在汇编里找到（去标点、去空白后子串匹配）。
  6. 统计待核标记：【待核】【凭记忆】【PDF页】【回原书】。

退出码：有问题为 1，全部通过为 0。
"""

import io
import re
import sys

FORBIDDEN = [
    "因此", "所以", "由此可见", "可见", "这说明", "这表明", "这意味着", "意味着",
    "揭示", "反映", "体现", "正是", "恰恰", "恰好", "不难看出", "显然",
    "值得注意的是", "实际上", "本质上", "归根结底", "换言之", "也就是说",
    "从根本上", "无非是", "不过是", "说明了", "证明了", "印证了", "支撑了",
    "深刻", "精辟", "有力", "典型", "经典",
]

PENDING_MARKS = ["【待核", "【凭记忆", "【PDF页", "【回原书", "页码待核", "版本待补"]

REF_RE = re.compile(r"\[\^(\d+)\](?!:)")
DEF_RE = re.compile(r"^\[\^(\d+)\]:\s*(.*)$")

QUOTED_RE = re.compile(r"“[^”]*”|「[^」]*」|\"[^\"]*\"")

PUNCT_RE = re.compile(r"[\s，。、；：？！“”‘’「」『』《》〈〉（）()\[\]\"'…—\-·,.;:?!\d\^]")


def read(path):
    with io.open(path, "r", encoding="utf-8") as f:
        return f.read()


def normalize(s):
    s = PUNCT_RE.sub("", s)
    return s


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2

    skeleton = read(argv[1])
    compendium = read(argv[2]) if len(argv) > 2 else None
    lines = skeleton.splitlines()
    problems = []

    # 1. refs vs defs
    ref_order = []
    for m in REF_RE.finditer(skeleton):
        n = int(m.group(1))
        if n not in ref_order:
            ref_order.append(n)
    defs = {}
    for i, line in enumerate(lines, 1):
        m = DEF_RE.match(line.strip())
        if m:
            n = int(m.group(1))
            if n in defs:
                problems.append("脚注 [^%d] 定义了两次（第 %d 行与第 %d 行）" % (n, defs[n][0], i))
            defs[n] = (i, m.group(2))
    for n in ref_order:
        if n not in defs:
            problems.append("脚注 [^%d] 有引用无定义" % n)
    for n in defs:
        if n not in ref_order:
            problems.append("脚注 [^%d] 有定义无引用（第 %d 行）" % (n, defs[n][0]))

    # 2. sequential order
    expected = list(range(1, len(ref_order) + 1))
    if ref_order != expected:
        problems.append("脚注编号未按出现顺序连续：实际顺序 %s" % ref_order)

    # 3. 同上 at first footnote
    if 1 in defs and re.match(r"^同上", defs[1][1]):
        problems.append("第 1 条脚注用了「同上」，前面没有可以「同」的脚注")
    # 同上 following a def whose text names a different work is not machine-checkable; skip.

    # 4. forbidden words in connective prose
    for i, line in enumerate(lines, 1):
        s = line.strip()
        if not s or s.startswith(">") or DEF_RE.match(s) or s.startswith("#"):
            continue
        if s.startswith("**（切配便签"):
            continue
        # 行内引文（"…"、「…」）不算连接句
        prose = QUOTED_RE.sub("", s)
        for w in FORBIDDEN:
            if w in prose:
                problems.append("第 %d 行连接句含禁用词「%s」：%s" % (i, w, s[:40]))

    # 5. quotes vs compendium
    if compendium is not None:
        comp_norm = normalize(compendium)
        for i, line in enumerate(lines, 1):
            s = line.strip()
            if not s.startswith(">"):
                continue
            q = REF_RE.sub("", s.lstrip("> ").strip())
            # split on ellipsis so 删节 quotes still match piecewise
            for piece in re.split(r"…+|……", q):
                pn = normalize(piece)
                if len(pn) < 8:
                    continue
                if pn not in comp_norm:
                    problems.append("第 %d 行引文在汇编中未找到：%s" % (i, piece[:40]))

    # 6. pending marks
    pending = []
    for i, line in enumerate(lines, 1):
        for mark in PENDING_MARKS:
            if mark in line:
                pending.append((i, mark))

    print("脚注引用 %d 条，定义 %d 条。" % (len(ref_order), len(defs)))
    if pending:
        print("待核标记 %d 处：" % len(pending))
        for i, mark in pending:
            print("  第 %d 行 %s" % (i, mark))
    if problems:
        print("问题 %d 项：" % len(problems))
        for p in problems:
            print("  - " + p)
        return 1
    print("未发现问题。")
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass
    sys.exit(main(sys.argv))
