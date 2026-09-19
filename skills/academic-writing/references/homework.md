# 课程作业流水线（homework）

连续作业用 `homework` 模板：课程身份在 `identity.tex`，每次题目在 `hwN/`。
封面和标题色是 `type=course` + `headingcolor=acadhead`。
实验报告、结课论文走 `report.md`，不要用作业骨架。

作业只区分两件事：**解**还是**证**。不要预设算法课的「正确性 / 复杂度」小节；
电磁学、分析、线代同样用这一套。某门课特有的标题或记号写进该课的
`preamble.tex`。

## 一道题怎么写

```latex
\problem[10]{题干一句话}
题目原文。

\begin{solution}
  % 作答
\end{solution}
```

`\problem[分数]{标题}` 渲染成「问题 1 标题（10 分）」。分数可省略。

| | `solution` | `proof` |
|---|---|---|
| 是什么 | 整道题的作答，标题「解答」 | 一条命题的证明，有证毕符 |
| 何时用 | 这道题要交答案 | 题目在问「证明 …」 |
| 电磁学计算、代数值、写步骤 | 只用这个 | 不用 |
| 「证明高斯定理在此条件下成立」 | 外层仍用这个 | 里面再用 `proof` |

纯计算：

```latex
\begin{solution}
由 $\nabla\cdot\vect{E}=\rho/\varepsilon_0$ 得 …
\end{solution}
```

证明题：外层仍是解答，里面才是证明——助教先看到「这是第几题的答案」，再看到证毕。

```latex
\begin{solution}
\begin{proof}
…
\end{proof}
\end{solution}
```

又要结果又要证明（例如先写出通解再证唯一性）：都放在同一个 `solution` 里，只把论证放进 `proof`。

不要把整道题外包一层 `proof`（没有单独的命题时，证毕符会莫名其妙）。

## 课程自己的记号

算法课若仍要「正确性证明 / 复杂度分析」小标题，或 `\bigO{n}`，写在
`preamble.tex`，不要改 `acadhomework.sty`。电磁学则在 preamble 里加自己的
$\varepsilon_0$、$\vect{B}$ 等（`acadmath` 已有 `\vect` `\dd`）。

## 封面

- `headingcolor=acadhead`：节标题藏青。打印加类选项 `print`。
- `\logo{...}` 写在 `identity.tex`。有校徽时封面不再重复学校全称。
- 校徽放课程目录 `figures/`。

## 文件分工

| 文件 | 放什么 |
|---|---|
| `identity.tex` | 学校、院系、课程、姓名学号、教师、校徽；全学期共用 |
| `preamble.tex` | **这门课**的宏包和记号 |
| `hwN/setup.tex` | 本次标题、日期、文献 |
| `hwN/sections/` | 每题一个文件 |
