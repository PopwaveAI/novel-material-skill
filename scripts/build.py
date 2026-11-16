#!/usr/bin/env python3
"""docx -> 切片 markdown + 索引。唯一数据源：本文件的 BOOKS。"""
import json, re, sys
from pathlib import Path
from docx import Document
from docx.table import Table
from docx.text.paragraph import Paragraph
from docx.oxml.ns import qn

ROOT = Path(__file__).resolve().parents[1]
SRC = Path("/Users/clairliu/Downloads")
OUT = ROOT / "references"
DOCS = ROOT / "docs"
MAX_CHARS = 3000
TITLE_LIMIT = 30

BOOKS = [
    ("01", "网文写作技巧·结构篇", "网文写作技巧：结构篇 1.0 版.docx", "通识", "完整", ""),
    ("02", "网文写作技巧·文笔篇", "网文写作技巧：文笔篇 1.0 版.docx", "通识", "完整", "表格密集，已转 Markdown 表格"),
    ("03", "网文设定素材手册", "网文设定素材手册 1.0 版.docx", "通识", "完整", ""),
    ("04", "女主人设手册", "女主人设手册 1.0 版 (2).docx", "人设", "完整", ""),
    ("05", "男主人设手册", "男主人设手册 1.0 版 (1).docx", "人设", "完整", ""),
    ("06", "CP设定手册", "CP设定手册 1.0版.docx", "关系", "完整", ""),
    ("07", "人性欲望创作手册", "附件 (1).docx", "关系", "完整", "源文件名为“附件”，已按内容定名"),
    ("08", "古言题材创作手册", "古言题材创作手册 1.0 版.docx", "题材", "完整", ""),
    ("09", "现言题材创作手册", "现言题材创作手册 1.0 版.docx", "题材", "完整", ""),
    ("10", "仙侠题材创作手册", "仙侠题材创作手册 1.0 版.docx", "题材", "完整", ""),
    ("11", "娱乐圈题材创作手册", "娱乐圈题材创作手册 1.0 版.docx", "题材", "完整", ""),
    ("12", "悬疑题材创作手册", "悬疑题材创作手册 1.0 版.docx", "题材", "完整", ""),
    ("13", "群像题材创作手册", "群像题材创作手册 1.0 版.docx", "题材", "完整", ""),
    ("14", "先婚后爱创作手册", "先婚后爱创作手册 1.0 版 (1).docx", "关系", "完整", ""),
    ("15", "强制爱创作手册", "强制爱创作手册 1.0 版.docx", "关系", "完整", ""),
    ("16", "伪骨科创作手册", "伪骨科创作手册 1.0 版 (1).docx", "关系", "完整", ""),
]

def iter_blocks(doc):
    for child in doc.element.body.iterchildren():
        if child.tag == qn("w:p"):
            yield Paragraph(child, doc)
        elif child.tag == qn("w:tbl"):
            yield Table(child, doc)

def cell_text(c):
    return re.sub(r"\s+", " ", c.text).strip().replace("|", "／")

def table_md(tbl):
    rows = [[cell_text(c) for c in r.cells] for r in tbl.rows]
    rows = [r for r in rows if any(r)]
    if not rows:
        return ""
    w = max(len(r) for r in rows)
    rows = [r + [""] * (w - len(r)) for r in rows]
    return "\n".join(["| " + " | ".join(rows[0]) + " |", "|" + "---|" * w] +
                     ["| " + " | ".join(r) + " |" for r in rows[1:]])

def heading_level(p):
    st = p.style.name if p.style is not None else ""
    m = re.match(r"(?:Heading|标题)\s*(\d)", st or "")
    return int(m.group(1)) if m else 0

def slug(s, limit=TITLE_LIMIT):
    s = re.sub(r"^\s*第[一二三四五六七八九十百]+部分\s*[:：]?\s*", "", s)
    s = re.sub(r"^\s*\d+(?:\.\d+)*\s*[、.．:：]?\s*", "", s)
    s = re.sub(r'[\\/:*?"<>|\r\n\t]', " ", s)
    s = re.sub(r"\s+", "", s).strip("·.-_ ")
    return (s[:limit] or "未命名")

