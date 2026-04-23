#!/usr/bin/env python3
"""
Batch-extract homepage sections into composable -apr26 files.
v2: auto-detect class names per section, properly trim last section,
compose index.apr26.json in order.
"""
import json
import re
from pathlib import Path

REPO = Path('/Users/bizmac22/coastline-revamp')
MONO = REPO / 'sections/cc-homepage.liquid'
OUT_SECTIONS = REPO / 'sections'
OUT_TEMPLATE = REPO / 'templates/index.apr26.json'

# (search_line_hint, name, label) — we'll locate the <section> near each hint
SECTIONS = [
    (553,  'press-apr26',         'Press logos'),
    (582,  'ask-apr26',           'Ask Coastline AI'),
    (670,  'genetics-stat-apr26', 'Genetics Stat'),
    (689,  'system-apr26',        'The System'),
    (858,  'ugc-apr26',           'UGC Community'),
    (889,  'benefits-apr26',      'Benefits'),
    (965,  'expert-apr26',        'Expert Narrative'),
    (1032, 'testimonials-apr26',  'Reviews'),
    (1132, 'video-apr26',         'Video'),
    (1229, 'comparison-apr26',    'Comparison table'),
    (1330, 'math-apr26',          'Do the Math'),
    (1379, 'story-apr26',         'Our Story'),
    (1408, 'faq-apr26',           'FAQ'),
    (1453, 'email-capture-apr26', 'Email Capture'),
    (1500, 'final-cta-apr26',     'Final CTA'),
]

with open(MONO) as f:
    lines = f.readlines()
    text = ''.join(lines)

# Find nearest <section> opening tag within ±20 lines of the hint
def find_section_start(hint):
    candidates = []
    for i in range(max(hint-20, 1), min(hint+20, len(lines)+1)):
        if lines[i-1].lstrip().startswith('<section'):
            candidates.append((abs(i - hint), i))
    if candidates:
        candidates.sort()
        return candidates[0][1]
    return hint

# Find matching </section> after start (depth-counted)
def find_section_end(start):
    depth = 0
    for i in range(start, len(lines)+1):
        line = lines[i-1]
        depth += len(re.findall(r'<section[\s>]', line))
        depth -= len(re.findall(r'</section>', line))
        if depth <= 0:
            return i
    return len(lines)

# Collect section ranges
ranges = []
for hint, name, label in SECTIONS:
    s = find_section_start(hint)
    e = find_section_end(s)
    ranges.append((s, e, name, label))

# Extract all CSS rules from monolith <style> blocks (with brace-depth parsing)
style_blocks = re.findall(r'<style>(.*?)</style>', text, re.DOTALL)
all_css = '\n'.join(style_blocks)

def parse_rules(css):
    """Return list of (selector_text, full_rule) at the top level."""
    rules = []
    i = 0
    n = len(css)
    while i < n:
        # skip whitespace + comments
        while i < n and css[i] in ' \t\n\r':
            i += 1
        if i >= n:
            break
        if css[i:i+2] == '/*':
            end = css.find('*/', i+2)
            i = (end + 2) if end != -1 else n
            continue
        # find next '{'
        brace = css.find('{', i)
        if brace == -1:
            break
        # find matching '}' accounting for nested braces
        depth = 1
        j = brace + 1
        while j < n and depth > 0:
            if css[j] == '{': depth += 1
            elif css[j] == '}': depth -= 1
            j += 1
        selector = css[i:brace].strip()
        rule = css[i:j]
        rules.append((selector, rule))
        i = j
    return rules

rules = parse_rules(all_css)

def find_classes_in_html(html):
    """Collect cc-*, v10-* class tokens."""
    tokens = set()
    for match in re.finditer(r'class\s*=\s*"([^"]+)"', html):
        for tok in match.group(1).split():
            if tok.startswith('cc-') or tok.startswith('v10-'):
                tokens.add(tok)
    return tokens

