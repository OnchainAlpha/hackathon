"""
Test script for Apollo.io integration with LeadOn CRM.
Demonstrates the complete workflow: Query → Parse → Search → Save → Display
"""

import os
import sys
import json
from pathlib import Path
from dotenv import load_dotenv

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

# Load environment variables
load_dotenv()

from ai_agent.intent_parser import IntentParser
from scrapers.apollo_scraper import ApolloClient
from scrapers.schemas import Contact


def print_header(text):
    """Print a formatted header"""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70)


def print_contact(contact: Contact, index: int):
    """Print contact details in a formatted way"""
    print(f"\n{index}. {contact.name}")
    if contact.title:
        print(f"   Title: {contact.title}")
    if contact.company:
        print(f"   Company: {contact.company}")
    if contact.email:
        print(f"   Email: {contact.email}")
    if contact.linkedin_url:
        print(f"   LinkedIn: {contact.linkedin_url}")
    if contact.city or contact.state:
        location = f"{contact.city}, {contact.state}" if contact.city and contact.state else contact.city or contact.state
        print(f"   Location: {location}")


def test_intent_parsing():
    """Test 1: Parse user intent"""
    print_header("TEST 1: Intent Parsing")
    
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY not set. Skipping intent parsing test.")
        return None
    
    try:
        parser = IntentParser()
        
        test_queries = [
            "Find CTOs at AI companies in San Francisco",
            "Get investors in the FinTech space",
            "Partnership outreach to SaaS CEOs in New York"
        ]
        
        for query in test_queries:
            print(f"\n📝 Query: \"{query}\"")
            intent = parser.parse_intent(query)
            
            print(f"   ✓ Parsed Intent:")
            print(f"     - Campaign: {intent.campaign_objective}")
            print(f"     - Titles: {intent.titles}")
            print(f"     - Industries: {intent.industries}")
            print(f"     - Locations: {intent.locations}")
            print(f"     - Max Results: {intent.max_results}")
        
        print("\n✅ Intent parsing test passed!")
        return parser
        
    except Exception as e:
        print(f"❌ Intent parsing test failed: {e}")
        return None


def test_apollo_search():
    """Test 2: Search Apollo.io API"""
    print_header("TEST 2: Apollo.io API Search")
    
    if not os.getenv("APOLLO_API_KEY"):
        print("❌ APOLLO_API_KEY not set. Skipping Apollo search test.")
        print("   To test with real data:")
        print("   1. Get API key from https://apollo.io/settings/api")
        print("   2. Add to .env: APOLLO_API_KEY=your_key_here")
        print("   3. Run this script again")
        return []
    
    try:
        client = ApolloClient()
        
        print("\n🔍 Searching for: CTOs at AI companies")
        result = client.search_people(
            titles=["CTO", "Chief Technology Officer"],
            industries=["Artificial Intelligence"],
            per_page=5  # Limit to 5 for testing
        )
        
        print(f"\n✅ Found {len(result.contacts)} contacts")
        print(f"   Total available: {result.total_results}")
        
        for i, contact in enumerate(result.contacts, 1):
            print_contact(contact, i)
        
        return result.contacts
        
    except Exception as e:
        print(f"❌ Apollo search test failed: {e}")
        print(f"   Error details: {str(e)}")
        return []


def test_end_to_end():
    """Test 3: End-to-end workflow"""
    print_header("TEST 3: End-to-End Workflow")
    
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY not set. Skipping end-to-end test.")
        return
    
    try:
        # Step 1: Parse intent
        print("\n📝 Step 1: Parsing user query...")
        parser = IntentParser()
        query = "Find 5 CEOs at AI startups in San Francisco"
        intent = parser.parse_intent(query)
        print(f"   ✓ Intent parsed: {intent.campaign_objective}")
        
        # Step 2: Search (Apollo or mock)
        print("\n🔍 Step 2: Searching for contacts...")
        contacts = []
        
        if os.getenv("APOLLO_API_KEY"):
            try:
                client = ApolloClient()
                result = client.search_people(
                    titles=intent.titles if intent.titles else None,
                    locations=intent.locations if intent.locations else None,
                    per_page=5
                )
                contacts = result.contacts
                print(f"   ✓ Found {len(contacts)} contacts from Apollo.io")
            except Exception as e:
                print(f"   ⚠️  Apollo failed: {e}")
                print("   ℹ️  Using mock data instead")
                from cli.search_mock import load_mock_contacts, filter_contacts
                all_contacts = load_mock_contacts()
                filtered = filter_contacts(all_contacts, titles=intent.titles, locations=intent.locations)
                contacts = filtered[:5]
        else:
            print("   ℹ️  Using mock data (Apollo API key not set)")
            from cli.search_mock import load_mock_contacts, filter_contacts
            all_contacts = load_mock_contacts()
            filtered = filter_contacts(all_contacts, titles=intent.titles, locations=intent.locations)
            contacts = filtered[:5]
        
        # Step 3: Display results
        print(f"\n📊 Step 3: Results ({len(contacts)} contacts)")
        for i, contact in enumerate(contacts, 1):
            print_contact(contact, i)
        
        # Step 4: Simulate database save
        print("\n💾 Step 4: Saving to database...")
        print(f"   ✓ Would save {len(contacts)} contacts to CRM")
        print(f"   ✓ Would sync to Twenty CRM (if configured)")
        
        # Step 5: Generate response
        print("\n💬 Step 5: Generating response...")
        response = parser.generate_response(intent, len(contacts))
        print(f"   Response: \"{response}\"")
        
        print("\n✅ End-to-end test completed successfully!")
        
    except Exception as e:
        print(f"❌ End-to-end test failed: {e}")
        import traceback
        traceback.print_exc()


def test_api_endpoint():
    """Test 4: Test the actual API endpoint"""
    print_header("TEST 4: API Endpoint Test")
    
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
            
            if data.get('intent'):
                print(f"\n   Parsed Intent:")
                print(f"     - Objective: {data['intent'].get('campaign_objective')}")
                print(f"     - Titles: {data['intent'].get('titles')}")
        else:
            print(f"❌ API call failed with status {response.status_code}")
            print(f"   Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to API server")
        print("   Make sure the server is running:")
        print("   python crm_integration/chat_api.py")
    except Exception as e:
        print(f"❌ API test failed: {e}")


def main():
    """Run all tests"""
    print("\n" + "🚀 LeadOn CRM - Apollo Integration Test Suite".center(70))
    
    # Check environment
    print_header("Environment Check")
    print(f"   OpenAI API:  {'✅ Configured' if os.getenv('OPENAI_API_KEY') else '❌ Not configured'}")
    print(f"   Apollo API:  {'✅ Configured' if os.getenv('APOLLO_API_KEY') else '❌ Not configured (will use mock data)'}")
    print(f"   Twenty CRM:  {'✅ Configured' if os.getenv('TWENTY_CRM_API_TOKEN') else '❌ Not configured'}")
    
    # Run tests
    test_intent_parsing()
    test_apollo_search()
    test_end_to_end()
    test_api_endpoint()
    
    # Summary
    print_header("Test Summary")
    print("\n✅ All tests completed!")
    print("\nNext steps:")
    print("1. Start the server: python crm_integration/chat_api.py")
    print("2. Open http://localhost:8000/ in your browser")
    print("3. Try queries like:")
    print("   - 'Find CTOs at AI companies in San Francisco'")
    print("   - 'Get investors in the FinTech space'")
    print("   - 'Find VPs of Sales at SaaS companies'")
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    main()

