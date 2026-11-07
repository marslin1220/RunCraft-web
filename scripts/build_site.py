#!/usr/bin/env python3
"""Build dependency-free localized pages for the existing GitHub Pages site."""
from html import escape
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://runcraft.marstudio.app'
LANGS = {'en': 'English', 'zh-Hant': '繁體中文', 'zh-Hans': '简体中文', 'ja': '日本語', 'ko': '한국어'}
GLOBE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M3 9h18M3 15h18M12 3c5 5 5 13 0 18-5-5-5-13 0-18Z"/></svg>'
MENU = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>'
APPLE = '<svg width="16" height="19" viewBox="0 0 16 19" fill="currentColor" aria-hidden="true"><path d="M13 10c0 2.6 2.3 3.5 2.3 3.5s-.4 1.3-1.2 2.5c-.7 1-1.5 2.1-2.6 2.1s-1.5-.7-2.8-.7-1.7.7-2.8.7S3.9 17 3.2 15.9C1.7 13.8.6 9.9 2.1 7.3c.8-1.3 2.1-2.1 3.6-2.2 1.1 0 2.2.8 2.8.8s2-.9 3.3-.8c.6 0 2.1.2 3.2 1.7-.1.1-1.9 1.1-2 3.2ZM11 3.7c.6-.7 1-1.7.9-2.8-.9.1-1.9.6-2.6 1.3-.5.7-1 1.7-.9 2.7 1 .1 1.9-.5 2.6-1.2Z"/></svg>'


def h(value):
    return escape(str(value), quote=True)


def route(lang, kind='home'):
    prefix = '' if lang == 'en' else f'{lang}/'
    return prefix + ('' if kind == 'home' else f'{kind}/')


def rel(path, target):
    import posixpath
    return posixpath.relpath(target or '.', path or '.') + ('/' if not Path(target).suffix else '')


def head(lang, c, kind):
    path = route(lang, kind)
    asset = rel(path, 'assets')
    title = 'RunCraft — ' + (c['guide_heading'] if kind == 'guide' else c['title'])
    description = c['guide_intro'] if kind == 'guide' else c['description']
    alternates = '\n'.join(f'<link rel="alternate" hreflang="{code}" href="{BASE}/{route(code, kind)}">' for code in LANGS)
    redirect = '''<script>
(function () {
  var supported = ['en', 'zh-Hant', 'zh-Hans', 'ja', 'ko'];
  var saved; try { saved = localStorage.getItem('rc-lang'); } catch (e) {}
  if (supported.indexOf(saved) !== -1) { if (saved !== 'en') location.replace(saved + '/' + location.hash); return; }
  var language = (navigator.language || '').toLowerCase();
  var target = language.indexOf('zh') === 0 ? (/^zh-(cn|hans|sg)/.test(language) ? 'zh-Hans' : 'zh-Hant') : language.indexOf('ja') === 0 ? 'ja' : language.indexOf('ko') === 0 ? 'ko' : null;
  if (target) location.replace(target + '/' + location.hash);
})();
</script>''' if lang == 'en' and kind == 'home' else ''
    return f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="apple-itunes-app" content="app-id=6789176694">
<title>{h(title)}</title>
<meta name="description" content="{h(description)}">
<meta property="og:type" content="website">
<meta property="og:title" content="{h(title)}">
<meta property="og:description" content="{h(description)}">
<meta property="og:url" content="{BASE}/{path}">
<meta property="og:image" content="{BASE}/assets/social/{lang}.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="{BASE}/{path}">
{alternates}
<link rel="alternate" hreflang="x-default" href="{BASE}/{route('en', kind)}">
<link rel="icon" href="{rel(path, 'icon.png')}">
<link rel="stylesheet" href="{asset}site.css">
<link rel="stylesheet" href="{asset}refresh.css">
{redirect}
</head>
<body class="refresh">
<a class="skip-link" href="#main">{h(c['skip'])}</a>
<div class="wrap">
'''


def nav(lang, c, kind):
    path = route(lang, kind)
    home = rel(path, route(lang)) if kind != 'home' else ''
    links = [(home + '#method', c['nav'][0]), (home + '#watch', c['nav'][1]),
             (rel(path, route(lang, 'guide')), c['nav'][2]), (home + '#pricing', c['nav'][3]), (home + '#support', c['nav'][4])]
    menu = ''.join(f'<a href="{url}">{h(label)}</a>' for url, label in links)
    languages = ''.join(f'<a href="{rel(path, route(code, kind))}" data-lang="{code}"{(" class=on aria-current=true" if code == lang else "")}>{label}</a>' for code, label in LANGS.items())
    return f'''<nav aria-label="RunCraft">
