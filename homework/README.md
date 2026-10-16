# 连续课程作业

在课程目录运行 `make` 编译所有 `hw*/`；在 `hw1/` 运行 `make` 只编译本次作业。
改题解时用 `make preview`（单轮，看内容）；交作业前用 `make` 或 `make check`。

- `identity.tex`：课程、姓名、学号、教师，各次共用。
- `preamble.tex`：课程共用宏包和记号。
- `hwN/setup.tex`：本次标题、日期、文献。
- `hwN/sections/`：本次题目和解答，每个文件带主文件标记。
- `hwN/build/`：PDF、SyncTeX 和编译缓存；编辑时打开这里的 PDF。

新增作业：`uv run python new-assignment.py hw2`。已有目录会拒绝覆盖，也不会复制旧答案。

每道题的写法：
- **题目环境（顶线嵌入式标题框）**：使用 `\begin{problem}[分值]{标题} ... \end{problem}`，自动生成嵌在顶边线上的标题并注册目录与书签；
- **单问作答**：作答用 `\begin{solution} ... \end{solution}`，以「解：」开头并在末尾自动右对齐空心方块；需证明时在解答里套 `proof`（自动统一为加粗黑体「证明：」并智能消除重复证毕符）；
- **多小问大题（逐问作答）**：大题题干放进 `problem` 框中作为已知条件，后续小问使用 `\begin{subproblems}` 包裹，每个小问用 `\subproblem[分值]{题干}` 紧接 `\begin{solution}`。小问内部支持 `\label`，正文可用 `\cref` 自动引用为「小问 (1)」。
- **版式与垂直节奏**：全局统一行间公式留白（`\abovedisplayskip`）与段落间隔，题解与小问保持纯黑正文字体，消除视觉杂质与多余底色。
- 标题色默认人教课本青蓝（`#1C60A9`），打印加类选项 `print` 自动切为纯黑细线框。

身份是占位符，先改 `identity.tex`。封面校徽示例是 `figures/cover.png`，换成自己的图即可。
