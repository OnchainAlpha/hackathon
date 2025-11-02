# Twenty CRM Setup Guide

## 🎯 Getting Your Twenty CRM API Token

Twenty CRM is an open-source CRM that you can self-host or use their cloud version. Here's how to get your API token:

---

## Option 1: Using Twenty Cloud (Easiest)

### Step 1: Sign Up or Log In
1. Go to https://app.twenty.com
2. Sign up for a free account or log in
3. Complete the onboarding process

### Step 2: Get Your API Token
1. Click on your profile icon (bottom left)
2. Go to **Settings**
3. Navigate to **Developers** section
4. Click on **API Keys**
5. Click **"Create API Key"**
6. Give it a name like "LeadOn Integration"
7. Copy the generated token (starts with `twenty_`)

### Step 3: Get Your GraphQL URL
Your GraphQL endpoint will be:
```
https://api.twenty.com/graphql
```

### Step 4: Add to .env File
```bash
TWENTY_CRM_API_TOKEN=twenty_your_token_here
TWENTY_CRM_API_URL=https://api.twenty.com/graphql
```

---

## Option 2: Self-Hosted Twenty CRM

If you're running Twenty CRM on your own server:

### Step 1: Access Your Instance
1. Go to your Twenty CRM instance URL (e.g., `https://crm.yourcompany.com`)
2. Log in with your credentials

### Step 2: Get Your API Token
1. Click on your profile icon
2. Go to **Settings** → **Developers**
3. Click **"Create API Key"**
4. Copy the token

### Step 3: Get Your GraphQL URL
Your GraphQL endpoint will be:
```
https://your-instance-url.com/graphql
```

### Step 4: Add to .env File
```bash
TWENTY_CRM_API_TOKEN=your_token_here
TWENTY_CRM_API_URL=https://your-instance-url.com/graphql
```

---

## Option 3: Don't Have Twenty CRM Yet?

### Quick Setup with Docker (5 minutes)

```bash
# Clone Twenty CRM
git clone https://github.com/twentyhq/twenty.git
cd twenty

# Start with Docker
docker-compose up -d

# Access at http://localhost:3000
```

Then follow the steps in Option 2 to get your API token.

---

## 🧪 Testing Your Twenty CRM Connection

Once you've added your token to `.env`, test the connection:

### Method 1: Using the Test Script

```bash
python test_twenty_connection.py
```

### Method 2: Manual Test with curl

```bash
# Replace with your actual token and URL
curl -X POST https://api.twenty.com/graphql \
  -H "Authorization: Bearer your_token_here" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "query { currentUser { id email } }"
  }'
```

If successful, you'll see:
```json
{
  "data": {
    "currentUser": {
      "id": "...",
      "email": "your@email.com"
    }
  }
}
```

---

## 🔧 Troubleshooting

### "Invalid token" or "Unauthorized"

**Problem**: Token is not working

**Solutions**:
1. Make sure you copied the entire token
2. Check for extra spaces in `.env` file
3. Verify the token hasn't expired
4. Try creating a new API key

### "Cannot connect to Twenty CRM"

**Problem**: Can't reach the GraphQL endpoint

**Solutions**:
1. Check your `TWENTY_CRM_API_URL` is correct
2. Make sure your Twenty instance is running
3. Check firewall/network settings
4. Verify the URL includes `/graphql` at the end

### "GraphQL error: Field not found"

**Problem**: API schema mismatch

**Solution**: Make sure you're using a recent version of Twenty CRM (v0.20.0+)

---

## 📊 What Happens When Twenty CRM is Connected?

When you have Twenty CRM configured, the system will:

1. **Automatically sync contacts** after each Apollo search
2. **Create Person records** in Twenty CRM
3. **Map fields** from Apollo to Twenty:
   - Name → firstName, lastName
   - Email → primaryEmail
   - Phone → primaryPhoneNumber
   - Title → jobTitle
   - Company → company (linked)
   - LinkedIn → linkedinLink
   - Location → city

4. **Run in background** - doesn't slow down your searches
5. **Handle errors gracefully** - if sync fails, contacts still saved locally

---

## 🎯 Your Current Setup Status

Based on your `.env` file:

```
✅ Apollo API:  Configured (AU1LGNrQFAwxQrVQKUIsnw)
❌ OpenAI API:  Not configured yet
❌ Twenty CRM:  Not configured yet
```

---

## 📝 Complete .env Example

Here's what your `.env` should look like when fully configured:

```bash
# Apollo.io API Configuration
APOLLO_API_KEY=AU1LGNrQFAwxQrVQKUIsnw

# OpenAI API Key (Required for AI features)
OPENAI_API_KEY=sk-proj-your-openai-key-here

# Twenty CRM Configuration (Optional)
TWENTY_CRM_API_TOKEN=twenty_your_token_here
TWENTY_CRM_API_URL=https://api.twenty.com/graphql

# Database Configuration
DATABASE_URL=postgresql://user:pass@localhost/sales_crm

# LinkedIn Credentials (for future automation)
LINKEDIN_EMAIL=your_email@example.com
LINKEDIN_PASSWORD=your_password

# Rate Limiting Configuration
MAX_DAILY_LINKEDIN_ACTIONS=50
SCRAPER_DELAY_SECONDS=2
APOLLO_REQUESTS_PER_MINUTE=60

# Logging
LOG_LEVEL=INFO
```

---

## 🚀 Next Steps

### 1. Get OpenAI API Key (Required)
The system uses OpenAI for AI features, not Claude. Get your key from:
https://platform.openai.com/api-keys

**Note**: You provided a Claude API key (`sk-ant-api03-...`), but this system uses OpenAI's GPT-4o-mini for:
- Parsing natural language queries
- Extracting search parameters
- Generating friendly responses

### 2. Get Twenty CRM Token (Optional)
Follow the steps above to get your Twenty CRM token.

### 3. Update .env File
Add both keys to your `.env` file.

### 4. Start the Server
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
============================================================
```

---

## 💡 Do You Need Twenty CRM?

**Twenty CRM is optional!** The system works perfectly fine without it:

### Without Twenty CRM:
- ✅ Contacts saved to in-memory database
- ✅ Can view contacts via API
- ✅ Can export contacts
- ✅ All search functionality works

### With Twenty CRM:
- ✅ All of the above, plus:
- ✅ Contacts synced to Twenty CRM
- ✅ Use Twenty's UI to manage contacts
- ✅ Access to Twenty's features (pipelines, tasks, etc.)
- ✅ Persistent storage in Twenty's database

**Recommendation**: Start without Twenty CRM, get the system working, then add it later if needed.

---

## 🆘 Need Help?

If you're having trouble:

1. **Check the logs** when starting the server
2. **Test your token** with the curl command above
3. **Verify your URL** includes `/graphql`
4. **Try creating a new API key** in Twenty CRM

---

## 📚 Additional Resources

- [Twenty CRM Documentation](https://twenty.com/developers)
- [Twenty CRM GitHub](https://github.com/twentyhq/twenty)
- [Twenty CRM API Reference](https://twenty.com/developers/graphql-api)
- [OpenAI API Keys](https://platform.openai.com/api-keys)

---

**Ready to get started? Follow the steps above to get your Twenty CRM token!**