def extract_css_for(tokens, current_scope):
    """Return concatenated CSS rules referencing any of the tokens,
       rewritten from .cc-homepage to .<current_scope>."""
    matched = []
    for selector, rule in rules:
        combined = selector
        # Only include if a token appears as a whole class in selector/rule preamble
        # Use word-boundary check
        for tok in tokens:
            if re.search(r'\.' + re.escape(tok) + r'(?![\w-])', selector):
                matched.append(rule)
                break
    # Also extract @media blocks that contain rules matching these tokens
    media_pattern = re.compile(r'@media[^{]*\{[^}]*(?:\.' + '|\\.'.join(re.escape(t) for t in tokens) + r')[^}]*\}[^}]*\}', re.DOTALL)
    # simpler: find @media blocks in all_css, include if any token is inside
    for m in re.finditer(r'@media[^{]*\{', all_css):
        mstart = m.start()
        # find matching close brace
        depth = 0
        j = m.end() - 1  # position of the opening {
        depth = 1
        j += 1
        while j < len(all_css) and depth > 0:
            if all_css[j] == '{': depth += 1
            elif all_css[j] == '}': depth -= 1
            j += 1
        mblock = all_css[mstart:j]
        if any(re.search(r'\.' + re.escape(tok) + r'(?![\w-])', mblock) for tok in tokens):
            if mblock not in matched:
                matched.append(mblock)
    out = '\n'.join(matched)
    # Rescope
    out = out.replace('.cc-homepage', '.' + current_scope)
    return out

def build_section(name, label, html_block, css_block):
    parts = []
    parts.append(f"{{%- comment -%}}\n  cc-{name} — {label}\n  Extracted from cc-homepage.liquid (Apr 26 rebuild, vanilla re-scope)\n{{%- endcomment -%}}\n\n")
    parts.append("{% render 'cc-deps' %}\n\n")
    parts.append(f'<div class="cc-apr26 cc-{name}">\n')
    for line in html_block.splitlines():
        parts.append('  ' + line + '\n')
    parts.append('</div>\n\n')
    if css_block.strip():
        parts.append("<style>\n")
        parts.append(css_block + '\n')
        parts.append("</style>\n\n")
    parts.append('{% schema %}\n')
    parts.append('{\n')
    parts.append(f'  "name": "{label} (apr26)",\n')
    parts.append('  "tag": "section",\n')
    parts.append(f'  "class": "section-cc-{name}",\n')
    parts.append('  "settings": [],\n')
    parts.append('  "presets": [\n')
    parts.append(f'    {{\n      "name": "{label} (apr26)",\n      "category": "Coastline"\n    }}\n')
    parts.append('  ]\n')
    parts.append('}\n')
    parts.append('{% endschema %}\n')
    return ''.join(parts)

# Process
written = []
for s, e, name, label in ranges:
    html = ''.join(lines[s-1:e]).rstrip() + '\n'
    scope = f'cc-{name}'
    tokens = find_classes_in_html(html)
    # include section-global tokens (like cc-home-* that the section's content uses)
    css = extract_css_for(tokens, scope) if tokens else ''
    file_out = OUT_SECTIONS / f'cc-{name}.liquid'
    file_out.write_text(build_section(name, label, html, css))
    written.append((name, label, s, e, len(tokens), len(css)))
    print(f"  ✓ cc-{name}.liquid  (lines {s}–{e}, {len(tokens)} classes, {len(css)} CSS chars)")

# Rebuild index.apr26.json
hero = {
    "type": "cc-hero-apr26",
    "settings": {
        "hero_label": "THE ULTIMATE LONGEVITY SYSTEM",
        "hero_headline": "Unlock a whole new <br>horizon of health.",
        "hero_subheadline": "13 science-backed, clinically-verified ingredients in one easy AM/PM routine to support brain, energy, muscle, gut, skin, sleep and more.",
        "hero_reviews": "2,000+ five-star reviews",
        "hero_cta_text": "START MY LONGEVITY SYSTEM",
        "hero_cta_link": "#cc-home-pricing",
        "hero_secondary_text": "SKIP TO PRICING",
        "hero_secondary_link": "#cc-home-pricing",
        "anchor": "cc-home-hero"
    }
}
sections_obj = {"cc-hero-apr26": hero}
order = ["cc-hero-apr26"]
# Insert remaining in proper on-page order (Pricing sits between video and comparison per live order)
on_page_order = [
    'press-apr26', 'ask-apr26', 'genetics-stat-apr26',
    'system-apr26', 'ugc-apr26', 'benefits-apr26',
    'expert-apr26', 'testimonials-apr26', 'video-apr26',
    # Pricing slot here — add after promoting snippet to section
    'comparison-apr26', 'math-apr26', 'story-apr26',
    'faq-apr26', 'email-capture-apr26', 'final-cta-apr26',
]
for n in on_page_order:
    key = f'cc-{n}'
    sections_obj[key] = {"type": key, "settings": {}}
    order.append(key)

OUT_TEMPLATE.write_text(json.dumps({"sections": sections_obj, "order": order}, indent=2) + "\n")
print(f"\nWrote {len(written)} sections, updated {OUT_TEMPLATE.name}")
