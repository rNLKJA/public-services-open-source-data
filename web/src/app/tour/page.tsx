import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Tour - SA Open Data',
  description: 'Interactive walkthrough of key features and workflows',
};

export default function TourPage() {
  return (
    <div className="container mx-auto px-4 py-8 max-w-5xl">
      <h1 className="text-4xl font-bold mb-4">Platform Tour</h1>
      <p className="text-lg text-muted-foreground mb-8">
        Explore the key features and workflows of the SA Open Data platform through these
        interactive walkthroughs.
      </p>

      {/* Workflow 1: Explore the Catalogue */}
      <section className="mb-12">
        <h2 className="text-2xl font-semibold mb-4">1. Explore the Catalogue</h2>
        <div className="aspect-video bg-muted rounded-lg overflow-hidden mb-4">
          <video
            controls
            muted
            playsInline
            preload="metadata"
            poster="/showcase/workflow-1-poster.jpg"
            className="w-full h-full"
          >
            <source src="/showcase/workflow-1-explore-catalogue.mp4" type="video/mp4" />
            Your browser does not support the video tag.
          </video>
        </div>
        <div className="prose dark:prose-invert max-w-none">
          <h3>Steps:</h3>
          <ol>
            <li>
              <strong>Navigate to the catalogue</strong> - Browse the collection of open datasets
            </li>
            <li>
              <strong>Filter by domain</strong> - Find relevant data by category (crime, health,
              education, transport)
            </li>
            <li>
              <strong>View dataset details</strong> - Examine metadata, attribution, and download
              options
            </li>
          </ol>
          <p className="text-sm text-muted-foreground mt-4">
            <strong>Transcript:</strong> This workflow demonstrates how to navigate the catalogue,
            apply filters to find specific datasets, and access detailed metadata with full
            attribution for proper data governance.
          </p>
        </div>
      </section>

      {/* Workflow 2: Quickstart Gallery */}
      <section className="mb-12">
        <h2 className="text-2xl font-semibold mb-4">2. Quickstart Gallery</h2>
        <div className="aspect-video bg-muted rounded-lg overflow-hidden mb-4">
          <video
            controls
            muted
            playsInline
            preload="metadata"
            poster="/showcase/workflow-2-poster.jpg"
            className="w-full h-full"
          >
            <source src="/showcase/workflow-2-quickstart-gallery.mp4" type="video/mp4" />
            Your browser does not support the video tag.
          </video>
        </div>
        <div className="prose dark:prose-invert max-w-none">
          <h3>Steps:</h3>
          <ol>
            <li>
              <strong>Visit the analysis gallery</strong> - See examples showcasing the
              catalogue&apos;s breadth
            </li>
            <li>
              <strong>Explore visualizations</strong> - Crime map, CPI timeline, crash heatmap,
              school locations, ED waits, population pyramid
            </li>
            <li>
              <strong>Interactive features</strong> - Each visualization includes methodology and
              statistical rigour
            </li>
          </ol>
          <p className="text-sm text-muted-foreground mt-4">
            <strong>Transcript:</strong> The analysis gallery demonstrates the breadth of the
            catalogue through six hero visualizations, each built with statistical rigour,
            uncertainty quantification, and transparent methodology.
          </p>
        </div>
      </section>

      {/* Workflow 3: Join Datasets */}
      <section className="mb-12">
        <h2 className="text-2xl font-semibold mb-4">3. Join Datasets</h2>
        <div className="aspect-video bg-muted rounded-lg overflow-hidden mb-4">
          <video
            controls
            muted
            playsInline
            preload="metadata"
            poster="/showcase/workflow-3-poster.jpg"
            className="w-full h-full"
          >
            <source src="/showcase/workflow-3-join-datasets.mp4" type="video/mp4" />
            Your browser does not support the video tag.
          </video>
        </div>
        <div className="prose dark:prose-invert max-w-none">
          <h3>Steps:</h3>
          <ol>
            <li>
              <strong>Explore cross-dataset case studies</strong> - See how multiple datasets
              combine for deeper insights
            </li>
            <li>
              <strong>View provenance graph</strong> - Understand data lineage and transformation
              steps
            </li>
            <li>
              <strong>Review methodology</strong> - Each join includes full methodology, uncertainty
              quantification, and reproducible code
            </li>
          </ol>
          <p className="text-sm text-muted-foreground mt-4">
            <strong>Transcript:</strong> The provenance view shows how datasets are joined and
            transformed, with complete methodology documentation, uncertainty quantification with
            confidence intervals, and reproducible code for transparency.
          </p>
        </div>
      </section>

      <section className="mb-12">
        <h2 className="text-2xl font-semibold mb-6">Feature Gallery</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <figure className="border rounded-lg overflow-hidden">
            <div className="relative aspect-video bg-muted">
              <span className="absolute inset-0 flex items-center justify-center text-muted-foreground">
                Landing page - light mode
              </span>
            </div>
            <figcaption className="p-3 text-sm text-muted-foreground bg-muted">
              Landing page with clear navigation and data governance focus
            </figcaption>
          </figure>

          <figure className="border rounded-lg overflow-hidden">
            <div className="relative aspect-video bg-muted">
              <span className="absolute inset-0 flex items-center justify-center text-muted-foreground">
                Catalogue browser
              </span>
            </div>
            <figcaption className="p-3 text-sm text-muted-foreground bg-muted">
              Catalogue browser with domain filtering and search
            </figcaption>
          </figure>

          <figure className="border rounded-lg overflow-hidden">
            <div className="relative aspect-video bg-muted">
              <span className="absolute inset-0 flex items-center justify-center text-muted-foreground">
                Analysis gallery
              </span>
            </div>
            <figcaption className="p-3 text-sm text-muted-foreground bg-muted">
              Analysis gallery with interactive visualizations
            </figcaption>
          </figure>

          <figure className="border rounded-lg overflow-hidden">
            <div className="relative aspect-video bg-muted">
              <span className="absolute inset-0 flex items-center justify-center text-muted-foreground">
                Provenance graph
              </span>
            </div>
            <figcaption className="p-3 text-sm text-muted-foreground bg-muted">
              Data provenance graph showing lineage and transformations
            </figcaption>
          </figure>

          <figure className="border rounded-lg overflow-hidden">
            <div className="relative aspect-video bg-muted">
              <span className="absolute inset-0 flex items-center justify-center text-muted-foreground">
                Methods documentation
              </span>
            </div>
            <figcaption className="p-3 text-sm text-muted-foreground bg-muted">
              Comprehensive methods documentation with decision records
            </figcaption>
          </figure>

          <figure className="border rounded-lg overflow-hidden">
            <div className="relative aspect-video bg-muted">
              <span className="absolute inset-0 flex items-center justify-center text-muted-foreground">
                AI audit log
              </span>
            </div>
            <figcaption className="p-3 text-sm text-muted-foreground bg-muted">
              AI audit log with transparency and exportable records
            </figcaption>
          </figure>
        </div>
      </section>

      {/* Mobile Views */}
      <section>
        <h2 className="text-2xl font-semibold mb-6">Mobile Experience</h2>
        <div className="flex gap-6 overflow-x-auto pb-4">
          <figure
            className="flex-shrink-0 border rounded-lg overflow-hidden"
            style={{ width: '195px' }}
          >
            <div className="relative bg-muted" style={{ height: '422px' }}>
              <span className="absolute inset-0 flex items-center justify-center text-muted-foreground text-sm">
                Mobile landing
              </span>
            </div>
            <figcaption className="p-2 text-xs text-muted-foreground bg-muted">
              Mobile landing
            </figcaption>
          </figure>

          <figure
            className="flex-shrink-0 border rounded-lg overflow-hidden"
            style={{ width: '195px' }}
          >
            <div className="relative bg-muted" style={{ height: '422px' }}>
              <span className="absolute inset-0 flex items-center justify-center text-muted-foreground text-sm">
                Mobile catalogue
              </span>
            </div>
            <figcaption className="p-2 text-xs text-muted-foreground bg-muted">
              Mobile catalogue
            </figcaption>
          </figure>

          <figure
            className="flex-shrink-0 border rounded-lg overflow-hidden"
            style={{ width: '195px' }}
          >
            <div className="relative bg-muted" style={{ height: '422px' }}>
              <span className="absolute inset-0 flex items-center justify-center text-muted-foreground text-sm">
                Mobile analysis
              </span>
            </div>
            <figcaption className="p-2 text-xs text-muted-foreground bg-muted">
              Mobile analysis
            </figcaption>
          </figure>
        </div>
      </section>
    </div>
  );
}
