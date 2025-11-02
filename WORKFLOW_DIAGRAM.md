# LeadOn CRM - Complete Workflow Diagram

## 🎯 User Journey: From Query to CRM

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER WRITES QUERY                            │
│  "Find CTOs at AI companies in San Francisco"                       │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    STEP 1: AI INTENT PARSING                         │
│  File: ai_agent/intent_parser.py                                    │
│  Function: IntentParser.parse_intent()                              │
│                                                                      │
│  Uses: OpenAI GPT-4o-mini with function calling                     │
│                                                                      │
│  Input:  "Find CTOs at AI companies in San Francisco"               │
│  Output: {                                                           │
│    "query": "CTO AI San Francisco",                                 │
│    "titles": ["CTO"],                                               │
│    "industries": ["AI"],                                            │
│    "locations": ["San Francisco, CA, USA"],                         │
│    "campaign_objective": "Find technical leaders",                  │
│    "max_results": 50                                                │
│  }                                                                   │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   STEP 2: APOLLO API SEARCH                          │
│  File: scrapers/apollo_scraper.py                                   │
│  Class: ApolloClient                                                │
│  Function: search_people()                                          │
│                                                                      │
│  API Call:                                                           │
│  POST https://api.apollo.io/api/v1/mixed_people/search              │
│  {                                                                   │
│    "person_titles": ["CTO"],                                        │
│    "person_locations": ["San Francisco, CA, USA"],                  │
│    "organization_industry_tag_ids": ["AI"],                         │
│    "per_page": 50                                                   │
│  }                                                                   │
│                                                                      │
│  Returns: SearchResult with Contact objects                         │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                  STEP 3: PARSE API RESPONSE                          │
│  File: scrapers/apollo_scraper.py                                   │
│  Function: _parse_people_response()                                 │
│                                                                      │
│  Converts Apollo JSON to Contact objects:                           │
│  Contact(                                                            │
│    name="John Doe",                                                 │
│    title="CTO",                                                     │
│    company="AI Startup Inc",                                        │
│    email="john@aistartup.com",                                      │
│    linkedin_url="https://linkedin.com/in/johndoe",                  │
│    city="San Francisco",                                            │
│    state="California",                                              │
│    source="apollo.io",                                              │
│    created_at=datetime.now()                                        │
│  )                                                                   │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│              STEP 4: SAVE TO CRM DATABASE                            │
│  File: crm_integration/chat_api.py                                  │
│  Variable: contacts_db (in-memory list)                             │
│                                                                      │
│  Deduplication Logic:                                               │
│  - Check if email already exists                                    │
│  - Check if LinkedIn URL already exists                             │
│  - Only add if new contact                                          │
│                                                                      │
│  Before: contacts_db = [100 contacts]                               │
│  After:  contacts_db = [123 contacts] (+23 new)                     │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│           STEP 5: SYNC TO TWENTY CRM (Background)                    │
│  File: crm_integration/twenty_sync.py                               │
│  Function: sync_apollo_to_twenty()                                  │
│                                                                      │
│  If TWENTY_CRM_API_TOKEN is set:                                    │
│  - Runs as background task (non-blocking)                           │
│  - Converts Contact to Twenty Person format                         │
│  - Creates people in batches of 10                                  │
│  - Handles errors gracefully                                        │
│                                                                      │
│  GraphQL Mutation:                                                   │
│  mutation CreatePerson {                                             │
│    createPerson(data: {                                             │
│      name: { firstName: "John", lastName: "Doe" }                   │
│      emails: { primaryEmail: "john@aistartup.com" }                 │
│      jobTitle: "CTO"                                                │
│      city: "San Francisco"                                          │
│    })                                                                │
│  }                                                                   │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│              STEP 6: GENERATE AI RESPONSE                            │
│  File: ai_agent/intent_parser.py                                    │
│  Function: generate_response()                                      │
│                                                                      │
│  Uses: OpenAI GPT-4o-mini                                           │
│                                                                      │
│  Input:                                                              │
│  - Intent: "Find technical leaders"                                 │
│  - Results: 23 contacts                                             │
│                                                                      │
│  Output:                                                             │
│  "Found 23 CTOs at AI companies in San Francisco! I've added        │
│   them to your CRM. (Data from Apollo.io)"                          │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    STEP 7: RETURN TO USER                            │
│  File: crm_integration/chat_api.py                                  │
│  Endpoint: POST /api/chat                                           │
│                                                                      │
│  Response: {                                                         │
│    "response": "Found 23 CTOs...",                                  │
│    "contacts_found": 23,                                            │
│    "contacts_added": 23,                                            │
│    "intent": {...},                                                 │
│    "timestamp": "2025-11-01T10:30:00Z"                              │
│  }                                                                   │
│                                                                      │
│  User sees: "Found 23 CTOs at AI companies in San Francisco!        │
│              I've added them to your CRM. (Data from Apollo.io)"    │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Data Flow Architecture

