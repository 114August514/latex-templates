# ----------------------------------------------------------------------------
# article 模板构建
#   make          终稿编译，PDF 输出到 ./main.pdf
#   make preview  单轮预览（看内容；引用/文献可能过期）
#   make watch    监视源文件变化，自动重编译并刷新预览
#   make check    检查排版警告（过长的行、未定义的引用/文献）
#   make clean    删中间文件
#   make distclean 删中间文件与 PDF
# ----------------------------------------------------------------------------

MAIN    := main
BUILD   := build
LATEXMK := latexmk

# 让 xelatex 直接调用时也能找到 ../common/acadmath.sty
export TEXINPUTS := ../common:$(TEXINPUTS)
export BIBINPUTS := ../common:$(BIBINPUTS)

.PHONY: all preview watch check clean distclean

all:
	$(LATEXMK) $(MAIN).tex
	@cp -f $(BUILD)/$(MAIN).pdf ./$(MAIN).pdf
	@cp -f $(BUILD)/$(MAIN).synctex.gz ./$(MAIN).synctex.gz
	@echo "==> $(CURDIR)/$(MAIN).pdf"

preview:
	@mkdir -p $(BUILD)
	xelatex -synctex=1 -halt-on-error -file-line-error -interaction=nonstopmode \
	  -output-directory=$(BUILD) $(MAIN).tex
	@cp -f $(BUILD)/$(MAIN).pdf ./$(MAIN).pdf
	@cp -f $(BUILD)/$(MAIN).synctex.gz ./$(MAIN).synctex.gz
	@echo "==> preview $(CURDIR)/$(MAIN).pdf  （引用/文献可能过期；交稿前 make）"

watch:
	$(LATEXMK) -pvc $(MAIN).tex

# 投稿前跑一遍。Overfull hbox 说明有行超出版心，必须改。
check: all
	@test -s $(BUILD)/$(MAIN).log
	@if grep -nE '(^!|LaTeX Error|Package .* Error|Missing character:|Overfull|LaTeX Warning: (Reference|Citation).*undefined|There were undefined|Rerun to get|Please .*rerun)' $(BUILD)/$(MAIN).log; then exit 1; fi
	@echo "编译与引用检查通过（Underfull 等提示仍请查看日志）"

clean:
	$(LATEXMK) -c $(MAIN).tex

distclean:
	$(LATEXMK) -C $(MAIN).tex
	@rm -rf $(BUILD) $(MAIN).pdf $(MAIN).synctex.gz
