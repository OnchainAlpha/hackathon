# 💬 Chat-Based CRM Guide

## Overview

Your new **conversational CRM interface** where you describe what you want in natural language, and the AI automatically scrapes and populates your CRM!

## 🎯 How It Works

```
┌─────────────────────────────────────────┐
│  💬 Chat Interface                      │
│  ─────────────────────────────────────  │
│  "Find CTOs at AI companies in SF"     │
│                                         │
│  AI: "Found 23 contacts! Added to CRM" │
└─────────────────────────────────────────┘
           ↓
    AI parses intent
           ↓
    Scrapes contacts
           ↓
┌─────────────────────────────────────────┐
│  📊 CRM Table                           │
│  ─────────────────────────────────────  │
│  ☑ John Smith - CTO - OpenAI           │
│  ☑ Sarah Lee - CTO - Anthropic         │
│  ☑ Mike Chen - CTO - Scale AI          │
│                                         │
│  [Select All] [Start Campaign] →       │
└─────────────────────────────────────────┘
```

## 🚀 Quick Start

### 1. Start the Chat CRM

```bash
# Option 1: Use the batch file
start_chat_crm.bat

# Option 2: Manual
python crm_integration/chat_api.py
```

### 2. Open in Browser

Navigate to: **http://localhost:8000**

### 3. Start Searching!

Type natural language queries like:
- "Find CTOs at AI companies in San Francisco"
- "Get investors in the FinTech space"
- "Partnership outreach to SaaS CEOs in New York"
- "Find VPs of Sales at Series B startups"

## 💡 Example Queries

### By Job Title
```
"Find CEOs at tech companies"
"Get CTOs and VPs of Engineering"
"Search for founders in the AI space"
```

### By Industry
```
"Find contacts in the FinTech industry"
"Get people at AI companies"
"Search SaaS executives"
```

### By Location
```
"Find CTOs in San Francisco"
"Get investors in New York"
"Search for founders in Austin"
```

### By Campaign Objective
```
"Partnership outreach to SaaS CEOs"
"Fundraising campaign for VC investors"
"Sales outreach to enterprise CTOs"
```

### Combined Queries
```
"Find CTOs at AI companies in San Francisco for partnership campaign"
"Get Series B investors in FinTech for fundraising"
"Search for VPs of Sales at SaaS companies in New York for sales outreach"
```

## 🏗️ Architecture

### Components

1. **Chat Interface** (`crm_integration/frontend/chat_crm.html`)
   - Beautiful, modern UI
   - Natural language input
   - Real-time responses
   - CRM table with selection

2. **AI Agent** (`ai_agent/intent_parser.py`)
   - Parses natural language using GPT-4
   - Extracts search parameters
   - Generates friendly responses
   - Fallback mode without OpenAI

3. **Scraper Orchestrator** (`ai_agent/intent_parser.py`)
   - Routes to appropriate scraper
   - Apollo.io integration
   - Website scraper (future)
   - Job board scraper (future)

4. **FastAPI Backend** (`crm_integration/chat_api.py`)
   - RESTful API
   - Chat endpoint
   - Contacts management
   - Statistics

5. **Twenty CRM Integration** (`crm_integration/twenty_sync.py`)
   - Syncs contacts to Twenty CRM
   - GraphQL API integration
   - Background sync

### Data Flow

```
User Input → AI Parser → Scraper → Local Storage → Twenty CRM
                ↓
         AI Response → User
```

## 🔧 Configuration

### Environment Variables

Create or update `.env`:

```bash
# OpenAI API Key (for AI parsing)
OPENAI_API_KEY=sk-your-key-here

# Apollo.io API Key (for real scraping)
APOLLO_API_KEY=your-apollo-key

# Twenty CRM API Token (for CRM sync)
TWENTY_CRM_API_TOKEN=apk_your-token-here

# Twenty CRM API URL
TWENTY_CRM_API_URL=http://localhost:3000/graphql
```

### Without OpenAI

The system works without OpenAI using a simple keyword-based parser:
- Extracts job titles (CEO, CTO, VP, etc.)
- Identifies industries (AI, SaaS, FinTech, etc.)
- Recognizes tags (investor, vc, etc.)

