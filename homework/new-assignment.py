#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Create a blank assignment without copying existing answers or build files."""
import argparse
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('name',help='e.g. hw2');args=p.parse_args()
if not args.name.startswith('hw') or not args.name[2:].isdigit(): p.error('name must be hw followed by digits')
root=Path(__file__).resolve().parent; dest=root/args.name
if dest.exists(): p.error(f'{dest} already exists')
(dest/'sections').mkdir(parents=True)
(dest/'main.tex').write_text((root/'hw1/main.tex').read_text())
(dest/'setup.tex').write_text('''% !TeX root = main.tex
\\input{identity}
\\title{Homework NUMBER}
\\submitdate{\\today}
\\runningtitle{Homework NUMBER}
\\addbibresource{refs.bib}
'''.replace('NUMBER',args.name[2:]))
(dest/'sections/01-problem1.tex').write_text('''% !TeX root = ../main.tex
\\problem{题目}
在这里填写题目。
\\begin{solution}
在这里填写解答。题目要求证明时，在本环境内再用 proof。
\\end{solution}
''')
(dest/'refs.bib').write_text('% 本次作业的参考文献\n')
for name in ['Makefile','latexmkrc']: (dest/name).symlink_to('../'+name)
print(dest)
