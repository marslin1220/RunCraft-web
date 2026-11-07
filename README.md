# RunCraft website

A five-language, static GitHub Pages website for RunCraft. The existing custom
domain, Jekyll privacy-policy route and plain HTML/CSS/JavaScript hosting remain
in place. No frontend framework, backend or tracking service is required.

## Edit and build

Edit the locale files in `content/`, then run:

```sh
python3 scripts/build_site.py
python3 scripts/check_site.py
```

The builder writes five homepages and guides, updates the existing press-kit
boilerplate, and generates `sitemap.xml` and `robots.txt`. Generated HTML is
checked in so normal hosting needs no custom build. The press updater preserves
founder biography, download assets, contact details and privacy-policy text.

- `assets/site.css`: retained brand and press styles.
- `assets/refresh.css`: updated landing/guide layouts and shared accessibility.
- `assets/nav.js`: language disclosure and keyboard-accessible mobile dialog.
- `scripts/check_site.py`: locale completeness, local routes/anchors, metadata,
  retired claims and reproducible generation. English `/privacy/` is produced
  by Jekyll from the existing `privacy.md` permalink.

## Preview and browser validation

```sh
python3 -m http.server 4187 --bind 127.0.0.1
```

Open `http://127.0.0.1:4187/zh-Hant/` or another locale. The English privacy route
needs Jekyll rather than this simple file server; localized policy HTML works
without it.

In a second terminal:

```sh
npm ci
npx playwright install chromium
npm run test:browser
```

The browser check covers all 15 updated routes at 375, 430, 768 and 1440 pixels,
30 axe WCAG A/AA audits, five-locale menu/focus/resize behavior, language routing,
FAQ, reduced motion and reading without JavaScript. Use `CHROME_PATH` to choose
an installed Chrome executable and `SITE_URL` for a different local origin.
Reports and screenshots default to `/tmp/runcraft-web-review`.

## Social cards

```sh
npm run render:social
```

This renders the checked-in localized copy and app icon into five 1200 × 630 PNG
cards. It does not create fictional app screenshots. Cards are checked in; rerun
when the headline, trial terms or visual identity changes.

## Release review

See [the content and release review](docs/content-release-review.md). This change
is prepared for review, not an instruction to merge or publish before the native
release is available. The website and App Store releases are separate actions.
