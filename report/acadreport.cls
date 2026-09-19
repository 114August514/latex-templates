%%% ---------------------------------------------------------------------------
%%% acadreport.cls —— 实验报告 / 技术报告 / 课程报告文档类
%%%
%%% 与 acadarticle.cls 共用 ../common/acadbase.sty，所以字体、数学正斜体、
%%% 三线表、定理环境、参考文献样式、交叉引用全都和论文模板一致——
%%% 实验报告里的记号可以原样搬进论文，不用重新调。
%%%
%%% 分层：
%%%   ../common/acadbase.sty  共用版式
%%%   本文件                   封面、版面、标题层次、报告特有环境
%%%   setup.tex                元数据（课程、实验名、姓名学号、指导教师……）
%%%   preamble.tex             你自己的宏包与命令
%%%   sections/                正文
%%%
%%% 类选项：
%%%   type      = lab | tech | course
%%%               lab    实验报告：课程/实验名/姓名学号/同组人/指导教师/成绩栏
%%%               tech   技术报告：报告编号/密级/承担单位/编写审核批准（GB/T 7713.3）
%%%               course 课程报告：简化封面，适合大作业与结课论文
%%%   lang      = zh | en
%%%   fontset   = fandol | noto | windows | mac | ubuntu | none
%%%   mathstyle = iso | tex
%%%   bibstyle  = gb7714 | gb7714ay | ieee | numeric | authoryear | none
%%%   anonymous / linenumbers / print   同 acadarticle
%%% ---------------------------------------------------------------------------
\NeedsTeXFormat{LaTeX2e}[2021/06/01]
\ProvidesClass{acadreport}[2026/07/26 v1.0 Laboratory and technical report class]

%%% ===========================================================================
%%% 0. 选项
%%% ===========================================================================
\RequirePackage{kvoptions}
\RequirePackage{etoolbox}

\SetupKeyvalOptions{family=acad, prefix=acad@}
\DeclareStringOption[lab]{type}
\DeclareStringOption[zh]{lang}
\DeclareStringOption[fandol]{fontset}
\DeclareStringOption[iso]{mathstyle}
\DeclareStringOption[gb7714]{bibstyle}
\DeclareStringOption[black]{headingcolor}
\DeclareBoolOption[false]{anonymous}
\DeclareBoolOption[false]{linenumbers}
\DeclareBoolOption[false]{print}
\DeclareDefaultOption{\PassOptionsToClass{\CurrentOption}{article}}
\ProcessKeyvalOptions*

\LoadClass[a4paper,12pt]{article}   % 报告比论文字号大一号，便于批阅

\RequirePackage{acadbase}

