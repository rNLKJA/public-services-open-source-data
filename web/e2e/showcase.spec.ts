import { test, expect, type Page } from '@playwright/test';

const BASE_URL = process.env.BASE_URL || 'https://sa-au-open-data.vercel.app';
const SHOWCASE_DIR = join(process.cwd(), '..', 'docs', 'showcase');

// Helper to add visible cursor highlight
async function addCursorHighlight(page: Page) {
  await page.evaluate(() => {
    const cursor = document.createElement('div');
    cursor.id = 'showcase-cursor';
    cursor.style.cssText = `
      position: fixed;
      width: 20px;
      height: 20px;
      border: 3px solid #ef4444;
      border-radius: 50%;
      pointer-events: none;
      z-index: 999999;
      transition: all 0.1s ease;
      box-shadow: 0 0 0 2px white, 0 0 10px rgba(239, 68, 68, 0.5);
    `;
    document.body.appendChild(cursor);

    document.addEventListener('mousemove', (e) => {
      cursor.style.left = e.pageX - 10 + 'px';
      cursor.style.top = e.pageY - 10 + 'px';
    });
  });
}

// Helper to add caption overlay
async function addCaption(page: Page, step: number, text: string) {
  await page.evaluate(
    ({ step, text }) => {
      let caption = document.getElementById('showcase-caption') as HTMLDivElement;
      if (!caption) {
        caption = document.createElement('div');
        caption.id = 'showcase-caption';
        caption.style.cssText = `
          position: fixed;
          bottom: 0;
          left: 0;
          right: 0;
          background: rgba(0, 0, 0, 0.85);
          color: white;
          padding: 16px 24px;
          font-family: system-ui, sans-serif;
          font-size: 16px;
          font-weight: 500;
          z-index: 999998;
          box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.3);
        `;
        document.body.appendChild(caption);
      }
      caption.innerHTML = `<span style="color: #60a5fa; font-weight: 600;">Step ${step}:</span> ${text}`;
    },
    { step, text }
  );
}

// Helper to wait with human pacing
async function humanWait(page: Page, ms = 1500) {
  await page.waitForTimeout(ms);
}

test.describe('Showcase: Key Feature Screenshots', () => {
  test.use({ viewport: { width: 1440, height: 900 } });

  test('01 - Landing page (light mode)', async ({ page }) => {
    await page.goto(BASE_URL, { waitUntil: 'networkidle' });

    // Ensure light mode
    await page.evaluate(() => {
      document.documentElement.classList.remove('dark');
    });
    await page.waitForTimeout(500);

    await page.screenshot({
      path: join(SHOWCASE_DIR, '01-landing-light.png'),
      fullPage: false,
    });
  });

  test('02 - Landing page (dark mode)', async ({ page }) => {
    await page.goto(BASE_URL, { waitUntil: 'networkidle' });

    // Ensure dark mode
    await page.evaluate(() => {
      document.documentElement.classList.add('dark');
    });
    await page.waitForTimeout(500);

    await page.screenshot({
      path: join(SHOWCASE_DIR, '02-landing-dark.png'),
      fullPage: false,
    });
  });

  test('03 - Catalogue browser', async ({ page }) => {
    await page.goto(`${BASE_URL}/catalogue`, { waitUntil: 'networkidle' });
    await page.waitForTimeout(1000);

    await page.screenshot({
      path: join(SHOWCASE_DIR, '03-catalogue.png'),
      fullPage: false,
    });
  });

  test('04 - Analysis gallery', async ({ page }) => {
    await page.goto(`${BASE_URL}/analyses`, { waitUntil: 'networkidle' });
    await page.waitForTimeout(1000);

    await page.screenshot({
      path: join(SHOWCASE_DIR, '04-analyses.png'),
      fullPage: false,
    });
  });

  test('05 - Provenance graph', async ({ page }) => {
    await page.goto(`${BASE_URL}/provenance`, { waitUntil: 'networkidle' });
    await page.waitForTimeout(1000);

    await page.screenshot({
      path: join(SHOWCASE_DIR, '05-provenance.png'),
      fullPage: false,
    });
  });

  test('06 - Methods page', async ({ page }) => {
    await page.goto(`${BASE_URL}/methods`, { waitUntil: 'networkidle' });
    await page.waitForTimeout(1000);

    await page.screenshot({
      path: join(SHOWCASE_DIR, '06-methods.png'),
      fullPage: false,
    });
  });

  test('07 - AI audit log', async ({ page }) => {
    await page.goto(`${BASE_URL}/ai-log`, { waitUntil: 'networkidle' });
    await page.waitForTimeout(1000);

    await page.screenshot({
      path: join(SHOWCASE_DIR, '07-ai-log.png'),
      fullPage: false,
    });
  });

  test('08 - Mobile landing', async ({ page }) => {
    await page.setViewportSize({ width: 390, height: 844 });
    await page.goto(BASE_URL, { waitUntil: 'networkidle' });
    await page.waitForTimeout(1000);

    await page.screenshot({
      path: join(SHOWCASE_DIR, '08-mobile-landing.png'),
      fullPage: false,
    });
  });

  test('09 - Mobile catalogue', async ({ page }) => {
    await page.setViewportSize({ width: 390, height: 844 });
    await page.goto(`${BASE_URL}/catalogue`, { waitUntil: 'networkidle' });
    await page.waitForTimeout(1000);

    await page.screenshot({
      path: join(SHOWCASE_DIR, '09-mobile-catalogue.png'),
      fullPage: false,
    });
  });

  test('10 - Mobile analysis', async ({ page }) => {
    await page.setViewportSize({ width: 390, height: 844 });
    await page.goto(`${BASE_URL}/analyses`, { waitUntil: 'networkidle' });
    await page.waitForTimeout(1000);

    await page.screenshot({
      path: join(SHOWCASE_DIR, '10-mobile-analyses.png'),
      fullPage: false,
    });
  });
});

