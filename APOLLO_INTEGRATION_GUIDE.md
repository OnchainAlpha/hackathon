# Apollo.io Integration Guide

## 🎯 Overview

This guide explains how to use the **real Apollo.io API** to fetch contacts and automatically save them to your CRM database.

## 🔄 Complete Workflow

```
User Types Query → AI Parses Intent → Apollo API Search → Save to Database → Sync to Twenty CRM → Return Results
```

### Example Flow:
1. **User writes**: "Find CTOs at AI companies in San Francisco"
2. **AI parses**: Extracts titles=[CTO], industries=[AI], locations=[San Francisco]
3. **Apollo searches**: Calls Apollo.io API with these parameters
4. **Database saves**: Contacts automatically added to CRM database
5. **Twenty syncs**: Background task syncs to Twenty CRM (if configured)
6. **User sees**: "Found 23 contacts! Added to CRM. (Data from Apollo.io)"

---

## 🚀 Quick Start

### 1. Set Up Apollo API Key

Get your Apollo.io API key:
1. Go to https://apollo.io
2. Sign up or log in
3. Navigate to Settings → API
4. Copy your API key

Add to your `.env` file:
```bash
APOLLO_API_KEY=your_apollo_api_key_here
```

### 2. Set Up OpenAI API Key (for intent parsing)

```bash
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. (Optional) Set Up Twenty CRM

```bash
TWENTY_CRM_API_TOKEN=your_twenty_crm_token_here
```

### 4. Start the Server

```bash
cd crm_integration
python chat_api.py
```

You should see:
```
============================================================
🚀 LeadOn Chat CRM API starting...
============================================================
   OpenAI API:    ✅ Configured
   Apollo API:    ✅ Configured (real data)
   Twenty CRM:    ✅ Configured

   📚 API Docs:   http://localhost:8000/docs
   💬 Chat UI:    http://localhost:8000/
============================================================
```

---

## 💬 Using the Chat Interface

### Method 1: Web UI

1. Open http://localhost:8000/ in your browser
2. Type your query in the chat box
3. Press Enter or click Send

### Method 2: API Call

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Find CTOs at AI companies in San Francisco"
  }'
```

### Method 3: Python Script

```python
import requests

response = requests.post(
    "http://localhost:8000/api/chat",
    json={
        "message": "Find CTOs at AI companies in San Francisco",
        "website_url": None  # Optional
    }
)

data = response.json()
print(f"Response: {data['response']}")
print(f"Contacts found: {data['contacts_found']}")
print(f"Contacts added: {data['contacts_added']}")
```

---

## 📝 Example Queries

### Finding Decision Makers
```
"Find CEOs at Series B startups in New York"
"Get CTOs at AI companies in San Francisco"
"Find VPs of Sales at SaaS companies"
```

### Fundraising
```
"Find investors in the FinTech space"
"Get VCs focused on AI startups"
"Find angel investors in healthcare"
```

### Partnership Outreach
```
"Find marketing directors at e-commerce companies"
"Get heads of partnerships at tech companies"
"Find business development managers in SaaS"
```

### Industry-Specific
```
"Find executives at healthcare startups in Boston"
"Get founders of AI companies with 10-50 employees"
"Find CTOs at fintech companies in London"
```

---

## 🔍 How It Works

### 1. Intent Parsing (AI Agent)

The system uses OpenAI GPT-4o-mini to parse your natural language query:

**Input**: "Find CTOs at AI companies in San Francisco"

**Parsed Intent**:
```json
{
  "query": "CTO AI San Francisco",
  "titles": ["CTO"],
  "industries": ["AI"],
  "locations": ["San Francisco, CA, USA"],
  "campaign_objective": "Find technical leaders",
  "max_results": 50
}
```

### 2. Apollo API Search

The system calls Apollo.io API with the parsed parameters:

```python
client = ApolloClient()
result = client.search_people(
    query="CTO AI San Francisco",
    titles=["CTO"],
    locations=["San Francisco, CA, USA"],
    per_page=50
)
```

### 3. Database Storage

Contacts are automatically saved to the in-memory database with deduplication:

```python
# Deduplicate by email or LinkedIn URL
for contact in results:
    if not exists_in_database(contact):
        contacts_db.append(contact)
```

