# Justin Thyme / STR Insider: Social Media System

Personal brand social media system for Justin Curtis (@justinthymecurtis). This is NOT NOVIQ. Never use NOVIQ branding, colors or claims here.

## Who it's for
Justin: 11+ years in short term rentals, 500+ Airbnb launches, North County San Diego, licensed CA agent. The brand blends STR and real estate authority with mindset, discipline and training, travel, and caring for others. Goal: 30,000 followers.

Justin has ADHD. One short command should produce a finished, ready to review output. Fewer decisions, clear checklists.

## Brand rules
* Palette and fonts live in `brand/palette.json` (dark and oak: ink, charcoal, cognac, oak, light oak, bone, plus olive and brass). Fonts: Inter Display 800 for headlines, Inter for body.
* Monogram: `brand/jt-monogram.svg`.
* Voice: human, punchy, short sentences, conversational, peer to peer.
* NEVER use hyphens or em dashes in copy. Use commas or full sentences. Run `python3 scripts/lint_copy.py <post folder>` before marking a post ready.
* Captions: Hook on line one (question, contrarian take, or number), then Story, Insight, CTA.
* In captions, never ask people to "reply yes" or "comment X". Ask a plain question.
* Reels: on screen hook in the first 2 seconds, native captions.
* Pillars (one per post), from Justin's Growth Lab: Faith, Impact, Joy, Business (Business includes STR and real estate authority).
* Reel text: bubbly but clean. Small DM Sans setup line over one huge Fraunces Soft word (`style: pop` in reel.json). See `brand/style-guide.md`.
* Rotation buckets: Educate, Prove, Personal, Offer. Target 4 to 6 posts a week, 3+ Reels.
* Nothing posts automatically. Status flow: idea, drafted, in review, approved, scheduled, posted.
* Never use "Road to 30K" as a brand, series, hashtag or kicker. The repo name is just a folder name.

## Strategy
Read `brand/style-guide.md` before planning or writing. It holds the Bloom founder story model, the data behind the format mix, and the video workflow. Never invent personal stories for Justin; ask him for the real one.

## Folders
* `brand/` palette, monogram, voice files
* `content/posts/<date-slug>/` one folder per post: `post.md` (frontmatter, caption, LinkedIn version, notes) and `slides.json` for carousels
* `scripts/render_carousel.py` renders `slides.json` to 1080x1350 PNGs in `exports/<slug>/`
* `scripts/make_reel.py` cuts a branded Reel from raw footage using `reel.json` (segments, speed, text overlays) into `exports/<slug>/reel.mp4`
* `raw/` raw footage, never committed
* `scripts/lint_copy.py` checks copy against brand rules
* `exports/` finished images ready to upload

## Making a new carousel
1. Copy an existing post folder, rename it `YYYY-MM-DD-slug`.
2. Edit `post.md` and `slides.json` (slide types: cover, lesson, cta).
3. `python3 scripts/lint_copy.py content/posts/<slug>`
4. `python3 scripts/render_carousel.py content/posts/<slug>`
