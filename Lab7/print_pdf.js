const path = require('path');
const puppeteer = require('../Lab5/node_modules/puppeteer');

(async () => {
  try {
    const browser = await puppeteer.launch({
      executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
      args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    const page = await browser.newPage();
    const htmlPath = path.resolve(__dirname, 'BaoCao_Lab06.html');
    const fileUrl = 'file:///' + htmlPath.replace(/\\/g, '/');
    console.log('Navigating to:', fileUrl);
    await page.goto(fileUrl, { waitUntil: 'networkidle0' });
    
    const pdfPath = path.resolve(__dirname, 'BaoCao_Lab06_KiCad.pdf');
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
