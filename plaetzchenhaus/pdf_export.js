// Exportiert die SVGs als A4-PDF (und optional PNG-Vorschau) mit Chromium/Playwright.
// Aufruf: node pdf_export.js [--png]
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

(async () => {
  const png = process.argv.includes('--png');
  const browser = await chromium.launch();
  for (const name of ['plaetzchenhaus-blaupause', 'plaetzchenhaus-druck']) {
    const svg = fs.readFileSync(path.join(__dirname, name + '.svg'), 'utf8');
    const html = `<!doctype html><html><head><meta charset="utf-8"><style>
      @page{size:210mm 297mm;margin:0} html,body{margin:0;padding:0}
      svg{display:block;width:210mm;height:297mm}</style></head><body>${svg.replace(/^<\?xml[^>]*>/, '')}</body></html>`;
    const page = await browser.newPage({ viewport: { width: 794, height: 1123 }, deviceScaleFactor: png ? 2 : 1 });
    await page.setContent(html, { waitUntil: 'load' });
    await page.evaluate(() => document.fonts.ready);
    if (png) {
      await page.screenshot({ path: path.join(process.env.OUT || __dirname, name + '.png'), fullPage: true });
    } else {
      await page.pdf({ path: path.join(__dirname, name + '.pdf'), width: '210mm', height: '297mm',
        printBackground: true, margin: { top: 0, right: 0, bottom: 0, left: 0 }, preferCSSPageSize: true });
    }
    await page.close();
    console.log('fertig:', name, png ? 'png' : 'pdf');
  }
  await browser.close();
})();