<a class="brand" href="{home or './'}"><img src="{rel(path, 'icon.png')}" alt="" width="32" height="32">RunCraft</a>
<div class="navlinks">{menu}</div>
<div class="navtools">
<button class="iconbtn langbtn" type="button" aria-expanded="false" aria-controls="languages" aria-label="{h(c['language'])}">{GLOBE}</button>
<div class="langmenu" id="languages" hidden>{languages}</div>
<button class="iconbtn menubtn" type="button" aria-expanded="false" aria-controls="mobile-navigation" aria-label="{h(c['menu'])}" data-close-label="{h(c['close'])}">{MENU}</button>
</div>
</nav>'''


def footer(lang, c, kind):
    path = route(lang, kind)
    privacy = 'privacy/' if lang == 'en' else f'{lang}/privacy.html'
    return f'''<footer>
<p>© 2026 RunCraft · {h(c['copyright'])}</p>
<div class="links"><a href="{rel(path, route(lang, 'guide'))}">{h(c['nav'][2])}</a><a href="{rel(path, privacy)}">{h(c['privacy'])}</a><a href="{rel(path, route(lang, 'press'))}">{h(c['press'])}</a><a href="https://github.com/marslin1220/RunCraft-web">GitHub</a></div>
</footer></div><script src="{rel(path, 'assets')}nav.js" defer></script></body></html>\n'''


def bullets(items):
    return '<ul class="benefits">' + ''.join(f'<li>{h(item)}</li>' for item in items) + '</ul>'


def store(c):
    return f'<a class="btn-store" href="https://apps.apple.com/app/id6789176694">{APPLE}{h(c["download"])}</a>'


def faq(c):
    return '<div class="faq-list">' + ''.join(f'<details><summary>{h(q)}</summary><p>{h(a)}</p></details>' for q, a in c['faq']) + '</div>'


def homepage(lang, c):
    asset = rel(route(lang), 'assets') + ('' if lang == 'en' else f'{lang}/')
    cards = ''.join(f'<article class="path-card"><span class="index" aria-hidden="true">0{i + 1}</span><h3>{h(title)}</h3><p>{h(body)}</p></article>' for i, (title, body) in enumerate(c['paths']))
    steps = ''.join(f'<li><span class="step-number" aria-hidden="true">0{i + 1}</span><div><h3>{h(title)}</h3><p>{h(body)}</p></div></li>' for i, (title, body) in enumerate(c['steps']))
    prices = ''.join(f'<article class="price-card"><div class="price-name">{h(name)}</div><h3>{h(title)}</h3><p>{h(body)}</p></article>' for name, title, body in c['tiers'])
    return head(lang, c, 'home') + nav(lang, c, 'home') + f'''
