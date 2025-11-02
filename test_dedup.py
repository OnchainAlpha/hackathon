"""
Test deduplication logic
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scrapers.apollo_scraper import ApolloClient
from database.db_manager import get_db_manager
from services.agentic_search_service import AgenticSearchService

print("=" * 70)
print("🔍 Testing Deduplication")
print("=" * 70)
print()

# Initialize services
apollo = ApolloClient()
db = get_db_manager()
agentic_search = AgenticSearchService(apollo, db)

# Test with a simple query
print("Running search: Find CEOs at SaaS companies")
print("Max contacts: 10")
print()

result = agentic_search.run_agentic_search(
    user_query="Find CEOs at SaaS companies",
    product_description="",
    max_iterations=1,
    min_results=5,
    max_results_per_query=10
)

print()
print("=" * 70)
print("Results:")
print("=" * 70)
print(f"Total contacts returned: {len(result['contacts'])}")
print(f"Total companies: {len(result['companies'])}")
print()

# Show all contacts
for i, contact in enumerate(result['contacts'], 1):
    print(f"{i}. {contact.get('name', 'Unknown')}")
    print(f"   Email: {contact.get('email', 'N/A')}")
    print(f"   LinkedIn: {contact.get('linkedin_url', 'N/A')}")
    print(f"   ID: {contact.get('id', 'N/A')}")
    print()