test.describe('Showcase: Workflow Recordings', () => {
  test('Workflow 1: Explore the catalogue', async ({ page }, testInfo) => {
    await page.setViewportSize({ width: 1280, height: 800 });
    await addCursorHighlight(page);
    await page.goto(BASE_URL, { waitUntil: 'networkidle' });
    await humanWait(page, 1000);

    // Step 1: Navigate to catalogue
    await addCaption(page, 1, 'Navigate to the catalogue to explore available datasets');
    await humanWait(page, 1000);

    const catalogueLink = page.locator('a[href="/catalogue"]').first();
    await catalogueLink.hover();
    await humanWait(page, 500);
    await catalogueLink.click();
    await page.waitForURL(`${BASE_URL}/catalogue`);
    await humanWait(page, 1500);

    // Step 2: Browse by domain
    await addCaption(
      page,
      2,
      'Browse datasets by domain - filter by category to find relevant data'
    );
    await humanWait(page, 1000);

    // Scroll to see more content
    await page.mouse.wheel(0, 400);
    await humanWait(page, 1000);

    // Step 3: View dataset details
    await addCaption(
      page,
      3,
      'Select a dataset to view metadata, attribution, and download options'
    );
    await humanWait(page, 1000);

    const firstDataset = page
      .locator('article, [data-dataset], .dataset-card, a[href*="/catalogue/"]')
      .first();
    if ((await firstDataset.count()) > 0) {
      await firstDataset.hover();
      await humanWait(page, 500);
    }

    await humanWait(page, 1500);
    const videoPath = testInfo.outputPath('workflow-1-explore-catalogue.webm');
    await page.video()?.saveAs(videoPath);
  });

  test('Workflow 2: Quickstart gallery', async ({ page, context }, testInfo) => {
    await page.setViewportSize({ width: 1280, height: 800 });
    await context.tracing.start({ screenshots: true, snapshots: true });

    try {
      await addCursorHighlight(page);
      await page.goto(BASE_URL, { waitUntil: 'networkidle' });
      await humanWait(page, 2000);

      // Step 1: Navigate to analyses
      await addCaption(page, 1, 'Visit the analysis gallery showcasing the catalogue breadth');
      await humanWait(page);

      const analysesLink = page.locator('a[href="/analyses"]').first();
      await analysesLink.hover();
      await humanWait(page, 800);
      await analysesLink.click();
      await page.waitForURL(`${BASE_URL}/analyses`);
      await humanWait(page, 2000);

      // Step 2: Scroll through visualizations
      await addCaption(
        page,
        2,
        'Explore 6 hero visualizations: crime map, CPI timeline, crash heatmap, and more'
      );
      await humanWait(page);

      await page.mouse.wheel(0, 400);
      await humanWait(page, 1500);
      await page.mouse.wheel(0, 400);
      await humanWait(page, 1500);

      // Step 3: Interact with a visualization
      await addCaption(
        page,
        3,
        'Interactive visualizations with filtering and drill-down capabilities'
      );
      await humanWait(page);

      const firstViz = page.locator('article, .analysis-card, [data-analysis]').first();
      if ((await firstViz.count()) > 0) {
        await firstViz.hover();
        await humanWait(page, 800);
        await firstViz.click();
        await humanWait(page, 2000);
      }

      // Step 4: View methodology
      await addCaption(page, 4, 'Each analysis includes methodology, assumptions, and limitations');
      await humanWait(page);

      await page.mouse.wheel(0, 400);
      await humanWait(page, 2000);
    } finally {
      await context.tracing.stop();
      const videoPath = testInfo.outputPath('workflow-2-quickstart-gallery.webm');
      await page.video()?.saveAs(videoPath);
    }
  });

  test('Workflow 3: Join datasets', async ({ page, context }, testInfo) => {
    await page.setViewportSize({ width: 1280, height: 800 });
    await context.tracing.start({ screenshots: true, snapshots: true });

    try {
      await addCursorHighlight(page);
      await page.goto(BASE_URL, { waitUntil: 'networkidle' });
      await humanWait(page, 2000);

      // Step 1: Navigate to provenance
      await addCaption(page, 1, 'Explore cross-dataset case studies and data lineage');
      await humanWait(page);

      const provenanceLink = page.locator('a[href="/provenance"]').first();
      await provenanceLink.hover();
      await humanWait(page, 800);
      await provenanceLink.click();
      await page.waitForURL(`${BASE_URL}/provenance`);
      await humanWait(page, 2000);

      // Step 2: View provenance graph
      await addCaption(page, 2, 'Provenance graph shows how datasets are joined and transformed');
      await humanWait(page, 2000);

      await page.mouse.wheel(0, 300);
      await humanWait(page);

      // Step 3: Select case study
      await addCaption(
        page,
        3,
        'View detailed case studies with methodology and statistical rigour'
      );
      await humanWait(page);

      const caseStudy = page.locator('article, .case-study, [data-case-study]').first();
      if ((await caseStudy.count()) > 0) {
        await caseStudy.hover();
        await humanWait(page, 800);
        await caseStudy.click();
        await humanWait(page, 2000);
      }

      // Step 4: Review methodology
      await addCaption(
        page,
        4,
        'Each join includes full methodology, uncertainty quantification, and reproducible code'
      );
      await humanWait(page);

      await page.mouse.wheel(0, 400);
      await humanWait(page, 2000);
    } finally {
      await context.tracing.stop();
      const videoPath = testInfo.outputPath('workflow-3-join-datasets.webm');
      await page.video()?.saveAs(videoPath);
    }
  });
});
