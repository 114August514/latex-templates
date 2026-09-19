# 编译报错对照表

先看日志里第一条 `!` 开头的错误，后面的报错往往是它的连锁反应。
`check.sh` 已经把前 30 条错误摘出来了。

## 找不到文件

### `File 'acadbase.sty' not found` / `acadmath.sty not found`

共享文件靠 `TEXINPUTS` 找到。三种情况：

1. 在模板目录里编译 —— 用 `make` 而不是直接 `xelatex`，Makefile 里设了
   `TEXINPUTS=../common//`
2. 手动编译 —— `export TEXINPUTS=../common//:$TEXINPUTS`
3. 把某个模板单独拷走了 —— 用 `scripts/new-project.py` 重新建项目，
   它会把共享文件展平进项目目录

### `File 'xxx.sty' not found`（宏包缺失）

各系统怎么查、完整安装命令见仓库 README「安装依赖」。常见归属：

| 宏包 | TeX Live 集合（名称因发行版而异） |
|---|---|
| `ctex` `xeCJK` fandol | `langchinese` / `texlive-lang-chinese` |
| `unicode-math` `siunitx` | `mathscience` / `texlive-science` |
| `biblatex-gb7714-2015` | `bibtexextra` / `texlive-bibtex-extra` |
| `caption` `algorithm` `listings` 等 | `latexextra` / `texlive-latex-extra` |
| TeX Gyre（含 `texgyretermes-math.otf`） | `fontsrecommended` |
| `latexmk` | `binextra`，Ubuntu 上是独立的 `latexmk` 包 |
| `biber` | 有的系统是独立包，不在 texlive 元包里 |

### `Package fontspec Error: The font "texgyretermes" cannot be found`

推荐字体集合没装。模板按**文件名**查找 OpenType，不依赖 fontconfig，
但 TeX 树里必须有这些 `.otf`。

### `Package fontspec Error: The font "Noto Serif CJK SC" cannot be found`

用了 `fontset=noto` 但系统没装 Noto CJK。改回 `fontset=fandol`，
或按 README 安装对应字体包。

## 参考文献

### 文献全是 `[?]`，PDF 里没有参考文献表

biber 没跑成功。依次检查：

1. `biber` 装了吗（`command -v biber`）
2. `\addbibresource{refs.bib}` 路径对吗
3. `build/main.blg` 里有没有 biber 的报错
4. 删掉 `build/` 重新 `make`（`.bcf` 与 `.bbl` 版本不匹配时会静默失败）

### `Package biblatex Error: Style 'gb7714-2015' not found`

`texlive-bibtexextra` 没装。或者临时改成 `bibstyle=numeric` 先编过。

### `Biber ... datamodel` 相关警告

多半是 `.bib` 里某个字段用错了条目类型。比如 `@thesis` 要 `type={phdthesis}`
和 `institution=`，不是 `school=`。

## 中文相关

### 中文全部不显示 / 显示成方块

`fontset` 用了 `none` 但没手动设 CJK 字体。改成 `fandol` 或 `noto`。

### `Package xeCJK Error: CJK family 'zhhei' is undefined`

`\heiti` 之类在 `fontset=none` 下没定义。模板里有 `\providecommand` 兜底，
如果还报错说明有别的代码在兜底之前用了它——检查 `preamble.tex` 是否
过早引用。

### PDF 书签乱码

用 XeLaTeX 编译（模板 `latexmkrc` 里 `$pdf_mode = 5` 已经设好）。
如果手动跑了 `pdflatex`，删掉 `build/` 用 `make` 重来。

## 数学

### `Package unicode-math Error: Math font ... does not contain ...`

TeX Gyre Termes Math 缺某个符号。两个办法：换字体
（`\setmathfont{texgyrepagella-math.otf}` 或 `texgyredejavu-math.otf`），
或者对那个符号单独用 `\setmathfontface`。

### `\bm` / `physics` 宏包不工作

`unicode-math` 与它们有已知冲突。用模板提供的 `\vect{}` `\mat{}` `\tens{}`
代替 `\bm`；`physics` 宏包建议不要用。

### `lineno` 打开后多行公式报错

`lineno` 与 `amsmath` 的已知冲突。把出问题的公式包起来：

```latex
\begin{linenomath}
\begin{align} ... \end{align}
\end{linenomath}
```

## beamer

### `\item<2->` 不起作用，覆盖全乱

载入了 `enumitem`。删掉它——beamer 用户最常踩的坑。要调列表间距在环境里写
`\setlength{\itemsep}{0.6em}`。

### 中文掉字 / 字体不对

`\documentclass` 和 `\usetheme` 的 `fontset` 不配套。必须成对：

```latex
\documentclass[fontset=fandol]{ctexbeamer} ←→ \usetheme[fontset=fandol]{Acad}
\documentclass[fontset=none]{ctexbeamer}   ←→ \usetheme[fontset=noto]{Acad}
```

### 页脚总页数不对，把备用页也算进去了

`\appendix` 写在备用页之前了吗？`appendixnumberbeamer` 靠它划界。

### `make notes` 出来的还是普通版

`preamble.tex` 里的 `\ifdefined\AcadShowNotes` 分支被改动过。Makefile 通过
`-usepretex='\def\AcadShowNotes{}'` 注入这个宏。

## 排版警告

### `Overfull \hbox (Xpt too wide)`

有内容超出版心。**不能忽略**——打印出来会跑到页边外面。按代价从低到高：

1. 改写那句话（最好的办法）
2. 长英文词/URL 加断词点：`\hyphenation{opti-mi-za-tion}` 或用 `\url{}`
3. 表格太宽：缩字号 `\small`、用 `\resizebox`、或改成横排 `\begin{sidewaystable}`
4. 公式太长：用 `align` 拆行

### `Underfull \vbox`

页面底部留白过多，通常是浮动体挤走了正文。调整图表位置参数
（`[htbp]` → `[!htbp]`），或把图移到别的位置。

### `LaTeX Warning: Reference 'xxx' undefined`

`\label` 拼错，或者 `\label` 写在了 `\caption` 之前（必须在之后）。
多编译一次也能解决首次编译的假警告——`latexmk` 会自动处理，
所以如果用 `make` 还报，就是真的拼错了。