<main id="main">
<header class="hero course-hero">
<div class="hero-copy">
<p class="kicker">{h(c['eyebrow'])}</p>
<h1>{h(c['hero'][0])}<br><em>{h(c['hero'][1])}</em></h1>
<p class="sub">{h(c['intro'])}</p>
<div class="cta">{store(c)}<a class="text-link" href="#method">{h(c['secondary'])}<span aria-hidden="true"> ↗</span></a></div>
<p class="badge-note">{h(c['badge'])}</p>
</div>
<figure class="hero-product">
<img class="hero-phone" src="{asset}live.png" alt="{h(c['alt'][0])}" width="1320" height="2868" fetchpriority="high">
<img class="hero-watch" src="{asset}watch-structured.png" alt="{h(c['alt'][1])}" width="410" height="502">
<figcaption>{h(c['caption'])}</figcaption>
</figure>
</header>
<section id="situations" class="path-section">
<p class="kicker">{h(c['path_kicker'])}</p><h2>{h(c['path_title'])}</h2><p class="lede">{h(c['path_intro'])}</p>
<div class="path-grid">{cards}</div>
</section>
<section id="method" class="method-section">
<span id="answers" class="anchor-alias" aria-hidden="true"></span>
<div class="section-intro"><p class="kicker">{h(c['steps_kicker'])}</p><h2>{h(c['steps_title'])}</h2><p class="lede">{h(c['steps_intro'])}</p><a class="text-link" href="guide/#course-review">{h(c['guide_link'])} <span aria-hidden="true">↗</span></a></div>
<ol class="steps">{steps}</ol>
</section>
<section class="daily-section">
<div class="section-intro"><p class="kicker">{h(c['daily_kicker'])}</p><h2>{h(c['daily_title'])}</h2><p class="lede">{h(c['daily_body'])}</p>{bullets(c['daily_bullets'])}</div>
<aside class="observation"><span class="observation-mark" aria-hidden="true">↗</span><h3>{h(c['observation_title'])}</h3><p>{h(c['observation_body'])}</p><a class="text-link" href="guide/#observations">{h(c['nav'][2])} <span aria-hidden="true">↗</span></a></aside>
</section>
<section id="watch" class="watch-feature">
<div><p class="kicker">{h(c['watch_kicker'])}</p><h2>{h(c['watch_title'])}</h2><p class="lede">{h(c['watch_body'])}</p>{bullets(c['watch_bullets'])}</div>
<div class="watch-gallery"><img src="{asset}watch-structured.png" alt="{h(c['alt'][1])}" width="410" height="502" loading="lazy"><img src="{asset}watch-open-goal.png" alt="{h(c['paths'][2][0])}" width="410" height="502" loading="lazy"></div>
</section>
<section class="review-feature">
<p class="kicker">{h(c['review_kicker'])}</p><h2>{h(c['review_title'])}</h2><p class="lede">{h(c['review_body'])}</p>{bullets(c['review_bullets'])}
</section>
<section id="guides" class="guide-callout"><div><h2>{h(c['guide_title'])}</h2><p>{h(c['guide_body'])}</p></div><a class="btn-secondary" href="guide/">{h(c['guide_link'])} <span aria-hidden="true">↗</span></a></section>
<section id="pricing"><p class="kicker">{h(c['pricing_kicker'])}</p><h2>{h(c['pricing_title'])}</h2><p class="lede">{h(c['pricing_intro'])}</p><div class="price-grid">{prices}</div><p class="fine-print">{h(c['trial_note'])}</p></section>
<section id="faq"><h2>{h(c['faq_title'])}</h2>{faq(c)}</section>
<section id="support" class="closing"><p class="kicker">RUNCRAFT</p><h2>{h(c['support_title'])}</h2><p class="lede">{h(c['support_body'])} <a href="mailto:support@marstudio.app">support@marstudio.app</a></p><div class="cta">{store(c)}</div></section>
</main>
''' + footer(lang, c, 'home')


def guide(lang, c):
    toc = ''.join(f'<a href="#{id}">{h(title)}</a>' for id, title, body in c['guide_sections'])
    articles = ''.join(f'<section id="{id}" class="guide-article"><p class="kicker">0{i + 1}</p><h2>{h(title)}</h2><p>{h(body)}</p></section>' for i, (id, title, body) in enumerate(c['guide_sections']))
    return head(lang, c, 'guide') + nav(lang, c, 'guide') + f'''