### Without Twenty CRM

The system stores contacts in memory and displays them in the web interface. You can still:
- Search for contacts
- View in CRM table
- Select contacts
- Export data

## 📊 Features

### Chat Interface

- **Natural Language Input**: Describe what you want in plain English
- **AI-Powered Parsing**: Automatically extracts search parameters
- **Real-Time Responses**: Get instant feedback
- **Website URL Support**: Optionally provide a website to scrape

### CRM Table

- **Contact Management**: View all contacts in a table
- **Bulk Selection**: Select individual or all contacts
- **Filtering**: Filter by tags, titles, companies
- **Statistics**: See total contacts, companies, selected count
- **LinkedIn Links**: Direct links to LinkedIn profiles
- **Email Display**: Contact emails for outreach

### Campaign Management

- **Select Contacts**: Choose which contacts to target
- **Start Campaign**: Launch LinkedIn automation
- **Track Progress**: Monitor campaign status (coming soon)

## 🎨 UI Features

### Chat Section

- Clean, modern design
- Gradient background
- Responsive layout
- Loading states
- Success animations

### CRM Table

- Sortable columns
- Hover effects
- Checkbox selection
- Tag badges with colors
- LinkedIn links
- Email display

### Statistics Bar

- Total contacts count
- Selected contacts count
- Unique companies count
- Real-time updates

## 🔄 Integration with Twenty CRM

### Automatic Sync

When Twenty CRM is configured, contacts are automatically synced in the background:

1. User searches via chat
2. Contacts are found and displayed
3. Background task syncs to Twenty CRM
4. Contacts appear in Twenty CRM UI

### Manual Sync

You can also manually sync contacts:

```python
from crm_integration.twenty_sync import sync_apollo_to_twenty
from scrapers.schemas import Contact

# Load contacts
contacts = [...]  # Your contacts

# Sync to Twenty CRM
sync_apollo_to_twenty(contacts, api_token="your_token")
```

### View in Twenty CRM

1. Start Twenty CRM: `cd CRM/twenty && yarn start`
2. Open: http://localhost:3001
3. Navigate to: People
4. See your synced contacts!

## 🤖 AI Intent Parsing

### How It Works

The AI agent uses GPT-4 to understand your intent:

**Input**: "Find CTOs at AI companies in San Francisco for partnership campaign"

**Parsed Intent**:
```json
{
  "query": "CTOs at AI companies in San Francisco",
  "titles": ["CTO"],
  "industries": ["AI"],
  "locations": ["San Francisco"],
  "tags": ["partnership"],
  "campaign_objective": "partnership campaign",
  "scraper_type": "apollo",
  "max_results": 50
}
```

**Output**: "I found 23 CTOs at AI companies in San Francisco. Added to your CRM for partnership outreach!"

### Supported Parameters

- **Titles**: CEO, CTO, VP, Founder, etc.
- **Industries**: AI, SaaS, FinTech, etc.
- **Locations**: Cities, states, countries
- **Companies**: Specific company names
- **Tags**: investor, vc, fundraising, partnership, etc.
- **Campaign Objective**: What you want to achieve

## 📈 API Endpoints

### POST /api/chat

Send a chat message and get contacts.

**Request**:
```json
{
  "message": "Find CTOs at AI companies in SF",
  "website_url": "https://example.com" // optional
}
```

**Response**:
```json
{
  "response": "Found 23 contacts! Added to CRM.",
  "contacts_found": 23,
  "contacts_added": 23,
  "intent": {...},
  "timestamp": "2025-11-01T10:00:00"
}
```

### GET /api/contacts

Get all contacts from CRM.

**Query Params**:
- `limit`: Max contacts to return (default: 100)
- `tags`: Filter by tags (comma-separated)
- `title`: Filter by job title

**Response**:
```json
{
  "contacts": [...],
  "total": 50,
  "timestamp": "2025-11-01T10:00:00"
}
```

### GET /api/stats

Get CRM statistics.

