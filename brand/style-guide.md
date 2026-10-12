# Style Guide and Data Playbook

## The model: Bloom (Greg LaVecchia and Mari Llewellyn)
Bloom grew from a founder's personal transformation post into a nine figure brand. What we copy:
* **Founder story first.** The origin and transformation story is the anchor of trust. For Justin: what he is learning in STR and real estate (including from his business partner, who has 500+ launches), plus mindset and discipline. Ask Justin for his own real numbers and stories.
* **Routine and day in the life.** Real routines over polished ads. For Justin: launch days, property walkthroughs, training, Sunday planning.
* **Plain, relatable language.** No hype, no clinical claims. Explain things like a friend would.
* **Community in the loop.** Ask followers what to cover next and show their input on screen.
* **Creators and collabs.** Bloom's creator videos averaged roughly 8x the views of its own brand videos. For Justin: collab posts with hosts, investors, trainers, and local San Diego creators.
* What we do NOT copy: Bloom's pastel palette. Justin's look stays neutral, masculine and warm.

## Data that drives the plan
* Carousels are the top engagement format on Instagram (about 0.50% vs 0.48% for Reels and 0.33% for images, Socialinsider Q2 2026).
* For accounts with 1K to 5K followers, carousels average 993 views vs 580 for Reels and 417 for images (Socialinsider).
* Reels drive the most comments at every account size (Socialinsider). Use Reels for conversation and reach.
* Carousels earn about 9x more saves than single images, and Reel watch time more than doubled in a year (Metricool, 24M posts studied).
* Single images are falling every year. Avoid them except for big announcements.
* 70% of consumers feel more connected to a brand whose CEO is active on social (Sprout Social, via Influencity). Justin's face goes on covers.

## Weekly mix (4 to 6 posts)
* 2 to 3 carousels: lessons, breakdowns, story posts. Goal: saves and shares.
* 2 to 3 Reels: day in the life, quick tips, behind the scenes. Goal: comments and reach.
* Daily Stories: polls and questions, so followers shape the content.
* Review every Friday in Metricool. Keep the format that earned the most saves and shares, cut what didn't.

## Visual rules
* Covers: Justin's photo full bleed, dark fade at the bottom, story headline in Inter Display 800.
* Lesson slides: sand background, big rust number, one idea per slide, an optional italic personal note.
* Close every carousel with Justin's face and one clear ask (follow, save, or share).
* Reels: hook text on screen in the first 2 seconds, burned in captions, brand colors on text.

## Video workflow
* **Edit and trends:** Instagram Edits (free, from Instagram). Use its Inspiration tab for trending audio and its Insights tab for Reel stats.
* **Trend proof:** CapCut templates show usage counts, which is a quick signal of what's trending. TikTok Creative Center is free and shows rising hashtags and songs with popularity over time.
* **Claude's part:** Justin uploads raw clips. Claude cuts, crops to 9:16, adds burned in captions and branded hook text with ffmpeg, then saves to `exports/`.
* **Scheduling:** Metricool, posts for review only.

## Reel text style (Justin's reference: "POV, you found the Airbnb spot")
What Justin likes: bubbly, vibrant, but clean.
* A small sans setup line (lowercase, medium weight, white) sitting on top of one huge, chunky serif word or phrase, stacked tight and centered.
* White text, no box, a soft shadow only, over moody or darker footage.
* One idea per screen. The big word is the punchline.
* Research backing: large serif works for short static hook overlays, but stick to bold sans for running captions (Blitzcut 2026 caption font guide). Running captions should be about 7 to 10% of frame height. About 85% of Instagram video is watched with the sound off, so the text carries the message.

Options rendered in `brand/caption-style-options.jpg` (all free Google Fonts, files in `brand/fonts/`):
* A: Gloock with DM Sans (closest match to the reference)
* B: Fraunces Soft Black with DM Sans (the most bubbly). Current default, used in `make_reel.py` as `style: pop`.
* C: Bricolage Grotesque with Instrument Serif italic in a warm peach
* D: Playfair Display Black with DM Sans and a rust period
