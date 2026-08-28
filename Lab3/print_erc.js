const puppeteer = require('puppeteer');
const path = require('path');

(async () => {
  const browser = await puppeteer.launch({ args: ['--no-sandbox', '--disable-setuid-sandbox'] });
  const page = await browser.newPage();
  await page.setViewport({ width: 800, height: 600 });
  const fileUrl = 'file://' + path.resolve('./erc_terminal.html');
  await page.goto(fileUrl, { waitUntil: 'networkidle0' });
  await page.screenshot({ path: './Pic/erc_cli_output.png' });
  await browser.close();
})();
