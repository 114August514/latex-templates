# ----------------------------------------------------------------------------
# 顶层构建
#   make            五套模板都编
#   make article    论文      → article/main.pdf
#   make report     实验/技术报告 → report/main.pdf
#   make beamer     会议幻灯片 → beamer/main.pdf
#   make defense    答辩幻灯片 → defense/main.pdf
#   make handout    幻灯片讲义版  → beamer/main-handout.pdf
#   make notes      幻灯片双屏备注版 → beamer/main-notes.pdf
#   make preview    五套都只跑单轮预览（看内容；交稿前仍要 make / make check）
#   make check      五套都跑排版检查
#   make setup      用 uv 创建项目内 .venv
#   make list-templates  列出可拷贝的模板
#   make clean      清中间文件
#   make distclean  清中间文件与 PDF
# ----------------------------------------------------------------------------

TEMPLATES := article report beamer defense homework
PYTHON    := uv run python

CHECK_TARGETS     := $(addsuffix -check,$(TEMPLATES))
PREVIEW_TARGETS   := $(addsuffix -preview,$(TEMPLATES))
CLEAN_TARGETS     := $(addsuffix -clean,$(TEMPLATES))
DISTCLEAN_TARGETS := $(addsuffix -distclean,$(TEMPLATES))

.PHONY: all article report beamer defense homework handout notes preview check setup list-templates clean distclean \
        $(CHECK_TARGETS) $(PREVIEW_TARGETS) $(CLEAN_TARGETS) $(DISTCLEAN_TARGETS)

setup:
	uv sync

list-templates:
	$(PYTHON) scripts/new-project.py --list

all: $(TEMPLATES)

article report beamer defense homework:
	$(MAKE) -C $@

handout:
	$(MAKE) -C beamer handout

notes:
	$(MAKE) -C beamer notes

preview: $(PREVIEW_TARGETS)
$(PREVIEW_TARGETS): %-preview:
	$(MAKE) -C $* preview

check: $(CHECK_TARGETS)
$(CHECK_TARGETS): %-check:
	$(MAKE) -C $* check

clean: $(CLEAN_TARGETS)
$(CLEAN_TARGETS): %-clean:
	$(MAKE) -C $* clean

distclean: $(DISTCLEAN_TARGETS)
$(DISTCLEAN_TARGETS): %-distclean:
	$(MAKE) -C $* distclean
