# APR26 Rebuild — Tracker

**Goal:** Break monolithic LP sections into composable `-apr26` sections; convert conversion LPs to product templates; layer in frontend audit fixes as each section is rebuilt.

**Hard rule:** Zero disruption to live. Build in parallel, preview via alt-templates, flip via Shopify draft theme only after full QA.

---

## Audit items — status

### ✅ Accepted (do during rebuild)
| Area | Item | Apply during |
|---|---|---|
| Global | Button hover effects | CSS polish pass |
| Global | Mobile font-size reduction (headings + body) | Per-section rebuild |
| Global | Move inline CSS off-section (into snippet `<style>` or scoped files) | Per-section rebuild |
| Cart drawer | Fix cursor visibility when open | Standalone CSS fix |
| Footer | Reduce vertical height + font sizes | Footer rebuild |
| Footer | Responsive redesign (tablet + mobile break) | Footer rebuild |
| Homepage | Testimonial section → carousel/slider | `cc-testimonials-apr26` |
| Homepage | Reduce section spacing (gaps between sections) | Per-section rebuild |
| Homepage | 5-column benefits grid → responsive/horizontal slider on mobile | `cc-benefits-apr26` |
| Product page | "View Details" → drawer/popup (no content push) | `cc-product-apr26` |
| Product page | Ingredients list → 2-3 column layout | `cc-product-apr26` |
| Product page | Testimonial section → carousel (desktop + mobile) | `cc-testimonials-apr26` (shared) |
| CMS pages | FAQ font size reduction | `cc-faq-apr26` |
| Backend #1 | Homepage → modular sections | Core of rebuild |
| Backend #3 | Unique JSON templates per page | Core of rebuild |
| Backend #4 | Product pages on single master template w/ dynamic data | Core of rebuild |

### ⏸ Deferred — revisit once structure is in place
| Item | Why deferred |
|---|---|
| Homepage length reduction (remove sections) | Need to pick which sections stay/go — discuss per-section during rebuild. Long LPs often test better in CRO; cut based on data, not aesthetics. |
| Footer detail review | User wants to review in detail as we go |
| Buttons detail review | User wants to review in detail as we go |

### ❌ Rejected
| Item | Reason |
|---|---|
| Widen article layout | Narrow columns (45-75 chars) support readability. Keeping as-is. |
| Widen CMS page layouts | Same reasoning. |
| Dynamic blog author (Backend #2) | All Coastline blog authors are the same person; no benefit. |
| Hire contractor for 77h | We're doing this in-house. |

---

## Sections to extract from monoliths

**Source:** `cc-homepage.liquid` (~2500 lines) + `cc-lp-v8.liquid` + `cc-landing-v10.liquid`

### Homepage blocks (inventory — all 17 extracted as first-draft sections)
1. [x] Hero → `cc-hero-apr26` *(vanilla CSS, full schema)*
2. [x] Press logos marquee → `cc-press-apr26`
3. [x] Ask Coastline (AI Q&A) → `cc-ask-apr26`
4. [x] Genetics Stat (animated 7% / 93%) → `cc-genetics-stat-apr26`
5. [x] System (AM + PM 3-step, 3 step blocks wired) → `cc-system-apr26`
6. [x] UGC — Coastline Community → `cc-ugc-apr26`
7. [x] Benefits (5 pillar blocks wired) → `cc-benefits-apr26` *(mobile carousel — TODO)*
8. [x] Expert Narrative (Greg Potter) → `cc-expert-apr26`
9. [x] Reviews (24 testimonial blocks wired) → `cc-testimonials-apr26` *(carousel rebuild — TODO)*
10. [x] Video → `cc-video-apr26`
11. [x] Pricing CTA → `cc-pricing-apr26` *(section wrapper around shared snippet)*
12. [x] Comparison Table → `cc-comparison-apr26`
13. [x] Do the Math → `cc-math-apr26`
14. [x] Our Story → `cc-story-apr26`
15. [x] FAQ (8 faq blocks wired) → `cc-faq-apr26`
16. [x] Email Capture → `cc-email-capture-apr26`
17. [x] Final CTA → `cc-final-cta-apr26`

**Preview:** `/?view=apr26` — composes all 17 above in the live on-page order.

**Known gaps in first-draft extraction (fix per-section in follow-ups):**
- Schema settings are empty on most sections — copy/images fall through to hardcoded defaults from the monolith. Theme-editor control requires adding `settings` arrays.
- Some custom CSS may not have been pulled for sections whose classes didn't match `cc-*` / `v10-*` prefix patterns — these will fall back to Tailwind defaults. Verify each on preview.
- Tailwind scope expanded to include `.cc-apr26` (tailwind.config.js + rebuilt `assets/cc-tailwind.css`).
- Carousel rebuilds (Benefits, Testimonials) still TODO — first draft keeps original grid.

### Templates to build
- [ ] `templates/index.apr26.json` — composed homepage (preview at `/?view=apr26`)
- [ ] `templates/product.lp-v8-apr26.json` — v8 as product template
- [ ] `templates/product.lp-v10-apr26.json` — v10 as product template
- [ ] `templates/product.lp-ag1-apr26.json` — AG1 as product template
- [ ] `templates/product.lp-blueprint-apr26.json` — Blueprint as product template

### Site-wide pieces
- [ ] `cc-footer-apr26` (section, not snippet — shows on every page)
- [ ] Global CSS polish: hover states, mobile font-size scale, cart drawer cursor

---

## Rollout phases

### Phase 1: Extract the big pieces (no template flip yet)
1. Inventory homepage blocks — confirm list above matches what's in the monolith
2. Extract sections one by one, each as `cc-<name>-apr26.liquid`, with its own schema + `<style>` block
3. For each extraction: apply relevant audit fix during the rebuild (carousel, mobile sizing, etc.)
4. Build `templates/index.apr26.json` that composes the new sections
5. Preview at `/?view=apr26` — live site remains on `index.json` (the monolith)

### Phase 2: Product templates for LPs
1. Extract LP-specific blocks (hero variants, comparison tables, etc.) as sections
2. Build `templates/product.lp-*.json` templates composing those sections
3. Preview each at `/products/coastline-welcome-pack?view=lp-<name>`
4. Replace hardcoded variant IDs with `product.selected_variant` / native selling-plan allocations

### Phase 3: Footer + global polish
1. Rebuild footer as `cc-footer-apr26` with responsive behavior + tighter scale
2. Global CSS polish pass (hover states, mobile type, cart cursor)

### Phase 4: Cutover (Shopify draft theme, then publish)
1. Duplicate live theme in Shopify admin
2. Swap active templates in the draft (`index.json` → uses new sections, `product.json` → new master)
3. Preview every page on the draft
4. Publish the draft — rollback = re-publish original (~10s)
5. Cleanup commit: remove orphaned monolithic sections

---

## Open questions (flag when they come up)
- _(none yet — add here as they surface)_

---

## Log
- **2026-04-23** — `cc-pricing-apr26` snippet shipped (homepage + v8 + v10 share one source of truth). First `-apr26` artifact. Will be promoted to a real section in Phase 1.
