/**
 * AI audit log using IndexedDB for client-side storage
 *
 * Stores all AI interactions for transparency and review.
 * No data is sent to our servers.
 */

import type { AIAuditLogEntry } from './types';

const DB_NAME = 'ai-audit-log';
const DB_VERSION = 1;
const STORE_NAME = 'entries';

let dbPromise: Promise<IDBDatabase> | null = null;

function getDB(): Promise<IDBDatabase> {
  if (dbPromise) return dbPromise;

  dbPromise = new Promise((resolve, reject) => {
    if (typeof window === 'undefined' || !window.indexedDB) {
      reject(new Error('IndexedDB not available'));
      return;
    }

    const request = indexedDB.open(DB_NAME, DB_VERSION);

    request.onerror = () => reject(request.error);
    request.onsuccess = () => resolve(request.result);

    request.onupgradeneeded = (event) => {
      const db = (event.target as IDBOpenDBRequest).result;
      if (!db.objectStoreNames.contains(STORE_NAME)) {
        const store = db.createObjectStore(STORE_NAME, { keyPath: 'id' });
        store.createIndex('timestamp', 'timestamp', { unique: false });
        store.createIndex('feature', 'feature', { unique: false });
      }
    };
  });

  return dbPromise;
}

export async function logAIInteraction(entry: Omit<AIAuditLogEntry, 'id'>): Promise<void> {
  try {
    const db = await getDB();
    const transaction = db.transaction([STORE_NAME], 'readwrite');
    const store = transaction.objectStore(STORE_NAME);

    const fullEntry: AIAuditLogEntry = {
      id: crypto.randomUUID(),
      ...entry,
    };

    store.add(fullEntry);

    await new Promise<void>((resolve, reject) => {
      transaction.oncomplete = () => resolve();
      transaction.onerror = () => reject(transaction.error);
    });
  } catch (error) {
    console.error('Failed to log AI interaction:', error);
    // Non-fatal: continue even if logging fails
  }
}

export async function getAuditLog(limit?: number): Promise<AIAuditLogEntry[]> {
  try {
    const db = await getDB();
    const transaction = db.transaction([STORE_NAME], 'readonly');
    const store = transaction.objectStore(STORE_NAME);
    const index = store.index('timestamp');

    const request = index.openCursor(null, 'prev'); // Newest first
    const entries: AIAuditLogEntry[] = [];

    await new Promise<void>((resolve, reject) => {
      request.onsuccess = () => {
        const cursor = request.result;
        if (cursor && (!limit || entries.length < limit)) {
          entries.push(cursor.value);
          cursor.continue();
        } else {
          resolve();
        }
      };
      request.onerror = () => reject(request.error);
    });

    return entries;
  } catch (error) {
    console.error('Failed to retrieve audit log:', error);
    return [];
  }
}

export async function updateHumanDecision(
  id: string,
  decision: 'accepted' | 'edited' | 'rejected'
): Promise<void> {
  try {
    const db = await getDB();
    const transaction = db.transaction([STORE_NAME], 'readwrite');
    const store = transaction.objectStore(STORE_NAME);

    const getRequest = store.get(id);
    await new Promise<void>((resolve, reject) => {
      getRequest.onsuccess = () => {
        const entry = getRequest.result;
        if (entry) {
          entry.humanDecision = decision;
          store.put(entry);
        }
        resolve();
      };
      getRequest.onerror = () => reject(getRequest.error);
    });

    await new Promise<void>((resolve, reject) => {
      transaction.oncomplete = () => resolve();
      transaction.onerror = () => reject(transaction.error);
    });
  } catch (error) {
    console.error('Failed to update human decision:', error);
  }
}

export async function exportAuditLog(): Promise<string> {
  const entries = await getAuditLog();
  return JSON.stringify(entries, null, 2);
}

export async function clearAuditLog(): Promise<void> {
  try {
    const db = await getDB();
    const transaction = db.transaction([STORE_NAME], 'readwrite');
    const store = transaction.objectStore(STORE_NAME);
    store.clear();

    await new Promise<void>((resolve, reject) => {
      transaction.oncomplete = () => resolve();
      transaction.onerror = () => reject(transaction.error);
    });
  } catch (error) {
    console.error('Failed to clear audit log:', error);
    throw error;
  }
}
