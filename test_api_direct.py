import requests
import json

API_KEY = "E0-borDrTehbfPZN5P4i5Q"

print("Testing Apollo API directly...")
print(f"API Key: {API_KEY[:10]}...")

url = "https://api.apollo.io/api/v1/mixed_people/search"

headers = {
    "Content-Type": "application/json",
    "Cache-Control": "no-cache",
    "X-Api-Key": API_KEY
}

payload = {
    "page": 1,
    "per_page": 5,
    "person_titles": ["CTO", "Chief Technology Officer"]
}

print("\nMaking request to Apollo API...")
print(f"URL: {url}")
print(f"Payload: {json.dumps(payload, indent=2)}")

try:
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    
    print(f"\nStatus Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("\n✅ SUCCESS! API is working!")
        print(f"Total results: {data.get('pagination', {}).get('total_entries', 0)}")
        
        people = data.get('people', [])
        print(f"Contacts returned: {len(people)}")
        
        if people:
            print("\n" + "="*70)
            print("REAL CONTACTS FROM APOLLO:")
            print("="*70)
            
            for i, person in enumerate(people[:5], 1):
                print(f"\n{i}. {person.get('name', 'N/A')}")
                print(f"   Title: {person.get('title', 'N/A')}")
                print(f"   Company: {person.get('organization', {}).get('name', 'N/A')}")
                print(f"   Email: {person.get('email', 'Not available')}")
                print(f"   LinkedIn: {person.get('linkedin_url', 'N/A')}")
        
        print("\n" + "="*70)
        print("🎉 YOUR UPGRADED APOLLO API IS WORKING!")
        print("="*70)
        
    else:
        print(f"\n❌ ERROR: Status {response.status_code}")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()

