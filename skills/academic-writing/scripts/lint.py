#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""
LaTeX 静态检查——**不需要装 TeX**。

    lint.py [项目目录]

在没有 TeX 环境、或者想在编译前快速过一遍时用。它查这些：
  1. 花括号平衡、\\begin/\\end 配对
  2. 用了但哪里都没定义的宏（对照白名单）
  3. 同一编译单元内被 \\newcommand 定义两次的宏
  4. 用了但未定义的环境
  5. \\input / \\addbibresource 指向的文件是否存在
  6. \\cref / \\ref 指向的 label 是否存在，是否有重复 label
  7. \\cite 的 key 是否在 .bib 里
  8. \\definecolor 数值列表里的空格（xcolor 解析不保证）

退出码 0 = 干净，1 = 有待确认项。

**它查不出来的**（只有真编译才知道）：宏包是否装了、字体是否找得到、
宏包选项是否合法、盒子是否超宽、页面是否排得下、宏展开时的语义错误。
所以它通过不等于能编译，只是能排掉一大类低级错误。
"""
import re, sys, pathlib, collections

# ---------------------------------------------------------------- 白名单
KERNEL = set("""
newcommand renewcommand providecommand def edef gdef xdef let global long outer
begin end usepackage RequirePackage documentclass LoadClass ProvidesClass
ProvidesPackage NeedsTeXFormat DeclareOption ProcessOptions PassOptionsToClass
PassOptionsToPackage CurrentOption endinput input include includeonly
NewDocumentCommand RenewDocumentCommand ProvideDocumentCommand
DeclareDocumentCommand NewDocumentEnvironment newenvironment renewenvironment
newtheorem newtheoremstyle theoremstyle
section subsection subsubsection paragraph subparagraph part chapter appendix
title author date maketitle thanks and abstract tableofcontents listoffigures
label ref pageref cite bibliography bibliographystyle footnote footnotetext
footnotemark item textbf textit texttt textsf textrm textsc textnormal emph
underline textsuperscript textsubscript
small footnotesize scriptsize tiny normalsize large Large LARGE huge Huge
bfseries mdseries itshape slshape scshape upshape rmfamily sffamily ttfamily
normalfont selectfont familydefault sfdefault rmdefault ttdefault
centering raggedright raggedleft center flushleft flushright
vspace hspace vskip hskip smallskip medskip bigskip par newpage clearpage
cleardoublepage pagebreak linebreak newline noindent indent parindent parskip
baselineskip linespread stretch fill hfill vfill hss vss nointerlineskip
setlength addtolength newlength settowidth setcounter addtocounter
newcounter stepcounter refstepcounter value thepage arabic roman Roman alph
Alph fnsymbol chinese
makebox mbox parbox framebox fbox raisebox rule phantom hphantom vphantom
fboxsep fboxrule linewidth textwidth textheight columnwidth paperwidth
paperheight dimexpr numexpr glueexpr
hangindent hangafter leftmargin rightmargin listparindent itemindent labelwidth
labelsep topsep itemsep parsep partopsep list trivlist
quad qquad enspace thinspace negthinspace
frac dfrac tfrac sqrt sum prod int oint lim inf sup max min log ln exp
sin cos tan sec csc cot arcsin arccos arctan sinh cosh tanh det dim ker deg
gcd hom arg Pr bmod pmod
alpha beta gamma delta epsilon varepsilon zeta eta theta vartheta iota kappa
lambda mu nu xi pi varpi rho varrho sigma varsigma tau upsilon phi varphi chi
psi omega Gamma Delta Theta Lambda Xi Pi Sigma Upsilon Phi Psi Omega
times div pm mp cdot cdots ldots vdots ddots dots
leq geq le ge neq ne approx equiv sim simeq propto ll gg subset supset
subseteq supseteq in notin ni cup cap setminus emptyset varnothing
forall exists neg land lor
rightarrow leftarrow Rightarrow Leftarrow leftrightarrow Leftrightarrow
to gets mapsto longrightarrow implies iff
partial nabla infty prime circ bullet star dagger ddagger checkmark
hat bar tilde vec dot ddot overline widehat widetilde overbrace underbrace
overrightarrow
mathbb mathcal mathrm mathbf mathit mathsf mathtt mathnormal boldsymbol
left right big Big bigg Bigg bigl bigr Bigl Bigr biggl biggr
langle rangle lvert rvert lVert rVert lfloor rfloor lceil rceil vert Vert
displaystyle textstyle scriptstyle scriptscriptstyle
text ensuremath relax empty space
if ifx ifnum ifdim ifdefined ifcase else fi or expandafter csname endcsname
string protect noexpand the number
begingroup endgroup bgroup egroup newif setbox box copy hbox vbox
AtBeginDocument AtEndDocument AtEndPreamble AtBeginSection AtBeginSubsection
AtEndOfClass AtEndOfPackage DeclareRobustCommand
addcontentsline addtocontents contentsline numberline
thefootnote thesection thesubsection thefigure thetable theequation
figurename tablename refname bibname abstractname contentsname appendixname
proofname listfigurename listtablename indexname partname chaptername
verb verbatim symbol char
textbar textbackslash textasciitilde textunderscore textbullet
textdegree textcelsius textperiodcentered textendash textemdash
odot oplus ominus otimes wedge vee perp parallel angle triangle colon
mathpunct mathopen mathclose mathbin mathrel mathop qedhere qed
""".split())

PKG = set("""
ctexset zihao songti heiti fangsong kaishu xeCJKsetup setCJKmainfont
setCJKsansfont setCJKmonofont newCJKfontfamily setmainfont setsansfont
setmonofont setmathfont newfontfamily geometry newgeometry
unimathsetup symbf symbfit symbfup symbb symup symit symsf symcal
mathtoolsset DeclarePairedDelimiter DeclarePairedDelimiterX delimsize
sisetup DeclareSIUnit qty num unit numrange qtyrange numlist ang percent
degreeCelsius kilogram metre meter second ampere kelvin mole candela gram
per squared cubed micro milli kilo mega giga tera nano pico kg m s A K mol cd
ifdefstring ifdefempty ifbool booltrue boolfalse newbool setbool notbool
ifdef ifundef AtBeginEnvironment AtEndEnvironment patchcmd apptocmd pretocmd
robustify csuse csdef cslet newrobustcmd
SetupKeyvalOptions DeclareStringOption DeclareBoolOption DeclareDefaultOption
ProcessKeyvalOptions DeclareVoidOption
hypersetup phantomsection bookmark bookmarksetup pdfbookmark href url nolinkurl
cref Cref crefname Crefname creflabelformat crefformat Crefformat cpageref
crefpairconjunction crefmiddleconjunction creflastconjunction
crefrangeconjunction crefpairgroupconjunction crefmiddlegroupconjunction
creflastgroupconjunction namecref labelcref
fancyhf fancyhead fancyfoot fancypagestyle pagestyle thispagestyle
headrulewidth footrulewidth headheight headsep footskip
definecolor color textcolor colorbox fcolorbox pagecolor colorlet
setlist setlistdepth
addbibresource printbibliography citet citep textcite parencite footcite
upcite bibfont bibitemsep bibnamesep DeclareFieldFormat
State Statex If ElsIf Else EndIf For ForAll While EndWhile EndFor Repeat Until
Function EndFunction Procedure EndProcedure Require Ensure Return Call Comment
algorithmicrequire algorithmicensure algorithmicreturn floatname listof
caption captionsetup subcaption subref phantomsubcaption
includegraphics graphicspath resizebox scalebox rotatebox
toprule midrule bottomrule cmidrule multicolumn multirow hline cline
tabcolsep arraystretch makecell thead
threeparttable tnote
lstset lstinline lstlistingname lstinputlisting
excludecomment includecomment specialcomment
linenumbers nolinenumbers linenomath
thmname thmnumber thmnote
mathindent abovedisplayskip belowdisplayskip abovedisplayshortskip
belowdisplayshortskip topfraction bottomfraction textfraction
floatpagefraction topnumber bottomnumber totalnumber
microtypesetup bm operatorname DeclareMathOperator
hyperlink hypertarget hyperref autoref nameref
providebool ifboolexpr providecommandx
""".split())

BEAMER = set("""
usetheme usecolortheme usefonttheme useinnertheme useoutertheme mode
setbeamertemplate setbeamercolor setbeamerfont setbeamersize setbeameroption
addtobeamertemplate usebeamercolor usebeamerfont usebeamertemplate
frame frametitle framesubtitle titlepage sectionpage subsectionpage
inserttitle insertsubtitle insertauthor insertshortauthor insertinstitute
insertshortinstitute insertdate insertframetitle insertframesubtitle
insertframenumber inserttotalframenumber insertshorttitle inserttitlegraphic
insertsectionnumber insertsectionhead insertsubsectionhead
insertcontinuationcount insertcontinuationcountroman insertdescriptionitem
alert structure onslide only uncover visible invisible transparent note pause
titlegraphic institute subtitle logo deftranslation translate uselanguage
beamerbutton beamergotobutton beamerreturnbutton beamerskipbutton
hyperlinkframestart hyperlinkframeend hyperlinkframestartnext
hyperlinkappendixstart hyperlinkpresentationend againframe
""".split())

AT_INTERNAL = set("""
@author @title @date @empty @ifpackageloaded @ifundefined @namedef @nameuse
@ne @gobble @firstofone @secondoftwo @onlypreamble @ifnextchar @ifstar
@arstrutbox @array @makeother
""".split())

WHITELIST = KERNEL | PKG | BEAMER | AT_INTERNAL

ENV_WHITELIST = set("""
document abstract titlepage
itemize enumerate description list trivlist
equation align gather multline eqnarray split cases array matrix pmatrix
bmatrix vmatrix smallmatrix aligned gathered
figure table tabular longtable tabularx threeparttable tablenotes
subfigure subtable minipage center flushleft flushright
verbatim quote quotation lstlisting
algorithm algorithmic
frame columns column block alertblock exampleblock beamercolorbox
theorem lemma proposition corollary definition assumption example remark proof
""".split())

# ---------------------------------------------------------------- 收集
HARD = [
    (r'^\s*\\newcommand\*?\s*\{?\\([a-zA-Z@]+)', 'newcommand'),
    (r'^\s*\\NewDocumentCommand\s*\{?\\([a-zA-Z@]+)', 'NewDocumentCommand'),
    (r'^\s*\\DeclareMathOperator\*?\s*\{\\([a-zA-Z@]+)', 'MathOperator'),
    (r'^\s*\\DeclarePairedDelimiterX?\s*\{\\([a-zA-Z@]+)', 'PairedDelimiter'),
    (r'^\s*\\DeclareSIUnit\s*\{\\([a-zA-Z@]+)', 'SIUnit'),
    (r'^\s*\\newlength\s*\{\\([a-zA-Z@]+)', 'newlength'),
    (r'^\s*\\newCJKfontfamily\s*(?:\[[^\]]*\])?\s*\\([a-zA-Z@]+)', 'CJKfont'),
]
SOFT = [
    r'\\(?:new|renew|provide)command\*?\s*\{?\\([a-zA-Z@]+)',
    r'\\(?:New|Renew|Provide|Declare)DocumentCommand\s*\{?\\([a-zA-Z@]+)',
    r'\\[gex]?def\s*\\([a-zA-Z@]+)', r'\\let\s*\\([a-zA-Z@]+)',
    r'\\DeclareMathOperator\*?\s*\{\\([a-zA-Z@]+)',
    r'\\DeclarePairedDelimiterX?\s*\{\\([a-zA-Z@]+)',
    r'\\DeclareSIUnit\s*\{\\([a-zA-Z@]+)',
    r'\\newlength\s*\{\\([a-zA-Z@]+)',
    r'\\newCJKfontfamily\s*(?:\[[^\]]*\])?\s*\\([a-zA-Z@]+)',
    r'\\newbool\s*\{([a-zA-Z@]+)\}', r'\\newtheoremstyle\s*\{([a-zA-Z@]+)\}',
]
ENV_DEF = [
    r'\\(?:new|renew)environment\s*\{([a-zA-Z@*]+)\}',
    r'\\newtheorem\*?\s*\{([a-zA-Z@]+)\}',
    r'\\(?:exclude|include|special)comment\s*\{([a-zA-Z@]+)\}',
]

def uncomment(text):
    return '\n'.join(re.sub(r'(?<!\\)%.*$', '', l) for l in text.splitlines())

def main():
    root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
    if not root.is_dir():
        print(f'错误：{root} 不是目录'); return 1
    files = [p for p in sorted(root.rglob('*'))
             if p.suffix in ('.tex', '.sty', '.cls') and not p.is_symlink()
             and 'build' not in p.parts]
    if not files:
        print(f'{root} 下没有找到 .tex/.sty/.cls'); return 1

    src = {p: uncomment(p.read_text(encoding='utf-8', errors='replace')) for p in files}
    noverb = {p: re.sub(r'\\begin\{(lstlisting|verbatim)\}.*?\\end\{\1\}', '', t, flags=re.S)
              for p, t in src.items()}
    rel = lambda p: str(p.relative_to(root))
    issues = 0

    def head(n, title):
        print(f'\n--- {n}. {title} ' + '-' * max(0, 56 - len(title)))

    # 1 括号与环境
    head(1, '花括号平衡与环境配对')
    ok = True
    for p, t in src.items():
        depth, stack, errs = 0, [], []
        for i, line in enumerate(t.splitlines(), 1):
            depth += (lambda s: s.count('{') - s.count('}'))(re.sub(r'\\[{}%&#_$]', '', line))
            for m in re.finditer(r'\\(begin|end)\{([^}]+)\}', line):
                k, n = m.groups()
                if k == 'begin': stack.append((n, i))
                elif not stack: errs.append(f'L{i} \\end{{{n}}} 无对应 begin')
                elif stack[-1][0] != n:
                    errs.append(f'L{i} \\end{{{n}}} 与 L{stack[-1][1]} 的 \\begin{{{stack[-1][0]}}} 不匹配')
                    stack.pop()
                else: stack.pop()
        errs += [f'L{i} \\begin{{{n}}} 未闭合' for n, i in stack]
        if depth: errs.append(f'花括号差 {depth:+d}')
        if errs:
            ok = False; issues += len(errs)
            print(f'  !! {rel(p)}')
            for e in errs: print(f'       {e}')
    if ok: print(f'  ✓ {len(files)} 个文件')

    # 收集定义
    hard, soft, envdefs = collections.defaultdict(list), set(), set()
    for p, t in src.items():
        for pat, kind in HARD:
            for m in re.finditer(pat, t, re.M): hard[m.group(1)].append((p, kind))
        for pat in SOFT: soft |= {m.group(1) for m in re.finditer(pat, t)}
        for pat in ENV_DEF: envdefs |= {m.group(1) for m in re.finditer(pat, t)}
        for m in re.finditer(r'\\DeclareStringOption\s*(?:\[[^\]]*\])?\s*\{([a-zA-Z]+)\}', t):
            soft |= {f'{pre}{m.group(1)}' for pre in ('acad@', 'Acad@')}
        for m in re.finditer(r'\\DeclareBoolOption\s*(?:\[[^\]]*\])?\s*\{([a-zA-Z]+)\}', t):
            soft |= {f'{pre}{m.group(1)}' for pre in ('ifacad@', 'ifAcad@')}
    WL = WHITELIST | soft

    # 2 未定义的宏
    #   \ifdefined\Foo 这种「故意可能没定义、由外部注入」的宏不算问题，
    #   模板里 make notes 就是靠 -usepretex 注入 \AcadShowNotes 的。
    head(2, '用了但没定义的宏')
    guarded = set()
    for t in src.values():
        guarded |= {m.group(1) for m in
                    re.finditer(r'\\(?:ifdefined|ifdef|ifundef|@ifundefined)\s*\{?\\?([a-zA-Z@]+)', t)}
    unknown = collections.defaultdict(set)
    for p, t in noverb.items():
        for m in re.finditer(r'\\([a-zA-Z@]{2,})', t):
            if m.group(1) not in WL and m.group(1) not in guarded:
                unknown[m.group(1)].add(rel(p))
    if unknown:
        for n in sorted(unknown):
            print(f'  \\{n:<26} {", ".join(sorted(unknown[n])[:3])}'); issues += 1
        print('  提示：白名单不可能覆盖所有宏包，逐个确认是不是真的没定义。')
    else: print('  ✓ 无')
    if guarded:
        print(f'  （已跳过 \\ifdefined 保护的：{", ".join("\\" + g for g in sorted(guarded))}）')

    # 3 重复硬定义
    #   同一文件里两个定义挨得很近、且前面有分支宏，说明是 if/else 的两个分支，
    #   运行时只执行一个，不算重复定义。
    head(3, '同名宏被 \\newcommand 定义两次')
    BRANCH = re.compile(r'\\(?:@ifpackageloaded|@ifclassloaded|ifdefstring|ifdefempty'
                        r'|ifbool|ifdef|ifundef|ifcsdef|[Aa]cad@ifzh|[Aa]cad@iftype)')
    def lineno_of(p, name, kind):
        for i, line in enumerate(src[p].splitlines(), 1):
            if re.match(r'\s*\\\w+\*?\s*\{?\\' + re.escape(name) + r'\b', line): yield i
    dup, safe = [], []
    for n, o in sorted(hard.items()):
        if len(o) < 2: continue
        if len({p for p, _ in o}) == 1:                     # 同一个文件
            p = o[0][0]; lines = list(lineno_of(p, n, None))
            if len(lines) >= 2 and lines[-1] - lines[0] <= 15:
                ctx = '\n'.join(src[p].splitlines()[max(0, lines[0] - 8):lines[0]])
                if BRANCH.search(ctx):
                    safe.append(n); continue
        dup.append((n, o))
    if dup:
        for n, o in dup:
            print(f'  \\{n}: ' + '; '.join(f'{rel(p)} ({k})' for p, k in o)); issues += 1
        print('  提示：跨文件同名而两个文件不会同时载入时（比如两套模板各自的'
              ' preamble），可以忽略。')
    else: print('  ✓ 无')
    if safe:
        print(f'  （已识别为条件分支、安全：{", ".join("\\" + s for s in safe)}）')

    # 4 未定义的环境
    head(4, '用了但没定义的环境')
    badenv = collections.defaultdict(set)
    for p, t in noverb.items():
        for m in re.finditer(r'\\begin\{([a-zA-Z@*]+)\}', t):
            n = m.group(1)
            if n not in ENV_WHITELIST and n.rstrip('*') not in ENV_WHITELIST and n not in envdefs:
                badenv[n].add(rel(p))
    if badenv:
        for n in sorted(badenv):
            print(f'  {n:<22} {", ".join(sorted(badenv[n])[:3])}'); issues += 1
    else: print('  ✓ 无')

    # 5 文件引用
    head(5, '\\input / \\addbibresource 目标')
    miss = False
    for p, t in src.items():
        for m in re.finditer(r'\\(?:input|include)\{([^}]+)\}', t):
            tgt = m.group(1)
            if not any((p.parent / c).exists() for c in (tgt, tgt + '.tex')):
                print(f'  !! {rel(p)}: \\input{{{tgt}}} 找不到'); miss = True; issues += 1
        for m in re.finditer(r'\\addbibresource\{([^}]+)\}', t):
            if not (p.parent / m.group(1)).exists():
                print(f'  !! {rel(p)}: {m.group(1)} 找不到'); miss = True; issues += 1
    if not miss: print('  ✓ 无')

    # 6 label
    head(6, '交叉引用与重复 label')
    labels = collections.defaultdict(list)
    used = set()
    for p, t in src.items():
        for m in re.finditer(r'\\label\{([^}]+)\}', t): labels[m.group(1)].append(rel(p))
        for m in re.finditer(r'\\(?:[Cc]ref|ref|pageref)\{([^}]+)\}', t):
            used |= {x.strip() for x in m.group(1).split(',') if x.strip()}
    bad6 = False
    for k in sorted(used - set(labels)):
        if '...' in k or '#' in k: continue
        print(f'  !! 引用了不存在的 label: {k}'); bad6 = True; issues += 1
    for k, v in sorted(labels.items()):
        if len(v) > 1:
            print(f'  !! 重复 label {k}: {", ".join(v)}'); bad6 = True; issues += 1
    if not bad6: print('  ✓ 无')

    # 7 cite
    head(7, '\\cite 的 key')
    keys = set()
    for b in root.rglob('*.bib'):
        keys |= {m.group(1) for m in
                 re.finditer(r'^@[a-zA-Z]+\{([^,]+),', b.read_text(encoding='utf-8', errors='replace'), re.M)}
    cited = set()
    for t in src.values():
        for m in re.finditer(r'\\(?:cite|citep|citet|parencite|textcite|footcite|upcite)\*?(?:\[[^\]]*\])*\{([^}]+)\}', t):
            cited |= {x.strip() for x in m.group(1).split(',') if x.strip()}
    bad7 = [k for k in sorted(cited - keys) if '...' not in k and '#' not in k]
    if bad7:
        for k in bad7: print(f'  !! .bib 里没有: {k}'); issues += 1
    else: print(f'  ✓ 无（.bib 共 {len(keys)} 条）')

    # 8 definecolor 空格
    head(8, '\\definecolor 数值列表里的空格')
    bad8 = False
    for p, t in src.items():
        for m in re.finditer(r'\\definecolor\{[^}]+\}\s*\{[A-Za-z]+\}\s*\{([^}]*\s[^}]*)\}', t):
            print(f'  !! {rel(p)}: {{{m.group(1)}}} —— 去掉空格更保险'); bad8 = True; issues += 1
    if not bad8: print('  ✓ 无')

    print('\n' + '=' * 62)
    if issues:
        print(f'{issues} 项待确认。注意本工具查不出宏包缺失、字体缺失、')
        print('宏包选项非法、盒子超宽——那些只有真编译才知道。')
    else:
        print('静态检查全部通过。但这不等于能编译：宏包/字体是否装了、')
        print('选项是否合法、盒子是否超宽，仍需要 xelatex 跑一遍才知道。')
    print('=' * 62)
    return 1 if issues else 0

sys.exit(main())
