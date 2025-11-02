# 🎉 Twenty CRM is Running!

## ✅ Status

Twenty CRM is now running on your machine:

- **Frontend**: http://localhost:3001
- **Backend API**: http://localhost:4000
- **GraphQL**: http://localhost:4000/graphql

## 🚀 Next Steps

### Step 1: Create Your Twenty CRM Account

1. Open **http://localhost:3001** in your browser
2. Click **"Continue with Email"**
3. Enter your email and create a password
4. Complete the onboarding wizard

### Step 2: Get Your API Token

1. In Twenty CRM, click the **⚙️ Settings** icon (bottom left)
2. Click **"API Keys"** or **"Developers"** in the left sidebar
3. Click **"+ Create API Key"** or **"+ New API Key"**
4. Name it: **"LeadOn Integration"**
5. **Copy the token** (starts with `apk_...`)

### Step 3: Update Your .env File

Open `.env` in the root directory and update this line:

```bash
TWENTY_CRM_API_TOKEN=apk_your_actual_token_here
```

Replace `apk_your_actual_token_here` with the token you copied from Twenty CRM.

### Step 4: Restart Your LeadOn Server

1. Go to the terminal running your LeadOn server (Terminal 54)
2. Press **Ctrl+C** to stop it
3. Restart it:
   ```bash
   python crm_integration\chat_api.py
   ```

### Step 5: Your Contacts Will Auto-Sync! 🎉

Once the server restarts with the correct token:
- Your **299 contacts** from the database will automatically sync to Twenty CRM
- Any new contacts you search for will also sync automatically
- You can view them at: **http://localhost:3001/objects/people**

---

## 🎯 Using Twenty CRM

### View Your Contacts

1. Open **http://localhost:3001**
2. Click **"People"** in the left sidebar
3. You'll see all your contacts in a beautiful table view

### Features You Can Use

✅ **Search** - Fast search across all contacts
✅ **Filter** - Create custom filters (e.g., by company, title, location)
✅ **Sort** - Sort by any column
✅ **Views** - Create custom views for different contact types
✅ **Export** - Export to CSV/Excel
✅ **Companies** - Link contacts to companies
✅ **Deals/Pipeline** - Track sales opportunities
✅ **Tasks & Notes** - Add tasks and notes to contacts

---

## 🔄 The Workflow

### Old Way (Basic HTML):
```
Search in LeadOn → View in basic HTML table → Limited features
```

### New Way (Twenty CRM):
```
Search in LeadOn → Auto-sync to Twenty CRM → View in professional CRM
                    ↓
                - Filter contacts
                - Create deals/pipelines
                - Track interactions
                - Export data
                - Much more!
```

---

## 📊 Port Configuration

We configured Twenty CRM to use port **4000** instead of **3000** to avoid conflicts:

| Service | Port | URL |
|---------|------|-----|
| LeadOn Server | 8000 | http://localhost:8000 |
| Twenty CRM Frontend | 3001 | http://localhost:3001 |
| Twenty CRM Backend | 4000 | http://localhost:4000 |
| Twenty CRM GraphQL | 4000 | http://localhost:4000/graphql |

---

## 🛠️ Managing Twenty CRM

### Start Twenty CRM
```bash
cd CRM\twenty\packages\twenty-docker
docker compose up -d
```

### Stop Twenty CRM
```bash
cd CRM\twenty\packages\twenty-docker
docker compose down
```

### View Logs
```bash
cd CRM\twenty\packages\twenty-docker
docker compose logs -f
```

### Check Status
```bash
docker ps
```

### Restart Twenty CRM
```bash
cd CRM\twenty\packages\twenty-docker
docker compose restart
```

---

## 💡 Pro Tips

### 1. Create Custom Views

In Twenty CRM, create custom views for different contact types:
- **"AI Companies"** - Filter by company name containing "AI"
- **"CTOs"** - Filter by title containing "CTO"
- **"San Francisco"** - Filter by city = "San Francisco"
- **"High Priority"** - Your most important leads

### 2. Use the Search

The search bar at the top searches across:
- Contact names
- Emails
- Companies
- Titles
- Notes

### 3. Add Custom Fields

You can add custom fields to the Person object:
1. Go to **Settings** > **Data Model**
2. Click on **"Person"**
3. Click **"+ Add Field"**
4. Add fields like:
   - **Tags** (Multi-select) - investor, ai, vc, tech, etc.
   - **Source** (Text) - apollo, linkedin, manual, etc.
   - **Lead Score** (Number) - 1-100
   - **Last Contacted** (Date)

### 4. Export Your Data

Need to share contacts with your team?
1. Go to **People** view
2. Click the **"..."** menu (top right)
3. Click **"Export"**
4. Choose CSV or Excel format

### 5. Create Deals/Opportunities

Track your sales pipeline:
1. Click **"Opportunities"** in the left sidebar
2. Click **"+ New Opportunity"**
3. Link it to a contact and company
4. Set the deal value and stage
5. Track progress through your pipeline

---

## 🔧 Troubleshooting

### Twenty CRM Not Loading?

Check if containers are running:
```bash
docker ps
```

You should see:
- `twenty-server-1` (healthy)
- `twenty-db-1` (healthy)
- `twenty-redis-1` (healthy)

### Contacts Not Syncing?

1. Make sure you added the API token to `.env`
2. Restart the LeadOn server
3. Check the LeadOn server logs for sync messages
4. Look for: `🔄 Syncing contacts to Twenty CRM...`

### Port Already in Use?

If you get port conflicts, check what's using the ports:
```bash
netstat -ano | findstr :4000
netstat -ano | findstr :3001
```

---

## 📚 Resources

- **Twenty CRM Docs**: https://twenty.com/developers
- **GraphQL Playground**: http://localhost:4000/graphql
- **REST API Docs**: http://localhost:4000/rest/open-api/core

---

## 🎉 You're All Set!

Your LeadOn CRM now has:

✅ **Professional UI** - Twenty CRM instead of basic HTML
✅ **Auto-Sync** - Contacts automatically sync from LeadOn to Twenty
✅ **299 Contacts Ready** - Your existing contacts will sync on next search
✅ **Full CRM Features** - Companies, deals, tasks, notes, and more
✅ **Persistent Storage** - PostgreSQL database (not in-memory)
✅ **Modern Stack** - React frontend, NestJS backend

**Next**: Get your API token from Twenty CRM and update the `.env` file!

---

## 🚀 Quick Start Commands

```bash
# 1. Open Twenty CRM
start http://localhost:3001

# 2. Create account and get API token

# 3. Update .env with your token
# TWENTY_CRM_API_TOKEN=apk_your_token_here

# 4. Restart LeadOn server
# Ctrl+C in Terminal 54, then:
python crm_integration\chat_api.py

# 5. Search for contacts in LeadOn
# They'll automatically sync to Twenty CRM!
```

**Enjoy your professional CRM!** 🎉

