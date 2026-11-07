/* Run against a local static server; never access user browser profiles. */
const assert = require('node:assert/strict');
const fs = require('node:fs/promises');
const path = require('node:path');

module.exports = async function checkBrowser(browser, { base = 'http://127.0.0.1:4187', output = '/tmp/runcraft-web-review', AxeBuilder } = {}) {
  await fs.mkdir(output, { recursive: true });
  const context = await browser.newContext({ locale: 'en-US', reducedMotion: 'reduce' });
  const page = await context.newPage();
  const issues = [], errors = [], results = [];
  page.on('pageerror', error => errors.push(error.message));
  page.on('response', response => { if (response.status() >= 400 && response.url().startsWith(base)) errors.push(`${response.status()} ${response.url()}`); });
  for (const lang of ['en', 'zh-Hant', 'zh-Hans', 'ja', 'ko']) {
    const prefix = lang === 'en' ? '' : lang + '/';
    for (const kind of ['', 'guide/', 'press/']) {
      for (const width of [375, 430, 768, 1440]) {
        await page.setViewportSize({ width, height: 900 });
        const url = `${base}/${prefix}${kind}`;
        const response = await page.goto(url);
        assert.equal(response.status(), 200, url);
        await page.evaluate(async () => {
          // Resolve lazy images before checking or photographing a long page.
          document.querySelectorAll('img').forEach(img => { img.loading = 'eager'; });
          await Promise.all(Array.from(document.images, img => img.decode().catch(() => {})));
          await document.fonts.ready;
        });
        const layout = await page.evaluate(() => ({
          overflow: document.documentElement.scrollWidth > innerWidth,
          broken: [...document.images].filter(img => !img.naturalWidth).map(img => img.src),
          language: document.documentElement.lang,
        }));
        assert.equal(layout.language, lang);
        assert.equal(layout.overflow, false, `${url} overflows at ${width}`);
        assert.deepEqual(layout.broken, [], `Broken images at ${url}`);
        // Full WCAG A/AA checks on both narrow and wide layouts.
        if (width === 375 || width === 1440) {
          const audit = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa']).analyze();
          issues.push(...audit.violations.map(v => ({ lang, kind, width, id: v.id, impact: v.impact, targets: v.nodes.map(n => n.target) })));
        }
        results.push({ lang, kind: kind || 'home', width, status: 'passed' });
        if (lang === 'zh-Hant' && kind === '' && (width === 375 || width === 1440)) {
          await page.screenshot({ path: path.join(output, `zh-Hant-${width}.png`) });
          if (width === 1440) await page.screenshot({ path: path.join(output, 'zh-Hant-full.png'), fullPage: true });
        }
      }
    }
  }

  // Closed mobile navigation is absent from keyboard focus and accessibility.
  for (const lang of ['en', 'zh-Hant', 'zh-Hans', 'ja', 'ko']) {
    const prefix = lang === 'en' ? '' : lang + '/';
    await page.setViewportSize({ width: 390, height: 844 });
    await page.goto(`${base}/${prefix}`);
    const trigger = page.locator('.menubtn');
    const drawer = page.locator('#mobile-navigation');
    assert.equal(await drawer.isVisible(), false);
    await trigger.click();
    assert.equal(await trigger.getAttribute('aria-expanded'), 'true');
    assert.equal(await page.locator('.drawerclose').evaluate(el => el === document.activeElement), true);
    assert.equal(await page.locator('.wrap').evaluate(el => el.inert), true);
    await page.keyboard.press('Shift+Tab');
    assert.equal(await drawer.locator('a').last().evaluate(el => el === document.activeElement), true);
    await page.keyboard.press('Tab');
    assert.equal(await page.locator('.drawerclose').evaluate(el => el === document.activeElement), true);
    await page.keyboard.press('Escape');
    assert.equal(await drawer.isVisible(), false);
    assert.equal(await trigger.evaluate(el => el === document.activeElement), true);
    assert.equal(await page.locator('.wrap').evaluate(el => el.inert), false);
    await trigger.click();
    await drawer.locator('a').first().click();
    assert.equal(await drawer.isVisible(), false);
    assert.equal(await page.evaluate(() => document.activeElement.id), 'method');
    await trigger.click();
    await page.setViewportSize({ width: 1440, height: 900 });
    await page.waitForFunction(() => document.getElementById('mobile-navigation').hidden);
    assert.equal(await page.locator('.brand').evaluate(el => el === document.activeElement), true);
    assert.equal(await drawer.isVisible(), false);
    assert.equal(await page.locator('body').evaluate(el => el.classList.contains('noscroll')), false);
    const globe = page.locator('.langbtn');
    await globe.click();
    await page.keyboard.press('Tab');
    assert.equal(await page.locator('.langmenu a').first().evaluate(el => el === document.activeElement), true);
    await page.keyboard.press('Escape');
    assert.equal(await globe.evaluate(el => el === document.activeElement), true);
    assert.equal(await page.locator('.langmenu').isVisible(), false);
    await page.locator('summary').first().click();
    assert.equal(await page.locator('details').first().getAttribute('open'), '');
    assert.equal(await page.evaluate(() => getComputedStyle(document.documentElement).scrollBehavior), 'auto');
  }

  // Locale switches keep readers on the guide, not the homepage.
  await page.goto(`${base}/zh-Hant/guide/`);
  await page.locator('.langbtn').click();
  await page.locator('.langmenu a[data-lang="ja"]').click();
  await page.waitForURL(`${base}/ja/guide/`);
  assert.equal(await page.evaluate(() => localStorage.getItem('rc-lang')), 'ja');
  await page.goto(base + '/#method');
  await page.waitForURL(`${base}/ja/#method`);
  await page.evaluate(() => localStorage.setItem('rc-lang', 'unsupported-language'));
  await page.goto(base + '/');
  assert.equal(page.url(), base + '/');

  // Reading and FAQ disclosures work with JavaScript disabled.
  const noScript = await browser.newContext({ javaScriptEnabled: false, locale: 'en-US', viewport: { width: 390, height: 844 } });
  const staticPage = await noScript.newPage();
  await staticPage.goto(`${base}/zh-Hant/`);
  assert.equal(await staticPage.locator('h1').count(), 1);
  await staticPage.locator('summary').first().click();
  assert.equal(await staticPage.locator('details').first().getAttribute('open'), '');
  await noScript.close();
  await context.close();
  const report = { layouts: results.length, accessibilityAudits: 30, interactionLocales: 5, issues, errors, results };
  await fs.writeFile(path.join(output, 'report.json'), JSON.stringify(report, null, 2) + '\n');
  assert.deepEqual(errors, [], 'Browser errors or failed local requests');
  assert.deepEqual(issues, [], 'Accessibility violations; see report.json');
  return report;
};

if (require.main === module) {
  (async () => {
    const { chromium } = require('playwright');
    const { default: AxeBuilder } = require('@axe-core/playwright');
    const browser = await chromium.launch(process.env.CHROME_PATH ? { executablePath: process.env.CHROME_PATH } : {});
    try {
      const result = await module.exports(browser, { AxeBuilder, base: process.env.SITE_URL || undefined });
      console.log(`PASS: ${result.layouts} layouts, ${result.accessibilityAudits} accessibility audits, 5-locale navigation, language routes, FAQ and no-JavaScript reading.`);
    } finally { await browser.close(); }
  })().catch(error => { console.error(error); process.exitCode = 1; });
}
