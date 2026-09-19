# 连续课程作业

在课程目录运行 `make` 编译所有 `hw*/`；在 `hw1/` 运行 `make` 只编译本次作业。
改题解时用 `make preview`（单轮，看内容）；交作业前用 `make` 或 `make check`。

- `identity.tex`：课程、姓名、学号、教师，各次共用。
- `preamble.tex`：课程共用宏包和记号。
- `hwN/setup.tex`：本次标题、日期、文献。
- `hwN/sections/`：本次题目和解答，每个文件带主文件标记。
- `hwN/build/`：PDF、SyncTeX 和编译缓存；编辑时打开这里的 PDF。

新增作业：`uv run python new-assignment.py hw2`。已有目录会拒绝覆盖，也不会复制旧答案。

写法：`\problem[20]{题目}`，解答放进 `solution` 环境，使用 `\correctness`、
`proof` 和 `\complexity` 组织论证。算法环境默认可浮动，确需紧随题目时再用 `[H]`。
无编号公式用 `\[ ... \]`，多行推导用 `align*`。通用复杂度记号包含
`\bigO{n}`、`\bigOmega{n}`、`\bigTheta{n}`。

模板中的身份均为占位符，首次使用先填写。标题颜色可设 `headingcolor=acadhead`，
打印用 `print`。封面字段宽度可在 preamble 中以
`\renewcommand{\coverlabelwidth}{5em}`、`\renewcommand{\coverfieldwidth}{12em}` 调整。
