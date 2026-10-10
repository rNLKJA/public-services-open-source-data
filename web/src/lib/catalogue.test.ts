import { describe, it, expect } from 'vitest';
import { formatBytes, getLicenceBadge } from './catalogue';

describe('formatBytes', () => {
  it('formats 0 bytes', () => {
    expect(formatBytes(0)).toBe('0 B');
  });

  it('formats bytes', () => {
    expect(formatBytes(500)).toBe('500 B');
  });

  it('formats kilobytes', () => {
    expect(formatBytes(1024)).toBe('1 KB');
    expect(formatBytes(1536)).toBe('1.5 KB');
  });

  it('formats megabytes', () => {
    expect(formatBytes(1048576)).toBe('1 MB');
    expect(formatBytes(5242880)).toBe('5 MB');
  });

  it('formats gigabytes', () => {
    expect(formatBytes(1073741824)).toBe('1 GB');
  });
});

describe('getLicenceBadge', () => {
  it('identifies CC BY 4.0', () => {
    const badge = getLicenceBadge('Creative Commons Attribution 4.0 International (CC BY 4.0)');
    expect(badge.short).toBe('CC BY 4.0');
    expect(badge.color).toContain('green');
  });

  it('identifies Crown Copyright', () => {
    const badge = getLicenceBadge('Crown Copyright with reuse permissions');
    expect(badge.short).toBe('Crown Copyright');
    expect(badge.color).toContain('blue');
  });

  it('identifies CC0', () => {
    const badge = getLicenceBadge('CC0 1.0 Universal');
    expect(badge.short).toBe('CC0');
    expect(badge.color).toContain('purple');
  });

  it('handles unknown licences', () => {
    const badge = getLicenceBadge('Some other licence');
    expect(badge.short).toBe('Other');
    expect(badge.color).toContain('slate');
  });
});
