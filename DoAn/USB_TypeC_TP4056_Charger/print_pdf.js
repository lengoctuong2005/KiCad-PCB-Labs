const path = require('path');
const puppeteer = require('../../Lab5/node_modules/puppeteer');

const fs = require('fs');
const CHROME_PATH = [
  process.env.CHROME_PATH,
  '/usr/bin/google-chrome',
  '/usr/bin/google-chrome-stable',
  '/usr/bin/chromium',
  '/usr/bin/chromium-browser'
].find((candidate) => candidate && fs.existsSync(candidate));
const NO_SANDBOX_ARGS = process.env.PUPPETEER_NO_SANDBOX === '1'
  ? ['--no-sandbox', '--disable-setuid-sandbox']
  : [];
const LAUNCH_OPTIONS = Object.assign(
  { args: NO_SANDBOX_ARGS },
  CHROME_PATH ? { executablePath: CHROME_PATH } : {}
);

(async () => {
  try {
    const browser = await puppeteer.launch(LAUNCH_OPTIONS);
    const page = await browser.newPage();
  await page.setJavaScriptEnabled(false);
    const htmlPath = path.resolve(__dirname, 'BaoCao_DoAn.html');
    const fileUrl = 'file:///' + htmlPath.replace(/\\/g, '/');
    console.log('Navigating to:', fileUrl);
    await page.goto(fileUrl, { waitUntil: 'networkidle0' });

    const pdfPath = path.resolve(__dirname, 'BaoCao_DoAn.pdf');
    await page.pdf({
      path: pdfPath,
      format: 'A4',
      printBackground: true,
      margin: { top: '0', bottom: '0', left: '0', right: '0' }
    });
    console.log('PDF exported successfully to:', pdfPath);
    await browser.close();
  } catch (err) {
    console.error('Error generating PDF:', err);
    process.exit(1);
  }
})();
