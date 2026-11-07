const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch(process.env.CHROME_PATH ? { executablePath: process.env.CHROME_PATH } : {});
  try { console.log(await require('./render_social.cjs')(browser)); }
  finally { await browser.close(); }
})().catch(error => { console.error(error); process.exitCode = 1; });
