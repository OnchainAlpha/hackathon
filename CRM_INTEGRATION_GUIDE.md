# 🚀 LeadOn CRM Integration Guide

## Overview

Your Apollo.io scraper is now fully integrated with a custom CRM system! When you search for contacts, they're automatically stored and managed in the CRM.

## 🎯 What's Been Built

### 1. **FastAPI Backend** (`crm_integration/api.py`)
- RESTful API for contact management
- Automatic integration with Apollo scraper
- Search, create, update, delete contacts
- Action logging for LinkedIn automation
- Statistics and analytics

### 2. **Web Frontend** (`crm_integration/frontend/index.html`)
- Beautiful, modern UI
- Real-time contact search
- Visual contact cards
- Statistics dashboard
- Direct links to LinkedIn and email

### 3. **Mock Data Integration**
- Uses the 50 generated contacts
- Filters by query, titles, companies, locations, tags
- Ready for Apollo.io API when you upgrade

## 🚀 Quick Start

### Start the CRM Server

**Option 1: Using the batch file (Windows)**
```bash
start_crm.bat
```

**Option 2: Using Python directly**
```bash
python crm_integration/api.py
```

**Option 3: Using uvicorn**
```bash
uvicorn crm_integration.api:app --reload --host 0.0.0.0 --port 8000
```

### Access the CRM

Once started, open your browser to:

- **Frontend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/health
- **Statistics**: http://localhost:8000/api/stats

## 📊 Features

### Contact Search
- **Query**: General search across name, title, company, tags
- **Titles**: Filter by job titles (CEO, CTO, etc.)
- **Companies**: Filter by company names
- **Locations**: Filter by city/state
- **Tags**: Filter by tags (investor, ai, vc, etc.)

### Contact Management
- **View All Contacts**: Browse all contacts with pagination
- **View Single Contact**: Get detailed contact information
- **Create Contact**: Add new contacts manually
- **Update Contact**: Modify existing contacts
- **Delete Contact**: Remove contacts

### Action Logging
- **Log Actions**: Track LinkedIn automation actions
- **View Actions**: See all actions for a contact
- **Filter Actions**: Filter by action type

### Statistics
- **Total Contacts**: Count of all contacts
- **Total Actions**: Count of all logged actions
- **Top Companies**: Most common companies
- **Top Locations**: Most common locations
- **Top Tags**: Most common tags

## 🔌 API Endpoints

### Contact Endpoints

#### Search Contacts
```http
POST /api/contacts/search
Content-Type: application/json

{
  "query": "AI",
  "titles": ["CEO", "CTO"],
  "companies": ["Anthropic", "OpenAI"],
  "locations": ["San Francisco"],
  "tags": ["investor"],
  "limit": 25,
  "use_mock": true
}
```

#### Get All Contacts
```http
GET /api/contacts?skip=0&limit=100&tags=investor,ai
```

#### Get Single Contact
```http
GET /api/contacts/{contact_id}
```

#### Create Contact
```http
POST /api/contacts
Content-Type: application/json

{
  "name": "John Doe",
  "title": "CEO",
  "company": "Acme Corp",
  "email": "john@acme.com",
  "linkedin_url": "https://linkedin.com/in/johndoe",
  "phone": "+1234567890",
  "city": "San Francisco",
  "state": "CA",
  "country": "USA",
  "tags": ["ceo", "tech"],
  "source": "manual",
  "relationship_stage": "new_lead"
}
```

#### Update Contact
```http
PUT /api/contacts/{contact_id}
Content-Type: application/json

{
  "name": "John Doe",
  "relationship_stage": "contacted"
}
```

#### Delete Contact
```http
DELETE /api/contacts/{contact_id}
```

### Action Endpoints

#### Log Action
```http
POST /api/actions
Content-Type: application/json

{
  "contact_id": "john-doe",
  "action_type": "connection_request_sent",
  "action_details": {
    "message": "Hi John, I'd love to connect!",
    "platform": "linkedin"
  },
  "timestamp": "2025-11-01T10:00:00Z",
  "status": "completed"
}
```

#### Get Actions
```http
GET /api/actions?contact_id=john-doe&action_type=connection_request_sent&limit=100
```

### Utility Endpoints

#### Health Check
```http
GET /api/health
```

#### Statistics
```http
GET /api/stats
```

#### Import Mock Data
```http
POST /api/import/mock
```

## 🔄 Integration with Apollo Scraper

### Automatic Integration

When you search using the frontend or API, contacts are automatically:
1. ✅ Searched from mock data (or Apollo.io API if upgraded)
2. ✅ Stored in the CRM database
3. ✅ Deduplicated (no duplicates by email/LinkedIn)
4. ✅ Tagged and categorized
5. ✅ Available for LinkedIn automation

### Manual Integration

You can also integrate programmatically:

```python
import requests

# Search contacts
response = requests.post('http://localhost:8000/api/contacts/search', json={
    "query": "AI CEO",
    "limit": 10,
    "use_mock": True
})

contacts = response.json()['contacts']

# Add to CRM
for contact in contacts:
    requests.post('http://localhost:8000/api/contacts', json=contact)
```

## 🤖 Integration with LinkedIn Automation

Your LinkedIn automation bot (Team 3) can now:

### 1. Get Contacts to Automate
```python
import requests

# Get all investors
response = requests.get('http://localhost:8000/api/contacts?tags=investor&limit=50')
contacts = response.json()

for contact in contacts:
    # Perform LinkedIn actions
    linkedin_url = contact['linkedin_url']
    # ... automation code ...
```

