# Justin Thyme / STR Insider: Social Media System

Personal brand social media system for Justin Curtis (@justinthymecurtis). This is NOT NOVIQ. Never use NOVIQ branding, colors or claims here.

## Who it's for
Justin: works in short term rentals and real estate, North County San Diego, licensed CA agent. The 500+ Airbnb launches belong to his business partner; never claim them as Justin's own. The brand blends STR and real estate authority with mindset, discipline and training, travel, and caring for others. Goal: 30,000 followers.

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
* Reel text: bubbly but clean. Small setup line over one huge word (`style: pop` in reel.json). Font is picked by letter with `"font": "G"` in reel.json; all lettered styles live in `scripts/caption_styles.py`. See `brand/style-guide.md`.
* No end card with handle or pillars on Reels unless Justin asks for one (removed Oct 2026).
* ALWAYS render 5 font style versions of every Reel (`"font_options": [5 letters]` in reel.json). make_reel.py then outputs `reel-<letter>.mp4` for each plus `compare-fonts.mp4`, a labeled side by side preview. Commit and push EVERY version (with beat, silent, cover) even after Justin picks one, and list them all in the project tracker (claude/content-tracker.md). Never delete unchosen versions. Mix in Justin's favorites U (Instrument Serif) and V (Montserrat + Caveat in light oak) with three others that suit the footage.
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
* `make_reel.py` grades: set `"grade": "lift_dark"` in reel.json for dark indoor footage (lifts shadows, light denoise), `"lift_light"` for slightly dim footage, or pass a raw ffmpeg filter string
* `scripts/caption_fonts.py <frame.jpg> "<setup>" "<big word>" [out.jpg] [letters]` renders a lettered sheet of caption styles (A to T) over a real frame so Justin can pick one
* Music: add `"music": {"file": "../../../raw/music/track.mp3", "start": 0, "volume": 1.0}` and optionally `"original_audio": 0.3` (keeps the clip's own sound under the music) to reel.json. Output is loudness normalized, and `reel-silent.mp4` is saved too. Only use tracks Justin has rights to (royalty free or licensed); for trending songs, post `reel-silent.mp4` and add the audio inside Instagram so the Reel links to the audio page.
* `scripts/make_beat.py raw/music/<name>.wav --bpm 86 --seconds 20 --mood dark|bright|boombap` generates an original, royalty free beat Justin fully owns. Use it when no licensed track is supplied. Never make AI soundalikes of real songs; they still copy the song. Original beats in a genre style (90s boom bap etc.) are fine.
* `raw/` raw footage, never committed
* `scripts/lint_copy.py` checks copy against brand rules
* `exports/` finished images ready to upload

## Delivery
Every finished, edited video also goes to the **Instagram Ready Posts** folder in Justin's personal Google Drive (jtcurtis.2009@gmail.com), never the NOVIQ Drive (justin@noviq.com). Check which account the Drive connector is signed into before uploading (name the file `<slug>.mp4`, upload the cover too). Folder id: `1W-_wlCwo3F9jHNj-DTFYII7q8Uj8ljUq`. The Drive connector can't carry full size video files, so videos go through Justin's linked computer (his Google Drive for desktop folder) when it's linked; otherwise send the video in chat for Justin to save, and upload the cover and caption to the folder directly.

## Making a new carousel
1. Copy an existing post folder, rename it `YYYY-MM-DD-slug`.
2. Edit `post.md` and `slides.json` (slide types: cover, lesson, cta).
3. `python3 scripts/lint_copy.py content/posts/<slug>`
4. `python3 scripts/render_carousel.py content/posts/<slug>`
