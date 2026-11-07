/* Render localized, text-only social cards without fabricated app screens. */
const fs = require('node:fs/promises');
const path = require('node:path');
const escape = value => value.replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('"', '&quot;');
module.exports = async function renderSocial(browser) {
  const root = path.resolve(__dirname, '..');
  const page = await browser.newPage({ viewport: { width: 1200, height: 630 }, deviceScaleFactor: 1 });
  const icon = (await fs.readFile(path.join(root, 'icon.png'))).toString('base64');
  await fs.mkdir(path.join(root, 'assets/social'), { recursive: true });
  for (const lang of ['en', 'zh-Hant', 'zh-Hans', 'ja', 'ko']) {
    const c = JSON.parse(await fs.readFile(path.join(root, 'content', lang + '.json'), 'utf8'));
    await page.setContent(`<!doctype html><html lang="${lang}"><meta charset="utf-8"><style>
      *{box-sizing:border-box}body{margin:0;width:1200px;height:630px;background:#05060c;color:#f4f6fa;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;padding:58px 70px;background-image:radial-gradient(ellipse at 80% 10%,#002a38,transparent 70%)}
      .brand{display:flex;align-items:center;gap:16px;font-size:26px;font-weight:700}.brand img{width:52px;height:52px;border-radius:13px}h1{font-size:62px;line-height:1.3;letter-spacing:-.025em;margin:54px 0 32px;max-width:1050px}em{font-style:normal;color:#00bef0}.note{font-size:20px;color:#b0b8c6;line-height:1.7}.rule{height:1px;background:#26303c;margin-top:40px}.url{margin-top:22px;font-size:18px;color:#929baa}
      </style><div class="brand"><img src="data:image/png;base64,${icon}" alt="">RunCraft</div><h1>${escape(c.hero[0])}<br><em>${escape(c.hero[1])}</em></h1><div class="note">${escape(c.badge)}</div><div class="rule"></div><div class="url">runcraft.marstudio.app</div></html>`);
    await page.screenshot({ path: path.join(root, 'assets/social', lang + '.png') });
  }
  await page.close();
  return 'Rendered 5 localized social cards (1200 × 630).';
};
