#!/usr/bin/env python3
"""Add block schema defs to block-based apr26 sections + distribute block instances in index.apr26.json."""
import json
import re
from pathlib import Path

REPO = Path('/Users/bizmac22/coastline-revamp')

# Read monolith schema blocks
mono_text = (REPO / 'sections/cc-homepage.liquid').read_text()
mono_schema_text = re.search(r'\{% schema %\}(.*?)\{% endschema %\}', mono_text, re.DOTALL).group(1)
mono_schema = json.loads(mono_schema_text)
block_defs = {b['type']: b for b in mono_schema.get('blocks', [])}

# Section → block type mapping
section_blocks = {
    'cc-system-apr26':       {'type': 'step',         'max': 3},
    'cc-benefits-apr26':     {'type': 'pillar',       'max': 5},
    'cc-testimonials-apr26': {'type': 'testimonial',  'max': 50},
    'cc-faq-apr26':          {'type': 'faq',          'max': 20},
}

# Update each section's schema to include its block definition
for section_name, meta in section_blocks.items():
    path = REPO / f'sections/{section_name}.liquid'
    content = path.read_text()
    m = re.search(r'(\{% schema %\})(.*?)(\{% endschema %\})', content, re.DOTALL)
    schema_body = m.group(2)
    schema = json.loads(schema_body)
    schema['blocks'] = [block_defs[meta['type']]]
    schema['max_blocks'] = meta['max']
    new_schema_text = '\n' + json.dumps(schema, indent=2) + '\n'
    new_content = content[:m.start(2)] + new_schema_text + content[m.end(2):]
    path.write_text(new_content)
    print(f"  ✓ Added '{meta['type']}' block def to {section_name}")

# Parse templates/index.json (strip comment header)
idx_raw = (REPO / 'templates/index.json').read_text()
m = re.search(r'\*/\s*(\{.*\})\s*$', idx_raw, re.DOTALL)
idx_body = m.group(1) if m else idx_raw
idx = json.loads(idx_body)

# Find cc-homepage section with blocks
home_section = None
for k, v in idx.get('sections', {}).items():
    if v.get('type') == 'cc-homepage':
        home_section = v
        break

if home_section is None:
    print("ERROR: no cc-homepage section found in templates/index.json")
    raise SystemExit(1)

blocks = home_section.get('blocks', {})
block_order = home_section.get('block_order', [])

# Group block IDs by type, preserving block_order
by_type = {}
for bid in block_order:
    b = blocks[bid]
    by_type.setdefault(b['type'], []).append(bid)

# Now update index.apr26.json
apr_path = REPO / 'templates/index.apr26.json'
apr = json.loads(apr_path.read_text())

type_to_section = {
    'step':        'cc-system-apr26',
    'pillar':      'cc-benefits-apr26',
    'testimonial': 'cc-testimonials-apr26',
    'faq':         'cc-faq-apr26',
}

for btype, section_key in type_to_section.items():
    ids = by_type.get(btype, [])
    if not ids:
        continue
    section_obj = apr['sections'].get(section_key, {'type': section_key, 'settings': {}})
    section_obj['blocks'] = {bid: blocks[bid] for bid in ids}
    section_obj['block_order'] = ids
    apr['sections'][section_key] = section_obj
    print(f"  ✓ {section_key} ← {len(ids)} {btype} blocks")

apr_path.write_text(json.dumps(apr, indent=2) + '\n')
print(f"\nUpdated {apr_path.name}")
