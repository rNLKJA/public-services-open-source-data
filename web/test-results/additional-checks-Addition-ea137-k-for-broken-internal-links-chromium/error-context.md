# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: additional-checks.spec.ts >> Additional regression checks >> Check for broken internal links
- Location: e2e/additional-checks.spec.ts:6:7

# Error details

```
Test timeout of 30000ms exceeded.
```

```
Error: locator.getAttribute: Test timeout of 30000ms exceeded.
Call log:
  - waiting for locator('a[href^="/"]').nth(8)

```

# Page snapshot

```yaml
- generic [active] [ref=f8e1]:
  - banner [ref=f8e2]:
    - generic [ref=f8e4]:
      - link "SA & AU Open Data Atlas" [ref=f8e10] [cursor=pointer]:
        - /url: /
      - navigation [ref=f8e11]:
        - link "Catalogue" [ref=f8e12] [cursor=pointer]:
          - /url: /catalogue
        - link "Quality" [ref=f8e13] [cursor=pointer]:
          - /url: /quality
        - link "Analyses" [ref=f8e14] [cursor=pointer]:
          - /url: /analyses
        - link "Methods" [ref=f8e15] [cursor=pointer]:
          - /url: /methods
        - link "About" [ref=f8e16] [cursor=pointer]:
          - /url: /about
        - button "Toggle theme" [ref=f8e17]
  - main [ref=f8e20]:
    - generic [ref=f8e22]:
      - heading "About This Project" [level=1] [ref=f8e23]
      - generic [ref=f8e24]:
        - generic [ref=f8e25]:
          - heading "What This Is" [level=2] [ref=f8e26]
          - paragraph [ref=f8e27]: The SA & AU Open Data Atlas is a curated collection of 95+ open South Australian and Australian government datasets for public-service research, policy analysis and civic tools. Every dataset in the catalogue traces back to an official government source with licence, retrieval date and field definitions documented.
          - paragraph [ref=f8e28]:
            - text: This is a
            - strong [ref=f8e29]: personal data curation project
            - text: started in July 2024. The contribution here is documentation, provenance tracking and metadata quality — not original statistical analysis or research findings.
        - generic [ref=f8e30]:
          - heading "What You'll Find" [level=2] [ref=f8e31]
          - generic [ref=f8e32]:
            - generic [ref=f8e39]:
              - heading "95+ Datasets" [level=3] [ref=f8e40]
              - paragraph [ref=f8e41]: Spanning education, health, justice, infrastructure, environment, social services, planning, economy, demographics and governance
            - generic [ref=f8e47]:
              - heading "Complete Documentation" [level=3] [ref=f8e48]
              - paragraph [ref=f8e49]: Every dataset includes source URL, licence, retrieval date, field definitions, coverage period and known issues
            - generic [ref=f8e54]:
              - heading "Traced Provenance" [level=3] [ref=f8e55]
              - paragraph [ref=f8e56]: PROVENANCE.md files document data lineage from original government publication to processed files
            - generic [ref=f8e62]:
              - heading "Open Licences" [level=3] [ref=f8e63]
              - paragraph [ref=f8e64]: Predominantly CC BY 4.0 from ABS, SA Government agencies, Productivity Commission and AIHW
        - generic [ref=f8e65]:
          - heading "Data Sources" [level=2] [ref=f8e66]
          - paragraph [ref=f8e67]: "All datasets are aggregate or de-identified public releases from official sources:"
          - list [ref=f8e68]:
            - listitem [ref=f8e69]: Australian Bureau of Statistics (ABS)
            - listitem [ref=f8e70]: SA Government agencies (CBS, DIT, DEW, SA Health, SA Police, EPA, PIRSA)
            - listitem [ref=f8e71]: Productivity Commission
            - listitem [ref=f8e72]: Australian Institute of Health and Welfare (AIHW)
            - listitem [ref=f8e73]: Federal agencies and statutory bodies
        - generic [ref=f8e74]:
          - heading "Civic Purpose" [level=2] [ref=f8e75]
          - paragraph [ref=f8e76]: This catalogue supports transparency, evidence-based policy and civic participation. Open government data enables researchers, journalists, community organisations and citizens to understand public services, track outcomes and build tools that serve the public interest. By documenting and linking these datasets, this project lowers the barrier to working with Australian public data.
        - generic [ref=f8e77]:
          - heading "Technical Stack" [level=2] [ref=f8e78]
          - generic [ref=f8e80]:
            - generic [ref=f8e81]:
              - heading "Original Catalogue" [level=3] [ref=f8e82]
              - list [ref=f8e83]:
                - listitem [ref=f8e84]: CSV, Excel, GeoJSON
                - listitem [ref=f8e85]: Python data processing
                - listitem [ref=f8e86]: Markdown documentation
            - generic [ref=f8e87]:
              - heading "Web Application" [level=3] [ref=f8e88]
              - list [ref=f8e89]:
                - listitem [ref=f8e90]: Next.js 16 (App Router)
                - listitem [ref=f8e91]: TypeScript, React 19
                - listitem [ref=f8e92]: Tailwind CSS v4
                - listitem [ref=f8e93]: Deployed on Vercel
        - generic [ref=f8e94]:
          - heading "Licences" [level=2] [ref=f8e95]
          - paragraph [ref=f8e96]:
            - strong [ref=f8e97]: "Catalogue metadata:"
            - text: CC0 1.0 Universal — the documentation, curation and metadata are dedicated to the public domain.
          - paragraph [ref=f8e98]:
            - strong [ref=f8e99]: "Datasets:"
            - text: Each dataset retains its original government licence (predominantly CC BY 4.0 or Crown Copyright with reuse permissions). See individual dataset README files for specific licence terms and attribution requirements.
        - generic [ref=f8e100]:
          - heading "Repository" [level=2] [ref=f8e101]
          - paragraph [ref=f8e102]: "The full catalogue, including raw data files, documentation and this web application, is available on GitHub:"
          - link "View on GitHub" [ref=f8e103] [cursor=pointer]:
            - /url: https://github.com/rNLKJA/public-services-open-source-data
        - generic [ref=f8e107]:
          - heading "Contact" [level=2] [ref=f8e108]
          - paragraph [ref=f8e109]:
            - text: This project is maintained by
            - link "Sunchuangyu \"Rin\" Huang" [ref=f8e110] [cursor=pointer]:
              - /url: https://github.com/rNLKJA
            - text: . For questions about the catalogue or to suggest datasets, please open an issue on the GitHub repository.
  - contentinfo [ref=f8e111]:
    - generic [ref=f8e112]:
      - generic [ref=f8e113]:
        - generic [ref=f8e114]:
          - heading "SA & AU Open Data Atlas" [level=3] [ref=f8e115]
          - paragraph [ref=f8e116]: A curated collection of South Australian and Australian government datasets for research and civic tools.
        - generic [ref=f8e117]:
          - heading "Resources" [level=3] [ref=f8e118]
          - list [ref=f8e119]:
            - listitem [ref=f8e120]:
              - link "Browse Catalogue" [ref=f8e121] [cursor=pointer]:
                - /url: /catalogue
            - listitem [ref=f8e122]:
              - link "About This Project" [ref=f8e123] [cursor=pointer]:
                - /url: /about
        - generic [ref=f8e124]:
          - heading "Connect" [level=3] [ref=f8e125]
          - link "View on GitHub" [ref=f8e126] [cursor=pointer]:
            - /url: https://github.com/rNLKJA/public-services-open-source-data
      - paragraph [ref=f8e130]: "Catalogue metadata: CC0 1.0. Datasets retain their original government licences (CC BY 4.0 or Crown Copyright). Built 2024."
  - alert [ref=f8e131]
```

