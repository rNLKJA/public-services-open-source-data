/**
 * AI provider types and interfaces for BYOK (Bring Your Own Key) functionality
 */

export type AIProvider = 'anthropic' | 'openai';

export interface AISettings {
  provider: AIProvider;
  apiKey: string;
  model: string;
  rememberKey: boolean;
}

export interface AIRequest {
  prompt: string;
  systemPrompt?: string;
  maxTokens?: number;
  temperature?: number;
}

export interface AIResponse {
  content: string;
  provider: AIProvider;
  model: string;
  usage?: {
    inputTokens: number;
    outputTokens: number;
  };
  latencyMs: number;
}

export interface AIAuditLogEntry {
  id: string;
  timestamp: string;
  feature: string;
  provider: AIProvider;
  model: string;
  inputText: string; // Prompt only, never the API key
  outputText: string;
  latencyMs: number;
  tokenUsage?: {
    input: number;
    output: number;
  };
  humanDecision?: 'accepted' | 'edited' | 'rejected';
}

export interface AIError {
  code: 'invalid_key' | 'rate_limit' | 'network' | 'unknown';
  message: string;
  retryable: boolean;
}
