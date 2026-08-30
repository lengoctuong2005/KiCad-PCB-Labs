const path = require('path');
const puppeteer = require('/mnt/Windows/HK3-25-26/KhoaHe_PCB/Lab3/node_modules/puppeteer');

(async () => {
  const browser = await puppeteer.launch({
    executablePath: '/usr/bin/google-chrome',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  const page = await browser.newPage();
  const fileUrl = 'file://' + path.resolve(__dirname, 'BaoCao_Lab05.html');
  await page.goto(fileUrl, { waitUntil: 'networkidle0' });
  await page.pdf({
    path: path.resolve(__dirname, 'BaoCao_Lab05_KiCad.pdf'),
    format: 'A4',
    printBackground: true,
    margin: { top: '0', bottom: '0', left: '0', right: '0' }
  });
  await browser.close();
})();