# Test source

```ts
  1   | import { test, expect } from '@playwright/test';
  2   | 
  3   | const BASE_URL = 'http://localhost:3717';
  4   | 
  5   | test.describe('Additional regression checks', () => {
  6   |   test('Check for broken internal links', async ({ page }) => {
  7   |     const errors: string[] = [];
  8   | 
  9   |     await page.goto(BASE_URL);
  10  | 
  11  |     // Get all internal links
  12  |     const links = await page.locator('a[href^="/"]').all();
  13  | 
  14  |     for (const link of links) {
> 15  |       const href = await link.getAttribute('href');
      |                               ^ Error: locator.getAttribute: Test timeout of 30000ms exceeded.
  16  |       if (href && !href.includes('#')) {
  17  |         const response = await page.goto(BASE_URL + href);
  18  |         if (response && response.status() !== 200) {
  19  |           errors.push(`${href} returned ${response.status()}`);
  20  |         }
  21  |       }
  22  |     }
  23  | 
  24  |     expect(errors).toEqual([]);
  25  |   });
  26  | 
  27  |   test('Check analyses page renders without API key', async ({ page }) => {
  28  |     await page.goto(`${BASE_URL}/analyses`);
  29  | 
  30  |     // Should show analyses content
  31  |     const analyses = await page.locator('h2, h3').allTextContents();
  32  |     expect(analyses.length).toBeGreaterThan(0);
  33  | 
  34  |     // Should not show any error about missing API key
  35  |     const bodyText = await page.textContent('body');
  36  |     expect(bodyText).not.toMatch(/API key required|Please provide.*key/i);
  37  |   });
  38  | 
  39  |   test('Check for missing alt text on images', async ({ page }) => {
  40  |     const routes = ['/', '/about', '/catalogue', '/methods', '/quality', '/provenance', '/analyses'];
  41  |     const imagesWithoutAlt: string[] = [];
  42  | 
  43  |     for (const route of routes) {
  44  |       await page.goto(BASE_URL + route);
  45  |       const images = await page.locator('img').all();
  46  | 
  47  |       for (const img of images) {
  48  |         const alt = await img.getAttribute('alt');
  49  |         const src = await img.getAttribute('src');
  50  |         if (alt === null || alt === '') {
  51  |           imagesWithoutAlt.push(`${route}: ${src}`);
  52  |         }
  53  |       }
  54  |     }
  55  | 
  56  |     if (imagesWithoutAlt.length > 0) {
  57  |       console.log('Images without alt text:', imagesWithoutAlt);
  58  |     }
  59  |   });
  60  | 
  61  |   test('Check statistical content has confidence intervals', async ({ page }) => {
  62  |     await page.goto(`${BASE_URL}/analyses`);
  63  | 
  64  |     const bodyText = await page.textContent('body');
  65  | 
  66  |     // Should mention confidence intervals or CI
  67  |     expect(bodyText).toMatch(/confidence interval|95%.*CI|\[.*,.*\]/i);
  68  |   });
  69  | 
  70  |   test('Verify dark mode contrast', async ({ page }) => {
  71  |     await page.goto(BASE_URL);
  72  | 
  73  |     // Enable dark mode
  74  |     await page.evaluate(() => {
  75  |       document.documentElement.classList.add('dark');
  76  |     });
  77  | 
  78  |     await page.waitForTimeout(300);
  79  | 
  80  |     // Check that text is visible (basic contrast check)
  81  |     const h1 = page.locator('h1').first();
  82  |     const color = await h1.evaluate((el) => {
  83  |       return window.getComputedStyle(el).color;
  84  |     });
  85  | 
  86  |     const bgColor = await page.locator('body').evaluate((el) => {
  87  |       return window.getComputedStyle(el).backgroundColor;
  88  |     });
  89  | 
  90  |     // Both should be defined
  91  |     expect(color).toBeTruthy();
  92  |     expect(bgColor).toBeTruthy();
  93  |   });
  94  | 
  95  |   test('Check mobile viewport has no horizontal scroll', async ({ page }) => {
  96  |     await page.setViewportSize({ width: 375, height: 667 });
  97  | 
  98  |     const routes = ['/', '/methods', '/analyses', '/quality', '/provenance'];
  99  | 
  100 |     for (const route of routes) {
  101 |       await page.goto(BASE_URL + route);
  102 | 
  103 |       const hasHorizontalScroll = await page.evaluate(() => {
  104 |         return document.documentElement.scrollWidth > document.documentElement.clientWidth;
  105 |       });
  106 | 
  107 |       expect(hasHorizontalScroll).toBe(false);
  108 |     }
  109 |   });
  110 | 
  111 |   test('Statistical library integration', async ({ page }) => {
  112 |     // Check that analyses use the statistical library
  113 |     await page.goto(`${BASE_URL}/analyses`);
  114 | 
  115 |     const bodyText = await page.textContent('body');
```