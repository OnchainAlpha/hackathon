"""
Test script to verify Twenty CRM connection
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

def print_header(text):
    """Print a formatted header"""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70)


def test_twenty_connection():
    """Test connection to Twenty CRM"""
    print_header("Twenty CRM Connection Test")
    
    # Check if token is set
    token = os.getenv("TWENTY_CRM_API_TOKEN")
    url = os.getenv("TWENTY_CRM_API_URL")
    
    if not token:
        print("\n❌ TWENTY_CRM_API_TOKEN not set in .env file")
        print("\nTo get your token:")
        print("1. Go to https://app.twenty.com (or your self-hosted instance)")
        print("2. Settings → Developers → API Keys")
        print("3. Create API Key")
        print("4. Add to .env: TWENTY_CRM_API_TOKEN=your_token_here")
        print("\nSee TWENTY_CRM_SETUP.md for detailed instructions.")
        return False
    
    if not url:
        print("\n❌ TWENTY_CRM_API_URL not set in .env file")
        print("\nAdd to .env:")
        print("TWENTY_CRM_API_URL=https://api.twenty.com/graphql")
        print("(or your self-hosted instance URL)")
        return False
    
    print(f"\n✓ Token found: {token[:20]}...")
    print(f"✓ URL: {url}")
    
    # Test connection with a simple query
    print("\n🔍 Testing connection...")
    
    query = """
    query {
        currentUser {
            id
            email
            firstName
            lastName
        }
    }
    """
    
    try:
        response = requests.post(
            url,
            json={"query": query},
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            },
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            
            if "errors" in data:
                print(f"\n❌ GraphQL Error:")
                for error in data["errors"]:
                    print(f"   {error.get('message', 'Unknown error')}")
                return False
            
            if "data" in data and data["data"].get("currentUser"):
                user = data["data"]["currentUser"]
                print(f"\n✅ Connection successful!")
                print(f"\n   User ID: {user.get('id')}")
                print(f"   Email: {user.get('email')}")
                print(f"   Name: {user.get('firstName', '')} {user.get('lastName', '')}")
                return True
            else:
                print(f"\n❌ Unexpected response format:")
                print(f"   {data}")
                return False
        
        elif response.status_code == 401:
            print(f"\n❌ Authentication failed (401 Unauthorized)")
            print(f"   Your token may be invalid or expired.")
            print(f"   Try creating a new API key in Twenty CRM.")
            return False
        
        elif response.status_code == 404:
            print(f"\n❌ Endpoint not found (404)")
            print(f"   Check your TWENTY_CRM_API_URL")
            print(f"   Current: {url}")
            print(f"   Should be: https://api.twenty.com/graphql")
            return False
        
        else:
            print(f"\n❌ HTTP Error {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"\n❌ Connection Error")
        print(f"   Could not connect to {url}")
        print(f"   Check:")
        print(f"   - Is the URL correct?")
        print(f"   - Is Twenty CRM running?")
        print(f"   - Is your internet connection working?")
        return False
    
    except requests.exceptions.Timeout:
        print(f"\n❌ Timeout")
        print(f"   Request to {url} timed out")
        return False
    
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_create_person():
    """Test creating a person in Twenty CRM"""
    print_header("Test Creating a Person")
    
    token = os.getenv("TWENTY_CRM_API_TOKEN")
    url = os.getenv("TWENTY_CRM_API_URL")
    
    if not token or not url:
        print("\n⚠️  Skipping (Twenty CRM not configured)")
        return False
    
    print("\n🔍 Attempting to create a test person...")
    
    mutation = """
    mutation CreatePerson($data: PersonCreateInput!) {
        createPerson(data: $data) {
            id
            name {
                firstName
                lastName
            }
            emails {
                primaryEmail
            }
            jobTitle
        }
    }
    """
    
    variables = {
        "data": {
            "name": {
                "firstName": "Test",
                "lastName": "Contact"
            },
            "emails": {
                "primaryEmail": "test@example.com"
            },
            "jobTitle": "Test Engineer"
        }
    }
    
    try:
        response = requests.post(
            url,
            json={"query": mutation, "variables": variables},
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            },
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            
            if "errors" in data:
                print(f"\n⚠️  GraphQL Error (this is normal if schema is different):")
                for error in data["errors"]:
                    print(f"   {error.get('message', 'Unknown error')}")
                print(f"\n   Note: This might be due to schema differences.")
                print(f"   The sync code will handle this automatically.")
                return False
            
            if "data" in data and data["data"].get("createPerson"):
                person = data["data"]["createPerson"]
                print(f"\n✅ Successfully created test person!")
                print(f"   ID: {person.get('id')}")
                print(f"   Name: {person.get('name', {}).get('firstName')} {person.get('name', {}).get('lastName')}")
                print(f"   Email: {person.get('emails', {}).get('primaryEmail')}")
                print(f"   Title: {person.get('jobTitle')}")
                return True
            else:
                print(f"\n⚠️  Unexpected response:")
                print(f"   {data}")
                return False
        else:
            print(f"\n❌ HTTP Error {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False


def main():
    """Run all tests"""
    print("\n" + "🔧 Twenty CRM Connection Test Suite".center(70))
    
    # Check environment
    print_header("Environment Check")
    print(f"   Apollo API:  {'✅ Configured' if os.getenv('APOLLO_API_KEY') else '❌ Not configured'}")
    print(f"   OpenAI API:  {'✅ Configured' if os.getenv('OPENAI_API_KEY') else '❌ Not configured'}")
    print(f"   Twenty CRM:  {'✅ Configured' if os.getenv('TWENTY_CRM_API_TOKEN') else '❌ Not configured'}")
    
    # Test connection
    connection_ok = test_twenty_connection()
    
    # Test creating a person (only if connection works)
    if connection_ok:
        test_create_person()
    
    # Summary
    print_header("Summary")
    
    if connection_ok:
        print("\n✅ Twenty CRM is properly configured!")
        print("\nYou can now:")
        print("1. Start the server: python crm_integration/chat_api.py")
        print("2. Search for contacts")
        print("3. Contacts will automatically sync to Twenty CRM")
    else:
        print("\n⚠️  Twenty CRM is not configured or connection failed")
        print("\nOptions:")
        print("1. Configure Twenty CRM (see TWENTY_CRM_SETUP.md)")
        print("2. Or skip it - the system works fine without Twenty CRM!")
        print("   Contacts will be saved locally and accessible via API")
    
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    main()

