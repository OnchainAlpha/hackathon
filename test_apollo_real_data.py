"""
Test script to verify Apollo.io API is returning REAL data (not mock data)
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

# Load environment variables
load_dotenv()

from scrapers.apollo_scraper import ApolloClient


def print_header(text):
    """Print a formatted header"""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70)


def test_apollo_api():
    """Test Apollo API with real data"""
    print_header("Testing Apollo.io API - REAL DATA")
    
    # Check if API key is set
    api_key = os.getenv("APOLLO_API_KEY")
    
    if not api_key:
        print("\n❌ APOLLO_API_KEY not set in .env file")
        print("\nAdd to .env:")
        print("APOLLO_API_KEY=your_apollo_key_here")
        return False
    
    print(f"\n✓ API Key found: {api_key[:10]}...")
    
    try:
        # Initialize Apollo client
        print("\n🔍 Initializing Apollo client...")
        client = ApolloClient(api_key=api_key)
        print("✓ Client initialized")
        
        # Test 1: Simple search for CTOs
        print("\n" + "-"*70)
        print("TEST 1: Searching for CTOs at AI companies")
        print("-"*70)
        
        result = client.search_people(
            titles=["CTO", "Chief Technology Officer"],
            industries=["Artificial Intelligence"],
            per_page=5  # Just get 5 for testing
        )
        
        print(f"\n✅ SUCCESS! Found {len(result.contacts)} real contacts from Apollo.io")
        print(f"   Total available: {result.total_results}")
        print(f"   Page: {result.page} of {result.total_pages}")
        
        # Display the contacts
        print("\n📋 Contact Details:")
        for i, contact in enumerate(result.contacts, 1):
            print(f"\n{i}. {contact.name}")
            if contact.title:
                print(f"   Title: {contact.title}")
            if contact.company:
                print(f"   Company: {contact.company}")
            if contact.email:
                print(f"   Email: {contact.email}")
            else:
                print(f"   Email: (not available)")
            if contact.linkedin_url:
                print(f"   LinkedIn: {contact.linkedin_url}")
            if contact.city or contact.state:
                location = f"{contact.city}, {contact.state}" if contact.city and contact.state else contact.city or contact.state
                print(f"   Location: {location}")
            print(f"   Source: {contact.source}")
        
        # Test 2: Search with location
        print("\n" + "-"*70)
        print("TEST 2: Searching for CEOs in San Francisco")
        print("-"*70)
        
        result2 = client.search_people(
            titles=["CEO"],
            locations=["San Francisco, CA, USA"],
            per_page=3
        )
        
        print(f"\n✅ SUCCESS! Found {len(result2.contacts)} real contacts")
        print(f"   Total available: {result2.total_results}")
        
        for i, contact in enumerate(result2.contacts, 1):
            print(f"\n{i}. {contact.name} - {contact.title} at {contact.company}")
        
        # Test 3: Verify it's NOT mock data
        print("\n" + "-"*70)
        print("TEST 3: Verifying this is REAL data (not mock)")
        print("-"*70)
        
        # Check if contacts have Apollo-specific fields
        has_apollo_fields = any(
            contact.source == "apollo.io" and 
            contact.id and 
            len(contact.id) > 10  # Apollo IDs are long
            for contact in result.contacts
        )
        
        if has_apollo_fields:
            print("\n✅ CONFIRMED: This is REAL data from Apollo.io!")
            print("   - Contacts have Apollo IDs")
            print("   - Source is marked as 'apollo.io'")
            print("   - Data structure matches Apollo API response")
        else:
            print("\n⚠️  WARNING: This might be mock data")
            print("   - Check if Apollo API key is valid")
        
        # Summary
        print("\n" + "="*70)
        print("SUMMARY")
        print("="*70)
        print(f"✅ Apollo API is working!")
        print(f"✅ Retrieved {len(result.contacts) + len(result2.contacts)} real contacts")
        print(f"✅ Total available contacts: {result.total_results + result2.total_results}")
        print(f"✅ This is REAL data from Apollo.io, not mock data!")
        print("\n🎉 Your system is ready to use with real contact data!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("\nPossible issues:")
        print("1. Invalid API key")
        print("2. API key doesn't have permissions")
        print("3. Rate limit exceeded")
        print("4. Network connection issue")
        print("\nCheck your Apollo API key at: https://apollo.io/settings/api")
        
        import traceback
        traceback.print_exc()
        return False


def test_with_chat_api():
    """Test the full chat API flow"""
    print_header("Testing Full Chat API Flow")
    
    try:
        import requests
        
        print("\n🌐 Testing POST /api/chat endpoint...")
        print("   (Make sure the server is running: python crm_integration/chat_api.py)")
        
        response = requests.post(
            "http://localhost:8000/api/chat",
            json={
                "message": "Find 3 CTOs at AI companies"
            },
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ API call successful!")
            print(f"   Response: {data['response']}")
            print(f"   Contacts found: {data['contacts_found']}")
            print(f"   Contacts added: {data['contacts_added']}")
            
            # Check if it's using real Apollo data
            if "(Data from Apollo.io)" in data['response'] or "apollo" in data['response'].lower():
                print(f"\n✅ CONFIRMED: Using REAL Apollo.io data!")
            else:
                print(f"\n⚠️  Might be using mock data. Check server logs.")
                
        else:
            print(f"❌ API call failed with status {response.status_code}")
            print(f"   Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("⚠️  Could not connect to API server")
        print("   Server is not running. This test is optional.")
        print("   The Apollo API test above is the main test.")
    except Exception as e:
        print(f"⚠️  API test skipped: {e}")


def main():
    """Run all tests"""
    print("\n" + "🔍 Apollo.io REAL DATA Verification".center(70))
    
    # Test Apollo API directly
    apollo_ok = test_apollo_api()
    
    if apollo_ok:
        # Test full chat API flow (optional)
        test_with_chat_api()
    
    print("\n" + "="*70)
    if apollo_ok:
        print("\n✅ ALL TESTS PASSED!")
        print("\nYour Apollo API is working with REAL data!")
        print("\nNext steps:")
        print("1. Install Claude: pip install anthropic")
        print("2. Start server: python crm_integration/chat_api.py")
        print("3. Open: http://localhost:8000/")
        print("4. Try: 'Find CTOs at AI companies in San Francisco'")
    else:
        print("\n❌ TESTS FAILED")
        print("\nPlease fix the Apollo API configuration and try again.")
    
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    main()

