# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: showcase.spec.ts >> Showcase: Workflow Recordings >> Workflow 3: Join datasets
- Location: e2e/showcase.spec.ts:281:7

# Error details

```
Test timeout of 90000ms exceeded.
```

```
Error: tracing.stop: Target page, context or browser has been closed
```

# Page snapshot

```yaml
- generic [active] [ref=e1]:
  - banner [ref=e2]:
    - generic [ref=e4]:
      - link "SA & AU Open Data Atlas" [ref=e10] [cursor=pointer]:
        - /url: /
      - navigation [ref=e11]:
        - link "Catalogue" [ref=e12] [cursor=pointer]:
          - /url: /catalogue
        - link "Quality" [ref=e13] [cursor=pointer]:
          - /url: /quality
        - link "Analyses" [ref=e14] [cursor=pointer]:
          - /url: /analyses
        - link "Methods" [ref=e15] [cursor=pointer]:
          - /url: /methods
        - link "About" [ref=e16] [cursor=pointer]:
          - /url: /about
        - button "Toggle theme" [ref=e17]
  - main [ref=e20]:
    - generic [ref=e21]:
      - generic [ref=e24]:
        - generic [ref=e25]: 95+ Government Datasets
        - heading "SA & AU Open Data Atlas" [level=1] [ref=e30]
        - paragraph [ref=e31]: A curated, sourced collection of South Australian and Australian government datasets for public-service research, policy analysis and civic tools. Every dataset traces back to an official government source with licence, retrieval date and field definitions documented.
        - generic [ref=e32]:
          - link "Browse Catalogue" [ref=e33] [cursor=pointer]:
            - /url: /catalogue
          - link "About This Project" [ref=e36] [cursor=pointer]:
            - /url: /about
      - generic [ref=e38]:
        - heading "Featured Datasets" [level=2] [ref=e39]
        - paragraph [ref=e40]: Explore a selection of high-impact datasets from across the catalogue
        - generic [ref=e41]:
          - generic [ref=e49]:
            - heading "SA Crime Statistics" [level=3] [ref=e50]
            - paragraph [ref=e51]: Recorded crime by suburb, 2010-2026
            - generic [ref=e52]: justice
          - generic [ref=e59]:
            - heading "Adelaide CPI" [level=3] [ref=e60]
            - paragraph [ref=e61]: Consumer Price Index trends
            - generic [ref=e62]: economy
          - generic [ref=e68]:
            - heading "SA Road Crashes" [level=3] [ref=e69]
            - paragraph [ref=e70]: Crash locations and severity, 2020-2024
            - generic [ref=e71]: infrastructure
          - generic [ref=e78]:
            - heading "SA School Locations" [level=3] [ref=e79]
            - paragraph [ref=e80]: Government school and preschool sites
            - generic [ref=e81]: education
          - generic [ref=e89]:
            - heading "ED Wait Times" [level=3] [ref=e90]
            - paragraph [ref=e91]: Emergency department performance
            - generic [ref=e92]: health
          - generic [ref=e98]:
            - heading "Renewable Installations" [level=3] [ref=e99]
            - paragraph [ref=e100]: Rooftop solar and battery installations
            - generic [ref=e101]: environment
      - generic [ref=e103]:
        - heading "What You'll Find" [level=2] [ref=e104]
        - generic [ref=e105]:
          - generic [ref=e106]:
            - heading "Searchable Catalogue" [level=3] [ref=e111]
            - paragraph [ref=e112]: Filter by domain, licence, and temporal coverage to find the datasets you need
          - generic [ref=e113]:
            - heading "Metadata Quality" [level=3] [ref=e117]
            - paragraph [ref=e118]: Every dataset includes source, licence, retrieval date, field definitions and known issues
          - generic [ref=e119]:
            - heading "Diverse Domains" [level=3] [ref=e125]
            - paragraph [ref=e126]: 95+ datasets across health, justice, education, infrastructure, environment and more
          - generic [ref=e127]:
            - heading "Open Access" [level=3] [ref=e132]
            - paragraph [ref=e133]: Predominantly CC BY 4.0 licenced data from official government sources
      - generic [ref=e135]:
        - heading "Data Domains" [level=2] [ref=e136]
        - generic [ref=e137]:
          - link "Health" [ref=e138] [cursor=pointer]:
            - /url: /catalogue?domain=health
          - link "Justice" [ref=e139] [cursor=pointer]:
            - /url: /catalogue?domain=justice
          - link "Education" [ref=e140] [cursor=pointer]:
            - /url: /catalogue?domain=education
          - link "Infrastructure" [ref=e141] [cursor=pointer]:
            - /url: /catalogue?domain=infrastructure
          - link "Environment" [ref=e142] [cursor=pointer]:
            - /url: /catalogue?domain=environment
          - link "Social Services" [ref=e143] [cursor=pointer]:
            - /url: /catalogue?domain=social-services
          - link "Planning" [ref=e144] [cursor=pointer]:
            - /url: /catalogue?domain=planning
          - link "Economy" [ref=e145] [cursor=pointer]:
            - /url: /catalogue?domain=economy
          - link "Demographics" [ref=e146] [cursor=pointer]:
            - /url: /catalogue?domain=demographics
          - link "Governance" [ref=e147] [cursor=pointer]:
            - /url: /catalogue?domain=governance
      - generic [ref=e149]:
        - heading "Start Exploring" [level=2] [ref=e150]
        - paragraph [ref=e151]: Browse the full catalogue to discover open government data for your research, analysis or civic project.
        - link "View All Datasets" [ref=e152] [cursor=pointer]:
          - /url: /catalogue
  - contentinfo [ref=e155]:
    - generic [ref=e156]:
      - generic [ref=e157]:
        - generic [ref=e158]:
          - heading "SA & AU Open Data Atlas" [level=3] [ref=e159]
          - paragraph [ref=e160]: A curated collection of South Australian and Australian government datasets for research and civic tools.
        - generic [ref=e161]:
          - heading "Resources" [level=3] [ref=e162]
          - list [ref=e163]:
            - listitem [ref=e164]:
              - link "Browse Catalogue" [ref=e165] [cursor=pointer]:
                - /url: /catalogue
            - listitem [ref=e166]:
              - link "About This Project" [ref=e167] [cursor=pointer]:
                - /url: /about
        - generic [ref=e168]:
          - heading "Connect" [level=3] [ref=e169]
          - link "View on GitHub" [ref=e170] [cursor=pointer]:
            - /url: https://github.com/rNLKJA/public-services-open-source-data
      - paragraph [ref=e174]: "Catalogue metadata: CC0 1.0. Datasets retain their original government licences (CC BY 4.0 or Crown Copyright). Built 2024."
  - alert [ref=e175]
  - generic [ref=e176]: "Step 1: Explore cross-dataset case studies and data lineage"
```

