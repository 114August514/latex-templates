---
name: academic-writing
description: >
  学术写作与排版的完整工作流——期刊/会议论文、实验报告、技术报告、课程大作业、
  组会与学术会议幻灯片、答辩。基于配套 LaTeX 模板（article / report / beamer /
  defense / homework），覆盖建项目、定骨架、写正文、编译、投稿自查，内置
  GB/T 7714、GB/T 3101、GB/T 7713、ISO 80000-2 等排版规范。Use this whenever
  the user is writing, revising, or reviewing a paper, lab report, technical
  report, course report, thesis section, homework write-up, or academic slide
  deck — including "帮我写实验报告"、"组会 PPT"、"这段改成论文语言"、
  "投稿前检查一下"、"参考文献格式对不对"、"公式排版规范吗"、"beamer 主题怎么改"、
  "把这些实验结果整理成报告". Also use it when turning raw notes, logs, or data
  into any of those deliverables, even if the user never mentions LaTeX.
  涉及三线表、图表标题、量和单位、正斜体、盲审匿名、交叉引用、文献样式的问题
  也走这个 skill。
---

# 学术写作工作流

三条流水线共用一套模板与一套排版规范，所以论文里的记号可以直接搬进报告和
幻灯片，不用重新调格式。

**模板根目录 `$TPL`**：本 skill 位于 `$TPL/skills/academic-writing/`。
从本文件向上找到含 `common/acadbase.sty` 的目录即为 `$TPL`。也可用环境变量
`ACAD_TEMPLATES` 覆盖。找不到就问用户模板在哪；没有模板时只用本 skill 的
写作规范（`references/standards.md`），不要假装模板存在。

本 skill 不绑定任何编程助手。仓库把文件放在 `skills/academic-writing/`；
若助手只从它自己的 skills 目录加载，把该目录链过去即可。调用脚本时用上面
解析出的 `$TPL`，不要写死家目录或某个产品的配置路径。

脚手架用仓库里的 uv 项目解释器：`uv run --directory "$TPL" python …`。

---

## 第一步：判断要产出什么

| 用户想要的 | 流水线 | 详细步骤 |
|---|---|---|
| 期刊/会议论文、投稿、论文某一节 | **paper** | 读 `references/paper.md` |
| 实验报告、技术报告、课程大作业、结课论文 | **report** | 读 `references/report.md` |
| 连续课程作业（多次 hwN） | **homework** | 读 `references/homework.md` |
| 组会汇报、会议 oral | **slides**（`beamer` 模板） | 读 `references/presenting.md` + `slides.md` |
| 开题 / 中期 / 学位答辩 | **slides**（`defense` 模板） | 读 `references/presenting.md` + `slides.md` |

判断不了就问一句，不要猜——骨架完全不同，选错了要推倒重来。
尤其别把答辩当会议报告做：会议报告可以只讲最亮的一条线，
答辩必须覆盖全部工作量与创新点，而且委员会手里有论文全文。

做任何幻灯片都**先读 `references/presenting.md`**。内容没想清楚就开始排版
是最大的浪费。

模板不止表里这几套。动手前先看实际有哪些：

```bash
uv run --directory "$TPL" python scripts/new-project.py --list
```

自定义模板的 `template.conf` 里 `doc =` 会指出该读哪份 `references/*.md`；
没写就按最接近的那条流水线走。

一次任务里可能要走两条（比如「把这篇论文讲一遍」= paper 已有 + slides 新建），
这种情况先做主产物，再从主产物派生次产物。

排版规范速查：`references/standards.md`。编译报错：`references/troubleshooting.md`。

---

## 第二步：建项目

新项目用仓库脚本从模板拷一份出来，共享文件会展平进项目，目录自包含：

```bash
uv run --directory "$TPL" python scripts/new-project.py <模板名> <目标目录>
```

在已有项目里工作就跳过这步。**不要**直接在 `$TPL` 里改正文，那是模板本体。

用户想加一套自己的模板时：在 `$TPL` 下新建目录，放 `template.conf`
（`name` / `desc` / `needs` / `hint` / `doc`）。单文档再放 `main.tex`；
课程集合放 `hwN/main.tex`。`--list` 会自动发现它。

---

## 第三步：先定骨架，再写内容

论证逻辑见 `references/writing.md`——动笔前读它。
`paper.md` / `report.md` 管流水线，它管内容层。