### 4. Twenty CRM Sync (Optional)

If Twenty CRM is configured, contacts are synced in the background:

```python
background_tasks.add_task(
    sync_apollo_to_twenty,
    results,
    api_token
)
```

---

## 📊 Viewing Your Contacts

### Get All Contacts
```bash
curl http://localhost:8000/api/contacts
```

### Filter by Tags
```bash
curl "http://localhost:8000/api/contacts?tags=cto,ai&limit=50"
```

### Filter by Title
```bash
curl "http://localhost:8000/api/contacts?title=CEO&limit=25"
```

### View Statistics
```bash
curl http://localhost:8000/api/stats
```

Response:
```json
{
  "total_contacts": 150,
  "total_chats": 5,
  "tags": {
    "cto": 45,
    "ai": 67,
    "saas": 38
  },
  "titles": {
    "CTO": 45,
    "CEO": 32,
    "VP Engineering": 18
  },
  "companies": {
    "OpenAI": 5,
    "Anthropic": 4,
    "Google": 8
  }
}
```

---

## 🔧 Configuration Options

### Apollo API Settings

In your code, you can customize:

```python
client = ApolloClient(
    api_key="your_key",
    rate_limit_requests=60,  # Max requests per minute
    rate_limit_window=60     # Time window in seconds
)
```

### Search Parameters

```python
result = client.search_people(
    query="AI startup",
    titles=["CEO", "CTO", "Founder"],
    locations=["San Francisco, CA", "New York, NY"],
    seniorities=["executive", "director"],
    company_names=["OpenAI", "Anthropic"],
    industries=["Artificial Intelligence"],
    employee_ranges=["11-50", "51-200"],
    per_page=100  # Max 100 per request
)
```

---

## 🚨 Troubleshooting

### "Apollo API key not set"

**Problem**: You see "(Using demo data - set APOLLO_API_KEY for real results)"

**Solution**: 
1. Get your API key from https://apollo.io/settings/api
2. Add to `.env`: `APOLLO_API_KEY=your_key_here`
3. Restart the server

### "Apollo API failed"

**Problem**: API returns an error

**Common causes**:
- Invalid API key
- Rate limit exceeded (free plan: 50 requests/month)
- Invalid search parameters

**Solution**: Check the logs for specific error messages. The system will automatically fall back to mock data.

### "No contacts found"

**Problem**: Search returns 0 results

**Possible reasons**:
- Search criteria too specific
- No matches in Apollo database
- Free plan limitations

**Solution**: Try broader search terms or upgrade your Apollo plan.

---

## 💡 Tips for Best Results

### 1. Be Specific but Not Too Narrow
✅ Good: "Find CTOs at AI companies in San Francisco"
❌ Too narrow: "Find CTOs named John at OpenAI in San Francisco"

### 2. Use Standard Job Titles
✅ Good: "CEO", "CTO", "VP Sales"
❌ Unclear: "Boss", "Tech guy", "Sales person"

### 3. Use Full Location Names
✅ Good: "San Francisco, CA, USA"
❌ Unclear: "SF", "Bay Area"

### 4. Combine Multiple Criteria
"Find VPs of Marketing at Series B SaaS companies in New York with 50-200 employees"

---

## 📈 Apollo API Limits

### Free Plan
- 50 API requests per month
- 25 results per request
- Basic contact data

### Paid Plans
- Higher rate limits
- More results per request
- Email verification
- Phone number reveal
- Advanced filters

---

## 🔗 Integration with Twenty CRM

When Twenty CRM is configured, contacts are automatically synced:

1. **Real-time sync**: Contacts synced as background task
2. **Deduplication**: Existing contacts are not duplicated
3. **Field mapping**: Apollo fields mapped to Twenty schema
4. **Batch processing**: Contacts synced in batches of 10

---

## 📚 Additional Resources

- [Apollo.io API Documentation](https://apolloio.github.io/apollo-api-docs/)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Twenty CRM Documentation](https://twenty.com/developers)

---

## 🎉 Success!

You're now set up to:
✅ Write natural language queries
✅ Get real contacts from Apollo.io
✅ Automatically save to CRM database
✅ Sync to Twenty CRM
✅ View and filter your contacts

**Next steps**: Start searching for contacts and building your pipeline!