**Response**:
```json
{
  "total_contacts": 50,
  "total_chats": 5,
  "tags": {"investor": 10, "ai": 15, ...},
  "titles": {"CEO": 20, "CTO": 15, ...},
  "companies": {"OpenAI": 5, "Anthropic": 3, ...}
}
```

### GET /api/chat/history

Get chat history.

**Response**:
```json
{
  "history": [...],
  "total": 5
}
```

## 🎯 Workflow Example

### 1. User Searches

```
User: "Find CTOs at AI companies in San Francisco for partnership campaign"
```

### 2. AI Parses Intent

```json
{
  "titles": ["CTO"],
  "industries": ["AI"],
  "locations": ["San Francisco"],
  "campaign_objective": "partnership campaign"
}
```

### 3. System Scrapes

- Searches Apollo.io (or mock data)
- Filters by criteria
- Returns 23 contacts

### 4. Contacts Added to CRM

- Displayed in table
- Synced to Twenty CRM (if configured)
- Ready for selection

### 5. User Selects Contacts

- Clicks checkboxes
- Selects 15 contacts

### 6. User Starts Campaign

- Clicks "Start Campaign"
- LinkedIn automation begins
- Connection requests sent
- Messages sent
- Responses tracked

## 🚀 Next Steps

### For Hackathon Demo

1. **Start the Chat CRM**: `start_chat_crm.bat`
2. **Open in browser**: http://localhost:8000
3. **Demo the chat**: Show natural language queries
4. **Show the CRM**: Display contacts in table
5. **Select contacts**: Demonstrate bulk selection
6. **Explain campaign**: Show how LinkedIn automation works

### For Production

1. **Configure OpenAI**: Add API key to `.env`
2. **Upgrade Apollo.io**: Get paid plan for real API access
3. **Start Twenty CRM**: Set up PostgreSQL and start Twenty
4. **Get API Token**: Create token in Twenty CRM settings
5. **Configure sync**: Add token to `.env`
6. **Test integration**: Search and verify sync to Twenty
7. **Add LinkedIn bot**: Integrate Team 3's automation
8. **Deploy**: Host on cloud (AWS, GCP, Azure)

## 🎉 Benefits

### vs. Traditional CRM

✅ **Natural Language**: No complex forms or filters
✅ **AI-Powered**: Understands intent automatically
✅ **Fast**: Find contacts in seconds
✅ **Integrated**: Scraping + CRM in one interface
✅ **Modern UI**: Beautiful, responsive design

### vs. Manual Scraping

✅ **Automated**: No manual copy-paste
✅ **Structured**: Data in consistent format
✅ **Deduplicated**: No duplicate contacts
✅ **Enriched**: Complete contact information
✅ **Actionable**: Ready for campaigns

## 📚 Documentation

- **`CHAT_CRM_GUIDE.md`** - This guide
- **`TWENTY_CRM_INTEGRATION.md`** - Twenty CRM integration
- **`HACKATHON_QUICK_START.md`** - Quick start for hackathon
- **`README_APOLLO.md`** - Apollo.io integration
- **API Docs**: http://localhost:8000/docs

## 🐛 Troubleshooting

### Chat not responding

**Issue**: No response after submitting query

**Solutions**:
1. Check if API is running: http://localhost:8000/docs
2. Check browser console for errors (F12)
3. Verify OpenAI API key (or use fallback mode)

### No contacts found

**Issue**: Search returns 0 contacts

**Solutions**:
1. Try broader queries ("Find CEOs" instead of specific companies)
2. Check if mock data is loaded
3. Verify scraper is working

### Sync to Twenty CRM fails

**Issue**: Contacts not appearing in Twenty CRM

**Solutions**:
1. Verify Twenty CRM is running: http://localhost:3001
2. Check API token is correct
3. Check Twenty CRM logs for errors
4. Verify GraphQL endpoint is accessible

## 🎉 You're All Set!

Your chat-based CRM is ready! Just:

1. Run `start_chat_crm.bat`
2. Open http://localhost:8000
3. Start searching for contacts!

**Good luck with your hackathon! 🚀**

