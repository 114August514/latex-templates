#!/usr/bin/env bash
# ----------------------------------------------------------------------------
# 编译并汇总排版问题。
#
#   check.sh [项目目录] [主文件名，默认 main]
#
# 退出码：
#   0  编译通过且无警告
#   1  编译失败 / 环境缺失
#   2  编译通过但有警告（超长行、未定义引用、未定义文献）
#
# 退出码 2 不是"可以忽略"的意思：Overfull hbox 表示有内容跑出版心，
# 未定义引用会在 PDF 里留下 ??，交出去都会被扣分。
# ----------------------------------------------------------------------------
set -uo pipefail

DIR="${1:-.}"
MAIN="${2:-main}"

die() { printf '错误：%s\n' "$1" >&2; exit 1; }

[[ -d "$DIR" ]] || die "目录不存在：$DIR"
cd "$DIR" || die "无法进入 $DIR"
[[ -f "$MAIN.tex" ]] || die "找不到 $DIR/$MAIN.tex（用第二个参数指定主文件名）"

command -v latexmk >/dev/null 2>&1 || die \
"没装 latexmk。各系统的安装方式见仓库 README「安装依赖」。"

printf '==> 编译 %s/%s.tex\n' "$DIR" "$MAIN"
latexmk "$MAIN.tex" >/dev/null 2>&1
BUILD_RC=$?

# 日志可能在 build/ 里（模板默认），也可能在当前目录
LOG=""
for cand in "build/$MAIN.log" "$MAIN.log"; do
  [[ -f "$cand" ]] && { LOG="$cand"; break; }
done
[[ -n "$LOG" ]] || die "编译没有产生日志，检查 latexmk 是否可用"

if [[ $BUILD_RC -ne 0 ]]; then
  printf '\n!! 编译失败。日志里的错误：\n\n'
  grep -nE '^![[:space:]]|^.*:[0-9]+:' "$LOG" | head -30
  printf '\n完整日志：%s/%s\n' "$DIR" "$LOG"
  printf '常见报错的修法见 references/troubleshooting.md\n'
  exit 1
fi

WARN=0

section() { printf '\n--- %s ---\n' "$1"; }

section "超出版心的行（Overfull hbox）"
if grep -nE 'Overfull \\hbox' "$LOG" | head -20 | grep .; then
  N=$(grep -cE 'Overfull \\hbox' "$LOG")
  printf '共 %s 处。断词或改写句子解决，不要用 \\hspace 硬挤。\n' "$N"
  WARN=1
else
  printf '无\n'
fi

section "未定义的交叉引用"
if grep -nE 'LaTeX Warning: Reference .* undefined' "$LOG" | head -20 | grep .; then
  printf '这些会在 PDF 里显示成 ??，检查 \\label 是否拼错。\n'
  WARN=1
else
  printf '无\n'
fi

section "未定义的文献"
if grep -nE 'LaTeX Warning: Citation .* undefined' "$LOG" | head -20 | grep .; then
  printf '检查 refs.bib 里有没有这个 key，以及 \\addbibresource 路径。\n'
  WARN=1
else
  printf '无\n'
fi

section "其他警告"
grep -nE '^Package .* Warning' "$LOG" \
  | grep -vE 'microtype|Font shape|hyperref Warning: Token not allowed' \
  | head -15 | grep . || printf '无\n'

PDF=""
for cand in "build/$MAIN.pdf" "$MAIN.pdf"; do
  [[ -f "$cand" ]] && { PDF="$cand"; break; }
done
[[ -n "$PDF" ]] && printf '\n==> 产物：%s/%s（%s 页）\n' "$DIR" "$PDF" \
  "$(pdfinfo "$PDF" 2>/dev/null | awk '/^Pages:/{print $2}' || echo '?')"

if [[ $WARN -eq 1 ]]; then
  printf '\n编译通过，但有上述问题需要处理。\n'
  exit 2
fi
printf '\n编译通过，无警告。\n'
exit 0