顺序固定：

1. **填 `setup.tex`** —— 题名、作者、单位这些元数据。
2. **列出各节的一句话主旨** —— 每个 `sections/*.tex` 或 `frames/*.tex`
   一句话，写成注释放进文件头。**拿给用户确认**再往下走。
3. **逐节写正文** —— 一次只动一个文件。

第 2 步不要跳。

---

## 三条流水线共同的铁律

### 内容与格式分离

`sections/` 和 `frames/` 里**不出现格式命令**。要改字号、间距、颜色，
去改 `.cls` 或主题 `.sty`。

### 引用、数值、交叉引用都不手写

| 不要写 | 要写 | 原因 |
|---|---|---|
| `[1]` | `\cite{key}` | 增删文献时编号自动重排 |
| `5 kg`、`1×10⁻³` | `\qty{5}{\kg}`、`\num{1e-3}` | 间距与正斜体由 siunitx 按 GB 3100 保证 |
| `图 3`、`式 (5)` | `\cref{fig:x}`、`\cref{eq:y}` | 类型词自动生成，中英切换不用改正文 |
| `E_{max}` | `E\subtext{max}` | 说明性下标必须正体（GB/T 3101） |
| `\mathbf{F}` | `\vect{F}` | 矢量粗斜体，全文统一 |

每个图、表、公式、算法都要有 `\label`，命名用 `fig:` `tab:` `eq:` `alg:`
`sec:` 前缀。

### 图表

- **表题在表上方，图题在图下方**。
- 表格用三线表：只有 `\toprule` `\midrule` `\bottomrule`，不画竖线。
- 图必须矢量（PDF），matplotlib 用 `plt.savefig('x.pdf')`。
- 坐标轴标注写「量 / 单位」，如 `t / s`，不写 `t (s)`。

### 数字要诚实

报告实验结果时给出重复次数与波动范围。只报最好的一次是最常见的失分点。

---

## 第四步：编译与自查

优先用项目里的 `make check`（终稿）。Unix 壳也可用：

```bash
"$TPL/skills/academic-writing/scripts/check.sh" <项目目录>
```

它会编译并汇总：编译错误、`Overfull hbox`、未定义的交叉引用与文献。
有错就修，不要把带 `??` 的 PDF 交出去。

写正文时用项目的 `make preview` 或编辑器里的单轮预览看内容；交稿前必须终稿。

改稿时先跑反向提纲：

```bash
uv run python "$TPL/skills/academic-writing/scripts/outline.py" <项目目录>
```

没有 TeX 环境时用静态检查：

```bash
uv run python "$TPL/skills/academic-writing/scripts/lint.py" <项目目录>
```

lint 通过只能说「静态检查通过，未经编译验证」。

TeX 环境的安装见仓库 README「安装依赖」，不要假设某一种包管理器。

**不要在编译不通过的情况下声称做完了。** 环境里装不了 TeX，就明确说
「未经编译验证」，并指出最可能出问题的地方。

---

## 写作质量

**结论句优先。** 章节标题、图题、幻灯片标题都尽量写成能独立成立的判断句。

**主动写出局限。** 每份产物都应该有一段讲适用范围与未消除的误差。

**数字要能追溯。** 结论里出现的每个数字，前文都应该出现过并有出处。

**中文学术语体。** 解法是改成无主语句，不是改成被动语态。详见
`references/writing.md` §3。专业术语首次出现时给出英文原文，之后统一用中文。

---

## 常见分支情况

**用户要 Word/Markdown 而不是 PDF**：写作规范仍适用，但不要硬套 LaTeX 模板。

**用户已有半成品**：不要推倒重来。先判断流水线，再按骨架增量修补。

**用户只要改一小段**：就改那一段。

**盲审/双盲送审**：`article` 和 `report` 加 `anonymous` 类选项。提醒 PDF
元数据和文件名里也不要留姓名。

---

## 参考文件

按需读，不要一次全读进来：

- `references/writing.md` —— 论证逻辑与文字
- `references/paper.md` —— 论文流水线
- `references/report.md` —— 报告流水线
- `references/homework.md` —— 课程作业：解答还是证明
- `references/presenting.md` —— 演示内容设计与答辩策略
- `references/slides.md` —— 幻灯片模板用法
- `references/standards.md` —— 排版规范速查
- `references/troubleshooting.md` —— 编译报错对照表
