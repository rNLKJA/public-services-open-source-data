/**
 * OpenAI API client for browser-based direct access
 *
 * API keys are provided by the user and never sent to our servers.
 */

import type { AIRequest, AIResponse, AIError } from './types';

const OPENAI_API_URL = 'https://api.openai.com/v1/chat/completions';

// Current OpenAI models (user can override)
export const OPENAI_MODELS = {
  GPT4O_MINI: 'gpt-4o-mini',
  GPT4O: 'gpt-4o',
} as const;

export async function callOpenAI(
  apiKey: string,
  request: AIRequest,
  model: string = OPENAI_MODELS.GPT4O_MINI
): Promise<AIResponse> {
  const startTime = Date.now();

  try {
    const messages: Array<{ role: string; content: string }> = [];
    if (request.systemPrompt) {
      messages.push({ role: 'system', content: request.systemPrompt });
    }
    messages.push({ role: 'user', content: request.prompt });

    const response = await fetch(OPENAI_API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${apiKey}`,
      },
      body: JSON.stringify({
        model,
        messages,
        max_tokens: request.maxTokens ?? 4096,
        temperature: request.temperature ?? 1.0,
      }),
    });

    const latencyMs = Date.now() - startTime;

    if (!response.ok) {
      throw await handleOpenAIError(response);
    }

    const data = await response.json();
    const content = data.choices[0].message.content;

    return {
      content,
      provider: 'openai',
      model,
      usage: {
        inputTokens: data.usage?.prompt_tokens ?? 0,
        outputTokens: data.usage?.completion_tokens ?? 0,
      },
      latencyMs,
    };
  } catch (error) {
    if (isAIError(error)) {
      throw error;
    }

    throw {
      code: 'network',
      message: error instanceof Error ? error.message : 'Network error occurred',
      retryable: true,
    } as AIError;
  }
}

async function handleOpenAIError(response: Response): Promise<AIError> {
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