```
┌──────────────┐
│   Frontend   │  User types query
│   (Browser)  │
└──────┬───────┘
       │ HTTP POST /api/chat
       │ {"message": "Find CTOs..."}
       ▼
┌──────────────────────────────────────────────────────────┐
│                    FastAPI Backend                        │
│              (crm_integration/chat_api.py)               │
│                                                           │
│  ┌─────────────────────────────────────────────────┐    │
│  │  1. Parse Intent (OpenAI)                       │    │
│  │     IntentParser.parse_intent()                 │    │
│  └────────────────┬────────────────────────────────┘    │
│                   │                                       │
│  ┌────────────────▼────────────────────────────────┐    │
│  │  2. Search Apollo API                           │    │
│  │     ApolloClient.search_people()                │    │
│  │     - Titles: ["CTO"]                           │    │
│  │     - Locations: ["San Francisco"]              │    │
│  └────────────────┬────────────────────────────────┘    │
│                   │                                       │
│  ┌────────────────▼────────────────────────────────┐    │
│  │  3. Save to Database                            │    │
│  │     contacts_db.append(contact)                 │    │
│  │     - Deduplicate by email/LinkedIn             │    │
│  └────────────────┬────────────────────────────────┘    │
│                   │                                       │
│  ┌────────────────▼────────────────────────────────┐    │
│  │  4. Background: Sync to Twenty CRM              │    │
│  │     sync_apollo_to_twenty()                     │    │
│  └────────────────┬────────────────────────────────┘    │
│                   │                                       │
│  ┌────────────────▼────────────────────────────────┐    │
│  │  5. Generate Response (OpenAI)                  │    │
│  │     IntentParser.generate_response()            │    │
│  └────────────────┬────────────────────────────────┘    │
│                   │                                       │
└───────────────────┼───────────────────────────────────────┘
                    │ HTTP 200 OK
                    │ {"response": "Found 23...", ...}
                    ▼
            ┌──────────────┐
            │   Frontend   │  Display results
            │   (Browser)  │
            └──────────────┘
```

---

## 📊 Database Schema

### In-Memory Database (contacts_db)

```python
contacts_db: List[Contact] = [
    Contact(
        id="uuid-1",
        name="John Doe",
        title="CTO",
        company="AI Startup Inc",
        email="john@aistartup.com",
        linkedin_url="https://linkedin.com/in/johndoe",
        phone="+1-555-0123",
        city="San Francisco",
        state="California",
        country="USA",
        tags=["cto", "ai", "executive"],
        source="apollo.io",
        relationship_stage="new_lead",
        created_at="2025-11-01T10:30:00Z",
        last_updated="2025-11-01T10:30:00Z"
    ),
    # ... more contacts
]
```

### Twenty CRM Schema (GraphQL)

```graphql
type Person {
  id: ID!
  name: FullName!
  emails: Emails
  phones: Phones
  jobTitle: String
  city: String
  linkedinLink: Link
  company: Company
  createdAt: DateTime!
  updatedAt: DateTime!
}
```

---

## 🔑 Key Files and Their Roles

| File | Role | Key Functions |
|------|------|---------------|
| `crm_integration/chat_api.py` | Main API server | `POST /api/chat` - Main endpoint |
| `ai_agent/intent_parser.py` | AI intent parsing | `parse_intent()`, `generate_response()` |
| `scrapers/apollo_scraper.py` | Apollo API client | `search_people()`, `enrich_person()` |
| `scrapers/schemas.py` | Data models | `Contact`, `Organization`, `SearchResult` |
| `crm_integration/twenty_sync.py` | Twenty CRM sync | `sync_apollo_to_twenty()` |
| `cli/search_mock.py` | Mock data fallback | `load_mock_contacts()`, `filter_contacts()` |

---

## 🎮 API Endpoints

### POST /api/chat
**Main endpoint for natural language queries**

Request:
```json
{
  "message": "Find CTOs at AI companies in San Francisco",
  "website_url": null
}
```

Response:
```json
{
  "response": "Found 23 CTOs at AI companies in San Francisco! I've added them to your CRM.",
  "contacts_found": 23,
  "contacts_added": 23,
  "intent": {
    "query": "CTO AI San Francisco",
    "titles": ["CTO"],
    "industries": ["AI"],
    "locations": ["San Francisco, CA, USA"],
    "campaign_objective": "Find technical leaders",
    "max_results": 50
  },
  "timestamp": "2025-11-01T10:30:00Z"
}
```

### GET /api/contacts
**Get all contacts from database**

Query params:
- `limit`: Max contacts to return (default: 100)
- `tags`: Filter by tags (comma-separated)
- `title`: Filter by job title

### GET /api/stats
**Get CRM statistics**

Response:
```json
{
  "total_contacts": 150,
  "total_chats": 5,
  "tags": {"cto": 45, "ai": 67},
  "titles": {"CTO": 45, "CEO": 32},
  "companies": {"OpenAI": 5, "Anthropic": 4}
}
```

---

## 🚀 Quick Start Commands

```bash
# 1. Set up environment
cp .env.example .env
# Edit .env and add your API keys

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start the server
python crm_integration/chat_api.py

# 4. Test the integration
python test_apollo_integration.py

# 5. Make a test query
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Find CTOs at AI companies"}'
```

---

## ✅ Success Indicators

When everything is working correctly, you should see:

1. **Server startup**:
   ```
   ✅ OpenAI API:    Configured
   ✅ Apollo API:    Configured (real data)
   ✅ Twenty CRM:    Configured
   ```

2. **Query processing**:
   ```
   🔍 Using Apollo.io API to search for contacts...
   ✅ Found 23 contacts from Apollo.io API
   💾 Added 23 new contacts to database (total: 123)
   🔄 Syncing contacts to Twenty CRM...
   ```

3. **User response**:
   ```
   "Found 23 CTOs at AI companies in San Francisco! 
    I've added them to your CRM. (Data from Apollo.io)"
   ```

---

## 🎯 Next Steps

1. ✅ User writes query
2. ✅ AI parses intent
3. ✅ Apollo API fetches contacts
4. ✅ Contacts saved to database
5. ✅ Synced to Twenty CRM
6. 🔜 LinkedIn automation (next phase)
7. 🔜 Email campaigns (next phase)

