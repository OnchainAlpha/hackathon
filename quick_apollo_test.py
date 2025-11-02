"""Quick test of Apollo API with upgraded plan"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()

print("="*70)
print("Testing Apollo API with Upgraded Plan")
print("="*70)

api_key = os.getenv("APOLLO_API_KEY")
print(f"\nAPI Key: {api_key[:10]}..." if api_key else "No API key found")

if not api_key:
    print("ERROR: No API key in .env file")
    sys.exit(1)

print("\nImporting Apollo client...")
from scrapers.apollo_scraper import ApolloClient

print("Creating client...")
client = ApolloClient(api_key=api_key)

print("\nSearching for CTOs at AI companies...")
print("(This will use REAL Apollo API)")

try:
    result = client.search_people(
        titles=["CTO"],
        industries=["Artificial Intelligence"],
        per_page=5
    )
    
    print(f"\n✅ SUCCESS!")
    print(f"Found {len(result.contacts)} contacts")
    print(f"Total available: {result.total_results}")
    
    print("\n" + "="*70)
    print("REAL CONTACTS FROM APOLLO:")
    print("="*70)
    
    for i, contact in enumerate(result.contacts, 1):
        print(f"\n{i}. {contact.name}")
        print(f"   Title: {contact.title}")
        print(f"   Company: {contact.company}")
        print(f"   Email: {contact.email or '(not available)'}")
        print(f"   Location: {contact.city}, {contact.state}" if contact.city else "")
        print(f"   Source: {contact.source}")
    
    print("\n" + "="*70)
    print("🎉 YOUR APOLLO API IS WORKING WITH REAL DATA!")
    print("="*70)
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()

