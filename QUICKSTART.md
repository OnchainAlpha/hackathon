# 🚀 Quick Start Guide - Apollo Integration

Get up and running with real Apollo.io contact data in 5 minutes!

---

## ⚡ 5-Minute Setup

### Step 1: Get Your API Keys (2 minutes)

#### OpenAI API Key (Required)
1. Go to https://platform.openai.com/api-keys
2. Click "Create new secret key"
3. Copy the key (starts with `sk-`)

#### Apollo.io API Key (Required for real data)
1. Go to https://apollo.io
2. Sign up or log in
3. Navigate to Settings → API
4. Copy your API key

#### Twenty CRM Token (Optional)
1. Go to your Twenty CRM instance
2. Settings → Developers → API Keys
3. Create and copy token

### Step 2: Configure Environment (1 minute)

Create a `.env` file in the project root:

```bash
# Required
OPENAI_API_KEY=sk-your-openai-key-here

# Required for real Apollo data (will use mock data if not set)
APOLLO_API_KEY=your-apollo-key-here

# Optional - for Twenty CRM sync
TWENTY_CRM_API_TOKEN=your-twenty-token-here
TWENTY_CRM_API_URL=https://your-instance.twenty.com/graphql
```

### Step 3: Install Dependencies (1 minute)

```bash
pip install -r requirements.txt
```

### Step 4: Start the Server (30 seconds)

```bash
python crm_integration/chat_api.py
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

### Step 5: Test It! (30 seconds)

Open http://localhost:8000/ and type:
```
Find CTOs at AI companies in San Francisco
```

You should get:
```
Found 23 CTOs at AI companies in San Francisco! 
I've added them to your CRM. (Data from Apollo.io)
```

---

## 🎯 What Just Happened?

1. **AI parsed your query** → Extracted: titles=[CTO], industries=[AI], locations=[San Francisco]
2. **Apollo API searched** → Found 23 real contacts
3. **Database saved** → Contacts automatically added to CRM
4. **Twenty synced** → Background task synced to Twenty CRM (if configured)
5. **Response generated** → Friendly AI response returned

---

## 💬 Try These Queries

### Finding Decision Makers
```
Find CEOs at Series B startups in New York
Get CTOs at AI companies in San Francisco
Find VPs of Sales at SaaS companies
```

### Fundraising
```
Find investors in the FinTech space
Get VCs focused on AI startups
Find angel investors in healthcare
```

### Partnership Outreach
```
Find marketing directors at e-commerce companies
Get heads of partnerships at tech companies
Find business development managers in SaaS
```

---

## 📊 View Your Contacts

### Web UI
Open http://localhost:8000/ and click "View Contacts"

### API
```bash
# Get all contacts
curl http://localhost:8000/api/contacts

# Filter by tags
curl "http://localhost:8000/api/contacts?tags=cto,ai"

# View statistics
curl http://localhost:8000/api/stats
```

### Python
```python
import requests

# Get contacts
response = requests.get("http://localhost:8000/api/contacts")
contacts = response.json()

print(f"Total contacts: {len(contacts)}")
for contact in contacts[:5]:
    print(f"- {contact['name']} ({contact['title']}) at {contact['company']}")
```

---

## 🔧 Troubleshooting

### "Apollo API key not set"

**Problem**: You see "(Using demo data - set APOLLO_API_KEY for real results)"

**Solution**: 
```bash
# Add to .env file
APOLLO_API_KEY=your_apollo_key_here

# Restart server
python crm_integration/chat_api.py
```

### "OpenAI API key not set"

**Problem**: Server won't start or uses fallback mode

**Solution**:
```bash
# Add to .env file
OPENAI_API_KEY=sk-your-key-here

# Restart server
python crm_integration/chat_api.py
```

### "No contacts found"

**Problem**: Search returns 0 results

**Possible causes**:
- Search criteria too specific
- Free Apollo plan limitations
- No matches in Apollo database

**Solution**: Try broader search terms:
```
❌ Too specific: "Find CTOs named John at OpenAI in San Francisco"
✅ Better: "Find CTOs at AI companies in San Francisco"
```

### "Rate limit exceeded"

**Problem**: Apollo API returns rate limit error

**Solution**:
- Free plan: 50 requests/month
- Upgrade your Apollo plan for higher limits
- System will automatically fall back to mock data

---

## 📈 Understanding the Response

When you send a query, you get:

```json
{
  "response": "Found 23 CTOs at AI companies in San Francisco! I've added them to your CRM. (Data from Apollo.io)",
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

**Fields explained**:
- `response`: Friendly AI-generated message
- `contacts_found`: Total contacts returned from Apollo
- `contacts_added`: New contacts added to database (after deduplication)
- `intent`: Parsed search parameters
- `timestamp`: When the search was performed

---

## 🎓 Next Steps

### 1. Explore the API
Visit http://localhost:8000/docs for interactive API documentation

### 2. View Your Data
```bash
# Get all contacts
curl http://localhost:8000/api/contacts

# Get statistics
curl http://localhost:8000/api/stats
```

### 3. Integrate with Your App
```python
import requests

def search_contacts(query):
    response = requests.post(
        "http://localhost:8000/api/chat",
        json={"message": query}
    )
    return response.json()

# Use it
result = search_contacts("Find CTOs at AI companies")
print(f"Found {result['contacts_found']} contacts!")
```

### 4. Run Tests
```bash
python test_apollo_integration.py
```

---

## 📚 Additional Resources

- **APOLLO_INTEGRATION_GUIDE.md** - Complete setup and usage guide
- **WORKFLOW_DIAGRAM.md** - Visual workflow and architecture
- **IMPLEMENTATION_SUMMARY.md** - Technical implementation details
- **test_apollo_integration.py** - Test script

---

## 🎉 You're All Set!

You now have a fully functional CRM system that:
- ✅ Accepts natural language queries
- ✅ Fetches real contacts from Apollo.io
- ✅ Automatically saves to database
- ✅ Syncs to Twenty CRM
- ✅ Returns friendly AI responses

**Start searching for contacts and building your pipeline!**

---

## 💡 Pro Tips

### 1. Be Specific but Not Too Narrow
```
✅ Good: "Find CTOs at AI companies in San Francisco"
❌ Too narrow: "Find CTOs named John at OpenAI"
```

### 2. Use Standard Job Titles
```
✅ Good: "CEO", "CTO", "VP Sales"
❌ Unclear: "Boss", "Tech guy"
```

### 3. Combine Multiple Criteria
```
"Find VPs of Marketing at Series B SaaS companies in New York with 50-200 employees"
```

### 4. Check Your Limits
- Free Apollo plan: 50 requests/month
- Each search = 1 request
- System automatically falls back to mock data if limit exceeded

---

## 🆘 Need Help?

1. **Check the logs** - Server prints detailed information
2. **Run tests** - `python test_apollo_integration.py`
3. **View docs** - http://localhost:8000/docs
4. **Read guides** - See APOLLO_INTEGRATION_GUIDE.md

---

**Happy lead hunting! 🎯**

