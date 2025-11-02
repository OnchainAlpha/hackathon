# 🚀 Twenty CRM Integration Guide

## Overview

This guide explains how to integrate your Apollo.io scraper with **Twenty CRM** - the open-source CRM you already have installed.

## Architecture

```
Apollo Scraper → Python Sync Service → Twenty CRM GraphQL API → Twenty CRM Database → Twenty CRM Frontend
```

### What We've Built

1. **`crm_integration/twenty_sync.py`** - Python service that syncs contacts to Twenty CRM
2. **GraphQL Integration** - Uses Twenty's native GraphQL API
3. **Data Mapping** - Maps Apollo Contact schema to Twenty Person schema
4. **Batch Operations** - Efficiently creates multiple contacts at once

## 🎯 Quick Start

### Step 1: Start Twenty CRM

```bash
cd CRM/twenty
yarn start
```

This will start:
- **Frontend**: http://localhost:3001
- **Backend API**: http://localhost:3000
- **GraphQL Playground**: http://localhost:3000/graphql

**Note**: First startup may take 5-10 minutes to:
- Install dependencies
- Set up PostgreSQL database
- Run migrations
- Start all services

### Step 2: Create Twenty CRM Account

1. Open http://localhost:3001
2. Click "Continue with Email"
3. Create your account
4. Complete onboarding

### Step 3: Get API Token

1. In Twenty CRM, go to **Settings** (⚙️ icon)
2. Click **API Keys** in the left sidebar
3. Click **+ Create API Key**
4. Name it "Apollo Scraper Integration"
5. Copy the generated token (starts with `apk_...`)

### Step 4: Configure Integration

Create or update `.env` file:

```bash
# Apollo.io API Key
APOLLO_API_KEY=F--Az_2MyIh9U0Gg_m4yZQ

# Twenty CRM API Token
TWENTY_CRM_API_TOKEN=apk_your_token_here

# Twenty CRM API URL
TWENTY_CRM_API_URL=http://localhost:3000/graphql
```

### Step 5: Sync Contacts

```bash
# Sync mock contacts to Twenty CRM
python crm_integration/twenty_sync.py

# Or use the integrated API
python -m crm_integration.api
```

## 📊 Data Mapping

### Apollo Contact → Twenty Person

| Apollo Field | Twenty Field | Notes |
|-------------|-------------|-------|
| `name` | `name.firstName` + `name.lastName` | Split on first space |
| `email` | `emails.primaryEmail` | |
| `phone` | `phones.primaryPhoneNumber` | Cleaned format |
| `title` | `jobTitle` | |
| `city` | `city` | |
| `linkedin_url` | `linkedinLink.primaryLinkUrl` | |
| `company` | `companyId` | Need to create/find company first |

### Custom Fields Needed

To store Apollo-specific data, we need to add custom fields to the Person object:

1. **Tags** (Multi-select) - investor, ai, vc, etc.
2. **Source** (Text) - apollo.io, manual, etc.
3. **Relationship Stage** (Select) - new_lead, contacted, connected, etc.

## 🔧 Adding Custom Fields

### Via Twenty CRM UI

1. Go to **Settings** > **Data Model**
2. Click on **Person** object
3. Click **+ Add Field**
4. Add these fields:

**Field 1: Tags**
- Name: `tags`
- Type: `Multi-select`
- Options: investor, ai, vc, tech, startup, fundraising_target

**Field 2: Source**
- Name: `source`
- Type: `Text`
- Default: `apollo.io`

**Field 3: Relationship Stage**
- Name: `relationshipStage`
- Type: `Select`
- Options: new_lead, contacted, connected, meeting_scheduled, opportunity, customer

### Via GraphQL API

```python
from crm_integration.twenty_sync import TwentyCRMSync

sync = TwentyCRMSync(api_token="your_token")

# Add Tags field
sync._execute_graphql("""
mutation CreateField {
    createOneField(input: {
        field: {
            name: "tags"
            label: "Tags"
            type: MULTI_SELECT
            objectMetadataId: "person_object_id"
            options: [
                {value: "investor", label: "Investor", color: "blue"}
                {value: "ai", label: "AI", color: "purple"}
                {value: "vc", label: "VC", color: "green"}
                {value: "tech", label: "Tech", color: "orange"}
            ]
        }
    }) {
        id
        name
        type
    }
}
""")
```

## 🔄 Synchronization Workflow

### Manual Sync

```python
from crm_integration.twenty_sync import sync_apollo_to_twenty
from scrapers.schemas import Contact
import json

# Load contacts from Apollo scraper
with open('exports/demo_contacts.json', 'r') as f:
    data = json.load(f)
    contacts = [Contact(**c) for c in data]

# Sync to Twenty CRM
sync_apollo_to_twenty(contacts, api_token="your_token")
```

### Automatic Sync (via FastAPI)

Update `crm_integration/api.py` to sync to Twenty CRM:

```python
from crm_integration.twenty_sync import TwentyCRMSync
import os

# Initialize Twenty CRM sync
twenty_sync = TwentyCRMSync(
    api_token=os.getenv("TWENTY_CRM_API_TOKEN")
)

@app.post("/api/contacts/search")
async def search_contacts(request: SearchRequest):
    # ... existing search logic ...
    
    # Sync results to Twenty CRM
    if request.sync_to_twenty:
        for contact in results:
            twenty_sync.create_person(contact)
    
    return SearchResponse(contacts=results, ...)
```

## 🎨 Customizing Twenty CRM

### Add Custom Views

