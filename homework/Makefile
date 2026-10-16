# Run make in the course directory or in an assignment directory.
ifeq ($(wildcard main.tex),)
HWS := $(sort $(wildcard hw*/))
HW_ALL       := $(addprefix all-,$(HWS))
HW_PREVIEW   := $(addprefix preview-,$(HWS))
HW_CHECK     := $(addprefix check-,$(HWS))
HW_CLEAN     := $(addprefix clean-,$(HWS))
HW_DISTCLEAN := $(addprefix distclean-,$(HWS))

.PHONY: all preview check clean distclean $(HW_ALL) $(HW_PREVIEW) $(HW_CHECK) $(HW_CLEAN) $(HW_DISTCLEAN)

all: $(HW_ALL)
$(HW_ALL): all-%:
	$(MAKE) -C $* all

preview: $(HW_PREVIEW)
$(HW_PREVIEW): preview-%:
	$(MAKE) -C $* preview

check: $(HW_CHECK)
$(HW_CHECK): check-%:
	$(MAKE) -C $* check

clean: $(HW_CLEAN)
$(HW_CLEAN): clean-%:
	$(MAKE) -C $* clean

distclean: $(HW_DISTCLEAN)
$(HW_DISTCLEAN): distclean-%:
	$(MAKE) -C $* distclean
else
# ----------------------------------------------------------------------------
# homework 单次作业构建
#   make          终稿编译，PDF 输出到 ./main.pdf
#   make preview  单轮预览（看内容；引用/文献可能过期）
#   make watch    监视源文件变化，自动重编译
#   make check    检查排版警告（过长的行、未定义的引用/文献）
#   make clean / distclean
# ----------------------------------------------------------------------------

MAIN    := main
BUILD   := build
LATEXMK := latexmk

export TEXINPUTS := ..:../../common:$(TEXINPUTS)
export BIBINPUTS := ..:../../common:$(BIBINPUTS)

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

check: all
	@test -s $(BUILD)/$(MAIN).log
	@if grep -nE '(^!|LaTeX Error|Package .* Error|Missing character:|Overfull|LaTeX Warning: (Reference|Citation).*undefined|There were undefined|Rerun to get|Please .*rerun)' $(BUILD)/$(MAIN).log; then exit 1; fi
	@echo "编译与引用检查通过（Underfull 等提示仍请查看日志）"

clean:
	$(LATEXMK) -c $(MAIN).tex

distclean:
	$(LATEXMK) -C $(MAIN).tex
	@rm -rf $(BUILD) $(MAIN).pdf $(MAIN).synctex.gz

endif