def nchars(t):
    """正文字符数：去掉空白与 Markdown 语法符号。"""
    t = re.sub(r"^\|[\s\-:|]+\|$", "", t, flags=re.M)
    t = t.replace("|", "")
    t = re.sub(r"^#{1,6}\s*", "", t, flags=re.M)
    t = re.sub(r"^>\s*", "", t, flags=re.M)
    return len(re.sub(r"\s", "", t))

def render(blocks):
    return "\n\n".join(("### " + v) if k == "h3" else v for k, v in blocks)

def atomize(kind, val, mx):
    if nchars(val) <= mx:
        return [(kind, val)]
    if kind == "t":
        lines = val.split("\n")
        head, body = lines[:2], lines[2:]
        out, cur = [], list(head)
        for ln in body:
            if nchars("\n".join(cur)) + nchars(ln) > mx and len(cur) > 2:
                out.append("\n".join(cur)); cur = list(head)
            cur.append(ln)
        if len(cur) > 2:
            out.append("\n".join(cur))
        return [("t", x) for x in out] or [(kind, val[:mx])]
    sents = re.findall(r"[^。！？；\n]*[。！？；\n]?", val)
    out, cur = [], ""
    for s in sents:
        if not s:
            continue
        if nchars(cur) + nchars(s) > mx and cur:
            out.append(cur); cur = ""
        if nchars(s) > mx:
            for i in range(0, len(s), mx):
                out.append(s[i:i + mx])
        else:
            cur += s
    if cur:
        out.append(cur)
    return [(kind, x) for x in out if x.strip()]

def pack(blocks, mx):
    flat = []
    for k, v in blocks:
        flat += atomize(k, v, mx - 10)
    chunks, cur = [], []
    for k, v in flat:
        if cur and nchars(render(cur + [(k, v)])) > mx:
            chunks.append(cur); cur = [(k, v)]
        else:
            cur = cur + [(k, v)]
    if cur:
        chunks.append(cur)
    return chunks

ALL, report = [], []
for bid, btitle, fname, cat, status, note in BOOKS:
    path = SRC / fname
    if not path.exists():
        c = sorted(SRC.glob(fname.replace(".docx", "*")))
        if not c:
            print("MISSING", fname); sys.exit(1)
        path = c[0]
    doc = Document(str(path))

    part = {"title": "前言", "sections": [], "pre": []}
    parts = [part]
    cur_sec = None
    for b in iter_blocks(doc):
        if isinstance(b, Paragraph):
            lv, t = heading_level(b), b.text.strip()
            if not t:
                continue
            if lv == 1:
                part = {"title": t, "sections": [], "pre": []}
                parts.append(part); cur_sec = None
            elif lv == 2:
                cur_sec = {"title": t, "blocks": []}
                part["sections"].append(cur_sec)
            elif lv == 3:
                if cur_sec is None:
                    cur_sec = {"title": part["title"] + "·开篇", "blocks": []}
                    part["sections"].append(cur_sec)
                cur_sec["blocks"].append(("h3", t))
            else:
                (cur_sec["blocks"] if cur_sec else part["pre"]).append(("p", t))
        else:
            md = table_md(b)
            if md:
                (cur_sec["blocks"] if cur_sec else part["pre"]).append(("t", md))

    front, body_parts = None, parts
    if parts and parts[0]["title"] == "前言" and parts[0]["pre"]:
        front, body_parts = parts[0], parts[1:]

    # 部分导语并入该部分第一节，避免 70 字空文件
    for p in body_parts:
        if p["pre"] and p["sections"]:
            p["sections"][0]["blocks"] = p["pre"] + p["sections"][0]["blocks"]
            p["pre"] = []

    bdir = OUT / btitle
    bdir.mkdir(parents=True, exist_ok=True)
    for old in bdir.glob("*.md"):
        old.unlink()

    stat = {"c": 0, "f": 0}

    def emit(rel, title, body):
        body = re.sub(r"(?m)^\s*[•·]\s*", "- ", body)
        txt = "# %s\n\n> 素材来源：novel-material-skill ·《%s》%s\n\n%s\n" % (title, btitle, title, body)
        (bdir / rel).write_text(txt, encoding="utf-8")
        c = nchars(body)
        stat["c"] += c; stat["f"] += 1
        return c

    def write_section(code, title, blocks):
        chunks = pack(blocks, MAX_CHARS)
        if not chunks:
            return
        tot = 0
        first = ""
        for ci, ch in enumerate(chunks, 1):
            body = render(ch)
            if not body.strip():
                continue
            rel = code + (".md" if ci == 1 else "__%d.md" % ci)
            c = emit(rel, title, body)
            tot += c
            first = first or rel
        if tot:
            ALL.append({"b": bid, "t": title, "f": first, "c": tot, "n": len(chunks)})

    if front:
        write_section("00-前言", "前言", front["pre"])

    for pi, p in enumerate(body_parts, 1):
        if not p["sections"]:
            write_section("%02d-00_%s" % (pi, slug(p["title"])), p["title"], p["pre"])
            continue
        for si, sec in enumerate(p["sections"], 1):
            write_section("%02d-%02d_%s" % (pi, si, slug(sec["title"])), sec["title"], sec["blocks"])

    report.append((bid, btitle, cat, stat["c"], len(body_parts), stat["f"], status, note))


