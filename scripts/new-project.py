#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Copy a template and its shared files into a standalone project."""
from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def template_names() -> list[str]:
    return sorted(
        path.name
        for path in ROOT.iterdir()
        if path.is_dir() and (path / "template.conf").exists()
    )


def conf(template: Path, key: str) -> str:
    path = template / "template.conf"
    if not path.is_file():
        return ""
    pattern = re.compile(rf"^\s*{re.escape(key)}\s*=\s*(.*?)\s*$")
    for line in path.read_text(encoding="utf-8").splitlines():
        match = pattern.match(line)
        if match:
            return match.group(1).strip()
    return ""


def rewrite_search_paths(dest: Path) -> None:
    """Standalone projects keep shared files in the project root."""
    replacements = (
        ("$template/../common", "$template"),
        ("$course/../common", "$course"),
        ("../../common", "."),
        ("../common", "."),
    )
    targets = [dest / "latexmkrc", dest / "Makefile"]
    targets.extend(dest.glob("*/latexmkrc"))
    targets.extend(dest.glob("*/Makefile"))
    targets.extend(dest.glob("**/.vscode/settings.json"))
    for path in targets:
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for old, new in replacements:
            text = text.replace(old, new)
        path.write_text(text, encoding="utf-8")


def copy_common(kind: Path, dest: Path) -> None:
    names = conf(kind, "needs").split()
    sources = (
        [ROOT / "common" / name for name in names]
        if names
        else [path for path in (ROOT / "common").iterdir() if path.is_file()]
    )
    for src in sources:
        if not src.is_file():
            print(f"警告：template.conf 需要 {src.name}，但 common/ 下没有")
            continue
        target = dest / src.name
        if target.is_symlink() or target.exists():
            target.unlink()
        shutil.copy2(src, target)


def main() -> None:
    names = template_names()
    parser = argparse.ArgumentParser()
    parser.add_argument("template", nargs="?", choices=names)
    parser.add_argument("destination", nargs="?")
    parser.add_argument("--list", action="store_true")
    args = parser.parse_args()
    if args.list:
        for name in names:
            kind = ROOT / name
            title = conf(kind, "name") or name
            desc = conf(kind, "desc")
            extra = f"  — {desc}" if desc else ""
            print(f"{name:12} {title}{extra}")
        return
    if not args.template or not args.destination:
        parser.error("provide template and destination, or --list")

    dest = Path(args.destination).expanduser()
    if dest.exists():
        parser.error(f"{dest} already exists")
    kind = ROOT / args.template
    shutil.copytree(
        kind,
        dest,
        symlinks=True,
        ignore=shutil.ignore_patterns(
            "build",
            "main.pdf",
            "main.synctex.gz",
            "main-handout.pdf",
            "main-notes.pdf",
            "template.conf",
        ),
    )
    dest = dest.resolve()
    for src in kind.rglob("*"):
        if not src.is_symlink():
            continue
        resolved = src.resolve()
        if resolved.is_relative_to(kind.resolve()):
            continue
        target = dest / src.relative_to(kind)
        if target.is_symlink() or target.exists():
            target.unlink()
        shutil.copy2(src, target)
    copy_common(kind, dest)
    for extra in ("STANDARDS.md", ".gitignore"):
        src = ROOT / extra
        if src.is_file():
            shutil.copy2(src, dest / extra)
    rewrite_search_paths(dest)
    print(dest)


if __name__ == "__main__":
    main()
