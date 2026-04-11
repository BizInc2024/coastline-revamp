# Landing Page V10 Brief

Build a new Shopify Liquid landing page section: cc-landing-v10.liquid

## CRITICAL CONTEXT — Read these first:
1. `/Users/bizmac22/coastline-revamp/reference-v8.html` — the v8 landing page (2088 lines). Use as structural reference.
2. `/Users/bizmac22/coastline-marketing/CLAUDE.md` — brand rules, visual identity, tone
3. `/Users/bizmac22/coastline-marketing/.claude/references/coastline-product-formulation.md` — 13 ingredients, mechanisms, doses
4. `/Users/bizmac22/coastline-marketing/.claude/references/social-proof-authority.md` — testimonials, expert quotes, press
5. `/Users/bizmac22/coastline-marketing/.claude/references/offer-mechanics-pricing.md` — pricing, subscription mechanics
6. `/Users/bizmac22/.claude/projects/-Users-bizmac22/memory/feedback_theme-architecture.md` — CRITICAL Shopify theme rules

## WHAT TO BUILD
A high-converting product journey landing page (NOT a 5-benefits listicle like v8). Structure:

### Section flow:
1. **Hero** — bold headline, lifestyle image, immediate CTA with social proof stars + "2,000+ reviews". Product-focused.
2. **Press logos bar** — same as v8
3. **Product system overview** — AM/PM two-moment system, what's in each step. Quick visual.
4. **Social proof #1** — 3 customer reviews with stars (mix male + female names)
5. **Influencer UGC gallery** — horizontal scroll of 5 images from `/Users/bizmac22/coastline-marketing/assets/influencers:UGC/CL-InfluencerStillsw:quotes/CL-NewInfluencerAds-Jan8-[1-5].png`
6. **Ingredient deep dive** — NOT a listicle. Show all 13 ingredients in a clean grid/table with doses. "Every dose published." Link to science.
7. **Social proof #2** — 2 more reviews scattered between content
8. **"How it works"** — 3-step: Morning scoop + softgel → Evening capsules → Feel the difference in 2-4 weeks
9. **Expert endorsement** — Greg Potter PhD quote (Lead Scientist, NOT founder)
10. **Comparison section** — Coastline vs typical supplements (transparent vs mystery blends)
11. **Social proof #3** — 2 more reviews
12. **Pricing/CTA section** — COPY EXACTLY from v8 lines 1573-1769 (variant IDs, selling plans, cart JS). DO NOT change any IDs or cart logic.
13. **FAQ** — 6-8 questions
14. **Trust footer** — badges, guarantee, free shipping

### CRO requirements:
- NO sticky buy bar on mobile
- Social proof scattered THROUGHOUT (not just in dedicated sections) — micro-testimonials, review counts, star ratings between sections
- "2,000+ Five-Star Reviews" mentioned at least 3 times
- Trust badges (Satisfaction Guaranteed · GMP Certified · Made in USA) appear at LEAST twice
- 60-day guarantee mentioned prominently near every CTA
- "$3.30/day — less than your daily coffee" near every price mention
- Urgency: "Limited Time — Save 34%" badge near pricing
- Free glass shaker callout
- Multiple CTAs throughout (not just at the bottom)

### Audience + imagery:
- Gender-neutral — NOT dad-specific. "Health-focused adults 35+"
- Mix male + female names in all reviews
- Traffic is primarily DESKTOP — design desktop-first, but ensure mobile is responsive
- Active lifestyle images from approved selects: `/Users/bizmac22/coastline-marketing/generated-images/2026-04-01/APPROVED-SELECTS/`
- Product images: `/Users/bizmac22/coastline-marketing/assets/products/`
- Influencer images: `/Users/bizmac22/coastline-marketing/assets/influencers:UGC/CL-InfluencerStillsw:quotes/`

### Theme architecture rules (CRITICAL):
- Use cc-deps.liquid snippet for fonts/Tailwind/Alpine
- Tailwind compiled with :where() scoping — use inline styles or scoped <style> for critical styling
- Cart add MUST use native fetch to /cart/add.js with the EXACT variant IDs and selling_plan IDs from v8
- cart_type MUST be "drawer" in settings
- WebView fallback: every .reveal element needs BOTH x-intersect AND x-init="setTimeout(() => $el.classList.add('visible'), 100)"
- NO custom layout files — use theme.liquid
- Greg Potter is "PhD, Lead Scientist" — NOT founder, NOT co-founder, NOT Chief Science Officer

### Banned words:
- "game-changer", "revolutionary", "results"
- "proprietary blends" → use "mystery ingredients" or "hidden doses"
- "Forever Jars" → use "easy-scoop powder sachet, softgels, evening capsules, free glass shaker"
- Any "dad" specific language

### Variant IDs (from v8 — DO NOT CHANGE):
- Unflavored: 42179764453445
- Lemonade: 42179764486213
- Monthly selling plan: 1892712517
- Two-month selling plan: 1862631493
- One-time: null (no selling plan)
- Prices: Monthly $99, Two-month $120, One-time $150

### Product timing rule:
- Morning blend + softgels TOGETHER (first moment)
- Evening capsules = SECOND moment
- TWO touchpoints per day

### Body systems (there are 11, not 8):
Brain, Energy/Mitochondria, Sleep, Muscle, Gut, Vision, Joints, Heart/Cardiovascular, Antioxidant Defense, Skin, Immune

### Output:
- Create `sections/cc-landing-v10.liquid`
- Create `templates/page.cc-landing-v10.json` pointing to it
- The section should be self-contained (all CSS inline or in <style>)
- Test by pushing to GitHub for Shopify sync

### Quality bar:
- This page needs to CONVERT. Apply every CRO best practice.
- Desktop-first. Traffic is primarily desktop.
- Fast loading — no unnecessary JS.
- Every section should either build desire, reduce objection, or provide social proof.
- No section should exist just to look nice — it must earn its place.
- **EVALUATION STANDARD:** Before delivering, evaluate this page as if 3 independent landing page conversion experts (CRO specialists) were scoring it 1-10. The page MUST score above 9.0 from all three. If any section would bring the score below 9.0, rework it before delivering. Think: would Peep Laja, Oli Gardner, and Joanna Wiebe approve this page? Every headline, every CTA, every trust element, every objection handler must be best-in-class.