SUPP = [
    ("网文写作技巧·思维篇（框架）", "网文写作技巧·思维篇 大纲.docx", "仅有框架"),
    ("情绪与悲剧叙事（框架）", "情绪与悲剧叙事创作手册 大纲.docx", "仅有框架"),
    ("末世与无限流（框架）", "末世与无限流题材创作手册 大纲.docx", "仅有框架"),
    ("掉马创作手册（精简版）", "掉马创作手册 1.0 版.docx", "精简版"),
    ("网文细节描写词库（雏形）", "网文细节描写词库 1.0 版.docx", "雏形"),
    ("正文缺陷清单", "正文缺陷清单 v1.docx", "工具清单"),
]
sdir = OUT / "补充材料"
sdir.mkdir(parents=True, exist_ok=True)
for old in sdir.glob("*.md"):
    old.unlink()
srows = []
for i, (name, fname, st_) in enumerate(SUPP, 1):
    doc = Document(str(SRC / fname))
    secs, cur = [], None
    for b in iter_blocks(doc):
        if isinstance(b, Paragraph):
            lv, t = heading_level(b), b.text.strip()
            if not t:
                continue
            if lv == 1:
                cur = {"title": t, "blocks": []}
                secs.append(cur)
            else:
                if cur is None:
                    cur = {"title": name, "blocks": []}
                    secs.append(cur)
                cur["blocks"].append(("h3" if lv == 2 else "p", t))
        else:
            md = table_md(b)
            if md:
                if cur is None:
                    cur = {"title": name, "blocks": []}
                    secs.append(cur)
                cur["blocks"].append(("t", md))
    if not secs:
        continue
    code = "%02d" % i
    tot, first, nf = 0, "", 0
    for si, sec in enumerate(secs, 1):
        for ci, ch in enumerate(pack(sec["blocks"], MAX_CHARS), 1):
            body = render(ch)
            if not body.strip():
                continue
            body = re.sub(r"(?m)^\s*[•·]\s*", "- ", body)
            rel = "%s-%02d_%s%s.md" % (code, si, slug(sec["title"]), "" if ci == 1 else "__%d" % ci)
            (sdir / rel).write_text("# %s\n\n> 素材来源：novel-material-skill ·《%s》%s\n\n%s\n" % (sec["title"], name, sec["title"], body), encoding="utf-8")
            tot += nchars(body); nf += 1
            first = first or rel
    if tot:
        ALL.append({"b": "S", "t": name, "f": first, "c": tot, "n": nf})
        srows.append((name, fname, tot, nf, st_))

lines = ["# 补充材料（已收录）", "", "| 项 | 值 |", "|---|---|",
         "| 份数 | %d |" % len(srows),
         "| 字数 | %s 字 |" % format(sum(r[2] for r in srows), ","),
         "| 说明 | 只有框架 / 精简版 / 工具清单，不计入 16 本正文 |", "",
         "## 目录", "", "| 文件 | 标题 | 字数 | 状态 |", "|---|---|---|---|"]
