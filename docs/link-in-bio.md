# Link in bio landing page

Page: `site/index.html` (plus `site/justin.jpg`). One file, no build step, loads fast on a phone.

**Job of the page:** turn people who are curious about Airbnbs into leads Justin talks to. It gives a little value first (4 lessons), then asks one question: "Where are you at with Airbnbs?"

## What's on it (top to bottom)
1. Photo, handle, hook: "Curious about Airbnbs?"
2. Short intro and one main button: **Talk Airbnbs with me**
3. Proof: 25 units closed in 8 months, partner's 500+ launches (clearly his), CA licensed agent
4. Value: 4 lessons from working next to 500+ launches (pricing left out on purpose)
5. Lead form: pick a stage (just curious, own a home, want to buy, already host), first name, email, optional phone and note
6. Short about, Instagram and LinkedIn buttons, the main button again
7. Footer: name, DRE #, brokerage, Equal Housing Opportunity

The stage question sorts leads for you. "Want to buy one" is a real estate lead. "Own a home" and "already host" are hosting conversations.

## Your checklist (about 20 minutes, one time)
Open `site/index.html`, find the `CONFIG` block near the bottom, fill in 4 values:

- [ ] **dre**: your DRE license number. Required by California law on first point of contact marketing (B&P 10140.6, Reg 2773). Do not go live without it.
- [ ] **brokerage**: your responsible broker's name exactly as licensed. Also required. Ask your broker if they need to approve the page.
- [ ] **formEndpoint**: free form at formspree.io. Sign up with your Gmail, create a form, paste its URL (looks like `https://formspree.io/f/abcdwxyz`). Every lead lands in your inbox. Free plan covers 50 leads a month.
- [ ] **linkedin**: your LinkedIn profile URL. The button stays hidden until this is filled.

Then put it online (free):
- [ ] Go to dash.cloudflare.com, then Workers and Pages, then Create, then Pages, then Connect to Git.
- [ ] Pick this repo, branch `main`, framework "None", build command empty, output directory `site`.
- [ ] You get a link like `justincurtis.pages.dev`. Optional: buy a domain (about $10 a year) and connect it in the same screen.
- [ ] Paste the link in your Instagram bio with tracking: `https://YOURLINK/?src=ig_bio`
- [ ] Add your DRE # to the Instagram bio too.
- [ ] Submit the form once yourself to test it.

Use a different `?src=` per place you share it (`ig_bio`, `reel`, `email`, `linkedin`). Each lead email shows where they came from.

## Upgrades later (in this order)
1. **Booking link.** A free Calendly or Google Calendar booking page for a 15 minute call. Add it as a second button.
2. **A local lead magnet.** Something like "North County Airbnb rules, city by city" or "First Airbnb in North County checklist". Generic revenue calculators lose to AirDNA, but local guides win. Kit (free up to 10,000 subscribers) can deliver it by email automatically.
3. **Start here posts.** Link your 2 or 3 best Reels once they exist.
4. **Your own domain** instead of `pages.dev`.

## Research summary (Oct 2026)
What the top business creators do on their link pages:

| Creator | Main ask |
|---|---|
| Justin Welsh, Sahil Bloom, Dan Koe, Codie Sanchez | Free newsletter or guide (email first) |
| Pace Morby | Free eBook |
| The Short Term Shop (Avery Carl) | Free STR training plus book a call |
| Ryan Serhant | Personal page for authority, a separate page for selling |
| Rob Abasolo (Robuilt) | "Learn how I launch Airbnbs," free STR education |

Patterns that show up again and again:
* One main ask, with everything else smaller. Keep it to about 3 to 7 tappable things.
* A free thing first, then the call or the offer.
* Proof near the top.
* Social icons kept small.
* Every form field you add costs conversions, so ask for email and first name and leave everything else optional.
* Instagram hides where visitors came from, so add `?src=` or UTM tags to every link you share.
* Speed matters: bounce rates climb fast after 1 to 3 seconds on mobile. This page is one small file and one photo.

Evidence strength: link-count and click-rate numbers come from vendors such as Linktree and Hootsuite, not independent studies. Treat them as direction, not law. The compliance points come from the CA Business and Professions Code and DRE regulations. Confirm details with your broker; this is not legal advice.

Why a custom page instead of Linktree or Stan: you don't sell digital products yet, you own the page, there are no platform fees, and it loads faster and looks fully on brand. Hosting: Cloudflare Pages allows business use for free. Vercel's free plan doesn't. GitHub Pages works too, but it isn't meant for business sites.
