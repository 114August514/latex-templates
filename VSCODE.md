# VS Code / LaTeX Workshop

打开项目目录，让 `.vscode/settings.json` 生效。写作和交稿用两套编译：

1. **第一次**先跑一次终稿，建立 `build/` 里的辅助文件（aux、bbl）。
2. **改正文时**保存或 Ctrl+Alt+B：默认「预览（单轮，看内容）」。只跑一轮
   XeLaTeX，用来看段落、公式、图表对不对。旧的引用编号沿用上次终稿的
   辅助文件；新加的标签或文献可能仍是 `??`。
3. **交稿前**用命令面板选「终稿（latexmk 完整编译）」，或在项目目录执行
   `make` / `make check`。这一步会按需重跑 biber 和多轮引用，检查过长行与
   未定义引用。

命令行对应关系：`make preview` = 单轮预览；`make` = 终稿；`make check` = 终稿
再加日志检查。不要每次 `make clean`。不要同时开 `make watch` 和插件自动编译。

然后用 Ctrl+Alt+V 打开插件 PDF 预览。PDF 和 `.synctex.gz` 都在主文件旁的 `build/`。

- 源码到 PDF：Ctrl+Alt+J（光标位于 `.tex` 中）。
- PDF 到源码：双击 PDF 正文；本项目已设为 double-click，插件默认是 Ctrl+单击。
- 编译成功后：自动把 PDF 定位到当前光标附近。
- 子文件以 `% !TeX root = ../main.tex` 指明主文件。共用配置不绑定某一次作业。

单轮预览省的是「改标签 / 文献时 latexmk 连跑多轮 + biber」，不是把一轮从数秒
压到 1 秒。一轮 XeLaTeX 几乎都花在宏包和 OpenType 字体上，和正文长短关系很小。
默认作业 / 论文模板在本机大约 3–4 秒一轮；`preamble.tex` 再加 listings、TikZ
一类宏包会回到 6 秒以上。预览故意不关字体、数学和 biblatex，这样改句子时仍能
看到中文、公式和上次编好的引用，而不是空白框。

做不到把这一轮压到约 1 秒：XeTeX 不能把已加载的 OpenType 字体写入自定义
format（`fontspec` / `ctex` / `unicode-math` 都会报
`Can't dump a format with native fonts`）。biblatex 单独可以预编译，但不能
和这套中文与数学字体一起 dump。换 LuaLaTeX 需要 `luatexja`，而且行距断行
可能和现在不一致。

不能跳转时先确认预览的是当前主文件的 PDF，且同目录有同名 `.synctex.gz`。
本项目的 `make` 同时复制 PDF 与 SyncTeX；推荐编辑时始终使用 `build/` 版本。
SyncTeX 提供段落/行附近的位置映射，不能保证每个数学符号逐字对应。

官方说明：
- https://github.com/James-Yu/LaTeX-Workshop/wiki/Compile
- https://github.com/James-Yu/LaTeX-Workshop/wiki/View
