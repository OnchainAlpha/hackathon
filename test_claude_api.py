"""
Test script to verify Claude API key functionality
"""
import anthropic
import os

def test_claude_api():
    """Test if the Claude API key is working"""
    
    # API key
    api_key = "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"
    
    try:
        # Initialize the Anthropic client
        client = anthropic.Anthropic(api_key=api_key)
        
        print("Testing Claude API key...")
        print("-" * 50)
        
        # Make a simple test request
        message = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=100,
            messages=[
                {
                    "role": "user",
                    "content": "Say 'Hello! The API key is working correctly.' in one sentence."
                }
            ]
        )
        
        # Extract and print the response
        response_text = message.content[0].text
        
        print("✓ API Key Status: VALID")
        print(f"✓ Model Used: {message.model}")
        print(f"✓ Response: {response_text}")
        print("-" * 50)
        print("SUCCESS: Claude API key is working correctly!")
        
        return True
        
    except anthropic.AuthenticationError as e:
        print("✗ API Key Status: INVALID")
        print(f"✗ Authentication Error: {e}")
        print("-" * 50)
        print("FAILED: The API key is not valid or has expired.")
        return False
        
    except anthropic.APIError as e:
        print("✗ API Error occurred")
        print(f"✗ Error: {e}")
        print("-" * 50)
        print("FAILED: An API error occurred.")
        return False
        
    except Exception as e:
        print("✗ Unexpected error occurred")
        print(f"✗ Error: {type(e).__name__}: {e}")
        print("-" * 50)
        print("FAILED: An unexpected error occurred.")
        return False

if __name__ == "__main__":
    test_claude_api()