1. Go to **People** page
2. Click **Views** dropdown
3. Create custom views:
   - "Investors" - Filter by tags contains "investor"
   - "AI Contacts" - Filter by tags contains "ai"
   - "New Leads" - Filter by relationshipStage = "new_lead"

### Add Custom Fields to Table

1. In People view, click **⚙️ Settings**
2. Click **Fields**
3. Drag and drop to reorder
4. Toggle visibility for:
   - Tags
   - Source
   - Relationship Stage
   - LinkedIn Link

### Create Kanban Board

1. Go to **People** page
2. Click **View Type** > **Kanban**
3. Group by: **Relationship Stage**
4. Now you can drag contacts between stages!

## 🤖 Integration with LinkedIn Automation

### Track Actions in Twenty CRM

Twenty CRM has built-in activity tracking. Use it for LinkedIn actions:

```python
from crm_integration.twenty_sync import TwentyCRMSync

sync = TwentyCRMSync(api_token="your_token")

# Log LinkedIn action as activity
mutation = """
mutation CreateActivity($data: ActivityCreateInput!) {
    createActivity(data: $data) {
        id
        title
        body
        type
        createdAt
    }
}
"""

variables = {
    "data": {
        "title": "LinkedIn Connection Request Sent",
        "body": "Sent connection request with message: 'Hi, I'd love to connect!'",
        "type": "NOTE",
        "assigneeId": "person_id_here"
    }
}

sync._execute_graphql(mutation, variables)
```

## 📈 Complete Workflow Example

```python
import os
from crm_integration.twenty_sync import TwentyCRMSync, sync_apollo_to_twenty
from scrapers.apollo_scraper import ApolloClient
from cli.search_mock import filter_contacts
import json

# 1. Search for contacts (using mock data for now)
with open('exports/demo_contacts.json', 'r') as f:
    all_contacts = json.load(f)

# Filter for AI investors
ai_investors = filter_contacts(
    all_contacts,
    query="AI",
    tags=["investor"]
)

print(f"Found {len(ai_investors)} AI investors")

# 2. Sync to Twenty CRM
api_token = os.getenv("TWENTY_CRM_API_TOKEN")
sync_apollo_to_twenty(ai_investors, api_token)

# 3. View in Twenty CRM
print("✅ Contacts synced! View them at: http://localhost:3001/objects/people")

# 4. LinkedIn automation can now read from Twenty CRM
sync = TwentyCRMSync(api_token=api_token)
people = sync.search_people(query="AI", limit=10)

for person in people:
    linkedin_url = person.get("linkedinLink", {}).get("primaryLinkUrl")
    if linkedin_url:
        print(f"🔗 {person['name']['firstName']} {person['name']['lastName']}: {linkedin_url}")
        # ... perform LinkedIn automation ...
```

## 🐛 Troubleshooting

### Twenty CRM won't start

**Issue**: `yarn start` fails

**Solutions**:
1. Check if PostgreSQL is running
2. Check if Redis is running
3. Try: `yarn install` first
4. Check logs in `CRM/twenty/packages/twenty-server/logs/`

### GraphQL authentication errors

**Issue**: `401 Unauthorized`

**Solutions**:
1. Verify API token is correct
2. Check token hasn't expired
3. Regenerate token in Twenty CRM settings

### Contacts not appearing

**Issue**: Sync succeeds but contacts don't show

**Solutions**:
1. Refresh Twenty CRM page
2. Check if contacts are in "Deleted" view
3. Verify workspace ID matches
4. Check GraphQL response for errors

### Database connection errors

**Issue**: `ECONNREFUSED` or database errors

**Solutions**:
1. Ensure PostgreSQL is running: `docker ps` or check services
2. Check database credentials in `.env`
3. Run migrations: `cd CRM/twenty && npx nx database:reset twenty-server`

## 🎉 Benefits of Using Twenty CRM

### vs. Building Custom CRM

✅ **Professional UI** - Beautiful, modern interface out of the box
✅ **Built-in Features** - Activities, tasks, notes, email sync
✅ **Customizable** - Add fields, objects, views without coding
✅ **Open Source** - No vendor lock-in, full control
✅ **Active Development** - Regular updates and improvements
✅ **GraphQL API** - Modern, flexible API
✅ **Multi-user** - Team collaboration built-in
✅ **Mobile Responsive** - Works on all devices

### vs. Other CRMs

✅ **Free** - No per-user pricing
✅ **Self-hosted** - Your data stays with you
✅ **Extensible** - Full API access
✅ **Modern Stack** - React, NestJS, PostgreSQL
✅ **Fast** - Optimized performance

## 📚 Next Steps

1. **Start Twenty CRM**: `cd CRM/twenty && yarn start`
2. **Create Account**: http://localhost:3001
3. **Get API Token**: Settings > API Keys
4. **Add Custom Fields**: Settings > Data Model > Person
5. **Sync Contacts**: `python crm_integration/twenty_sync.py`
6. **View Contacts**: http://localhost:3001/objects/people
7. **Customize Views**: Create filters for investors, AI contacts, etc.
8. **Integrate LinkedIn Bot**: Use Twenty's API to read contacts and log actions

## 🔗 Resources

- **Twenty CRM Docs**: https://docs.twenty.com
- **GraphQL API**: http://localhost:3000/graphql
- **GitHub**: https://github.com/twentyhq/twenty
- **Discord**: https://discord.gg/cx5n4Jzs57

---

**You now have a production-ready CRM integrated with your Apollo scraper!** 🎉

