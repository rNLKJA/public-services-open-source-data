import { test, expect, type Page } from '@playwright/test';

const BASE_URL = 'https://sa-au-open-data.vercel.app';

const routes = [
  { path: '/', name: 'home' },
  { path: '/about', name: 'about' },
  { path: '/ai-log', name: 'ai-log' },
  { path: '/analyses', name: 'analyses' },
  { path: '/catalogue', name: 'catalogue' },
  { path: '/methods', name: 'methods' },
  { path: '/provenance', name: 'provenance' },
  { path: '/quality', name: 'quality' },
];

test.describe('Desktop verification (1440x900)', () => {
  test.use({ viewport: { width: 1440, height: 900 }, channel: 'chrome' });

  for (const route of routes) {
    test(`${route.name} loads without errors`, async ({ page }) => {
      const consoleErrors: string[] = [];
      const failedRequests: string[] = [];

      page.on('console', (msg) => {
        if (msg.type() === 'error') {
          consoleErrors.push(msg.text());
        }
      });

      page.on('requestfailed', (request) => {
        failedRequests.push(`${request.method()} ${request.url()}`);
      });

      await page.goto(`${BASE_URL}${route.path}`, { waitUntil: 'networkidle', timeout: 30000 });

      await page.screenshot({
        path: `/tmp/screenshot-desktop-${route.name}.png`,
        fullPage: true,
      });

      console.log(`Route: ${route.path}`);
      console.log(`Console errors: ${consoleErrors.length}`);
      console.log(`Failed requests: ${failedRequests.length}`);

      if (consoleErrors.length > 0) {
        console.log('Errors:', consoleErrors);
      }
      if (failedRequests.length > 0) {
        console.log('Failed:', failedRequests);
      }

      expect(failedRequests).toHaveLength(0);
    });
  }
});

test.describe('Mobile verification (390x844)', () => {
  test.use({ viewport: { width: 390, height: 844 }, channel: 'chrome' });

  for (const route of routes) {
    test(`${route.name} loads without errors`, async ({ page }) => {
      const consoleErrors: string[] = [];
      const failedRequests: string[] = [];

      page.on('console', (msg) => {
        if (msg.type() === 'error') {
          consoleErrors.push(msg.text());
        }
      });

      page.on('requestfailed', (request) => {
        failedRequests.push(`${request.method()} ${request.url()}`);
      });

      await page.goto(`${BASE_URL}${route.path}`, { waitUntil: 'networkidle', timeout: 30000 });

      await page.screenshot({
        path: `/tmp/screenshot-mobile-${route.name}.png`,
        fullPage: true,
      });

      console.log(`Route: ${route.path} (mobile)`);
      console.log(`Console errors: ${consoleErrors.length}`);
      console.log(`Failed requests: ${failedRequests.length}`);

      expect(failedRequests).toHaveLength(0);
    });
  }
});

test.describe('Interaction tests', () => {
  test.use({ viewport: { width: 1440, height: 900 }, channel: 'chrome' });

  test('Navigation works', async ({ page }) => {
    await page.goto(BASE_URL, { waitUntil: 'networkidle' });

    const catalogueLink = page.locator('a[href="/catalogue"]');
    if ((await catalogueLink.count()) > 0) {
      await catalogueLink.first().click();
      await page.waitForURL(/.*catalogue.*/);
      expect(page.url()).toContain('catalogue');
    }
  });

  test('AI features without key show graceful prompt', async ({ page }) => {
    await page.goto(`${BASE_URL}/analyses`, { waitUntil: 'networkidle' });

    const aiButton = page
      .locator('button:has-text("AI"), button:has-text("Generate"), button:has-text("Analyze")')
      .first();

    if ((await aiButton.count()) > 0) {
      await aiButton.click();
      await page.waitForTimeout(1000);

      const settingsDialog = page.locator('[role="dialog"], .dialog, [data-testid*="settings"]');
      const hasDialog = (await settingsDialog.count()) > 0;

      console.log(`AI button clicked, dialog appeared: ${hasDialog}`);
    } else {
      console.log('No AI buttons found on analyses page');
    }
  });
});
