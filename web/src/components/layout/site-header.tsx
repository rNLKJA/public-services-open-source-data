'use client';

import Link from 'next/link';
import { Database, Menu, X } from 'lucide-react';
import { ThemeToggle } from './theme-toggle';
import { useState } from 'react';

export function SiteHeader() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  return (
    <header className="sticky top-0 z-50 w-full border-b border-slate-200 dark:border-slate-800 bg-white/95 dark:bg-slate-950/95 backdrop-blur supports-[backdrop-filter]:bg-white/75 dark:supports-[backdrop-filter]:bg-slate-950/75">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 items-center justify-between">
          <div className="flex items-center gap-2">
            <Database className="h-6 w-6 text-federal-blue" aria-hidden="true" />
            <Link
              href="/"
              className="text-lg font-semibold text-slate-900 dark:text-slate-100 hover:text-federal-blue transition-colors"
            >
              SA & AU Open Data Atlas
            </Link>
          </div>

          <nav className="hidden md:flex items-center gap-6">
            <Link
              href="/catalogue"
              className="text-sm font-medium text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-100 transition-colors"
            >
              Catalogue
            </Link>
            <Link
              href="/about"
              className="text-sm font-medium text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-100 transition-colors"
            >
              About
            </Link>
            <ThemeToggle />
          </nav>

          <button
            className="md:hidden p-2 text-slate-600 dark:text-slate-400"
            onClick={() => setIsMenuOpen(!isMenuOpen)}
            aria-label="Toggle menu"
          >
            {isMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
          </button>
        </div>

        {isMenuOpen && (
          <nav className="md:hidden py-4 space-y-2">
            <Link
              href="/catalogue"
              className="block px-4 py-2 text-sm font-medium text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-900 rounded-md"
              onClick={() => setIsMenuOpen(false)}
            >
              Catalogue
            </Link>
            <Link
              href="/about"
              className="block px-4 py-2 text-sm font-medium text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-900 rounded-md"
              onClick={() => setIsMenuOpen(false)}
            >
              About
            </Link>
            <div className="px-4 py-2">
              <ThemeToggle />
            </div>
          </nav>
        )}
      </div>
    </header>
  );
}
