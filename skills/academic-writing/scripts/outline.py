#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""
反向提纲（reverse outline）——**不需要装 TeX**。

    outline.py [项目目录] [--full]

把已经写好的正文抽成「每段一句话」的骨架，让你在一屏之内读完全文的论证。
这是检验结构最有效的方法：句子层面的问题看不出来，但顺序错了、
两段在说同一件事、从 A 跳到 C 缺了 B——在这张表上一眼就能看见。

改稿顺序应该是「结构 → 段落 → 句子 → 词汇」。先打磨句子再发现整段要删，
那些功夫全白费。所以先跑这个。

还会顺带报几类中文学术写作的高频病灶（名词化、机械连接词、超长句、模糊词），
每一类都给出行号，方便直接去改。判断依据见 references/writing.md。

--full  连同每段的完整首句一起输出（默认截断到 50 字）
"""
import re, sys, pathlib, collections

# 这些环境里的内容不是叙述文字，整体丢掉
DROP_ENVS = ('figure', 'figure\\*', 'table', 'table\\*', 'tabular', 'longtable',
             'threeparttable', 'equation', 'equation\\*', 'align', 'align\\*',
             'gather', 'gather\\*', 'multline', 'multline\\*', 'algorithm',
             'algorithmic', 'lstlisting', 'verbatim', 'subfigure', 'tikzpicture')

# 这些命令连同它的花括号参数一起丢掉
DROP_CMDS = ('label', 'cite', 'citep', 'citet', 'ref', 'cref', 'Cref', 'pageref',
             'includegraphics', 'placeholder', 'input', 'usepackage', 'bibliography',
             'addbibresource', 'index', 'nocite', 'vspace', 'hspace', 'setlength')

# 这些命令丢掉命令本身、保留花括号里的文字
KEEP_ARG = ('textbf', 'textit', 'emph', 'texttt', 'textrm', 'textsf', 'alert',
            'underline', 'text', 'mbox', 'caption', 'href', 'url', 'lstinline')

def detex(s):
    """把 LaTeX 源码压成大致可读的纯文本。不求精确，够做提纲即可。"""
    s = re.sub(r'(?<!\\)%.*$', '', s, flags=re.M)                  # 注释
    for env in DROP_ENVS:                                          # 非叙述环境
        s = re.sub(r'\\begin\{' + env + r'\}.*?\\end\{' + env.replace('\\*', r'\*') + r'\}',
                   ' ', s, flags=re.S)
    s = re.sub(r'\$\$.*?\$\$', ' ', s, flags=re.S)                 # 行间公式
    s = re.sub(r'(?<!\\)\$.*?(?<!\\)\$', '〔式〕', s, flags=re.S)   # 行内公式
    for c in DROP_CMDS:
        s = re.sub(r'\\' + c + r'\*?(\[[^\]]*\])?(\{[^{}]*\})*', ' ', s)
    for c in KEEP_ARG:
        s = re.sub(r'\\' + c + r'\*?(\[[^\]]*\])?\{([^{}]*)\}', r'\2', s)
    s = re.sub(r'\\(begin|end)\{[^}]*\}', '\n\n', s)               # 其余环境边界当段落分隔
    s = re.sub(r'\\[a-zA-Z@]+\*?(\[[^\]]*\])?', ' ', s)            # 剩下的命令
    s = re.sub(r'[{}]', '', s)
    s = re.sub(r'[ \t]+', ' ', s)
    s = re.sub(r' +([，。；：！？、）」』])', r'\1', s)      # 剥掉命令后遗留的空格
    s = re.sub(r'([（「『]) +', r'\1', s)
    return s

SENT_END = '。！？!?'
def first_sentence(p):
    p = re.sub(r'\s+', ' ', p).strip()      # 源码换行不是句子的一部分
    CJK = r'\u4e00-\u9fff\u3000-\u303f\uff00-\uffef'
    p = re.sub(f'(?<=[{CJK}]) (?=[{CJK}])', '', p)   # 汉字与中文标点之间不留空格
    for i, ch in enumerate(p):
        if ch in SENT_END:
            return p[:i + 1]
        if ch == '.' and i + 1 < len(p) and p[i + 1] in ' \n':      # 英文句号
            return p[:i + 1]
    return p

def width(s):                                                       # 汉字算 2
    return sum(2 if ord(c) > 0x2E80 else 1 for c in s)

def clip(s, n):
    out, w = '', 0
    for c in s:
        cw = 2 if ord(c) > 0x2E80 else 1
        if w + cw > n:
            return out + '…'
        out += c; w += cw
    return out

SEC = re.compile(r'\\(section|subsection|subsubsection)\*?\{(.+?)\}')
NEWCMD = re.compile(r'\\newcommand\*?\s*\{?\\([a-zA-Z]+)\}?\s*\{([^{}]*)\}')

def macro_table(root):
    """收集项目里无参数的文本宏（\\ourmethod、\\dataset 之类），提纲里展开它们。
    否则「本文提出 \\ourmethod{}。」会被剥成「本文提出 。」，读不出意思。"""
    tbl = {}
    for p in list(root.rglob('*.tex')) + list(root.rglob('*.sty')) + list(root.rglob('*.cls')):
        if p.is_symlink() or 'build' in p.parts:
            continue
        txt = re.sub(r'(?<!\\)%.*$', '', p.read_text(encoding='utf-8', errors='replace'),
                     flags=re.M)
        for m in NEWCMD.finditer(txt):
            name, body = m.group(1), m.group(2)
            if '#' in body or '\\' in body or not body.strip():
                continue                                            # 只要纯文本宏
            tbl.setdefault(name, body.strip())
    return tbl

def expand(s, tbl):
    for name, body in tbl.items():
        s = re.sub(r'\\' + name + r'(\{\})?(?![a-zA-Z])', body, s)
    return s

def analyse(path, tbl):
    # 关键：标题位置与切块必须在**同一份**文本上算，否则位置错配会把段落切碎
    clean = re.sub(r'(?<!\\)%.*$', '', path.read_text(encoding='utf-8', errors='replace'),
                   flags=re.M)
    clean = expand(clean, tbl)
    marks = [(m.start(), m.group(1), m.group(2)) for m in SEC.finditer(clean)]
    blocks = []
    for i, (pos, lvl, title) in enumerate(marks):
        end = marks[i + 1][0] if i + 1 < len(marks) else len(clean)
        blocks.append((lvl, re.sub(r'\\[a-zA-Z@]+\*?', '', title).strip('{} '),
                       clean[pos:end]))
    if not blocks:
        blocks = [(None, None, clean)]

    out = []
    for lvl, title, body in blocks:
        body = SEC.sub(' ', body, count=1)                           # 去掉本节标题本身
        paras = [p for p in re.split(r'\n\s*\n', detex(body))
                 if len(re.sub(r'[\s〔〕]', '', p)) > 12]
        out.append((lvl, title, [first_sentence(p) for p in paras]))
    return out

# ---- 中文学术写作的高频病灶 ----
CHECKS = [
    ('名词化', re.compile(r'(进行|实现|完成|开展|作出|给出)了?(一定|相应|有效)?的?'
                          r'[\u4e00-\u9fff]{2,6}(研究|分析|设计|改进|优化|提升|采集|处理|验证|比较)'),
     '把「进行了……的研究」改成「研究了……」，全文能短 10%~15%'),
    ('机械连接词', re.compile(r'(首先|其次|再次|最后|然后)[，,、]'),
     '这类词只说明有顺序，不说明为什么是这个顺序；换成有信息量的连接'),
    ('模糊词', re.compile(r'(基本上|相对来说|一定程度上|较为|有所提升|有所改善|大体上|差不多)'),
     '学术写作里这些词等于没说，要么给数字要么删掉'),
    ('被动堆叠', re.compile(r'被[\u4e00-\u9fff]{1,4}所'),
     '「被……所……」是欧化句式，中文里改成主动或无主语句'),
]

def lint_prose(path):
    hits = collections.defaultdict(list)
    for i, line in enumerate(path.read_text(encoding='utf-8', errors='replace').splitlines(), 1):
        code = re.sub(r'(?<!\\)%.*$', '', line)
        for name, pat, _ in CHECKS:
            for m in pat.finditer(code):
                hits[name].append((i, m.group(0)))
        # 超长句：两个句号之间超过 60 个汉字
        for seg in re.split(r'[。！？]', re.sub(r'\\[a-zA-Z@]+\*?(\{[^{}]*\})*', '', code)):
            n = len(re.findall(r'[\u4e00-\u9fff]', seg))
            if n > 60:
                hits['超长句'].append((i, f'{n} 字'))
    return hits

def main():
    args = [a for a in sys.argv[1:] if not a.startswith('-')]
    full = '--full' in sys.argv
    root = pathlib.Path(args[0] if args else '.').resolve()
    if not root.is_dir():
        print(f'错误：{root} 不是目录'); return 1

    files = sorted([p for p in root.rglob('*.tex')
                    if not p.is_symlink() and 'build' not in p.parts
                    and p.stem not in ('main', 'setup', 'preamble')])
    if not files:
        print(f'{root} 下没有正文 .tex（跳过了 main/setup/preamble）'); return 1

    print('=' * 68)
    print(f'反向提纲：{root.name}')
    print('=' * 68)
    print('把每段抽成一句话。读这张表，问三个问题：')
    print('  顺序对吗？ 有没有两段在说同一件事？ 有没有从 A 跳到 C 缺了 B？')
    print()

    tbl = macro_table(root)
    total_par = 0
    thin, fat, sec_acc = [], [], []
    for f in files:
        print(f'\033[1m{f.relative_to(root)}\033[0m' if sys.stdout.isatty()
              else f'--- {f.relative_to(root)} ---')
        for lvl, title, sents in analyse(f, tbl):
            indent = {'section': '', 'subsection': '  ', 'subsubsection': '    '}.get(lvl, '')
            if title:
                print(f'{indent}▍{title}')
            for i, s in enumerate(sents, 1):
                s = s if full else clip(s, 68)
                print(f'{indent}   ¶{i}  {s}')
            total_par += len(sents)
            if lvl == 'section':
                cur = [f.name, title, len(sents)]; sec_acc.append(cur)
            elif sec_acc:
                sec_acc[-1][2] += len(sents)      # 子节的段落算进所属的节
        print()

    for fn, title, n in sec_acc:
        if n <= 1: thin.append((fn, title, n))
        if n >= 12: fat.append((fn, title, n))

    print('=' * 68)
    print(f'共 {len(files)} 个正文文件，{total_par} 个段落')
    if thin:
        print('\n段落过少的节（可能没展开，或者本来就不该单独成节）：')
        for fn, t, n in thin: print(f'  {t}（{n} 段） in {fn}')
    if fat:
        print('\n段落过多的节（可能该拆成子节）：')
        for fn, t, n in fat: print(f'  {t}（{n} 段） in {fn}')

    print('\n' + '=' * 68)
    print('文字层的高频病灶（依据 references/writing.md §2、§3）')
    print('=' * 68)
    any_hit = False
    for f in files:
        hits = lint_prose(f)
        if not hits: continue
        any_hit = True
        print(f'\n{f.relative_to(root)}')
        for name, items in hits.items():
            why = next((w for n, _, w in CHECKS if n == name), '')
            shown = items[:5]
            print(f'  {name}（{len(items)} 处）'
                  + (f' —— {why}' if why else ''))
            for ln, txt in shown:
                print(f'      L{ln}: {txt}')
            if len(items) > len(shown):
                print(f'      … 另有 {len(items) - len(shown)} 处')
    if not any_hit:
        print('\n  无')

    print('\n' + '=' * 68)
    print('注意：这是**结构**检查，不判断内容对不对。')
    print('提纲读着通顺不等于论证成立——论证上的硬伤见 writing.md §6。')
    print('=' * 68)
    return 0

sys.exit(main())
