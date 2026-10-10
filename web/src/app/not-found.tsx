import Link from 'next/link';
import { AlertCircle, Home, Database } from 'lucide-react';

export default function NotFound() {
  return (
    <div className="min-h-[60vh] flex items-center justify-center bg-white dark:bg-slate-950">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="max-w-md mx-auto text-center">
          <div className="inline-flex items-center justify-center p-4 rounded-full bg-federal-blue/10 dark:bg-federal-blue/20 text-federal-blue mb-6">
            <AlertCircle className="h-12 w-12" />
          </div>
          <h1 className="text-4xl font-semibold text-slate-900 dark:text-slate-100 mb-3">
            404 – Page Not Found
          </h1>
          <p className="text-lg text-slate-600 dark:text-slate-400 mb-8">
            The page you&apos;re looking for doesn&apos;t exist or has been moved.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              href="/"
              className="inline-flex items-center justify-center gap-2 px-6 py-3 rounded-lg bg-federal-blue text-white font-medium hover:bg-federal-blue/90 transition-colors"
            >
              <Home className="h-4 w-4" />
              Go Home
            </Link>
            <Link
              href="/catalogue"
              className="inline-flex items-center justify-center gap-2 px-6 py-3 rounded-lg border border-slate-300 dark:border-slate-700 text-slate-700 dark:text-slate-300 font-medium hover:bg-slate-100 dark:hover:bg-slate-900 transition-colors"
            >
              <Database className="h-4 w-4" />
              Browse Catalogue
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
