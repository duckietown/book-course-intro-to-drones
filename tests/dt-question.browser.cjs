// Requires Playwright (development only). Pass the URL of the built demo page.
const { chromium } = require('playwright');
const assert = require('node:assert/strict');

(async () => {
  const browser = await chromium.launch({ headless: true });
  try {
    const context = await browser.newContext({ viewport: { width: 1100, height: 1000 } });
    // The shared book theme includes external services. Keep this local test offline.
    await context.route('**/*', route => {
      const url = new URL(route.request().url());
      return ['localhost', '127.0.0.1'].includes(url.hostname) ? route.continue() : route.abort();
    });
    const page = await context.newPage();
    await page.goto(process.argv[2]);
    const questions = page.locator('fieldset.dt-question');
    await questions.first().locator('button').waitFor({ state: 'visible' });
    assert.equal(await questions.count(), 3);
    const first = questions.nth(0);
    const status = first.locator('[role="status"]');
    await first.locator('button').click();
    assert.match(await status.textContent(), /Choose an answer/);
    assert.equal(await first.locator('input').first().evaluate(el => el === document.activeElement), true);
    await page.keyboard.press('Space');
    await first.locator('button').click();
    assert.match(await status.textContent(), /^Incorrect\./);
    await first.locator('input').first().focus();
    await page.keyboard.press('ArrowDown');
    assert.equal(await status.textContent(), '');
    await first.locator('button').click();
    assert.match(await status.textContent(), /^Correct\./);
    assert.equal(await questions.nth(1).locator('[role="status"]').textContent(), '');
    await questions.nth(1).locator('input[value="a"]').check();
    await questions.nth(1).locator('button').click();
    assert.match(await questions.nth(1).locator('[role="status"]').textContent(), /^Correct\./);
    await questions.nth(2).locator('input[value="c"]').check();
    await questions.nth(2).locator('button').click();
    assert.match(await questions.nth(2).locator('[role="status"]').textContent(), /^Correct\./);
    assert.equal(await page.evaluate(() => localStorage.length + sessionStorage.length), 0);
    if (process.env.SCREENSHOT) await page.screenshot({ path: process.env.SCREENSHOT, fullPage: true });
    await page.reload();
    await first.locator('button').waitFor({ state: 'visible' });
    assert.equal(await page.locator('.dt-question input:checked').count(), 0);
    assert.equal(await status.textContent(), '');
    await page.setViewportSize({ width: 375, height: 812 });
    assert.equal(await first.evaluate(el => el.getBoundingClientRect().right <= innerWidth), true);

    const noJS = await browser.newContext({ javaScriptEnabled: false });
    await noJS.route('**/*', route => {
      const url = new URL(route.request().url());
      return ['localhost', '127.0.0.1'].includes(url.hostname) ? route.continue() : route.abort();
    });
    const readable = await noJS.newPage();
    await readable.goto(process.argv[2]);
    assert.equal(await readable.locator('fieldset.dt-question').count(), 3);
    assert.equal(await readable.locator('.dt-question input:disabled').count(), 9);
    assert.equal(await readable.locator('.dt-question button').first().isVisible(), false);
    await readable.locator('.dt-question summary').first().click();
    assert.equal(await readable.locator('.dt-question details p').first().isVisible(), true);
    assert.match(await readable.locator('.dt-question details p').first().textContent(), /Correct answer: \(b\)/);
    console.log('PASS: keyboard, empty selection, wrong/correct feedback, retries, independent groups, fresh reload, mobile width, no storage, no-JS fallback.');
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
