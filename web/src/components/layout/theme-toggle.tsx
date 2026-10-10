'use client';

import { Moon, Sun } from 'lucide-react';
import { useTheme } from 'next-themes';
import { useState } from 'react';

export function ThemeToggle() {
  const { theme, setTheme, resolvedTheme } = useTheme();
  const [, setMounted] = useState(false);

  // Use resolvedTheme instead of mounted state check
  const currentTheme = theme === 'system' ? resolvedTheme : theme;

  return (
    <button
      onClick={() => {
        setMounted(true);
        setTheme(currentTheme === 'dark' ? 'light' : 'dark');
      }}
      className="inline-flex items-center justify-center rounded-md p-2 text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-900 transition-colors"
      aria-label="Toggle theme"
      suppressHydrationWarning
    >
      {currentTheme === 'dark' ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
    </button>
  );
}