# Test source

```ts
  228 |     await context.tracing.start({ screenshots: true, snapshots: true });
  229 | 
  230 |     try {
  231 |     await addCursorHighlight(page);
  232 |     await page.goto(BASE_URL, { waitUntil: 'networkidle' });
  233 |     await humanWait(page, 2000);
  234 | 
  235 |     // Step 1: Navigate to analyses
  236 |     await addCaption(page, 1, 'Visit the analysis gallery showcasing the catalogue breadth');
  237 |     await humanWait(page);
  238 | 
  239 |     const analysesLink = page.locator('a[href="/analyses"]').first();
  240 |     await analysesLink.hover();
  241 |     await humanWait(page, 800);
  242 |     await analysesLink.click();
  243 |     await page.waitForURL(`${BASE_URL}/analyses`);
  244 |     await humanWait(page, 2000);
  245 | 
  246 |     // Step 2: Scroll through visualizations
  247 |     await addCaption(page, 2, 'Explore 6 hero visualizations: crime map, CPI timeline, crash heatmap, and more');
  248 |     await humanWait(page);
  249 | 
  250 |     await page.mouse.wheel(0, 400);
  251 |     await humanWait(page, 1500);
  252 |     await page.mouse.wheel(0, 400);
  253 |     await humanWait(page, 1500);
  254 | 
  255 |     // Step 3: Interact with a visualization
  256 |     await addCaption(page, 3, 'Interactive visualizations with filtering and drill-down capabilities');
  257 |     await humanWait(page);
  258 | 
  259 |     const firstViz = page.locator('article, .analysis-card, [data-analysis]').first();
  260 |     if (await firstViz.count() > 0) {
  261 |       await firstViz.hover();
  262 |       await humanWait(page, 800);
  263 |       await firstViz.click();
  264 |       await humanWait(page, 2000);
  265 |     }
  266 | 
  267 |     // Step 4: View methodology
  268 |     await addCaption(page, 4, 'Each analysis includes methodology, assumptions, and limitations');
  269 |     await humanWait(page);
  270 | 
  271 |     await page.mouse.wheel(0, 400);
  272 |     await humanWait(page, 2000);
  273 | 
  274 |     } finally {
  275 |       await context.tracing.stop();
  276 |       const videoPath = testInfo.outputPath('workflow-2-quickstart-gallery.webm');
  277 |       await page.video()?.saveAs(videoPath);
  278 |     }
  279 |   });
  280 | 
  281 |   test('Workflow 3: Join datasets', async ({ page, context }, testInfo) => {
  282 |     await page.setViewportSize({ width: 1280, height: 800 });
  283 |     await context.tracing.start({ screenshots: true, snapshots: true });
  284 | 
  285 |     try {
  286 |     await addCursorHighlight(page);
  287 |     await page.goto(BASE_URL, { waitUntil: 'networkidle' });
  288 |     await humanWait(page, 2000);
  289 | 
  290 |     // Step 1: Navigate to provenance
  291 |     await addCaption(page, 1, 'Explore cross-dataset case studies and data lineage');
  292 |     await humanWait(page);
  293 | 
  294 |     const provenanceLink = page.locator('a[href="/provenance"]').first();
  295 |     await provenanceLink.hover();
  296 |     await humanWait(page, 800);
  297 |     await provenanceLink.click();
  298 |     await page.waitForURL(`${BASE_URL}/provenance`);
  299 |     await humanWait(page, 2000);
  300 | 
  301 |     // Step 2: View provenance graph
  302 |     await addCaption(page, 2, 'Provenance graph shows how datasets are joined and transformed');
  303 |     await humanWait(page, 2000);
  304 | 
  305 |     await page.mouse.wheel(0, 300);
  306 |     await humanWait(page);
  307 | 
  308 |     // Step 3: Select case study
  309 |     await addCaption(page, 3, 'View detailed case studies with methodology and statistical rigour');
  310 |     await humanWait(page);
  311 | 
  312 |     const caseStudy = page.locator('article, .case-study, [data-case-study]').first();
  313 |     if (await caseStudy.count() > 0) {
  314 |       await caseStudy.hover();
  315 |       await humanWait(page, 800);
  316 |       await caseStudy.click();
  317 |       await humanWait(page, 2000);
  318 |     }
  319 | 
  320 |     // Step 4: Review methodology
  321 |     await addCaption(page, 4, 'Each join includes full methodology, uncertainty quantification, and reproducible code');
  322 |     await humanWait(page);
  323 | 
  324 |     await page.mouse.wheel(0, 400);
  325 |     await humanWait(page, 2000);
  326 | 
  327 |     } finally {
> 328 |       await context.tracing.stop();
      |                             ^ Error: tracing.stop: Target page, context or browser has been closed
  329 |       const videoPath = testInfo.outputPath('workflow-3-join-datasets.webm');
  330 |       await page.video()?.saveAs(videoPath);
  331 |     }
  332 |   });
  333 | });
  334 | 
```