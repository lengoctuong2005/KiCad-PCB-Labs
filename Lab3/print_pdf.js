const puppeteer = require('puppeteer');
const path = require('path');

(async () => {
  const browser = await puppeteer.launch({ args: ['--no-sandbox', '--disable-setuid-sandbox'] });
  const page = await browser.newPage();
  const fileUrl = 'file://' + path.resolve('./BaoCao_Lab03.html');
  await page.goto(fileUrl, { waitUntil: 'networkidle0' });
  await page.pdf({ path: './BaoCao_Lab03_KiCad.pdf', format: 'A4', printBackground: true, margin: { top: '0', bottom: '0', left: '0', right: '0' } });
  await browser.close();
})();