\ifacad@print\def\acad@headingcolor{black}\fi
\newcommand{\acad@iftype}[3]{\ifdefstring{\acad@type}{#1}{#2}{#3}}

%%% ===========================================================================
%%% 1. 版面
%%%    报告经常要手写批注，页边距比论文留得宽一些。
%%% ===========================================================================
\geometry{top = 2.6cm, bottom = 2.4cm, left = 2.8cm, right = 2.4cm}

\acad@ifzh{\linespread{1.4}}{\linespread{1.1}}
\setlength{\parindent}{2em}
\setlength{\parskip}{0pt plus 1pt}

%%% ===========================================================================
%%% 2. 标题层次
%%%    默认阿拉伯数字分级（GB/T 7713.2）。
%%%    若你的课程要求「一、二、三」的传统写法，把 section 的两行换成：
%%%      name = {,、}, number = \chinese{section},
%%% ===========================================================================
\acad@ifzh{%
  \ctexset{
    section = {
      name = {,}, number = \arabic{section},
      format     = \zihao{-3}\heiti\raggedright\color{\acad@headingcolor},
      aftername  = \quad,
      beforeskip = {16pt plus 3pt minus 2pt},
      afterskip  = {9pt plus 2pt minus 1pt},
    },
    subsection = {
      name = {,},
      format     = \zihao{4}\heiti\raggedright\color{\acad@headingcolor},
      aftername  = \quad,
      beforeskip = {11pt plus 2pt minus 2pt},
      afterskip  = {6pt plus 1pt minus 1pt},
    },
    subsubsection = {
      name = {,},
      format     = \zihao{-4}\heiti\raggedright\color{\acad@headingcolor},
      aftername  = \quad,
      beforeskip = {9pt plus 2pt minus 2pt},
      afterskip  = {5pt plus 1pt minus 1pt},
    },
    paragraph = {name = {,}, format = \zihao{-4}\heiti,
                 aftername = \quad, runin = true},
  }%
}{%
  \ctexset{
    section       = {format = \Large\bfseries\sffamily\raggedright\color{\acad@headingcolor},
                     aftername = {\hspace{0.6em}}},
    subsection    = {format = \large\bfseries\sffamily\raggedright\color{\acad@headingcolor},
                     aftername = {\hspace{0.6em}}},
    subsubsection = {format = \normalsize\bfseries\sffamily\raggedright\color{\acad@headingcolor},
                     aftername = {\hspace{0.6em}}},
  }%
}
\setcounter{secnumdepth}{4}
\setcounter{tocdepth}{2}

%%% ===========================================================================
%%% 3. 元数据（在 setup.tex 里填写）
%%% ===========================================================================
% —— 通用 ——
\newcommand{\acad@school}{}        \newcommand{\school}[1]{\renewcommand{\acad@school}{#1}}
\newcommand{\acad@department}{}    \newcommand{\department}[1]{\renewcommand{\acad@department}{#1}}
\newcommand{\acad@subtitle}{}      \newcommand{\subtitle}[1]{\renewcommand{\acad@subtitle}{#1}}
\newcommand{\acad@logo}{}          \newcommand{\logo}[1]{\renewcommand{\acad@logo}{#1}}
\newcommand{\acad@keywords}{}      \newcommand{\keywords}[1]{\renewcommand{\acad@keywords}{#1}}

% —— type=lab / course ——
\newcommand{\acad@course}{}        \newcommand{\course}[1]{\renewcommand{\acad@course}{#1}}
\newcommand{\acad@expname}{}       \newcommand{\experimentname}[1]{\renewcommand{\acad@expname}{#1}}
\newcommand{\acad@expno}{}         \newcommand{\experimentno}[1]{\renewcommand{\acad@expno}{#1}}
\newcommand{\acad@studentname}{}   \newcommand{\studentname}[1]{\renewcommand{\acad@studentname}{#1}}
\newcommand{\acad@studentid}{}     \newcommand{\studentid}[1]{\renewcommand{\acad@studentid}{#1}}
\newcommand{\acad@classname}{}     \newcommand{\classname}[1]{\renewcommand{\acad@classname}{#1}}
\newcommand{\acad@partners}{}      \newcommand{\partners}[1]{\renewcommand{\acad@partners}{#1}}
\newcommand{\acad@instructor}{}    \newcommand{\instructor}[1]{\renewcommand{\acad@instructor}{#1}}
\newcommand{\acad@expdate}{}       \newcommand{\expdate}[1]{\renewcommand{\acad@expdate}{#1}}
\newcommand{\acad@submitdate}{}    \newcommand{\submitdate}[1]{\renewcommand{\acad@submitdate}{#1}}

% —— type=tech（GB/T 7713.3—2014 科技报告编写规则）——
\newcommand{\acad@reportno}{}      \newcommand{\reportno}[1]{\renewcommand{\acad@reportno}{#1}}
\newcommand{\acad@seclevel}{}      \newcommand{\seclevel}[1]{\renewcommand{\acad@seclevel}{#1}}
\newcommand{\acad@organization}{}  \newcommand{\organization}[1]{\renewcommand{\acad@organization}{#1}}
\newcommand{\acad@authors}{}       \newcommand{\authors}[1]{\renewcommand{\acad@authors}{#1}}
\newcommand{\acad@reviewer}{}      \newcommand{\reviewer}[1]{\renewcommand{\acad@reviewer}{#1}}
\newcommand{\acad@approver}{}      \newcommand{\approver}[1]{\renewcommand{\acad@approver}{#1}}
\newcommand{\acad@reportversion}{} \newcommand{\reportversion}[1]{\renewcommand{\acad@reportversion}{#1}}

%%% ===========================================================================
%%% 4. 页眉页脚
%%%    页眉右侧带姓名学号，打印后不容易和同学的报告混在一起。
%%% ===========================================================================
\newcommand{\acad@runningtitle}{}
\newcommand{\runningtitle}[1]{\renewcommand{\acad@runningtitle}{#1}}
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\footnotesize\acad@runningtitle}
\fancyhead[R]{\footnotesize\acad@studentname\ \acad@studentid}
\fancyfoot[C]{\footnotesize\thepage}
\renewcommand{\headrulewidth}{0.4pt}
\renewcommand{\footrulewidth}{0pt}
\fancypagestyle{plain}{%
  \fancyhf{}\fancyfoot[C]{\footnotesize\thepage}%
  \renewcommand{\headrulewidth}{0pt}%
}

%%% ===========================================================================
%%% 5. 封面
%%%    \makecover 按 type 选项渲染三种封面之一。
%%%    改封面版式只动这一节。
%%% ===========================================================================
% 标签宽度：中文标签手工用 \qquad 排成等宽，英文标签需要更宽
\acad@ifzh{\newcommand{\coverlabelwidth}{5em}}{\newcommand{\coverlabelwidth}{8em}}
\newcommand{\coverfieldwidth}{12em}
\newcommand{\acad@lbl}[1]{\makebox[\coverlabelwidth][l]{\heiti #1}}
\newcommand{\acad@val}[2][\coverfieldwidth]{\underline{\makebox[#1][c]{#2}}}

% \acad@row[值的宽度]{中文标签}{英文标签}{值}
\newcommand{\acad@row}[4][\coverfieldwidth]{%
  \acad@lbl{\acad@ifzh{#2}{#3}}%
  \acad@ifzh{：}{:\hspace{0.4em}}%
  \acad@val[#1]{#4}\par\vspace{1.0em}%
}

\newcommand{\makecover}{%
  \hypersetup{pageanchor=false}%
  \begin{titlepage}
  \thispagestyle{empty}
  \centering
  \ifdefempty{\acad@logo}{}{{\acad@logo\par}\vspace{1.0em}}%
  \acad@iftype{tech}{%
    %%% —— 技术报告封面（GB/T 7713.3）——
    \begingroup\raggedright\zihao{-4}\songti
      \ifdefempty{\acad@reportno}{}{%
        \acad@ifzh{报告编号：}{Report No.: }\acad@reportno\par}%
      \ifdefempty{\acad@seclevel}{}{%
        \acad@ifzh{密\qquad 级：}{Classification: }\acad@seclevel\par}%
    \endgroup
    \vspace{4.5cm}
    {\zihao{2}\heiti\@title\par}%
    \ifdefempty{\acad@subtitle}{}{\vspace{0.8em}{\zihao{3}\heiti\acad@subtitle\par}}%
    \ifdefempty{\acad@reportversion}{}{\vspace{1.2em}{\zihao{4}\songti\acad@reportversion\par}}%
    \vspace{4.0cm}
    \begingroup\zihao{4}\songti
      \acad@row{承担单位}{Organization}{\acad@organization}%
      \acad@row{编\qquad 写}{Prepared by}{\acad@authors}%
      \acad@row{审\qquad 核}{Reviewed by}{\acad@reviewer}%
      \acad@row{批\qquad 准}{Approved by}{\acad@approver}%
      \acad@row{日\qquad 期}{Date}{\acad@submitdate}%
    \endgroup
  }{%
    \acad@iftype{course}{%
      %%% —— 课程报告封面（简化）——
      \vspace{2.5cm}
      \ifdefempty{\acad@school}{}{{\zihao{2}\heiti\acad@school\par}\vspace{0.5em}}%
      \ifdefempty{\acad@department}{}{{\zihao{3}\heiti\acad@department\par}}%
      \vspace{3.0cm}
      \ifdefempty{\acad@course}{}{{\zihao{3}\songti\acad@course\par}\vspace{1.2em}}%
      {\zihao{2}\heiti\@title\par}%
      \ifdefempty{\acad@subtitle}{}{\vspace{0.8em}{\zihao{4}\songti\acad@subtitle\par}}%
      \vspace{2.0cm}
      \begingroup\zihao{4}\songti
        \acad@row{姓\qquad 名}{Name}{\acad@studentname}%
        \acad@row{学\qquad 号}{Student ID}{\acad@studentid}%
        \acad@row{院\qquad 系}{Department}{\acad@department}%
        \acad@row{课程名称}{Course}{\acad@course}%
        \acad@row{授课老师}{Instructor}{\acad@instructor}%
        \acad@row{日\qquad 期}{Date}{\acad@submitdate}%
      \endgroup
    }{%
      %%% —— 实验报告封面（默认，type=lab）——
      \vspace{1.8cm}
      \ifdefempty{\acad@school}{}{{\zihao{2}\heiti\acad@school\par}\vspace{0.4em}}%
      \ifdefempty{\acad@department}{}{{\zihao{3}\heiti\acad@department\par}}%
      \vspace{2.4cm}
      {\zihao{1}\heiti\acad@ifzh{实\quad 验\quad 报\quad 告}{Laboratory Report}\par}%
      \vspace{2.6cm}
      \begingroup\zihao{4}\songti
        \acad@row[14em]{课程名称}{Course}{\acad@course}%
        \acad@row[14em]{实验名称}{Experiment}{%
          \ifdefempty{\acad@expno}{}{\acad@ifzh{实验\acad@expno}{No.~\acad@expno}\quad}%
          \acad@expname}%
        \acad@row[14em]{姓\qquad 名}{Name}{\acad@studentname}%
        \acad@row[14em]{学\qquad 号}{Student ID}{\acad@studentid}%
        \acad@row[14em]{班\qquad 级}{Class}{\acad@classname}%
        \ifdefempty{\acad@partners}{}{%
          \acad@row[14em]{同\ 组\ 人}{Partners}{\acad@partners}}%
        \acad@row[14em]{指导教师}{Instructor}{\acad@instructor}%
        \acad@row[14em]{实验日期}{Date Performed}{\acad@expdate}%
        \acad@row[14em]{提交日期}{Date Submitted}{\acad@submitdate}%
        \vspace{0.6em}%
        \acad@row[14em]{成\qquad 绩}{Grade}{}%
      \endgroup
    }%
  }%
  \vfill
  \end{titlepage}
  \setcounter{page}{1}%
  \hypersetup{pageanchor=true}%
}

%%% ===========================================================================
%%% 6. 摘要（技术报告需要；实验报告一般不需要，不写就不会出现）
%%% ===========================================================================
\renewenvironment{abstract}{%
  \par\small
  \acad@ifzh{\hangindent=4.2em\hangafter=1\noindent{\heiti 摘\quad 要：}}%
            {\noindent{\bfseries Abstract\quad}}%
}{%
  \par
  \ifdefempty{\acad@keywords}{}{%
    \par\vspace{2pt}%
    \acad@ifzh{\hangindent=4.2em\hangafter=1\noindent{\heiti 关键词：}\acad@keywords}%
              {\noindent{\bfseries Keywords\quad}\acad@keywords}\par}%
  \par\vspace{8pt}\normalsize
}

%%% ===========================================================================
%%% 7. 报告特有的环境
%%% ===========================================================================
% 原始数据 / 待批改处的留白框，方便打印后手写补充
\newcommand{\blankbox}[2][\linewidth]{%
  \par\vspace{4pt}%
  \fbox{\parbox[c][#2][c]{\dimexpr#1-2\fboxsep-2\fboxrule\relax}{}}%
  \par\vspace{4pt}%
}

% 「注意事项 / 安全提示」框，实验报告里常要求单列
\newenvironment{caution}{%
  \par\vspace{6pt}%
  \begin{list}{}{%
    \setlength{\leftmargin}{2em}\setlength{\rightmargin}{1em}%
    \setlength{\itemindent}{0pt}\setlength{\labelwidth}{0pt}%
    \setlength{\labelsep}{0pt}\setlength{\listparindent}{2em}}%
  \item[]\small{\heiti\acad@ifzh{注意}{Caution}\hspace{0.6em}}%
}{%
  \end{list}\par\vspace{6pt}%
}

%%% ===========================================================================
%%% 8. 附录
%%% ===========================================================================
\let\acad@origappendix\appendix
\renewcommand{\appendix}{%
  \acad@origappendix
  \acad@ifzh{\ctexset{section/name = {附录,}}}%
            {\ctexset{section/name = {Appendix~,}}}%
  \setcounter{figure}{0}\renewcommand{\thefigure}{\Alph{section}\arabic{figure}}%
  \setcounter{table}{0}\renewcommand{\thetable}{\Alph{section}\arabic{table}}%
  \setcounter{equation}{0}\renewcommand{\theequation}{\Alph{section}\arabic{equation}}%
}


% Apply after setup.tex: identity must not leak through cover or headers.
\AtBeginDocument{%
  \ifacad@anonymous
    \def\acad@studentname{Anonymous}\def\acad@studentid{}%
    \def\acad@school{}\def\acad@department{}\def\acad@logo{}%
    \def\acad@classname{}\def\acad@partners{}\def\acad@instructor{}%
    \def\acad@organization{}\def\acad@authors{Anonymous}%
    \def\acad@reviewer{}\def\acad@approver{}%
    \hypersetup{pdfauthor={}}%
  \else
    \acad@iftype{tech}{\hypersetup{pdfauthor={\acad@authors}}}%
                       {\hypersetup{pdfauthor={\acad@studentname}}}%
  \fi
  \hypersetup{pdftitle={\@title},pdfkeywords={\acad@keywords}}%
}
\endinput
