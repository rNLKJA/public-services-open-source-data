import Link from 'next/link';
import { GitHubLogoIcon } from '@radix-ui/react-icons';

export function SiteFooter() {
  return (
    <footer className="border-t border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-900/50">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div>
            <h3 className="text-sm font-semibold text-slate-900 dark:text-slate-100 mb-3">
              SA & AU Open Data Atlas
            </h3>
            <p className="text-sm text-slate-600 dark:text-slate-400">
              A curated collection of South Australian and Australian government datasets for
              research and civic tools.
            </p>
          </div>

          <div>
            <h3 className="text-sm font-semibold text-slate-900 dark:text-slate-100 mb-3">
              Resources
            </h3>
            <ul className="space-y-2">
              <li>
                <Link
                  href="/catalogue"
                  className="text-sm text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-100"
                >
                  Browse Catalogue
                </Link>
              </li>
              <li>
                <Link
                  href="/about"
                  className="text-sm text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-100"
                >
                  About This Project
                </Link>
              </li>
            </ul>
          </div>

          <div>
            <h3 className="text-sm font-semibold text-slate-900 dark:text-slate-100 mb-3">
              Connect
            </h3>
            <a
              href="https://github.com/rNLKJA/public-services-open-source-data"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 text-sm text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-100"
            >
              <GitHubLogoIcon className="h-4 w-4" />
              View on GitHub
            </a>
          </div>
        </div>

        <div className="mt-8 pt-8 border-t border-slate-200 dark:border-slate-800">
          <p className="text-xs text-slate-600 dark:text-slate-400 text-center">
            Catalogue metadata: CC0 1.0. Datasets retain their original government licences (CC BY
            4.0 or Crown Copyright). Built 2026.
          </p>
        </div>
      </div>
    </footer>
  );
}
