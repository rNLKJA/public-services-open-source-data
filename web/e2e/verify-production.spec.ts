import { test, expect, type Page } from '@playwright/test';

const BASE_URL = 'https://sa-au-open-data.vercel.app';
const ROUTES = [
  '/',
  '/about',
  '/ai-log',
  '/analyses',
  '/catalogue',
  '/methods',
  '/provenance',
  '/quality',
];

const DESKTOP_VIEWPORT = { width: 1440, height: 900 };
const MOBILE_VIEWPORT = { width: 390, height: 844 };

test.describe('Production Verification - Desktop', () => {
  test.use({ viewport: DESKTOP_VIEWPORT });

  for (const route of ROUTES) {
    test(`${route} loads without errors on desktop`, async ({ page }) => {
      const consoleErrors: string[] = [];
      const failedRequests: string[] = [];

      page.on('console', (msg) => {
        if (msg.type() === 'error') {
          consoleErrors.push(msg.text());
        }
      });

      page.on('requestfailed', (request) => {
        failedRequests.push(`${request.method()} ${request.url()} - ${request.failure()?.errorText}`);
      });

      await page.goto(`${BASE_URL}${route}`, { waitUntil: 'networkidle' });

      // Take screenshot
      await page.screenshot({
        path: `/tmp/screenshots/desktop${route.replace(/\//g, '_') || '_home'}.png`,
        fullPage: true
      });

      // Check for errors
      if (consoleErrors.length > 0) {
        console.log(`Console errors on ${route}:`, consoleErrors);
      }
      if (failedRequests.length > 0) {
        console.log(`Failed requests on ${route}:`, failedRequests);
      }

      expect(consoleErrors.length).toBe(0);
      expect(failedRequests.length).toBe(0);
    });
  }
});

test.describe('Production Verification - Mobile', () => {
  test.use({ viewport: MOBILE_VIEWPORT });

  for (const route of ROUTES) {
    test(`${route} loads without errors on mobile`, async ({ page }) => {
      const consoleErrors: string[] = [];
      const failedRequests: string[] = [];

      page.on('console', (msg) => {
        if (msg.type() === 'error') {
          consoleErrors.push(msg.text());
        }
      });

      page.on('requestfailed', (request) => {
        failedRequests.push(`${request.method()} ${request.url()} - ${request.failure()?.errorText}`);
      });

      await page.goto(`${BASE_URL}${route}`, { waitUntil: 'networkidle' });

      // Take screenshot
      await page.screenshot({
        path: `/tmp/screenshots/mobile${route.replace(/\//g, '_') || '_home'}.png`,
        fullPage: true
      });

      // Check for errors
      if (consoleErrors.length > 0) {
        console.log(`Console errors on ${route}:`, consoleErrors);
      }
      if (failedRequests.length > 0) {
        console.log(`Failed requests on ${route}:`, failedRequests);
      }

      expect(consoleErrors.length).toBe(0);
      expect(failedRequests.length).toBe(0);
    });
  }
});

test.describe('Primary Interactions', () => {
  test('AI features show BYOK prompt without key', async ({ page }) => {
    await page.goto(`${BASE_URL}/analyses`, { waitUntil: 'networkidle' });

    // Look for AI-related buttons or interactions
    const aiButtons = await page.locator('button:has-text("AI"), button:has-text("Generate"), [data-ai]').count();

    if (aiButtons > 0) {
      // Click first AI button
      await page.locator('button:has-text("AI"), button:has-text("Generate"), [data-ai]').first().click();

      // Should see BYOK prompt
      await expect(page.locator('text=/API key|settings|configure|bring.*key/i').first()).toBeVisible({ timeout: 5000 });
    }

    await page.screenshot({ path: '/tmp/screenshots/ai-byok-check.png' });
  });

  test('Navigation works', async ({ page }) => {
    await page.goto(BASE_URL, { waitUntil: 'networkidle' });

    // Click on About link if visible
    const aboutLink = page.locator('a[href="/about"], nav a:has-text("About")');
    if (await aboutLink.count() > 0) {
      await aboutLink.first().click();
      await page.waitForURL(`${BASE_URL}/about`);
      expect(page.url()).toBe(`${BASE_URL}/about`);
    }

    await page.screenshot({ path: '/tmp/screenshots/navigation-check.png' });
  });

  test('Dark mode toggle works', async ({ page }) => {
    await page.goto(BASE_URL, { waitUntil: 'networkidle' });

    // Look for theme toggle button
    const themeButton = page.locator('button[aria-label*="theme" i], button:has-text("Dark"), button:has-text("Light"), [data-theme-toggle]');

    if (await themeButton.count() > 0) {
      // Get initial class
      const htmlClasses = await page.locator('html').getAttribute('class');

      // Toggle theme
      await themeButton.first().click();
      await page.waitForTimeout(500);

      // Check class changed
      const newHtmlClasses = await page.locator('html').getAttribute('class');
      expect(htmlClasses).not.toBe(newHtmlClasses);

      await page.screenshot({ path: '/tmp/screenshots/theme-toggle.png' });
    }
  });
});
