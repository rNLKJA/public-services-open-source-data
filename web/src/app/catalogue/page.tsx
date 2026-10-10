import { CatalogueTable } from '@/components/catalogue-table';
import { getCatalogueData } from '@/lib/catalogue';

export const metadata = {
  title: 'Catalogue - SA & AU Open Data Atlas',
  description:
    'Browse 95+ curated South Australian and Australian government datasets by domain, licence and temporal coverage.',
};

export default function CataloguePage() {
  const catalogue = getCatalogueData();

  return (
    <div className="py-12 bg-white dark:bg-slate-950">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mb-8">
          <h1 className="text-3xl sm:text-4xl font-semibold text-slate-900 dark:text-slate-100 mb-3">
            Dataset Catalogue
          </h1>
          <p className="text-lg text-slate-600 dark:text-slate-400">
            {catalogue.dataset_count} curated datasets from South Australian and Australian
            government sources. Filter by domain, search by name, or browse the full collection.
          </p>
        </div>

        <CatalogueTable datasets={catalogue.datasets} />
      </div>
    </div>
  );
}
