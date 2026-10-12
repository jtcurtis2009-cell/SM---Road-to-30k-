"""Check post copy against brand rules.

Usage:
    python3 scripts/lint_copy.py content/posts/<slug>

Fails if captions or slide text contain hyphens or em/en dashes
(hashtags, handles and URLs are ignored), or if a pillar is missing.
"""
import json
import re
import sys
from pathlib import Path

DASH = re.compile(r"[—–]|(?<=\w)-(?=\w)|\s-\s")


def clean(line: str) -> str:
    line = re.sub(r"https?://\S+", "", line)
    line = re.sub(r"[#@]\S+", "", line)
    line = re.sub(r"\S*/\S*", "", line)  # file paths
    return line


def main(post_dir: str) -> int:
    post = Path(post_dir)
    problems = []
    md = (post / "post.md").read_text()
    parts = md.split("\n---\n", 1)
    body = parts[1] if md.startswith("---") and len(parts) > 1 else md
    if "pillar:" not in md:
        problems.append("post.md: missing pillar in frontmatter")
    for n, line in enumerate(body.splitlines(), 1):
        if re.match(r"#{1,6} ", line):
            continue
        if DASH.search(clean(line)):
            problems.append(f"post.md line {n}: dash found: {line.strip()}")
    slides = post / "slides.json"
    if slides.exists():
        for i, s in enumerate(json.loads(slides.read_text())["slides"], 1):
            for k, v in s.items():
                if isinstance(v, str) and DASH.search(clean(v)):
                    problems.append(f"slide {i} {k}: dash found: {v}")
    for p in problems:
        print("FAIL", p)
    if not problems:
        print("PASS: copy follows brand rules")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
