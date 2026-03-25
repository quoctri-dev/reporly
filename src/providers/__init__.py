"""
Reporly — LLM Provider (swap-ready via LiteLLM)
Swap provider = change LLM_MODEL in .env. No code change needed.

Supported: gemini/gemini-2.0-flash, claude-sonnet-4-6, groq/llama-3.1-70b, etc.
"""
import time
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Public interface
# ---------------------------------------------------------------------------

@dataclass
class LLMResponse:
    """Normalized LLM response."""
    content: str
    model: str
    usage_tokens: int = 0


def call_llm(
    prompt: str,
    model: str | None = None,
    api_key: str | None = None,
    temperature: float = 0.3,
    max_tokens: int = 2000,
    max_retries: int = 3,
) -> LLMResponse:
    """
    Call LLM via LiteLLM (provider-agnostic).

    Args:
        prompt: The prompt to send
        model: LiteLLM model string (e.g. "gemini/gemini-2.0-flash")
        api_key: API key (auto-detected by LiteLLM if not provided)
        temperature: Sampling temperature
        max_tokens: Max response tokens
        max_retries: Retry count with exponential backoff

    Returns:
        LLMResponse with normalized content

    Raises:
        RuntimeError: After all retries exhausted
    """
    from litellm import completion  # lazy import — only when actually called

    last_error = None

    for attempt in range(max_retries):
        try:
            kwargs = {
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": temperature,
                "max_tokens": max_tokens,
            }
            if api_key:
                kwargs["api_key"] = api_key

            response = completion(**kwargs)

            content = response.choices[0].message.content or ""
            usage = getattr(response, "usage", None)
            tokens = usage.total_tokens if usage else 0

            logger.info(
                "LLM call OK",
                extra={"model": model, "tokens": tokens, "attempt": attempt + 1},
            )

            return LLMResponse(content=content, model=model or "", usage_tokens=tokens)

        except Exception as e:
            last_error = e
            wait = 2 ** attempt  # 1s, 2s, 4s
            logger.warning(
                "LLM call failed (attempt %d/%d): %s — retrying in %ds",
                attempt + 1, max_retries, str(e), wait,
            )
            time.sleep(wait)

    raise RuntimeError(
        f"LLM call failed after {max_retries} retries. Last error: {last_error}"
    )


__all__ = ["call_llm", "LLMResponse"]
