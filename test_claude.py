import os
from dotenv import load_dotenv

load_dotenv()

print("Testing Claude/Anthropic client with proxy fix...")

api_key = os.getenv("ANTHROPIC_API_KEY")
print(f"API Key found: {api_key[:20]}..." if api_key else "No API key")

try:
    from anthropic import Anthropic
    import httpx
    print("✓ Anthropic module imported")

    # Create httpx client without proxy
    http_client = httpx.Client(
        timeout=60.0,
        follow_redirects=True
    )

    client = Anthropic(api_key=api_key, http_client=http_client)
    print("✓ Client created successfully (with proxy fix)")

    # Test a simple API call with different model names
    models_to_try = [
        "claude-3-5-sonnet-20241022",
        "claude-3-5-sonnet-20240620",
        "claude-3-opus-20240229",
        "claude-3-sonnet-20240229",
        "claude-3-haiku-20240307"
    ]

    for model in models_to_try:
        print(f"\nTrying model: {model}...")
        try:
            response = client.messages.create(
                model=model,
                max_tokens=50,
                messages=[{"role": "user", "content": "Say hello"}]
            )

            print(f"✓ SUCCESS with {model}!")
            print(f"Response: {response.content[0].text}")
            print("\n🎉 Claude is working!")
            break
        except Exception as e:
            print(f"✗ Failed: {str(e)[:100]}")

except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()

