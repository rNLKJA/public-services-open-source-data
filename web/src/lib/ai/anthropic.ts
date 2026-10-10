/**
 * Anthropic API client for browser-based direct access
 *
 * Uses the anthropic-dangerous-direct-browser-access header for CORS.
 * API keys are provided by the user and never sent to our servers.
 */

import type { AIRequest, AIResponse, AIError } from './types';

const ANTHROPIC_API_URL = 'https://api.anthropic.com/v1/messages';

// Current Anthropic models (as of Oct 2024)
export const ANTHROPIC_MODELS = {
  HAIKU: 'claude-3-5-haiku-20241022',
  SONNET: 'claude-3-7-sonnet-20250219',
} as const;

export async function callAnthropic(
  apiKey: string,
  request: AIRequest,
  model: string = ANTHROPIC_MODELS.HAIKU
): Promise<AIResponse> {
  const startTime = Date.now();

  try {
    const response = await fetch(ANTHROPIC_API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'anthropic-version': '2023-06-01',
        'anthropic-dangerous-direct-browser-access': 'true',
        'x-api-key': apiKey,
      },
      body: JSON.stringify({
        model,
        max_tokens: request.maxTokens ?? 4096,
        temperature: request.temperature ?? 1.0,
        system: request.systemPrompt,
        messages: [
          {
            role: 'user',
            content: request.prompt,
          },
        ],
      }),
    });

    const latencyMs = Date.now() - startTime;

    if (!response.ok) {
      throw await handleAnthropicError(response);
    }

    const data = await response.json();
    const content = data.content[0].text;

    return {
      content,
      provider: 'anthropic',
      model,
      usage: {
        inputTokens: data.usage?.input_tokens ?? 0,
        outputTokens: data.usage?.output_tokens ?? 0,
      },
      latencyMs,
    };
  } catch (error) {
    if (isAIError(error)) {
      throw error;
    }

    // Network or unknown error
    throw {
      code: 'network',
      message: error instanceof Error ? error.message : 'Network error occurred',
      retryable: true,
    } as AIError;
  }
}

async function handleAnthropicError(response: Response): Promise<AIError> {
  const status = response.status;

  try {
    const data = await response.json();
    const errorMessage = data.error?.message || response.statusText;

    if (status === 401) {
      return {
        code: 'invalid_key',
        message: 'Invalid API key. Please check your key and try again.',
        retryable: false,
      };
    }

    if (status === 429) {
      return {
        code: 'rate_limit',
        message: 'Rate limit exceeded. Please try again in a few moments.',
        retryable: true,
      };
    }

    return {
      code: 'unknown',
      message: errorMessage,
      retryable: status >= 500,
    };
  } catch {
    return {
      code: 'unknown',
      message: `HTTP ${status}: ${response.statusText}`,
      retryable: status >= 500,
    };
  }
}

function isAIError(error: unknown): error is AIError {
  return (
    typeof error === 'object' &&
    error !== null &&
    'code' in error &&
    'message' in error &&
    'retryable' in error
  );
}
