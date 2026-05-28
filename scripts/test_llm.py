"""
Quick test script to verify LLM client setup
"""
import sys
import os
from llm_client import LLMClient


def test_provider(provider: str, model: str, api_key_env: str):
    """Test a specific provider"""
    print(f"\n{'='*60}")
    print(f"Testing {provider.upper()} with {model}")
    print(f"{'='*60}")

    # Check API key
    api_key = os.getenv(api_key_env)
    if not api_key:
        print(f"❌ API key not found: {api_key_env}")
        print(f"   Set it with: export {api_key_env}=your-key-here")
        return False

    print(f"✓ API key found: {api_key_env}")

    # Try to create client
    try:
        client = LLMClient(provider=provider, model=model)
        print(f"✓ Client initialized successfully")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Client initialization failed: {e}")
        return False

    # Try to generate
    try:
        print("  Sending test prompt...")
        response = client.generate(
            prompt="Say 'Hello, AgenticSDLC!' and nothing else.",
            temperature=0.0,
            max_tokens=50
        )
        print(f"✓ Response received: {response[:100]}")
        return True
    except Exception as e:
        print(f"❌ Generation failed: {e}")
        return False


def main():
    print("AgenticSDLC LLM Client Test")
    print("="*60)

    providers_to_test = [
        ("openai", "gpt-4o-mini", "OPENAI_API_KEY"),
        ("anthropic", "claude-3-5-sonnet-20241022", "ANTHROPIC_API_KEY"),
        ("google", "gemini-pro", "GOOGLE_API_KEY"),
    ]

    results = {}
    for provider, model, api_key_env in providers_to_test:
        try:
            success = test_provider(provider, model, api_key_env)
            results[provider] = success
        except KeyboardInterrupt:
            print("\n\nTest interrupted by user")
            sys.exit(1)

    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    for provider, success in results.items():
        status = "✓ PASS" if success else "❌ FAIL"
        print(f"{provider:12} {status}")

    if any(results.values()):
        print("\n✓ At least one provider is working!")
        print("  You can now run agents with run_agent.py")
    else:
        print("\n❌ No providers are working")
        print("  Please check your API keys and package installations")
        print("  See README_LLM_SETUP.md for setup instructions")


if __name__ == "__main__":
    main()
