# Justin Thyme Social System

Content system for Justin Thyme / STR Insider (@justinthymecurtis).

## Setup
```
pip install playwright
python3 -m playwright install chromium
```
Fonts: install Inter and Inter Display (free from rsms.me/inter) so slides render in brand type.

## Make a post
1. Copy a folder in `content/posts/` and rename it `YYYY-MM-DD-slug`.
2. Write the caption in `post.md` and slide text in `slides.json`.
3. Check copy: `python3 scripts/lint_copy.py content/posts/<slug>`
4. Render slides: `python3 scripts/render_carousel.py content/posts/<slug>`
5. Set status to `in review` in `post.md`. Justin approves, then it gets scheduled in Metricool.

Brand rules are in `CLAUDE.md`. Read them before writing anything.
