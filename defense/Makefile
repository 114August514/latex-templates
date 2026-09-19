# ----------------------------------------------------------------------------
# defense 模板构建
#   make           终稿普通版  → main.pdf
#   make preview   单轮预览（看内容；引用/文献可能过期）
#   make handout   讲义版      → main-handout.pdf（忽略所有 \pause，一帧一页）
#   make notes     双屏备注版  → main-notes.pdf（左幻灯片、右备注，配 pdfpc 用）
#   make watch     监视重编译
#   make check     检查排版警告
#   make clean / distclean
# ----------------------------------------------------------------------------

MAIN    := main
BUILD   := build
LATEXMK := latexmk

export TEXINPUTS := ../common:$(TEXINPUTS)
export BIBINPUTS := ../common:$(BIBINPUTS)

.PHONY: all preview handout notes watch check clean distclean

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

# handout 由 \PassOptionsToClass 注入，不用改 main.tex
handout:
	$(LATEXMK) -jobname=$(MAIN)-handout \
	  -usepretex='\PassOptionsToClass{handout}{ctexbeamer}' $(MAIN).tex
	@cp -f $(BUILD)/$(MAIN)-handout.pdf ./$(MAIN)-handout.pdf
	@echo "==> $(CURDIR)/$(MAIN)-handout.pdf"

# \AcadShowNotes 由 preamble.tex 检测，切到双屏备注模式
notes:
	$(LATEXMK) -jobname=$(MAIN)-notes \
	  -usepretex='\def\AcadShowNotes{}' $(MAIN).tex
	@cp -f $(BUILD)/$(MAIN)-notes.pdf ./$(MAIN)-notes.pdf
	@echo "==> $(CURDIR)/$(MAIN)-notes.pdf  （用 pdfpc 播放）"

watch:
	$(LATEXMK) -pvc $(MAIN).tex

check: all
	@test -s $(BUILD)/$(MAIN).log
	@if grep -nE '(^!|LaTeX Error|Package .* Error|Missing character:|Overfull|LaTeX Warning: (Reference|Citation).*undefined|There were undefined|Rerun to get|Please .*rerun)' $(BUILD)/$(MAIN).log; then exit 1; fi
	@echo "编译与引用检查通过（Underfull 等提示仍请查看日志）"

clean:
	$(LATEXMK) -c $(MAIN).tex

distclean:
	$(LATEXMK) -C $(MAIN).tex
	@rm -rf $(BUILD) $(MAIN).pdf $(MAIN).synctex.gz $(MAIN)-handout.pdf $(MAIN)-notes.pdf
