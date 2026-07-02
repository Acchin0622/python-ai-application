from google import genai
from google.genai import types

from config import DEFAULT_MODEL, GEMINI_API_KEY

# Rough estimate: ~4 characters per token in Japanese/English mix
CHARS_PER_TOKEN = 4
GEMINI_CONTEXT_LIMIT = 30000  # Conservative estimate for free tier


def get_client() -> genai.Client:
    if not GEMINI_API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY が設定されていません。.env ファイルにキーを記入してください。"
        )
    return genai.Client(api_key=GEMINI_API_KEY)


def estimate_tokens(text: str) -> int:
    """Rough token count estimate (actual varies by content)."""
    return len(text) // CHARS_PER_TOKEN


def validate_input_length(text: str, max_tokens: int = GEMINI_CONTEXT_LIMIT) -> tuple[bool, str]:
    """Check if text exceeds context limits. Returns (is_valid, warning_message)."""
    estimated = estimate_tokens(text)
    if estimated > max_tokens:
        return False, f"入力が長すぎます（推定 {estimated:,} トークン > {max_tokens:,} 制限）。テキストを短縮してください。"
    if estimated > max_tokens * 0.8:  # Warn at 80%
        return True, f"⚠️ 入力が長いです（推定 {estimated:,} トークン）。生成が遅くなる可能性があります。"
    return True, ""


def generate_text(
    prompt: str,
    system_instruction: str | None = None,
    temperature: float = 0.7,
    model: str = DEFAULT_MODEL,
) -> str:
    client = get_client()
    config = types.GenerateContentConfig(
        temperature=temperature,
        system_instruction=system_instruction,
    )
    try:
        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config=config,
        )
        return response.text or ""
    except Exception as e:
        error_msg = str(e)
        if "401" in error_msg or "UNAUTHENTICATED" in error_msg:
            raise RuntimeError("API キーが無効です。.env ファイルを確認してください。") from e
        if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
            raise RuntimeError("API レート制限に達しました。しばらく待ってから再度お試しください。") from e
        if "400" in error_msg or "INVALID_ARGUMENT" in error_msg:
            raise RuntimeError(f"リクエスト形式エラー: テキストが長すぎるか、特殊文字が含まれている可能性があります。") from e
        raise RuntimeError(f"生成エラー: {error_msg}") from e
