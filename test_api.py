#!/usr/bin/env python3
"""Quick API connectivity and basic functionality test."""

from utils.gemini_client import get_client, generate_text, validate_input_length, estimate_tokens

def test_api_key():
    """Verify API key is set."""
    try:
        client = get_client()
        print("✅ API key configured successfully")
        return True
    except RuntimeError as e:
        print(f"❌ API key error: {e}")
        return False


def test_token_estimation():
    """Test token counting utility."""
    test_texts = [
        "短い文",
        "これはやや長めのテキストです。複数の文を含んでいます。",
        "A" * 10000,  # ~2500 tokens
    ]
    print("\n📊 Token Estimation:")
    for text in test_texts:
        tokens = estimate_tokens(text)
        print(f"  {len(text)} chars → ~{tokens} tokens")


def test_input_validation():
    """Test input length validation."""
    print("\n✔️  Input Validation:")

    # Normal length
    is_valid, msg = validate_input_length("普通のテキスト" * 100)
    print(f"  Normal text: {is_valid} {msg}")

    # Very long
    is_valid, msg = validate_input_length("A" * 200000)
    print(f"  Very long text: {is_valid} {msg}")


def test_basic_generation():
    """Test a simple generation request."""
    print("\n🤖 Testing basic generation:")
    try:
        result = generate_text(
            "短くて良いので、素早く応答してください。",
            system_instruction="You are a helpful assistant.",
            temperature=0.5
        )
        if result:
            print(f"  ✅ Generation successful ({len(result)} chars)")
            print(f"  Sample: {result[:100]}...")
        else:
            print("  ❌ Empty response")
    except Exception as e:
        print(f"  ❌ Generation failed: {e}")


if __name__ == "__main__":
    print("🧪 AI Writing Tool - API Test Suite\n")
    print("=" * 50)

    if test_api_key():
        test_token_estimation()
        test_input_validation()
        test_basic_generation()

    print("\n" + "=" * 50)
    print("✨ All checks complete!")
