# 幻灯片流水线（beamer / defense）

**动手前先读 `presenting.md`。** 那份讲的是「放什么内容、怎么讲、答辩怎么打」，
包含有实证支撑的 Assertion-Evidence 结构、时长-页数预算、提问预判。
本文只讲怎么驱动模板。内容没想清楚就开始排版，是做幻灯片最大的浪费。

## 两套模板，选哪个

| | `beamer` | `defense` |
|---|---|---|
| 场合 | 组会、会议 oral | 开题 / 中期 / 学位答辩 |
| 听众 | 陌生同行，没看过你的论文 | 委员会，**手里有你的论文全文** |
| 骨架 | 动机 → 方法 → 结果 → 结论 | 选题 → 现状 → 内容 → 工作 → 创新点 → 成果 |
| 页脚左侧 | 作者名 | 当前节标题（`mode=defense`） |
| 备用页 | 3~5 页 | 8~25 页，带索引与跳转 |

视觉主题是同一套，切换只是骨架和 `mode` 选项的差别。

## 文件分工

| 文件 | 放什么 |
|---|---|
| `main.tex` | `\documentclass` + `\usetheme` + 一串 `\input` |
| `setup.tex` | 题名、副题名、作者、单位、日期、封面图 |
| `preamble.tex` | biblatex、`\AtBeginSection` 节页钩子、自定义记号、备注开关 |
| `frames/*.tex` | 内容，一个文件一段 |
| `beamerthemeAcad.sty` | 装配 + 字体 + 数学 + 定理译名 + `evidence`/`\takeaway`/跳转 |
| `beamercolorthemeAcad.sty` | 配色（通常只改前两个 `\definecolor`） |
| `beamerfontthemeAcad.sty` | 字号字形 |
| `beamerinnerthemeAcad.sty` | 标题页、节页、列表符号、block、图表标题 |
| `beamerouterthemeAcad.sty` | 页边距、帧标题栏、页脚 |

改配色只动 color 文件，改页脚只动 outer 文件——这是 beamer 官方的主题拆分
惯例，好处是改一处不会波及别处。

**主题文件在模板库里位于 `common/`**（两套演示模板共用），
用 `scripts/new-project.py` 生成的项目里则被展平到项目根目录，直接改即可。

## 主题提供的三个专用件

```latex
% 1. 证据区：主视觉在剩余空间里垂直居中
\begin{evidence}
  \includegraphics[width=0.8\linewidth]{ablation}
\end{evidence}

% 2. 一句话结论条，压在证据下面。只放一句，多了失去作用
\takeaway{增益集中在小目标，说明提升来自特征保留而非分类能力}

% 3. 备用页跳转（用 beamer 自带的 [label=]，没有额外机制）
\begin{frame}[label=bk:proof]{完整证明} ... \returnbutton{main:end}\end{frame}
\backuplink{bk:proof}{方差不增的完整证明}      % 写在索引页上
```

配色改过之后要重跑验证（对比度 + 色觉缺陷），脚本在 `presenting.md` §5.1。

## 一个关键配套

`\documentclass` 与 `\usetheme` 的 `fontset` 必须一致：

```latex
\documentclass[fontset=fandol]{ctexbeamer}   ←→  \usetheme[fontset=fandol]{Acad}
\documentclass[fontset=none]{ctexbeamer}     ←→  \usetheme[fontset=noto]{Acad}
```

改一个忘另一个，中文会掉字或回退到默认字体。

## 内容组织

### 分帧原则

**一帧一个论点。** 塞不下就拆帧，不要缩字号——投影仪上正文小于等效 20 pt
后排就看不清了，16:9 下模板的 `\normalsize` 已经接近这个下限。

### 帧标题写成结论句

这是幻灯片和论文最大的差别。听众只看标题就该拿到结论：

| 不要 | 要 |
|---|---|
| 实验结果 | mAP 提升 3.7 个百分点，小目标提升 6.2 个 |
| 方法介绍 | 让每个位置自己决定信任哪一层特征 |
| 相关工作 | 现有特征金字塔的两处结构性缺陷 |

### 逐步揭示

用 `\pause` 或 `\onslide<2->{}`，不要用转场特效。覆盖语法示例：

```latex
\begin{enumerate}
  \item<1-> 第一点
  \item<2-> 第二点
\end{enumerate}
\onslide<3->{\begin{block}{小结}...\end{block}}
```

**不要载入 `enumitem`**，它会破坏 `\item<2->` 的覆盖语法。这是 beamer
用户最常踩的坑。要调列表间距就在环境里写 `\setlength{\itemsep}{0.6em}`。

### 表格要比论文里再删一半

只留支撑当前论点的行与列，完整表格放备用页。用 `\alert{}` 或加粗指出
该看哪个数字。

### 备用页

`main.tex` 里 `\appendix` 之后的帧不计入页脚总页数（`appendixnumberbeamer`
的作用），所以听众看到的 "12/18" 不会被备用页误导。

放什么：预判会被问到的问题的答案——完整推导、完整对比表、失败案例、
超参数、与某篇相关工作的区别。提问环节直接翻过来，比现场画图有说服力。

### 演讲备注

在帧里写 `\note{...}`，然后：

```bash
make notes    # 生成双屏 PDF（左幻灯片、右备注），配 pdfpc 播放
```

备注写「讲的时候要强调什么」「预判的提问怎么答」，不要抄幻灯片上已有的字。

## 三个产物

```bash
make            # 普通版      main.pdf
make handout    # 讲义版      main-handout.pdf（忽略所有 \pause，一帧一页）
make notes      # 双屏备注版  main-notes.pdf
```

讲义版发给听众，普通版自己讲，备注版投影时用。

## 从论文派生幻灯片

如果论文已经写好，不要重写内容，按这个映射走：

| 论文 | 幻灯片 |
|---|---|
| 引言第 3 段（已有工作的不足） | 第 1–2 帧，全场的立论点，讲慢一点 |
| 方法的核心公式（1–2 个） | 1 帧，其余推导进备用页 |
| 主结果表 | 1 帧，删到只剩 3–4 行 |
| 消融表 | 1 帧，配一句「说明两个模块处理不同的误差来源」 |
| 定性结果图 | 1 帧，左右对比 |
| 结论 | 1 帧，三条，加局限与下一步 |

论文的记号直接复用——`acadmath.sty` 是两边共用的，`\vect{F}`、`\norm{}`、
`\argmin` 在幻灯片里写法完全一样，听众看完报告再看论文不用重新建立对应关系。

自定义记号（`\ourmethod`、`\dataset` 之类）记得从论文的 `preamble.tex`
拷到幻灯片的 `preamble.tex`。

## 配色

改 `beamercolorthemeAcad.sty` 最上面两行就能整体换一套：

```latex
\definecolor{AcadPrimary}  {RGB}{ 11,  61, 107}   % 主色
\definecolor{AcadSecondary}{RGB}{163, 100,  20}   % 强调色（\alert）
```

投影仪对比度低于显示器，正文与背景的亮度差要留足。默认这套在白底上的
对比度都高于 4.5:1。
