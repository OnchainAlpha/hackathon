"""
Test script for agentic search service
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
print("🤖 Testing Agentic Search Service")
print("=" * 70)
print()

# Initialize services
print("Initializing services...")
apollo = ApolloClient()
db = get_db_manager()
agentic_search = AgenticSearchService(apollo, db)
print("✅ Services initialized")
print()

# Test queries
test_queries = [
    {
        "query": "Find CEOs at SaaS companies",
        "product": "Sales automation platform for B2B companies"
    },
    {
        "query": "Find CTOs at AI companies",
        "product": "AI development tools and APIs"
    },
    {
        "query": "Find VPs of Sales at technology companies",
        "product": "CRM and sales enablement software"
    }
]

# Run tests
for i, test in enumerate(test_queries, 1):
    print("=" * 70)
    print(f"Test {i}/{len(test_queries)}")
    print("=" * 70)
    print(f"Query: {test['query']}")
    print(f"Product: {test['product']}")
    print()
    
    try:
        result = agentic_search.run_agentic_search(
            user_query=test['query'],
            product_description=test['product'],
            max_iterations=2,  # Limit to 2 iterations for testing
            min_results=5,     # Find at least 5 contacts
            max_results_per_query=10  # Max 10 per query
        )
        
        print()
        print("✅ Search Complete!")
        print(f"   Contacts found: {result['stats']['total_contacts']}")
        print(f"   Companies: {result['stats']['total_companies']}")
        print(f"   Iterations: {result['iterations']}")
        print(f"   Queries executed: {result['stats']['queries_executed']}")
        print(f"   Avg results/query: {result['stats']['avg_results_per_query']:.1f}")
        print()
        
        # Show sample contacts
        if result['contacts']:
            print("Sample contacts:")
            for contact in result['contacts'][:3]:
                print(f"   • {contact.get('name', 'Unknown')} - {contact.get('title', 'Unknown')} at {contact.get('organization_name', 'Unknown')}")
        
        print()
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
    
    print()

print("=" * 70)
print("🎉 All tests complete!")
print("=" * 70)

