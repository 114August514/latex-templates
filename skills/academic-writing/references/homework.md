# 课程作业流水线（homework）

连续作业用 `homework` 模板：课程身份在 `identity.tex`，每次题目在 `hwN/`。
封面和标题色与课程报告同一套（`type=course` + `headingcolor=acadhead`）。
实验报告、结课论文仍走 `report.md`。

## 一道题怎么写

先抄题目，再包一层 **解答**。证明只包「要证的那句话」，不要把整道题塞进 `proof`。

```latex
\problem[20]{题干一句话}
题目原文或改写。需要算法时把伪代码放在题目或解答里。

\begin{solution}
  % 整道题的作答：算法、计算、说明、证明都可以放这里
\end{solution}
```

`\problem[分数]{标题}` 渲染成「问题 1 标题（20 分）」。分数可省略。

## 何时用 solution、何时用 proof

| 环境 / 命令 | 它是什么 | 什么时候用 |
|---|---|---|
| `solution` | 整道题的作答容器，标题是「解答」 | **每道要交的题都用**。算法、数值、说明、证明都装在里面 |
| `proof` | amsthm 的证明环境，结尾有证毕符 | 只包**一条明确命题**的论证。正确性、下界、恒等式、递推式成立 |
| `\correctness` | 小标题「正确性证明」 | 解答里即将写出证明，给助教一个锚点；后面通常接 `proof` |
| `\complexity` | 小标题「复杂度分析」 | 写时间 / 空间。多数是计数或主定理，**不必**再套 `proof` |

判断句：**这句话是不是在证「某命题为真」？** 是，用 `proof`；不是，写在 `solution` 里即可。

| 题目在问 | 写法 |
|---|---|
| 给出算法 / 算出一个数 / 解释步骤 | 只放 `solution`，不要 `proof` |
| 「证明正确性」「证明 … 成立」 | `solution` 里 `\correctness` + `proof` |
| 「分析复杂度」「给出 $\Theta$」 | `solution` 里 `\complexity`，直接写 $T(n)$ |
| 「严格证明 $T(n)=\ldots$」 | `\complexity` 后再用 `proof` 证递推 |
| 既要算法又要正确性和复杂度 | 算法 → `\correctness`+`proof` → `\complexity` |

不要做的事：

- 整道解答外包一层 `proof`（没有证毕对象，证毕符会莫名其妙）
- 用英文手写 `Proof of Correctness:`，用 `\correctness`
- 把循环次数的口算写成 `proof`（那是分析，不是命题证明）

## 例子

算法题（模板 `hw1` 的骨架）：

```latex
\begin{solution}
\begin{algorithm}[htbp]
  \caption{数组求和}\label{alg:sum}
  ...
\end{algorithm}
\correctness
\begin{proof}
完成第 $i$ 次迭代后，$s=\sum_{j=1}^{i} A[j]$。
\end{proof}
\complexity
\cref{alg:sum} 的时间复杂度为 $\bigTheta{n}$，额外空间为 $\bigO{1}$。
\end{solution}
```

纯证明题（下界、恒等式）：题目本身就是命题，解答里可以直接 `proof`，不必再写「正确性证明」。

```latex
\begin{solution}
\begin{proof}
...
\end{proof}
\end{solution}
```

算法放在题目里、下面只证明（像 StoogeSort 那种题）：伪代码可以在 `solution` 之前，证明仍进 `solution`。

## 封面与标题色

- `headingcolor=acadhead`：节标题藏青。打印用类选项 `print`，标题转黑。
- `\logo{...}` 写在 `identity.tex`。有校徽时封面不再重复学校全称。
- 校徽放课程目录的 `figures/`，各次作业都能找到（`\graphicspath` 已含 `../figures/`）。

## 文件分工

| 文件 | 放什么 |
|---|---|
| `identity.tex` | 学校、院系、课程、姓名学号、教师、校徽；全学期共用 |
| `preamble.tex` | 课程共用宏包和记号 |
| `hwN/setup.tex` | 本次标题、日期、文献 |
| `hwN/sections/` | 每题一个文件 |
