# 网文写作素材库

**16 本 · 3,078,704 字 · 3,194 个切片 · 全部开源**

一份网文工作室的内部培训资料：题材手册、人设手册、CP 设定、结构篇、文笔篇、设定素材。
不是梗合集，是可套用的模板——每一节都带「定义 / 例子 / 行为逻辑 / 标志动作 / 台词 / 崩点 + 修法」。

给 AI 用，也给写手直接翻。

---

## 它解决什么问题

写手最耗时的不是灵感，是**把一句话变成能落地的设定**。

你说「古言、女扮男装、先婚后爱」，普通素材库给你一堆标签；这份素材给你：女主的三种出身怎么写、先婚后爱的第一次同框放在第几章、男主在第几章必须露破绽、读者会在第几章弃文。

每一节都是这个密度：

<details>
<summary>点开看一节真实原文（《伪骨科创作手册》3.1 关系起源模板）</summary>

两个人是怎么住进同一个屋檐的，房子怎么摆，称呼怎么叫，第一千天和第一天差在哪。这一部分把开局那层壳搭出来，壳搭稳了，后面越界才有落差。

「关系起源」是两个人住进同一屋檐的合法理由，是壳的地基。起源定了，后面所有矛盾都从这根藤上长出来。

把两个人绑进一个屋檐，不是随便一句「他们是兄妹」就够了。读者要信这件事，得有一个站得住的来历。来历不同，两个人之间的权力结构、债务感、第三方阻力全都不一样。下面六种，每种给成立条件、谁先住进来、第一天的一个场面、天然埋的矛盾、最适合的赛道。

</details>

---

## 三条主张

1. **全开源。** 3,078,704 字，不做付费墙、不做「关注后领取」、不藏 20%。素材 CC BY 4.0，商用写书也可以，标个来源就行。
2. **不是标签库，是模板库。** 每个类型都拆到「他为什么会这样 / 他会做什么动作 / 他会说什么台词 / 写崩了长什么样 / 怎么救」。
3. **给 AI 用的。** 按小节切片，单文件 ≤3000 字，配两层索引。AI 读 3 个文件就能出方案，不用把 300 万字塞进上下文。

---

## 目录结构

```
SKILL.md                  ← 给 AI 读的入口（定位规则、路由、交付格式）
references/
├── INDEX.md              ← 按产出物找书（要开局 / 要人设 / 要改稿）
├── 书目状态.md            ← 16 本的字数、部分数、切片数、完整度
├── 伪骨科创作手册/
│   ├── _index.md         ← 本书目录：文件 · 标题 · 字数
│   ├── 01-01_....md      ← 一节一个文件，≤3000 字
│   └── ...
└── ... 共 16 本
```

---

## 怎么装

```bash
git clone https://github.com/PopwaveAI/novel-material-skill.git

# Claude Code
cp -r novel-material-skill ~/.claude/skills/novel-material

# DeepSeek Harness / 兼容 Agent Skills 的宿主
cp -r novel-material-skill ~/.agents/skills/novel-material

# Codex
cp -r novel-material-skill ~/.codex/skills/novel-material
```

装完直接说人话，不用记命令：

> 「古言，女扮男装，先婚后爱，给我一个女主设定和前三章方案」

---

## 十六本

| 分类 | 书 | 字数 |
|---|---|---|
| 通识 | [网文写作技巧·结构篇](references/网文写作技巧·结构篇/_index.md) | 125,377 |
| 通识 | [网文写作技巧·文笔篇](references/网文写作技巧·文笔篇/_index.md) | 252,468 |
| 通识 | [网文设定素材手册](references/网文设定素材手册/_index.md) | 104,110 |
| 人设 | [女主人设手册](references/女主人设手册/_index.md) | 265,725 |
| 人设 | [男主人设手册](references/男主人设手册/_index.md) | 249,077 |
| 关系 | [CP设定手册](references/CP设定手册/_index.md) | 176,986 |
| 关系 | [人性欲望创作手册](references/人性欲望创作手册/_index.md) | 179,154 |
| 题材 | [古言题材创作手册](references/古言题材创作手册/_index.md) | 222,895 |
| 题材 | [现言题材创作手册](references/现言题材创作手册/_index.md) | 234,241 |
| 题材 | [仙侠题材创作手册](references/仙侠题材创作手册/_index.md) | 177,315 |
| 题材 | [娱乐圈题材创作手册](references/娱乐圈题材创作手册/_index.md) | 149,947 |
| 题材 | [悬疑题材创作手册](references/悬疑题材创作手册/_index.md) | 154,619 |
| 题材 | [群像题材创作手册](references/群像题材创作手册/_index.md) | 240,841 |
| 关系 | [先婚后爱创作手册](references/先婚后爱创作手册/_index.md) | 156,161 |
| 关系 | [强制爱创作手册](references/强制爱创作手册/_index.md) | 142,535 |
| 关系 | [伪骨科创作手册](references/伪骨科创作手册/_index.md) | 247,253 |

---

## 它不包含什么

- **不含**「思维篇」「情绪与悲剧叙事」「末世与无限流」——只有大纲，没收全本（合计 6,596 字）
- **不含**「掉马创作手册」「网文细节描写词库」全本——前者只有 3,698 字精简版，后者只有 4,107 字雏形
- 这些都在 [`references/书目状态.md`](references/书目状态.md) 里单列，**不计入总字数**

## 统计口径

字数按仓库内正文统计：含标点，不含空白与 Markdown 符号，也不含每节的文件头（标题行和「素材来源」行）。你可以自己验：

```bash
python3 - <<'PY'
import re, pathlib
def n(t):
    t = re.sub(r"^\|[\s\-:|]+\|$", "", t, flags=re.M).replace("|", "")
    t = re.sub(r"^#{1,6}\s*", "", t, flags=re.M)
    t = re.sub(r"^>\s*", "", t, flags=re.M)
    return len(re.sub(r"\s", "", t))
tot = 0
for p in pathlib.Path("references").rglob("*.md"):
    if p.name == "_index.md" or p.parent.name == "references":
        continue
    keep = [l for l in p.read_text().splitlines()
            if l and not l.startswith("# ") and not l.startswith("> 素材来源")]
    tot += n("\n".join(keep))
print(tot)   # 3078704
```

---

## 网页版

[`docs/index.html`](docs/index.html) 是一个单页搜索：只加载标题索引（270KB），点开才取那一节的正文。
部署：仓库 Settings → Pages → 选 `main` / `root`。

## 授权

- **素材**（`references/`）：[CC BY 4.0](LICENSE) —— 随便用、商用、改编，标来源即可
- **脚本**（`scripts/`）：[MIT](LICENSE-CODE)

引用格式：

```
素材来源：novel-material-skill ·《伪骨科创作手册》§3.3
```

## 更新

素材来自内部培训资料，后续按月补书（思维篇、情绪与悲剧、末世与无限流已在排队）。
重建索引：`python3 scripts/build.py`（需要 `pip install python-docx`，并把 docx 放进 `source-docx/`）。

---

如果这份素材帮你少走了一章弯路，点个 ⭐ 让下一个写手也能搜到它。
