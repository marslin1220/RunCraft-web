#!/usr/bin/env python3
"""Check generated content, routes, anchors, metadata and image references."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
LANGS = ['en', 'zh-Hant', 'zh-Hans', 'ja', 'ko']
errors = []

class Page(HTMLParser):
    def __init__(self, file):
        super().__init__()
        self.file, self.ids, self.refs, self.tags, self.attrs = file, [], [], [], []
        self.feed(file.read_text())
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append(tag)
        self.attrs.append((tag, attrs))
        if tag == 'meta' and attrs.get('property') == 'og:image':
            self.refs.append(attrs['content'])
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        for key in ['href', 'src']:
            if key in attrs:
                self.refs.append(attrs[key])
        if tag == 'img' and 'alt' not in attrs:
            errors.append(f'{self.file.relative_to(ROOT)}: image missing alt')

pages = []
schema = None
for lang in LANGS:
    content = json.loads((ROOT / 'content' / f'{lang}.json').read_text())
    if schema is None:
        schema = set(content)
    if set(content) != schema:
        errors.append(f'{lang}: content keys differ from English')
    for key, value in content.items():
        if not value:
            errors.append(f'{lang}: empty {key}')
    if len(content['steps']) != 3 or len(content['faq']) != 6 or len(content['guide_sections']) != 8:
        errors.append(f'{lang}: missing workflow/FAQ/guide sections')
    prefix = ROOT if lang == 'en' else ROOT / lang
    pages += [Page(prefix / 'index.html'), Page(prefix / 'guide/index.html'), Page(prefix / 'press/index.html')]
by_file = {page.file.resolve(): page for page in pages}
refs = 0
for page in pages:
    file = page.file
    if len(page.ids) != len(set(page.ids)):
        errors.append(f'{file}: duplicate IDs')
    for tag in ['h1', 'main']:
        if page.tags.count(tag) != 1:
            errors.append(f'{file}: expected one {tag}')
    if not any(tag == 'link' and a.get('rel') == 'canonical' for tag, a in page.attrs):
        errors.append(f'{file}: missing canonical URL')
    if len([a for tag, a in page.attrs if tag == 'link' and a.get('hreflang')]) != 6:
        errors.append(f'{file}: missing language alternatives')
    for ref in page.refs:
        url = urlsplit(ref)
        if url.scheme or url.netloc:
            # First-party absolute social images must also exist locally.
            if url.netloc == 'runcraft.marstudio.app' and url.path.startswith('/assets/'):
                if not (ROOT / url.path.lstrip('/')).is_file():
                    errors.append(f'{file}: missing public asset {ref}')
            continue
        if not url.path:
            target = file
        else:
            target = (ROOT / unquote(url.path.lstrip('/'))) if url.path.startswith('/') else (file.parent / unquote(url.path))
            target = target.resolve()
            if url.path.endswith('/') or target.is_dir():
                target = target / 'index.html'
        refs += 1
        if not target.exists():
            # The existing English policy is built by GitHub Pages/Jekyll.
            if target == ROOT / 'privacy/index.html' and (ROOT / 'privacy.md').exists():
                continue
            errors.append(f'{file.relative_to(ROOT)}: missing target {ref}')
        elif url.fragment and target.suffix == '.html':
            parsed = by_file.get(target.resolve()) or Page(target)
            if unquote(url.fragment) not in parsed.ids:
                errors.append(f'{file.relative_to(ROOT)}: missing anchor {ref}')
    text = file.read_text().lower()
    for retired in ['adaptive running coach', '自適應訓練教練', '自适应跑步教练', 'before the jump becomes an injury', '80/20', 'coaching.png', 'loadbanner.png', 'recovery.png']:
        if retired in text:
            errors.append(f'{file.relative_to(ROOT)}: retired claim or image {retired}')
# Ensure regeneration does not silently drift committed pages.
outputs = [p.file for p in pages] + [ROOT / 'sitemap.xml', ROOT / 'robots.txt']
before = {p: p.read_bytes() for p in outputs}
subprocess.run([sys.executable, str(ROOT / 'scripts/build_site.py')], check=True, stdout=subprocess.DEVNULL)
for p, data in before.items():
    if p.read_bytes() != data:
        errors.append(f'{p.relative_to(ROOT)}: build is not reproducible')
if errors:
    print('\n'.join(errors))
    sys.exit(1)
print(f'PASS: 5 locale schemas, 15 pages, {refs} local references, metadata, retired claims and reproducible build.')
