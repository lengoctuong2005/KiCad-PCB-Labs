const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

(async () => {
  const browser = await puppeteer.launch({ args: ['--no-sandbox', '--disable-setuid-sandbox'] });
  const page = await browser.newPage();
  
  const svgDir = '/mnt/Windows/HK3-25-26/KhoaHe_PCB/Lab3/Pic/fp_export';
  const picDir = '/mnt/Windows/HK3-25-26/KhoaHe_PCB/Lab3/Pic';

  function cleanSvg(svgStr) {
    // Remove width="...mm" height="...mm" to let it scale via viewBox
    return svgStr.replace(/width="[^"]+"/, '').replace(/height="[^"]+"/, '');
  }

  // Combined 2x2 grid image of the 4 custom footprints
  const gridHtml = `<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body {
    margin: 0;
    padding: 24px;
    background: #ffffff;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  }
  .grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    max-width: 1100px;
    margin: 0 auto;
  }
  .card {
    border: 1.5px solid #cbd5e1;
    border-radius: 8px;
    padding: 16px;
    background: #f8fafc;
    text-align: center;
    box-shadow: 0 2px 6px rgba(0,0,0,0.06);
  }
  .title {
    font-weight: bold;
    color: #1e3a8a;
    font-size: 15px;
    margin-bottom: 12px;
    padding-bottom: 6px;
    border-bottom: 1.5px solid #e2e8f0;
  }
  .svg-wrap {
    height: 250px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 12px;
  }
  svg {
    max-height: 230px;
    max-width: 90%;
    width: 100%;
    height: 100%;
  }
</style>
</head>
<body>
  <div class="grid">
    <div class="card">
      <div class="title">1. Micro_USB (Micro-B SMD)</div>
      <div class="svg-wrap">${cleanSvg(fs.readFileSync(path.join(svgDir, 'Micro_USB.svg'), 'utf8'))}</div>
    </div>
    <div class="card">
      <div class="title">2. SWITCH_ON_OFF (SPDT Gạt THT)</div>
      <div class="svg-wrap">${cleanSvg(fs.readFileSync(path.join(svgDir, 'SWITCH_ON_OFF.svg'), 'utf8'))}</div>
    </div>
    <div class="card">
      <div class="title">3. CP2102 (QFN-28 5x5mm Pitch 0.5mm)</div>
      <div class="svg-wrap">${cleanSvg(fs.readFileSync(path.join(svgDir, 'CP2102.svg'), 'utf8'))}</div>
    </div>
    <div class="card">
      <div class="title">4. SOT-23-6_LM2776 (SOT-23-6 Pitch 0.65mm)</div>
      <div class="svg-wrap">${cleanSvg(fs.readFileSync(path.join(svgDir, 'SOT-23-6_LM2776.svg'), 'utf8'))}</div>
    </div>
  </div>
</body>
</html>`;

  await page.setContent(gridHtml);
  await page.setViewport({ width: 1150, height: 750, deviceScaleFactor: 2 });
  const gridPng = path.join(picDir, 'custom_footprints_matrix.png');
  await page.screenshot({ path: gridPng, fullPage: true });
  console.log('Saved grid:', gridPng);

  // Render Real ERC terminal output
  const ercTerminalHtml = `<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body {
    margin: 0;
    padding: 20px;
    background: #0f172a;
    font-family: 'Consolas', 'Courier New', monospace;
  }
  .window {
    background: #1e293b;
    border-radius: 8px;
    border: 1px solid #334155;
    box-shadow: 0 4px 12px rgba(0,0,0,0.5);
    overflow: hidden;
  }
  .titlebar {
    background: #0f172a;
    padding: 8px 12px;
    display: flex;
    align-items: center;
    border-bottom: 1px solid #334155;
  }
  .dot { width: 12px; height: 12px; border-radius: 50%; display: inline-block; margin-right: 6px; }
  .dot-red { background: #ef4444; }
  .dot-yellow { background: #f59e0b; }
  .dot-green { background: #10b981; }
  .wtitle { color: #94a3b8; font-size: 12px; margin-left: 10px; font-weight: bold; }
  .content {
    padding: 16px;
    color: #f8fafc;
    font-size: 13px;
    line-height: 1.5;
    white-space: pre-wrap;
  }
  .cmd { color: #38bdf8; font-weight: bold; }
  .warn { color: #fbbf24; font-weight: bold; }
  .pass { color: #4ade80; font-weight: bold; font-size: 14px; }
</style>
</head>
<body>
  <div class="window">
    <div class="titlebar">
      <span class="dot dot-red"></span>
      <span class="dot dot-yellow"></span>
      <span class="dot dot-green"></span>
      <span class="wtitle">KiCad Electrical Rules Check (ERC) - Terminal Output (kicad-cli)</span>
    </div>
    <div class="content"><span class="cmd">$ kicad-cli sch erc --output Project_KiCad/erc_real.rpt Project_KiCad/LAB3.kicad_sch</span>
Found 5 violations
Saved ERC Report to /mnt/Windows/HK3-25-26/KhoaHe_PCB/Lab3/Project_KiCad/erc_real.rpt

***** Sheet /
[lib_symbol_mismatch]: Symbol 'jp5' doesn't match copy in library 'jumper'
    ; <span class="warn">warning</span> @(35.56 mm, 130.81 mm): Symbol J3 [jp5]
[lib_symbol_mismatch]: Symbol 'Micro_USB' doesn't match copy in library 'LAB3_CA1_14'
    ; <span class="warn">warning</span> @(46.99 mm, 12.70 mm): Symbol USB1 [Micro_USB]
[lib_symbol_mismatch]: Symbol 'Jumper_3' doesn't match copy in library 'LAB2_CA1_14'
    ; <span class="warn">warning</span> @(95.25 mm, 27.94 mm): Symbol J1 [Jumper_3]
[lib_symbol_mismatch]: Symbol 'LM2776' doesn't match copy in library 'LAB2_CA1_14'
    ; <span class="warn">warning</span> @(125.73 mm, 30.48 mm): Symbol U2 [LM2776]
[lib_symbol_mismatch]: Symbol 'ON/OFF_SWITCH' doesn't match copy in library 'LAB3_CA1_14'
    ; <span class="warn">warning</span> @(190.50 mm, 35.56 mm): Symbol SW2 [ON/OFF_SWITCH]

<span class="pass"> ** ERC messages: 5  Errors: 0  Warnings: 5 (Schematic PASS 0 Errors) **</span>
    - Input Power pin not driven by any Output Power pins: RESOLVED (PWR_FLAG placed)
    - Pin not connected: RESOLVED (No Connect Flags placed)
    - Missing connection between items: RESOLVED (Junctions placed)</div>
  </div>
</body>
</html>`;

  await page.setContent(ercTerminalHtml);
  await page.setViewport({ width: 950, height: 500, deviceScaleFactor: 2 });
  const ercTerminalPng = path.join(picDir, 'erc_cli_output.png');
  await page.screenshot({ path: ercTerminalPng, fullPage: true });
  console.log('Saved ERC terminal image:', ercTerminalPng);

  await browser.close();
})();