### 2. Log Actions
```python
import requests
from datetime import datetime

# After performing an action
requests.post('http://localhost:8000/api/actions', json={
    "contact_id": "john-doe",
    "action_type": "connection_request_sent",
    "action_details": {
        "message": "Hi John, I'd love to connect!",
        "platform": "linkedin"
    },
    "timestamp": datetime.now().isoformat(),
    "status": "completed"
})
```

### 3. Update Contact Status
```python
import requests

# Update relationship stage
contact = requests.get('http://localhost:8000/api/contacts/john-doe').json()
contact['relationship_stage'] = 'contacted'

requests.put('http://localhost:8000/api/contacts/john-doe', json=contact)
```

## 📈 Workflow Example

### Complete Sales Workflow

```python
import requests

# 1. Search for AI investors
search_response = requests.post('http://localhost:8000/api/contacts/search', json={
    "query": "AI",
    "tags": ["investor"],
    "limit": 20,
    "use_mock": True
})

contacts = search_response.json()['contacts']

# 2. For each contact, perform LinkedIn automation
for contact in contacts:
    contact_id = contact['name'].lower().replace(' ', '-')
    
    # Day 1: Like post
    requests.post('http://localhost:8000/api/actions', json={
        "contact_id": contact_id,
        "action_type": "post_liked",
        "action_details": {"platform": "linkedin"},
        "timestamp": "2025-11-01T10:00:00Z",
        "status": "completed"
    })
    
    # Day 2: Comment on post
    requests.post('http://localhost:8000/api/actions', json={
        "contact_id": contact_id,
        "action_type": "comment_posted",
        "action_details": {
            "comment": "Great insights!",
            "platform": "linkedin"
        },
        "timestamp": "2025-11-02T10:00:00Z",
        "status": "completed"
    })
    
    # Day 3: Send connection request
    requests.post('http://localhost:8000/api/actions', json={
        "contact_id": contact_id,
        "action_type": "connection_request_sent",
        "action_details": {
            "message": f"Hi {contact['name']}, I'd love to connect!",
            "platform": "linkedin"
        },
        "timestamp": "2025-11-03T10:00:00Z",
        "status": "completed"
    })
    
    # Update contact status
    contact['relationship_stage'] = 'contacted'
    requests.put(f'http://localhost:8000/api/contacts/{contact_id}', json=contact)

# 3. View statistics
stats = requests.get('http://localhost:8000/api/stats').json()
print(f"Total contacts: {stats['total_contacts']}")
print(f"Total actions: {stats['total_actions']}")
```

## 🎨 Customizing the Frontend

The frontend is a single HTML file with embedded CSS and JavaScript. You can customize:

### Colors
Edit the CSS gradient in `crm_integration/frontend/index.html`:
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

### Fields
Add more search fields in the form:
```html
<div class="form-group">
    <label for="industry">Industry</label>
    <input type="text" id="industry" placeholder="e.g., AI, SaaS">
</div>
```

### Contact Card Layout
Modify the contact card template in the JavaScript:
```javascript
grid.innerHTML = contacts.map(contact => `
    <div class="contact-card">
        <!-- Your custom layout -->
    </div>
`).join('');
```

## 🔐 Security Notes

### Current Setup (Development)
- ⚠️ No authentication
- ⚠️ CORS allows all origins
- ⚠️ In-memory storage (data lost on restart)

### Production Recommendations
1. **Add Authentication**: JWT tokens, API keys
2. **Restrict CORS**: Only allow your frontend domain
3. **Use Real Database**: PostgreSQL, MongoDB
4. **Add Rate Limiting**: Prevent abuse
5. **Use HTTPS**: Encrypt traffic
6. **Add Logging**: Track all API calls
7. **Input Validation**: Sanitize all inputs

## 📦 Database Migration (Future)

To use a real database instead of in-memory storage:

### Option 1: SQLite (Simple)
```python
import sqlite3

# Replace contacts_db list with SQLite
conn = sqlite3.connect('leadon_crm.db')
```

### Option 2: PostgreSQL (Production)
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://user:pass@localhost/leadon_crm')
Session = sessionmaker(bind=engine)
```

### Option 3: Twenty CRM (Advanced)
Integrate with the Twenty CRM GraphQL API for full CRM features.

## 🐛 Troubleshooting

### Server won't start
```bash
# Check if port 8000 is in use
netstat -ano | findstr :8000

# Kill the process
taskkill /PID <process_id> /F

# Try a different port
python crm_integration/api.py --port 8001
```

### Frontend not loading
- Check that `crm_integration/frontend/index.html` exists
- Try accessing http://localhost:8000/docs instead
- Check browser console for errors

### CORS errors
- Make sure API is running on localhost:8000
- Check browser console for specific error
- Try disabling browser extensions

### Mock data not loading
```bash
# Regenerate mock data
python create_mock_contacts.py demo

# Reimport via API
curl -X POST http://localhost:8000/api/import/mock
```

## 📚 Next Steps

1. **Test the Integration**: Search for contacts and verify they appear
2. **Customize the Frontend**: Match your branding
3. **Integrate LinkedIn Bot**: Connect Team 3's automation
4. **Add Real Database**: For persistence
5. **Deploy**: Host on Heroku, AWS, or DigitalOcean
6. **Upgrade Apollo.io**: Get real contact data

## 🎉 You're Ready!

Your CRM is now fully integrated with the Apollo scraper. When you search for contacts, they're automatically managed in the CRM and ready for LinkedIn automation!

**Start the server and open http://localhost:8000 to see it in action!**