<main id="main"><header class="guide-hero"><p class="kicker">{h(c['nav'][2])}</p><h1>{h(c['guide_heading'])}</h1><p class="lede">{h(c['guide_intro'])}</p></header>
<div class="guide-layout"><aside class="guide-toc" aria-label="{h(c['nav'][2])}">{toc}</aside><div class="guide-articles">{articles}<section id="pricing"><h2>{h(c['pricing_title'])}</h2><p>{h(c['pricing_intro'])}</p><p>{h(c['tiers'][1][2])}</p><p>{h(c['trial_note'])}</p></section><section id="faq"><h2>{h(c['faq_title'])}</h2>{faq(c)}</section></div></div></main>
''' + footer(lang, c, 'guide')


def update_press(lang, c):
    path = ROOT / route(lang, 'press') / 'index.html'
    text = path.read_text()
    # Keep founder biography, downloads, contacts and brand assets intact.
    paragraphs = [c['press_one'], c['press_short'], *c['press_long']]
    about = re.search(r'(<section id="about">)(.*?)(</section>)', text, re.S)
    body = about[2]
    iterator = iter(paragraphs)
    body = re.sub(r'<p>(.*?)</p>', lambda m: '<p>' + h(next(iterator)) + '</p>', body, flags=re.S)
    text = text[:about.start(2)] + body + text[about.end(2):]
    # Retire old planning / automatic-adjustment screenshots, including alt text.
    for name in ['plan', 'coaching', 'recovery', 'insights']:
        text = re.sub(r'\s*<figure[^>]*>\s*<img[^>]*src="[^"]*/' + name + r'\.png".*?</figure>', '', text, flags=re.S)
    text = re.sub(r'(<section id="screenshots">\s*<h2>.*?</h2>\s*<p class="lede">).*?(</p>)', lambda m: m[1] + h(c['screens_note']) + m[2], text, flags=re.S)
    # One description shared with the homepage instead of a second marketing promise.
    for key in ['description', 'og:description']:
        text = re.sub(r'(<meta (?:name|property)="' + key + r'" content=")[^"]*', lambda m: m[1] + h(c['press_one']), text)
    text = re.sub(r'(<meta property="og:image" content=")[^"]*', lambda m: m[1] + f'{BASE}/assets/social/{lang}.png', text)
    # Replace the old purchase-only facts value, not the optional long-form copy.
    text = re.sub(r'(<div><dt>[^<]+</dt><dd>)(?:One.time purchase, no subscription|一次买断，无订阅|一次買斷，無訂閱|買い切り、サブスクリプションなし|한 번 구매, 구독 없음)(</dd></div>)', lambda m: m[1] + h(c['pricing_intro']) + m[2], text)
    if 'assets/refresh.css' not in text:
        text = text.replace('</head>', f'<link rel="stylesheet" href="{rel(route(lang, "press"), "assets")}refresh.css">\n</head>')
    if '<main' not in text:
        text = text.replace('  <header class="hero presshero">', '  <main id="main">\n  <header class="hero presshero">')
        text = text.replace('  <footer>', '  </main>\n  <footer>')
        text = text.replace('<body>', f'<body>\n<a class="skip-link" href="#main">{h(c["skip"])}</a>')
    text = re.sub(r'(<button class="iconbtn menubtn")', lambda m: m[1] + f' data-close-label="{h(c["close"])}"', text) if 'data-close-label' not in text else text
    # Add same-kind language alternatives to the press page.
    if 'hreflang=' not in text:
        alternatives = '\n'.join(f'<link rel="alternate" hreflang="{code}" href="{BASE}/{route(code, "press")}">' for code in LANGS)
        text = text.replace('</head>', alternatives + f'\n<link rel="alternate" hreflang="x-default" href="{BASE}/press/">\n</head>')
    path.write_text(text)


def main():
    for lang in LANGS:
        c = json.loads((ROOT / 'content' / f'{lang}.json').read_text())
        for kind, render in [('home', homepage), ('guide', guide)]:
            path = ROOT / route(lang, kind) / 'index.html'
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(render(lang, c))
        update_press(lang, c)
    urls = [BASE + '/' + route(lang, kind) for lang in LANGS for kind in ['home', 'guide', 'press']]
    urls += [BASE + '/privacy/'] + [BASE + f'/{lang}/privacy.html' for lang in LANGS if lang != 'en']
    (ROOT / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{url}</loc></url>\n' for url in urls) + '</urlset>\n')
    (ROOT / 'robots.txt').write_text(f'User-agent: *\nAllow: /\nDisallow: /threads-auth/\nDisallow: /_devframe.html\nSitemap: {BASE}/sitemap.xml\n')
    print('Built 5 homepages, 5 guides; updated 5 press kits, sitemap and robots.txt.')


if __name__ == '__main__':
    main()
