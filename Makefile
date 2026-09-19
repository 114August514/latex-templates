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

.PHONY: all article report beamer defense homework handout notes preview check setup list-templates clean distclean

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

preview:
	@set -e; for d in $(TEMPLATES); do \
	  echo "===== $$d preview ====="; \
	  $(MAKE) -C $$d preview; \
	done

check:
	@set -e; for d in $(TEMPLATES); do \
	  echo "===== $$d ====="; \
	  $(MAKE) -C $$d check; \
	done

clean:
	@set -e; for d in $(TEMPLATES); do $(MAKE) -C $$d clean; done

distclean:
	@set -e; for d in $(TEMPLATES); do $(MAKE) -C $$d distclean; done
