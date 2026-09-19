# 连续课程作业

在课程目录运行 `make` 编译所有 `hw*/`；在 `hw1/` 运行 `make` 只编译本次作业。
改题解时用 `make preview`（单轮，看内容）；交作业前用 `make` 或 `make check`。

- `identity.tex`：课程、姓名、学号、教师，各次共用。
- `preamble.tex`：课程共用宏包和记号。
- `hwN/setup.tex`：本次标题、日期、文献。
- `hwN/sections/`：本次题目和解答，每个文件带主文件标记。
- `hwN/build/`：PDF、SyncTeX 和编译缓存；编辑时打开这里的 PDF。

新增作业：`uv run python new-assignment.py hw2`。已有目录会拒绝覆盖，也不会复制旧答案。

每道题：题目 + `solution`。题目要你证明时，在解答里再套 `proof`。
电磁学计算、代数值、写步骤只用 `solution`。算法课若要「正确性 / 复杂度」小标题，
写在 `preamble.tex`，不要改类文件。

身份是占位符，先改 `identity.tex`。校徽用 `\logo{\includegraphics[width=0.62\textwidth]{cover}}`，
图放课程目录 `figures/`。标题色默认藏青（`headingcolor=acadhead`），打印加类选项 `print`。
