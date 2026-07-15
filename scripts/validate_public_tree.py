#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'MANIFEST.json'
IMPORTER = ROOT / 'scripts' / 'docsync_import.py'

spec = importlib.util.spec_from_file_location('docsync_import', IMPORTER)
if spec is None or spec.loader is None:
    raise RuntimeError(f'Unable to load importer module from {IMPORTER}')
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)

manifest = json.loads(MANIFEST.read_text())
errors: list[str] = []
secret_hits: list[str] = []
personal_hits: list[str] = []
appledouble_entries: list[str] = []

for entry in manifest['documents']:
    rel = entry['imported_path']
    p = ROOT / rel
    if not p.exists():
        errors.append(f'missing {rel}')
        continue
    if '..' in Path(rel).parts:
        errors.append(f'bad path {rel}')
    if p.name.startswith('._'):
        appledouble_entries.append(rel)
        continue
    text = p.read_text(encoding='utf-8', errors='replace')
    if mod.has_secret_signal(text):
        secret_hits.append(rel)
    if mod.has_personal_signal(p, text):
        personal_hits.append(rel)

prompt = (ROOT / 'pinakes' / 'prompts' / 'classify.md').read_text(encoding='utf-8')
examples = re.findall(r'Assistant:\n```\n(\{.*?\})\n```', prompt, flags=re.S)
for example in examples:
    json.loads(example)

result = {
    'manifest_docs': len(manifest['documents']),
    'imported_count': manifest['imported_count'],
    'review_count': manifest['review_count'],
    'missing_or_bad': errors[:50],
    'secret_hits': secret_hits[:50],
    'personal_hits': personal_hits[:50],
    'appledouble_entries': appledouble_entries[:50],
    'classify_examples': len(examples),
}
print(json.dumps(result, indent=2))

if (
    manifest['imported_count'] != len(manifest['documents'])
    or errors
    or secret_hits
    or personal_hits
    or appledouble_entries
):
    sys.exit(1)
