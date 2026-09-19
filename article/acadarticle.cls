%%% ---------------------------------------------------------------------------
%%% acadarticle.cls —— 正式学术论文文档类
%%%
%%% 分层（借鉴 ustcthesis）：
%%%   ../common/acadbase.sty  三个文档类共用的版式（字体/数学/图表/定理/文献/超链接）
%%%   本文件                   论文特有的版面、标题层次、标题块、摘要、致谢、附录
%%%   setup.tex                元数据（题名、作者、单位、基金……）
%%%   preamble.tex             你自己的宏包与自定义命令
%%%   sections/                正文——里面不应出现任何格式命令
%%%
%%% 排版依据见 ../STANDARDS.md。引擎：XeLaTeX。
%%%
%%% 类选项：
%%%   lang      = zh | en           语言（影响标题体例、图表标签、定理名）
%%%   fontset   = fandol | noto | windows | mac | ubuntu | none
%%%   mathstyle = iso | tex         iso 遵循 GB/T 3101（大写字母作变量时亦斜体）
%%%   bibstyle  = gb7714 | gb7714ay | ieee | numeric | authoryear | none
%%%   anonymous                     盲审：隐去作者/单位/基金/致谢
%%%   linenumbers                   行号（送审稿用）
%%%   print                         纸质版：超链接一律黑色
%%%   其余选项（如 twocolumn、12pt）原样传给 article
%%% ---------------------------------------------------------------------------
\NeedsTeXFormat{LaTeX2e}[2021/06/01]
\ProvidesClass{acadarticle}[2026/07/26 v1.1 Formal academic article class]

%%% ===========================================================================
%%% 0. 选项
%%% ===========================================================================
\RequirePackage{kvoptions}
\RequirePackage{etoolbox}

\SetupKeyvalOptions{family=acad, prefix=acad@}
\DeclareStringOption[zh]{lang}
\DeclareStringOption[fandol]{fontset}
\DeclareStringOption[iso]{mathstyle}
\DeclareStringOption[gb7714]{bibstyle}
\DeclareBoolOption[false]{anonymous}
\DeclareBoolOption[false]{linenumbers}
\DeclareBoolOption[false]{print}
\DeclareDefaultOption{\PassOptionsToClass{\CurrentOption}{article}}
\ProcessKeyvalOptions*

\LoadClass[a4paper,11pt]{article}

%%% ===========================================================================
%%% 1. 共用版式层
%%%    载入全部宏包并设好通用默认值；下面各节只做论文特有的覆盖。
%%% ===========================================================================
\RequirePackage{acadbase}

%%% ===========================================================================
%%% 2. 版面
%%% ===========================================================================
\geometry{
  top = 2.8cm, bottom = 2.5cm, left = 2.5cm, right = 2.5cm,
}

% 行距：中文 1.35 倍（正文小四时视觉接近 1.5 倍行距），西文 1.05
\acad@ifzh{\linespread{1.35}}{\linespread{1.05}}
\setlength{\parindent}{2em}        % 中文首行缩进 2 字符
\setlength{\parskip}{0pt plus 1pt}

%%% ===========================================================================
%%% 3. 标题层次
%%%    依据：GB/T 7713.2—2022（正文层次用阿拉伯数字分级编号，不超过 4 级）
%%% ===========================================================================
\acad@ifzh{%
  \ctexset{
    section = {
      name = {,}, number = \arabic{section},
      format     = \zihao{4}\heiti\raggedright,
      aftername  = \quad,
      beforeskip = {14pt plus 3pt minus 2pt},
      afterskip  = {8pt plus 2pt minus 1pt},
    },
    subsection = {
      name = {,},
      format     = \zihao{-4}\heiti\raggedright,
      aftername  = \quad,
      beforeskip = {10pt plus 2pt minus 2pt},
      afterskip  = {6pt plus 1pt minus 1pt},
    },
    subsubsection = {
      name = {,},
      format     = \zihao{5}\heiti\raggedright,
      aftername  = \quad,
      beforeskip = {8pt plus 2pt minus 2pt},
      afterskip  = {5pt plus 1pt minus 1pt},
    },
    paragraph = {
      name = {,}, format = \zihao{5}\heiti, aftername = \quad, runin = true,
    },
  }%
}{%
  \ctexset{
    section       = {format = \Large\bfseries\sffamily\raggedright,
                     aftername = {\hspace{0.6em}}},
    subsection    = {format = \large\bfseries\sffamily\raggedright,
                     aftername = {\hspace{0.6em}}},
    subsubsection = {format = \normalsize\bfseries\sffamily\raggedright,
                     aftername = {\hspace{0.6em}}},
  }%
}
\setcounter{secnumdepth}{4}
\setcounter{tocdepth}{3}

