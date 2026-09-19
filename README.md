# 学术 LaTeX 模板（论文 / 报告 / 幻灯片 / 答辩 / 作业）

参照 [ustctug/ustcthesis](https://github.com/ustctug/ustcthesis) 的分层方式做的五套模板：
**样式全部收在文档类 / 主题文件里，正文文件里不出现任何格式命令**，所以改版式
和写内容互不干扰。

排版规则对应的国标与 ISO 条目见 [STANDARDS.md](STANDARDS.md)。
写作流程（定骨架、论证、投稿自查）在配套 skill：
[`skills/academic-writing/`](skills/academic-writing/SKILL.md)。

引擎是 **XeLaTeX** + **latexmk** + **biber**。脚手架脚本由 [uv](https://docs.astral.sh/uv/)
提供项目内 Python，不走系统全局解释器。

```bash
uv sync
uv run python scripts/new-project.py --list
uv run python scripts/new-project.py homework ~/Projects/algorithm-homework
uv run python scripts/new-project.py report ~/Projects/dl-lab3
```

Windows 把目标路径换成你的用户目录即可，例如
`uv run python scripts/new-project.py article %USERPROFILE%\Documents\my-paper`。

连续课程作业见 [homework/README.md](homework/README.md)，
编辑器编译与双向跳转见 [VSCODE.md](VSCODE.md)。
课程集合请用本仓库的 `scripts/new-project.py`，不要只用含 `main.tex` 的单文档拷贝。

---

## 目录结构

```text
latex-templates/
├── STANDARDS.md              学术排版标准考察（先看这个）
├── Makefile                  一键构建五套模板
├── homework/                 连续作业：identity.tex + hwN/
├── scripts/new-project.py    生成自包含项目
├── skills/academic-writing/  配套写作 skill
├── VSCODE.md                 编译与双向跳转说明
│
├── common/                   模板间共享
│   ├── acadbase.sty          article/report 的共用版式层
│   ├── acadmath.sty          数学记号约定（\vect \mat \norm \argmin \dd …）
│   ├── beamerthemeAcad.sty        ┐
│   ├── beamercolorthemeAcad.sty   │ beamer/defense 共用的视觉主题，
│   ├── beamerfontthemeAcad.sty    │ 按 beamer 官方惯例拆成五个文件
│   ├── beamerinnerthemeAcad.sty   │
│   ├── beamerouterthemeAcad.sty   ┘
│   └── refs.bib              参考文献库（各模板下是符号链接，改一处处处生效）
│
├── article/                  期刊论文 / 会议论文
│   ├── main.tex              ← 主控，只做装配
│   ├── acadarticle.cls       ← 论文特有版式（版面/标题层次/标题块/摘要/致谢）
│   ├── setup.tex             ← 题名/作者/单位/关键词/基金
│   ├── preamble.tex          ← 你自己的宏包与命令
│   ├── sections/             ← 正文
│   │   ├── abstract.tex
│   │   ├── 01-introduction.tex   …   05-conclusion.tex
│   │   ├── acknowledgements.tex
│   │   └── appendix.tex
│   ├── figures/
│   ├── latexmkrc
│   └── Makefile
│
├── report/                   实验报告 / 技术报告 / 课程报告
│   ├── main.tex              ← 主控
│   ├── acadreport.cls        ← 报告特有版式，三种封面在第 5 节
│   ├── setup.tex             ← 课程/实验名/姓名学号/指导教师，或报告编号/密级
│   ├── preamble.tex          ← 含代码清单（listings）配置
│   ├── sections/             ← 目的/原理/环境/步骤/数据/分析/结论/思考题
│   ├── figures/
│   ├── latexmkrc
│   └── Makefile
│
├── beamer/                   组会 / 会议 oral 幻灯片
│   ├── main.tex              ← 主控
│   ├── setup.tex             ← 题名/作者/单位/日期
│   ├── preamble.tex          ← 你自己的宏包与命令
│   ├── frames/               ← 内容，一个文件一段
│   ├── figures/
│   ├── latexmkrc
│   └── Makefile
│
└── defense/                  开题 / 中期 / 学位答辩幻灯片
    ├── main.tex              ← 与 beamer 同一套视觉主题，mode=defense
    ├── setup.tex             ← 题名/作者/导师/学号
    ├── preamble.tex
    ├── frames/               ← 选题→现状→内容→工作→创新点→成果→备用页
    ├── figures/
    ├── latexmkrc
    └── Makefile
```

---

## 安装依赖

需要：`xelatex`、`latexmk`、`biber`，以及中文/数学/文献相关宏包。
装好后用下面三条确认：

```bash
xelatex --version
latexmk -v
biber --version
```

脚手架另外需要 [uv](https://docs.astral.sh/uv/getting-started/installation/)（各系统安装方式见该页）。
然后在仓库根目录：

```bash
uv sync
```

### Arch Linux

```bash
sudo pacman -S texlive-basic texlive-latex texlive-latexrecommended texlive-latexextra \
  texlive-fontsrecommended texlive-mathscience texlive-bibtexextra texlive-binextra \
  texlive-xetex texlive-langchinese biber
```

一把梭（体积很大）：`sudo pacman -S texlive-meta biber`

缺宏包时：`pacman -F xxx.sty`

### Ubuntu / Debian

```bash
sudo apt update
sudo apt install texlive-xetex texlive-lang-chinese texlive-science \
  texlive-bibtex-extra texlive-fonts-recommended texlive-latex-extra \
  latexmk biber make
```

一把梭：`sudo apt install texlive-full`

缺宏包时：`apt-file update && apt-file search xxx.sty`

### Windows

任选其一：

1. **TeX Live**（[官方安装器](https://tug.org/texlive/windows.html)），勾选 scheme 时至少包含
   XeLaTeX、latexmk、biber、Chinese、LaTeX extra、Science、推荐字体。
2. **MiKTeX**（[官网](https://miktex.org/)），缺宏包时允许自动安装。
3. **WSL2 + Ubuntu**：按上一节装，Makefile 最省事。

没有 GNU Make 时，进入模板目录直接：

```bat
latexmk -xelatex -synctex=1 -interaction=nonstopmode -outdir=build main.tex
```

单轮预览（看内容，不跑 biber）：

```bat
xelatex -synctex=1 -halt-on-error -interaction=nonstopmode -output-directory=build main.tex
```

系统字体可把 `fontset` 改成 `windows`（ctex 调 SimSun / SimHei 等）。

### macOS

```bash
brew install --cask mactex-no-gui
```

或 BasicTeX 再 `tlmgr` 补集合。系统字体可把 `fontset` 改成 `mac`。
Make 一般随 Xcode Command Line Tools 提供。

### 字体

默认 `fontset=fandol`，Fandol 随 TeX Live 中文集合走，**零配置**，跨平台一致。

想更好看的中文，可改 `fontset=noto`（需系统 Noto CJK；等宽可用 Sarasa Gothic）：

| 系统 | Noto CJK |
| --- | --- |
| Arch | `sudo pacman -S noto-fonts-cjk ttf-sarasa-gothic` |
| Ubuntu / Debian | `sudo apt install fonts-noto-cjk` |
| Windows / macOS | 从 [Google Fonts Noto CJK](https://github.com/notofonts/noto-cjk) 安装 |

改法：

- `article` / `report` / `homework`：`main.tex` 里 `fontset = fandol` 改成 `noto`
- `beamer` / `defense`：`\documentclass[... fontset=none]` 与
  `\usetheme[... fontset=noto]{Acad}` **必须配套改**

也可用操作系统自带中文字体：`fontset=windows` / `mac` / `ubuntu`（ctex 内置映射）。

Noto 没有楷体和仿宋，模板里退化成宋体。要真楷体可装霞鹜文楷，把类文件 /
主题文件里 `\kaishu` 的字体名改成 `LXGW WenKai`。

西文用 TeX Gyre Termes + Heros，按**文件名**查找，不依赖 fontconfig。

### 配套 skill

写作工作流在 [`skills/academic-writing/`](skills/academic-writing/SKILL.md)，
和模板同一仓库，**不绑定任何编程助手**。助手若扫描项目下的 `skills/` 目录，
克隆后即可用；若只从它自己的用户 skills 目录加载，把
`skills/academic-writing` 链过去。脚本都通过 `$TPL`（含 `common/acadbase.sty`
的仓库根）定位模板，不要写死家目录。

---

## 编译

```bash
make setup      # uv 创建项目内 .venv（跑 Python 脚手架前）
make            # 五套都编（终稿）
make preview    # 五套单轮预览（看内容；引用可能过期）
make article    # 论文           → article/main.pdf
make report     # 实验/技术报告   → report/main.pdf
make beamer     # 组会/会议幻灯片 → beamer/main.pdf
make defense    # 答辩幻灯片      → defense/main.pdf
make homework   # 全部课程作业    → homework/hwN/main.pdf
make clean      # 清中间文件
```

写正文用 `make preview` 或编辑器里的「预览（单轮，看内容）」；交稿前用 `make`
或 `make check`。说明见 [VSCODE.md](VSCODE.md)。

`beamer` 和 `defense` 共用同一套视觉主题，区别在骨架：前者是
「动机→方法→结果→结论」，后者是「选题→现状→内容→工作→创新点→成果」，
后者的页脚还会显示当前节标题（委员会想知道你讲到哪了）。
怎么选、每节讲多久、答辩会被问什么，见
`skills/academic-writing/references/presenting.md`。

`report/` 一个类选项切三种形态：`type=lab`（实验报告，带课程/实验名/姓名学号/
同组人/指导教师/成绩栏封面）、`type=tech`（技术报告，GB/T 7713.3 的报告编号
与密级封面）、`type=course`（课程大作业，简化封面）。

也可以进到子目录单独用（无 Make 时改用上一节的 `latexmk` / `xelatex`）：

```bash
cd article && make watch
```

beamer 额外的两个产物：

```bash
cd beamer && make handout    # 讲义版，忽略所有 \pause，一帧一页
```

```bash
cd beamer && make notes      # 双屏备注版，配 pdfpc 播放
```

投稿前跑一遍检查：

```bash
cd article && make check     # 列出超长行、未定义的引用与文献
```

---

## 常见改动去哪里改

先分清是「多套都该改」还是「只改一套」——前者在 `common/`，后者在各自的
`.cls` / 主题文件里。

| 想改什么 | 改哪个文件 |
| --- | --- |
| 中英文切换 | 各 `main.tex` 的 `lang=zh\|en` |
| 中西文字体 | `common/acadbase.sty` §1 |
| 图表标题的位置与格式 | `common/acadbase.sty` §4 的 `captionsetup` |
| 定理环境的名字与样式 | `common/acadbase.sty` §6 |
| 参考文献样式 | 各 `main.tex` 的 `bibstyle=`（gb7714 / ieee / numeric / authoryear） |
| 数学正斜体规则 | 各 `main.tex` 的 `mathstyle=`（iso / tex） |
| 共享的数学记号 | `common/acadmath.sty` |
| 论文的页边距、行距 | `article/acadarticle.cls` §2 |
| 论文各级标题的字体与间距 | `article/acadarticle.cls` §3 的 `\ctexset` |
| 论文标题块、摘要块 | `article/acadarticle.cls` §6、§7 |
| 报告封面（三种） | `report/acadreport.cls` §5 的 `\makecover` |
| 报告的标题层次（改「一、二、三」） | `report/preamble.tex` 末尾有现成的一行 |
| 代码清单的配色与行号 | `report/preamble.tex` 的 `\lstset` |
| 幻灯片配色 | `common/beamercolorthemeAcad.sty`（通常只改前两个 `\definecolor`） |
| 幻灯片字号 | `common/beamerfontthemeAcad.sty` |
| 帧标题栏、页脚 | `common/beamerouterthemeAcad.sty` |
| 标题页、节页、列表符号 | `common/beamerinnerthemeAcad.sty` |
| 答辩模式的页脚（显示节标题） | `common/beamerthemeAcad.sty` 的 `mode=defense` |

---

## 加一套自己的模板

`article/`、`report/`、`beamer/`、`defense/` 不是写死的。这个目录下含 `template.conf` 的子目录会被 `scripts/new-project.py --list` 发现。

要加一套（学位论文、开题报告、海报、简历……）：

1. 新建目录，比如 `thesis/`
2. 单文档放 `main.tex`；课程集合可放 `hwN/main.tex`，由 Makefile 组织编译
3. 建议再放 `setup.tex` / `preamble.tex` / `sections/` / `latexmkrc` / `Makefile`，
   后两个里把 `TEXINPUTS` 设成 `../common//`（照抄 `article/` 的即可）
4. 写一个 `template.conf`：

```text
name  = 学位论文
desc  = 一句话说明，会显示在 --list 里
needs = acadbase.sty acadmath.sty     # 要哪些共享文件；留空则全拷
hint  = 建好项目之后第一件该做的事
doc   = paper.md                      # 对应 skill 里 references/ 下的写作指南
```

新模板要不要复用 `common/acadbase.sty`，取决于它是不是「一篇正文类文档」：
论文、报告、学位论文都该复用（字体、正斜体、三线表、定理、文献全都一致）；
海报、简历这类版式差异极大的，只复用 `acadmath.sty` 拿记号就够。

`template.conf` 只对模板本身有意义，`scripts/new-project.py` 生成项目时会把它剔掉。

---

## 几个用起来要注意的点

**盲审版一条命令切换。** `article/main.tex` 的类选项加上 `anonymous`，作者、
单位、基金、通信作者、致谢会自动隐去，正文一个字都不用改。注意
`\end{acknowledgements}` 必须**单独成行**，这是 `comment` 宏包的限制。

**送审加行号**：类选项加 `linenumbers`。`lineno` 与 `amsmath` 的多行公式
有已知冲突，若报错，把出问题的公式用 `\begin{linenomath}…\end{linenomath}` 包起来。

**单位不要手写。** 写 `\qty{5}{\kg}` 而不是 `5 kg`，写 `\num{1e-4}` 而不是
`1×10⁻⁴`。间距、正斜体、分节符都由 `siunitx` 按 GB 3100 处理好了。

**交叉引用一律用 `\cref`**，它会自动补上「图 / 表 / 式 / 定理」这些类型词，
中英文切换时也不用改正文。

**beamer 里不要载入 `enumitem`**，它会破坏 `\item<2->` 的覆盖语法——这是
beamer 用户最常踩的坑。要调列表间距就在 `itemize` 环境里写
`\setlength{\itemsep}{0.6em}`。

**共享文件靠 `TEXINPUTS`。** `common/acadmath.sty` 是通过 `latexmkrc` 和
`Makefile` 里设的 `TEXINPUTS=../common//` 找到的。如果你要把 `article/` 单独
拷到别处用，请改用 `scripts/new-project.py`，它会把共享文件展平进项目。

---

## 编译验证

默认示例在 XeLaTeX / TeX Live 2026 下验证过。
`make check` 会先编译，再检查缺失字符、超出版心与未解析引用，失败返回非零状态。
Underfull 和字体替代提示仍需按实际版面判断。新增模板或修改选项后应重新检查。

报告支持 `anonymous`，隐去模板提供的身份字段；正文、手写页眉标题与图片中的
身份仍需自行检查。`headingcolor=` 控制报告标题色，`print` 强制标题为黑色。
通用 tabular 不再自动缩小字号，表格浮动体和 longtable 保留表格字号设置。

仓库内项目生成器复制全部 common 文件以保证自包含；template.conf 的 needs/doc/hint 保留供外部写作工具使用。
