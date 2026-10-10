/**
 * AI settings management for browser storage
 *
 * Stores API keys in sessionStorage (default) or localStorage (opt-in).
 * Keys are NEVER sent to our servers.
 */

import type { AISettings, AIProvider } from './types';
import { ANTHROPIC_MODELS } from './anthropic';
import { OPENAI_MODELS } from './openai';

const SESSION_KEY = 'ai-settings';
const PERSISTENT_KEY = 'ai-settings-persistent';

export function getAISettings(): AISettings | null {
  // Check localStorage first (persistent), then sessionStorage
  const persistent = typeof window !== 'undefined' ? localStorage.getItem(PERSISTENT_KEY) : null;
  if (persistent) {
    try {
      return JSON.parse(persistent);
    } catch {
      // Invalid JSON, ignore
    }
  }

  const session = typeof window !== 'undefined' ? sessionStorage.getItem(SESSION_KEY) : null;
  if (session) {
    try {
      return JSON.parse(session);
    } catch {
      // Invalid JSON, ignore
    }
  }

  return null;
}

export function saveAISettings(settings: AISettings): void {
  if (typeof window === 'undefined') return;

  const json = JSON.stringify(settings);

  if (settings.rememberKey) {
    localStorage.setItem(PERSISTENT_KEY, json);
    sessionStorage.removeItem(SESSION_KEY);
  } else {
    sessionStorage.setItem(SESSION_KEY, json);
    localStorage.removeItem(PERSISTENT_KEY);
  }
}

export function clearAISettings(): void {
  if (typeof window === 'undefined') return;
  sessionStorage.removeItem(SESSION_KEY);
  localStorage.removeItem(PERSISTENT_KEY);
}

export function getDefaultModel(provider: AIProvider): string {
  return provider === 'anthropic' ? ANTHROPIC_MODELS.HAIKU : OPENAI_MODELS.GPT4O_MINI;
}

export function validateAPIKey(provider: AIProvider, key: string): boolean {
  if (!key || key.trim().length === 0) {
    return false;
  }

  // Basic format validation
  if (provider === 'anthropic') {
    return key.startsWith('sk-ant-');
  }

  if (provider === 'openai') {
    return key.startsWith('sk-');
  }

  return false;
}