%%% ===========================================================================
%%% 4. 页眉页脚
%%% ===========================================================================
\newcommand{\acad@runningtitle}{}
\newcommand{\runningtitle}[1]{\renewcommand{\acad@runningtitle}{#1}}
\pagestyle{fancy}
\fancyhf{}
\fancyhead[C]{\footnotesize\acad@runningtitle}
\fancyfoot[C]{\footnotesize\thepage}
\renewcommand{\headrulewidth}{0.4pt}
\renewcommand{\footrulewidth}{0pt}
\fancypagestyle{plain}{%
  \fancyhf{}\fancyfoot[C]{\footnotesize\thepage}%
  \renewcommand{\headrulewidth}{0pt}%
}

%%% ===========================================================================
%%% 5. 元数据命令（在 setup.tex 里填写）
%%% ===========================================================================
\newcommand{\acad@affiliation}{}
\newcommand{\acad@entitle}{}
\newcommand{\acad@enauthor}{}
\newcommand{\acad@enaffiliation}{}
\newcommand{\acad@keywords}{}
\newcommand{\acad@enkeywords}{}
\newcommand{\acad@clc}{}
\newcommand{\acad@doccode}{}
\newcommand{\acad@funding}{}
\newcommand{\acad@corresponding}{}

\newcommand{\affiliation}[1]{\renewcommand{\acad@affiliation}{#1}}
\newcommand{\entitle}[1]{\renewcommand{\acad@entitle}{#1}}
\newcommand{\enauthor}[1]{\renewcommand{\acad@enauthor}{#1}}
\newcommand{\enaffiliation}[1]{\renewcommand{\acad@enaffiliation}{#1}}
\newcommand{\keywords}[1]{\renewcommand{\acad@keywords}{#1}}
\newcommand{\enkeywords}[1]{\renewcommand{\acad@enkeywords}{#1}}
\newcommand{\clcnumber}[1]{\renewcommand{\acad@clc}{#1}}      % 中图分类号
\newcommand{\doccode}[1]{\renewcommand{\acad@doccode}{#1}}    % 文献标志码
\newcommand{\funding}[1]{\renewcommand{\acad@funding}{#1}}    % 基金项目
\newcommand{\corresponding}[1]{\renewcommand{\acad@corresponding}{#1}}

%%% ===========================================================================
%%% 6. 标题块
%%%    依据：GB/T 7713.2—2022 前置部分顺序
%%%    题名 → 作者 → 单位 →（摘要、关键词由 abstract 环境负责）
%%% ===========================================================================
\renewcommand{\maketitle}{%
  \begingroup
  \thispagestyle{plain}
  \centering
  \acad@ifzh{%
    {\zihao{2}\heiti\@title\par}%
    \vspace{12pt}%
    {\zihao{4}\fangsong
      \ifacad@anonymous 匿名作者\else\@author\fi\par}%
    \vspace{4pt}%
    {\zihao{-5}\songti
      \ifacad@anonymous （送审匿名版，作者单位已隐去）\else\acad@affiliation\fi\par}%
  }{%
    {\LARGE\bfseries\@title\par}%
    \vspace{12pt}%
    {\large\ifacad@anonymous Anonymous Author(s)\else\@author\fi\par}%
    \vspace{4pt}%
    {\small\itshape
      \ifacad@anonymous Affiliation withheld for review\else\acad@affiliation\fi\par}%
  }%
  \vspace{6pt}%
  \endgroup
  \ifacad@anonymous\else
    \ifdefempty{\acad@funding}{}{%
      \acad@blfootnote{\footnotesize\acad@ifzh{基金项目：}{Funding: }\acad@funding}}%
    \ifdefempty{\acad@corresponding}{}{%
      \acad@blfootnote{\footnotesize
        \acad@ifzh{通信作者：}{Corresponding author: }\acad@corresponding}}%
  \fi
  \par\vspace{4pt}%
}

%%% ===========================================================================
%%% 7. 摘要 / 关键词
%%%     中文块：摘要、关键词、中图分类号、文献标志码
%%%     英文块：题名、作者、单位、Abstract、Keywords
%%% ===========================================================================
\newcommand{\acad@absindent}{\hangindent=4.2em\hangafter=1\noindent}

\renewenvironment{abstract}{%
  \par\small
  \acad@ifzh{\acad@absindent{\heiti 摘\quad 要：}}%
            {\noindent{\bfseries Abstract\quad}}%
}{%
  \par
  \ifdefempty{\acad@keywords}{}{%
    \par\vspace{2pt}%
    \acad@ifzh{\acad@absindent{\heiti 关键词：}\acad@keywords}%
              {\noindent{\bfseries Keywords\quad}\acad@keywords}\par}%
  \acad@ifzh{%
    \ifdefempty{\acad@clc}{}{%
      \par\vspace{2pt}\noindent{\heiti 中图分类号：}\acad@clc
      \ifdefempty{\acad@doccode}{}{\hspace{2em}{\heiti 文献标志码：}\acad@doccode}\par}%
  }{}%
  \par\vspace{8pt}\normalsize
}

% 英文摘要块（lang=zh 时使用；lang=en 时通常不需要）
\newenvironment{enabstract}{%
  \par\small
  \begingroup
    \centering
    \ifdefempty{\acad@entitle}{}{{\large\bfseries\acad@entitle\par}\vspace{6pt}}%
    \ifdefempty{\acad@enauthor}{}{%
      {\normalsize\ifacad@anonymous Anonymous Author(s)\else\acad@enauthor\fi\par}%
      \vspace{3pt}}%
    \ifdefempty{\acad@enaffiliation}{}{%
      {\footnotesize\itshape
        \ifacad@anonymous Affiliation withheld for review\else\acad@enaffiliation\fi\par}}%
  \endgroup
  \vspace{6pt}%
  \hangindent=4.6em\hangafter=1\noindent{\bfseries Abstract:\quad}%
}{%
  \par
  \ifdefempty{\acad@enkeywords}{}{%
    \par\vspace{2pt}%
    \hangindent=4.6em\hangafter=1\noindent{\bfseries Keywords:\quad}\acad@enkeywords\par}%
  \par\vspace{8pt}\normalsize
}

%%% ===========================================================================
%%% 8. 致谢
%%%     GB/T 7713：致谢在参考文献**之前**。
%%%     anonymous 模式下整段丢弃（注意 \end{acknowledgements} 须单独成行）。
%%% ===========================================================================
\newenvironment{acad@ackbody}{%
  \section*{\acad@ifzh{致\quad 谢}{Acknowledgements}}%
  \addcontentsline{toc}{section}{\acad@ifzh{致谢}{Acknowledgements}}%
}{}
\ifacad@anonymous
  \excludecomment{acknowledgements}
\else
  \newenvironment{acknowledgements}
    {\begin{acad@ackbody}}{\end{acad@ackbody}}
\fi

%%% ===========================================================================
%%% 9. 附录
%%% ===========================================================================
\let\acad@origappendix\appendix
\renewcommand{\appendix}{%
  \acad@origappendix
  % \appendix 本身已把 \thesection 改成 \Alph{section}，这里只加前缀词
  \acad@ifzh{\ctexset{section/name = {附录,}}}%
            {\ctexset{section/name = {Appendix~,}}}%
  \setcounter{figure}{0}\renewcommand{\thefigure}{\Alph{section}\arabic{figure}}%
  \setcounter{table}{0}\renewcommand{\thetable}{\Alph{section}\arabic{table}}%
  \setcounter{equation}{0}\renewcommand{\theequation}{\Alph{section}\arabic{equation}}%
}

\endinput
