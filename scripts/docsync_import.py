#!/usr/bin/env python3
"""Import owner-permitted project documents into Pinakes.

This script walks /Volumes/samsungT7/projects, classifies text documents with a
safety-first policy, copies permitted documents into external/, and writes
MANIFEST.json + INDEX.md. Documents with secrets, credentials, or personal/private
signals such as Elijah are written only to the ignored local REVIEW.private.md queue
so they do not get pushed to the public Pinakes repo.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable
from urllib.parse import urlparse
from urllib.request import Request, urlopen

PROJECTS_ROOT = Path('/Volumes/samsungT7/projects')
PINAKES_ROOT = Path('/Volumes/samsungT7/projects/Pinakes')
EXTERNAL_ROOT = PINAKES_ROOT / 'external'
REVIEW_PRIVATE = PINAKES_ROOT / 'REVIEW.private.md'
MANIFEST = PINAKES_ROOT / 'MANIFEST.json'
INDEX = PINAKES_ROOT / 'INDEX.md'

DOC_EXTS = {'.md', '.mdx', '.rst', '.adoc', '.txt'}
SKIP_DIRS = {
    '.git', '.hg', '.svn',
    'node_modules', '.venv', 'venv', 'env',
    'dist', 'build', '.next', 'DerivedData', '.dart_tool', '.gradle', 'Pods',
    '__pycache__', '.pytest_cache', '.mypy_cache', '.ruff_cache',
    'target', 'vendor', 'vendors', 'third_party', 'third-party', 'external',
    'vcpkg', 'vcpkg_installed', 'site-packages', '.cache', 'cache', 'fastembed_cache', '.tox', 'coverage', '.coverage',
    'uploads', 'tmp', 'temp', 'logs', '.obsidian',
}
PUBLIC_PATH_SEGMENTS = {'public'}
PUBLIC_DOC_NAMES = {
    'README.md', 'README.mdx', 'readme.md',
    'CONTRIBUTING.md', 'SECURITY.md', 'LICENSE.md', 'NOTICE.md',
    'ACKNOWLEDGMENTS.md', 'CHANGELOG.md', 'CODE_OF_CONDUCT.md',
}
PUBLIC_NAME_HINTS = (
    'quickstart', 'getting_started', 'getting-started', 'guide', 'tutorial',
    'api_reference', 'api-reference', 'api-docs', 'docs',
)
INTERNAL_NAME_HINTS = (
    'claude', 'agents', 'agent', 'system_prompt', 'prompt', 'todo', 'plan',
    'roadmap', 'audit', 'postmortem', 'strategy', 'trading', 'finance', 'key_rotation',
    'vpn', 'deployment', 'env', 'secret', 'private', 'internal', 'meeting', 'session',
    'bug', 'fix', 'complete', 'success', 'implementation', 'report', 'prd', 'spec',
)
SECRET_PATTERNS = [
    re.compile(r'-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----'),
    re.compile(r'(?i)\bBearer\s+[A-Za-z0-9._~+/=-]{20,}'),
    re.compile(r'(?i)\b(seed phrase|recovery phrase|mnemonic)\b'),
    re.compile(r'ghp_[A-Za-z0-9_]{20,}'),
    re.compile(r'sk-[A-Za-z0-9]{20,}'),
    re.compile(r'sb_secret_[A-Za-z0-9_-]{20,}'),
]
CREDENTIAL_ASSIGNMENT_RE = re.compile(
    r'''(?ix)
    ^\s*(?:export\s+)?
    [A-Z0-9_]*(?:API[_-]?KEY|SECRET|PASSWORD|PASSWD|TOKEN|PRIVATE[_-]?KEY)
    \s*[:=]\s*["']?(?P<value>[^"'\s#,`]+)
    '''
)
PERSONAL_PATH_HINTS = (
    'elijah', 'people', 'person', 'personal', 'private', 'family', 'journal',
    'diary', 'therapy', 'medical', 'health', 'self', 'contacts', 'contact',
    'me', 'cv', 'resume', 'résumé', 'interview-prep', 'story-bank',
    'conversations', 'conversation', 'daily',
)
PERSONAL_PATTERNS = [
    re.compile(r'(?i)\bElijah\b'),
    re.compile(r'(?i)^\s*(ssn|social security|date of birth|dob|home address)\s*[:=]', re.M),
]
FRONTMATTER_RE = re.compile(r'\A---\s*\n(.*?)\n---\s*\n', re.S)
VISIBILITY_RE = re.compile(r'^\s*visibility\s*:\s*(internal|external)\s*$', re.I | re.M)

PUBLIC_REPO_CACHE: dict[Path, bool] = {}
GITHUB_VIS_CACHE: dict[str, bool] = {}

@dataclass
class ManifestEntry:
    source_project: str
    source_relative_path: str
    imported_path: str
    visibility: str
    confidence: str
    reason: str
    bytes: int
    updated_utc: str

@dataclass
class ReviewEntry:
    source_project: str
    source_relative_path: str
    reason: str


def run(cmd: list[str], cwd: Path | None = None) -> str:
    return subprocess.check_output(cmd, cwd=str(cwd) if cwd else None, text=True, stderr=subprocess.DEVNULL).strip()


def discover_git_root(path: Path) -> Path | None:
    cur = path if path.is_dir() else path.parent
    while cur != cur.parent and cur != PROJECTS_ROOT.parent:
        if (cur / '.git').exists():
            return cur
        if cur == PROJECTS_ROOT:
            return None
        cur = cur.parent
    return None


def github_owner_repo(remote: str) -> str | None:
    remote = remote.strip()
    if remote.startswith('git@github.com:'):
        s = remote.removeprefix('git@github.com:')
    elif 'github.com' in remote:
        parsed = urlparse(remote)
        s = parsed.path.lstrip('/')
    else:
        return None
    if s.endswith('.git'):
        s = s[:-4]
    parts = s.split('/')
    if len(parts) >= 2:
        return f'{parts[0]}/{parts[1]}'
    return None


def is_public_github_repo(owner_repo: str) -> bool:
    if owner_repo in GITHUB_VIS_CACHE:
        return GITHUB_VIS_CACHE[owner_repo]
    url = f'https://api.github.com/repos/{owner_repo}'
    try:
        req = Request(url, headers={'Accept': 'application/vnd.github+json', 'User-Agent': 'pinakes-docsync'})
        with urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
        public = bool(data.get('private') is False)
    except Exception:
        public = False
    GITHUB_VIS_CACHE[owner_repo] = public
    return public


def git_repo_is_public(git_root: Path | None) -> bool:
    if git_root is None:
        return False
    if git_root in PUBLIC_REPO_CACHE:
        return PUBLIC_REPO_CACHE[git_root]
    public = False
    try:
        remote = run(['git', 'remote', 'get-url', 'origin'], git_root)
        owner_repo = github_owner_repo(remote)
        if owner_repo:
            public = is_public_github_repo(owner_repo)
    except Exception:
        public = False
    PUBLIC_REPO_CACHE[git_root] = public
    return public


def frontmatter_visibility(text: str) -> str | None:
    m = FRONTMATTER_RE.search(text)
    if not m:
        return None
    vm = VISIBILITY_RE.search(m.group(1))
    return vm.group(1).lower() if vm else None


def has_secret_signal(text: str) -> bool:
    if any(p.search(text) for p in SECRET_PATTERNS):
        return True
    placeholder_prefixes = ('change-me', 'changeme', 'example', 'your_', 'your-', '<', '$', 'redacted', 'credentials.', 'process.env')
    for line in text.splitlines():
        m = CREDENTIAL_ASSIGNMENT_RE.search(line)
        if not m:
            continue
        value = m.group('value').strip().strip('"\'')
        lower = value.lower()
        if not value or lower in {'none', 'null', 'true', 'false'}:
            continue
        if lower.startswith(placeholder_prefixes):
            continue
        if re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*(\.[A-Za-z_][A-Za-z0-9_]*)+', value):
            # Code variable/property reference, not an embedded secret value.
            continue
        if len(value) >= 12:
            return True
    return False


def has_personal_signal(path: Path, text: str) -> bool:
    rel_parts = [part.lower() for part in path.relative_to(PROJECTS_ROOT).parts]
    rel_joined = '/'.join(rel_parts)
    if 'elijah' in rel_joined:
        return True
    stems = {Path(part).stem.lower() for part in rel_parts}
    if any(part in PERSONAL_PATH_HINTS for part in rel_parts) or any(stem in PERSONAL_PATH_HINTS for stem in stems):
        return True
    sample = text[:8000]
    return any(p.search(sample) for p in PERSONAL_PATTERNS)


def is_public_path(path: Path, project_root: Path) -> bool:
    rel_parts = path.relative_to(project_root).parts
    lower_parts = [p.lower() for p in rel_parts]
    if any(part in PUBLIC_PATH_SEGMENTS for part in lower_parts):
        return True
    joined = '/'.join(lower_parts)
    return '/docs/public/' in f'/{joined}/'


def public_name_hint(path: Path) -> bool:
    name = path.name
    lower = name.lower()
    if name in PUBLIC_DOC_NAMES:
        return True
    stem = path.stem.lower()
    return any(h in stem for h in PUBLIC_NAME_HINTS)


def internal_name_hint(path: Path) -> bool:
    lower = '/'.join(p.lower() for p in path.parts)
    return any(h in lower for h in INTERNAL_NAME_HINTS)


def iter_documents() -> Iterable[Path]:
    for project in sorted(PROJECTS_ROOT.iterdir(), key=lambda p: p.name.lower()):
        if not project.is_dir() or project.resolve() == PINAKES_ROOT.resolve():
            continue
        for dirpath, dirnames, filenames in os.walk(project):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith('._')]
            for filename in sorted(filenames):
                if filename.startswith('._') or filename == '.DS_Store':
                    continue
                path = Path(dirpath) / filename
                if path.suffix.lower() in DOC_EXTS:
                    yield path


def classify(path: Path) -> tuple[str, str, str]:
    try:
        text = path.read_text(encoding='utf-8', errors='replace')
    except Exception as e:
        return 'internal', 'low', f'unreadable: {e}'

    if has_secret_signal(text):
        return 'internal', 'high', 'secret/credential signal'

    if has_personal_signal(path, text):
        return 'internal', 'high', 'personal/private signal'

    return 'external', 'high', 'owner-permitted: no secret/personal signal'


def safe_dest(path: Path) -> Path:
    rel = path.relative_to(PROJECTS_ROOT)
    parts = [re.sub(r'[^A-Za-z0-9._-]+', '_', p) for p in rel.parts]
    return EXTERNAL_ROOT.joinpath(*parts)


def main() -> int:
    if not PROJECTS_ROOT.exists():
        raise SystemExit(f'missing projects root: {PROJECTS_ROOT}')
    if not PINAKES_ROOT.exists():
        raise SystemExit(f'missing Pinakes repo: {PINAKES_ROOT}')

    if EXTERNAL_ROOT.exists():
        shutil.rmtree(EXTERNAL_ROOT)
    EXTERNAL_ROOT.mkdir(parents=True, exist_ok=True)

    manifest: list[ManifestEntry] = []
    review: list[ReviewEntry] = []
    total = 0
    for path in iter_documents():
        total += 1
        project = path.relative_to(PROJECTS_ROOT).parts[0]
        src_rel = str(path.relative_to(PROJECTS_ROOT))
        visibility, confidence, reason = classify(path)
        if visibility == 'external':
            dest = safe_dest(path)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, dest)
            manifest.append(ManifestEntry(
                source_project=project,
                source_relative_path=src_rel,
                imported_path=str(dest.relative_to(PINAKES_ROOT)),
                visibility=visibility,
                confidence=confidence,
                reason=reason,
                bytes=dest.stat().st_size,
                updated_utc=datetime.now(timezone.utc).isoformat(timespec='seconds'),
            ))
        else:
            review.append(ReviewEntry(project, src_rel, reason))

    manifest.sort(key=lambda e: e.imported_path.lower())
    data = {
        'generated_utc': datetime.now(timezone.utc).isoformat(timespec='seconds'),
        'projects_root': str(PROJECTS_ROOT),
        'policy': 'owner-permitted: copy all scanned documents except those with secret/credential or personal/private signals; private review queue is gitignored',
        'total_candidates': total,
        'imported_count': len(manifest),
        'review_count': len(review),
        'documents': [asdict(e) for e in manifest],
    }
    MANIFEST.write_text(json.dumps(data, indent=2, sort_keys=True) + '\n', encoding='utf-8')

    lines = [
        '# Pinakes Index',
        '',
        f'Generated: `{data["generated_utc"]}`',
        '',
        f'- Candidate documents scanned: **{total}**',
        f'- Owner-permitted documents imported: **{len(manifest)}**',
        f'- Secret/personal documents held for private review: **{len(review)}**',
        '',
        'Documents are copied unless they contain secret/credential or personal/private signals. Held files are not included in this public repo.',
        '',
        '## Imported documents',
        '',
    ]
    by_project: dict[str, list[ManifestEntry]] = {}
    for entry in manifest:
        by_project.setdefault(entry.source_project, []).append(entry)
    for project in sorted(by_project, key=str.lower):
        lines.append(f'### {project}')
        lines.append('')
        for entry in by_project[project]:
            lines.append(f'- [`{entry.source_relative_path}`]({entry.imported_path}) — {entry.reason}')
        lines.append('')
    INDEX.write_text('\n'.join(lines).rstrip() + '\n', encoding='utf-8')

    review_lines = [
        '# Pinakes Private Review Queue',
        '',
        'This file is intentionally gitignored because source paths may reveal private project details.',
        'Review entries here manually. Files here matched secret/credential or personal/private safety filters and are not safe to publish until cleaned.',
        '',
        f'Generated: `{data["generated_utc"]}`',
        f'Total held: **{len(review)}**',
        '',
    ]
    by_reason: dict[str, list[ReviewEntry]] = {}
    for entry in review:
        by_reason.setdefault(entry.reason, []).append(entry)
    for reason in sorted(by_reason):
        review_lines.append(f'## {reason}')
        review_lines.append('')
        for entry in by_reason[reason][:5000]:
            review_lines.append(f'- `{entry.source_relative_path}`')
        if len(by_reason[reason]) > 5000:
            review_lines.append(f'- ... {len(by_reason[reason]) - 5000} more')
        review_lines.append('')
    REVIEW_PRIVATE.write_text('\n'.join(review_lines).rstrip() + '\n', encoding='utf-8')

    print(json.dumps({
        'scanned': total,
        'imported': len(manifest),
        'review': len(review),
        'manifest': str(MANIFEST),
        'index': str(INDEX),
        'review_private': str(REVIEW_PRIVATE),
    }, indent=2))
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
