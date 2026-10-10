'use client';

import { useEffect, useState } from 'react';
import { Download, Trash2, AlertCircle } from 'lucide-react';
import { getAuditLog, clearAuditLog, updateHumanDecision, exportAuditLog } from '@/lib/ai/audit-log';
import type { AIAuditLogEntry } from '@/lib/ai/types';

export default function AILogPage() {
  const [entries, setEntries] = useState<AIAuditLogEntry[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showClearConfirm, setShowClearConfirm] = useState(false);

  useEffect(() => {
    loadEntries();
  }, []);

  async function loadEntries() {
    try {
      setLoading(true);
      const data = await getAuditLog();
      setEntries(data);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load audit log');
    } finally {
      setLoading(false);
    }
  }

  async function handleClear() {
    try {
      await clearAuditLog();
      setEntries([]);
      setShowClearConfirm(false);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to clear audit log');
    }
  }

  async function handleExportJSON() {
    try {
      const json = await exportAuditLog();
      const blob = new Blob([json], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `ai-audit-log-${new Date().toISOString().split('T')[0]}.json`;
      a.click();
      URL.revokeObjectURL(url);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to export audit log');
    }
  }

  async function handleExportCSV() {
    try {
      const data = await getAuditLog();
      const headers = ['timestamp', 'feature', 'provider', 'model', 'inputText', 'outputText', 'latencyMs', 'tokensInput', 'tokensOutput', 'humanDecision'];
      const rows = data.map(entry => [
        new Date(entry.timestamp).toISOString(),
        entry.feature,
        entry.provider,
        entry.model,
        `"${(entry.inputText || '').replace(/"/g, '""')}"`,
        `"${(entry.outputText || '').replace(/"/g, '""')}"`,
        entry.latencyMs?.toString() || '',
        entry.tokenUsage?.input.toString() || '',
        entry.tokenUsage?.output.toString() || '',
        entry.humanDecision || '',
      ]);
      const csv = [headers.join(','), ...rows.map(row => row.join(','))].join('\n');
      const blob = new Blob([csv], { type: 'text/csv' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `ai-audit-log-${new Date().toISOString().split('T')[0]}.csv`;
      a.click();
      URL.revokeObjectURL(url);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to export CSV');
    }
  }

  async function handleUpdateDecision(id: string, decision: 'accepted' | 'edited' | 'rejected') {
    try {
      await updateHumanDecision(id, decision);
      await loadEntries(); // Reload to show updated decision
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update decision');
    }
  }

  if (loading) {
    return (
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="max-w-6xl mx-auto">
          <p className="text-slate-600 dark:text-slate-400">Loading audit log...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="max-w-6xl mx-auto">
        <div className="flex items-start justify-between mb-6">
          <div>
            <h1 className="text-4xl font-semibold text-slate-900 dark:text-slate-100 mb-2">
              AI Audit Log
            </h1>
            <p className="text-lg text-slate-600 dark:text-slate-400">
              Complete record of AI interactions (stored locally in your browser)
            </p>
          </div>
          <div className="flex gap-2">
            <button
              onClick={handleExportJSON}
              className="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-federal-blue text-white font-medium hover:bg-federal-blue/90 transition-colors"
              disabled={entries.length === 0}
            >
              <Download className="h-4 w-4" />
              JSON
            </button>
            <button
              onClick={handleExportCSV}
              className="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-federal-blue text-white font-medium hover:bg-federal-blue/90 transition-colors"
              disabled={entries.length === 0}
            >
              <Download className="h-4 w-4" />
              CSV
            </button>
            <button
              onClick={() => setShowClearConfirm(true)}
              className="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-red-600 text-white font-medium hover:bg-red-700 transition-colors"
              disabled={entries.length === 0}
            >
              <Trash2 className="h-4 w-4" />
              Clear
            </button>
          </div>
        </div>

        {error && (
          <div className="mb-6 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg flex items-start gap-3">
            <AlertCircle className="h-5 w-5 text-red-600 dark:text-red-400 flex-shrink-0 mt-0.5" />
            <p className="text-sm text-red-800 dark:text-red-200">{error}</p>
          </div>
        )}

        {entries.length === 0 ? (
          <div className="bg-slate-50 dark:bg-slate-900/50 rounded-lg p-12 text-center">
            <AlertCircle className="h-12 w-12 text-slate-400 mx-auto mb-4" />
            <p className="text-slate-600 dark:text-slate-400">
              No AI interactions recorded yet. When you use AI features, they will appear here.
            </p>
          </div>
        ) : (
          <div className="space-y-4">
            <p className="text-sm text-slate-600 dark:text-slate-400">
              Total entries: {entries.length}
            </p>
            {entries.map((entry) => (
              <div
                key={entry.id}
                className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg p-6"
              >
                <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-4 text-sm">
                  <div>
                    <span className="text-slate-500 dark:text-slate-400 font-medium">Timestamp:</span>
                    <div className="text-slate-900 dark:text-slate-100 font-mono">
                      {new Date(entry.timestamp).toLocaleString()}
                    </div>
                  </div>
                  <div>
                    <span className="text-slate-500 dark:text-slate-400 font-medium">Feature:</span>
                    <div className="text-slate-900 dark:text-slate-100">{entry.feature}</div>
                  </div>
                  <div>
                    <span className="text-slate-500 dark:text-slate-400 font-medium">Provider:</span>
                    <div className="text-slate-900 dark:text-slate-100">{entry.provider}</div>
                  </div>
                  <div>
                    <span className="text-slate-500 dark:text-slate-400 font-medium">Model:</span>
                    <div className="text-slate-900 dark:text-slate-100 font-mono text-xs">{entry.model}</div>
                  </div>
                </div>

                <div className="space-y-3">
                  <div>
                    <span className="text-slate-500 dark:text-slate-400 font-medium text-sm">Input:</span>
                    <div className="mt-1 p-3 bg-slate-50 dark:bg-slate-800/50 rounded text-sm text-slate-900 dark:text-slate-100 whitespace-pre-wrap">
                      {entry.inputText}
                    </div>
                  </div>

                  <div>
                    <span className="text-slate-500 dark:text-slate-400 font-medium text-sm">Output:</span>
                    <div className="mt-1 p-3 bg-slate-50 dark:bg-slate-800/50 rounded text-sm text-slate-900 dark:text-slate-100 whitespace-pre-wrap">
                      {entry.outputText}
                    </div>
                  </div>
                </div>

                <div className="mt-4 flex items-center justify-between">
                  <div className="flex gap-4 text-xs text-slate-500 dark:text-slate-400">
                    {entry.latencyMs && <span>Latency: {entry.latencyMs}ms</span>}
                    {entry.tokenUsage && <span>Tokens: {entry.tokenUsage.input + entry.tokenUsage.output}</span>}
                  </div>

                  <div className="flex items-center gap-2">
                    <span className="text-xs text-slate-500 dark:text-slate-400">Human decision:</span>
                    <select
                      value={entry.humanDecision || ''}
                      onChange={(e) => handleUpdateDecision(entry.id, e.target.value as 'accepted' | 'edited' | 'rejected')}
                      className="text-xs px-2 py-1 rounded border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100"
                    >
                      <option value="">Not recorded</option>
                      <option value="accepted">Accepted</option>
                      <option value="edited">Edited</option>
                      <option value="rejected">Rejected</option>
                    </select>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {showClearConfirm && (
          <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
            <div className="bg-white dark:bg-slate-900 rounded-lg p-6 max-w-md w-full border border-slate-200 dark:border-slate-800">
              <h2 className="text-xl font-semibold text-slate-900 dark:text-slate-100 mb-4">
                Clear Audit Log?
              </h2>
              <p className="text-sm text-slate-600 dark:text-slate-400 mb-6">
                This will permanently delete all {entries.length} audit log entries from your browser.
                This action cannot be undone. Consider exporting first.
              </p>
              <div className="flex gap-3 justify-end">
                <button
                  onClick={() => setShowClearConfirm(false)}
                  className="px-4 py-2 rounded-lg border border-slate-300 dark:border-slate-700 text-slate-900 dark:text-slate-100 hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors"
                >
                  Cancel
                </button>
                <button
                  onClick={handleClear}
                  className="px-4 py-2 rounded-lg bg-red-600 text-white hover:bg-red-700 transition-colors"
                >
                  Clear Log
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