for x in sorted([a for a in ALL if a["b"] == "S"], key=lambda a: a["f"]):
    lines.append("| [%s](%s) | %s | %s | %s |" % (x["f"].split("_")[0], x["f"], x["t"], format(x["c"], ","),
                 dict((r[0], r[4]) for r in srows).get(x["t"], "")))
(sdir / "_index.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

for bid, btitle, cat, total, nparts, files, status, note in report:
    rows = sorted([x for x in ALL if x["b"] == bid], key=lambda x: x["f"])
    lines = ["# 《%s》目录" % btitle, "", "| 项 | 值 |", "|---|---|",
             "| 字数 | %s 字 |" % format(total, ","),
             "| 部分数 | %d |" % nparts,
             "| 切片数 | %d |" % files,
             "| 完整度 | %s |" % status,
             "| 版本 | 1.0 |",
             "| 来源 | 内部培训资料 · CC BY 4.0 |", ""]
    if note:
        lines += ["注：%s" % note, ""]
    lines += ["## 章节索引", "",
              "| 文件 | 标题 | 字数 |", "|---|---|---|"]
    for x in rows:
        code = x["f"].split("_")[0]
        tail = "" if x["n"] == 1 else "（%d 段）" % x["n"]
        lines.append("| [%s](%s) | %s%s | %s |" % (code, x["f"], x["t"].replace("|", "／"), tail, format(x["c"], ",")))
    (OUT / btitle / "_index.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

tot = sum(r[3] for r in report)
files_all = sum(r[5] for r in report)
lines = ["# 书目状态", "",
         "共 **%d 本**、**%s 字**、**%s 个切片**（按仓库内正文统计，含标点、不含空白与 Markdown 符号）。" % (
             len(report), format(tot, ","), format(files_all, ",")), "",
         "| 序 | 书名 | 分类 | 字数 | 部分数 | 切片数 | 完整度 |", "|---|---|---|---|---|---|---|"]
for bid, btitle, cat, total, nparts, files, status, note in report:
    lines.append("| %s | [%s](%s/_index.md) | %s | %s | %d | %d | %s |" % (
        bid, btitle, btitle, cat, format(total, ","), nparts, files, status))
lines += ["", "## 补充材料（已收录，不计入 16 本正文）", "",
          "共 %d 份、%s 字，见 [补充材料/_index.md](补充材料/_index.md)。" % (len(srows), format(sum(r[2] for r in srows), ",")), "",
          "| 名称 | 字数 | 状态 |", "|---|---|---|"] + \
         ["| %s | %s | %s |" % (r[0], format(r[2], ","), r[4]) for r in srows] + [""]
(OUT / "书目状态.md").write_text("\n".join(lines), encoding="utf-8")

DOCS.mkdir(exist_ok=True)
(DOCS / "index.json").write_text(json.dumps({
    "total": tot, "files": files_all,
    "books": [{"id": r[0], "name": r[1], "cat": r[2], "chars": r[3], "files": r[5]} for r in report] + \
             [{"id": "S", "name": "补充材料", "cat": "补充", "chars": sum(r[2] for r in srows), "files": sum(r[3] for r in srows)}],
    "items": [[x["b"], x["t"], x["f"], x["c"], x["n"]] for x in ALL],
}, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")

bad = []
for x in ALL:
    if x["b"] == "S":
        continue
    d = OUT / [r[1] for r in report if r[0] == x["b"]][0]
    for f in d.glob(x["f"].split("_")[0] + "*.md"):
        body = f.read_text(encoding="utf-8").split("\n\n", 2)[-1]
        if nchars(body) > MAX_CHARS:
            bad.append((f.name, nchars(body)))
print("books", len(report), "sections", len(ALL), "files", files_all)
print("chars", format(tot, ","), "| json KB", round((DOCS / "index.json").stat().st_size / 1024, 1))
print("over-limit", len(bad), bad[:3])
print("supplement", len(srows), "files", sum(r[3] for r in srows), "chars", format(sum(r[2] for r in srows), ","))