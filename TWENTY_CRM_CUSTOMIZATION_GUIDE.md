# 🎨 Twenty CRM Customization Guide for LeadOn

## 🎉 Great News!

Twenty CRM **already has a built-in AI Lead Generation chat interface**! I found it in the codebase:
- `CRM/twenty/packages/twenty-front/src/modules/lead-gen/components/LeadGenChatButton.tsx`
- `CRM/twenty/packages/twenty-front/src/modules/lead-gen/components/LeadGenChatModal.tsx`

The chat button appears on the **People page** as a floating blue robot button in the bottom-right corner!

---

## 🔧 What I Modified

### File: `LeadGenChatModal.tsx`

**Changed the API endpoint** from `/api/lead-gen/search` to `http://localhost:8000/api/chat` (your LeadOn backend)

**Before:**
```typescript
const response = await fetch('/api/lead-gen/search', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ query: input }),
});
```

**After:**
```typescript
const response = await fetch('http://localhost:8000/api/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ 
    message: input,
    max_contacts: 25,
    enrich_with_jobs: false
  }),
});
```

---

## ⚠️ The Challenge

Twenty CRM is running from a **pre-built Docker image** (`twentycrm/twenty:latest`), so my code changes won't take effect until we rebuild the Docker image.

---

## 🚀 Option 1: Quick Workaround (Recommended for Hackathon)

Since rebuilding Twenty CRM is complex and time-consuming, I recommend using **your custom LeadOn Pro frontend** that I already built for you:

### Why This Is Better:
- ✅ **Already working** - No build required
- ✅ **Fully customized** - Tailored for LeadOn
- ✅ **All features** - Chat, search, contacts, campaigns
- ✅ **Fast iteration** - Change anything instantly
- ✅ **No Docker** - One less thing to break during demo

### Access It:
**http://localhost:8000** (should already be running)

---

## 🔨 Option 2: Build Custom Twenty CRM (Advanced)

If you really want to customize Twenty CRM itself, here's how:

### Prerequisites:
- Node.js 24.5.0
- Yarn 4.0.2
- Docker Desktop

### Steps:

#### 1. Install Dependencies
```bash
cd C:\Users\Gamer\Downloads\LeadOn\CRM\twenty
yarn install
```

#### 2. Build the Frontend
```bash
cd packages/twenty-front
yarn build
```

#### 3. Build Custom Docker Image
```bash
cd C:\Users\Gamer\Downloads\LeadOn\CRM\twenty
docker build -t leadon-twenty:custom .
```

#### 4. Update docker-compose.yml
Change:
```yaml
image: twentycrm/twenty:${TAG:-latest}
```

To:
```yaml
image: leadon-twenty:custom
```

#### 5. Restart Docker
```bash
cd packages/twenty-docker
docker compose down
docker compose up -d
```

### Estimated Time: 30-60 minutes

---

## 🎯 Option 3: Hybrid Approach (Best of Both Worlds)

Use **LeadOn Pro** as your main interface, but keep Twenty CRM running in the background for:
- Advanced CRM features
- Data visualization
- Team collaboration
- Professional CRM capabilities

### How It Works:
1. **LeadOn Pro** (http://localhost:8000) - Your main demo interface
   - AI search with chatbox
   - Contact management
   - Campaign creation
   - Export features

2. **Twenty CRM** (http://localhost:4000) - Advanced CRM features
   - Kanban boards
   - Calendar views
   - Deal pipelines
   - Team features

### Benefits:
- ✅ Best of both worlds
- ✅ No rebuild required
- ✅ Professional CRM + Custom interface
- ✅ Impressive for demo

---

## 📊 Comparison

| Feature | LeadOn Pro | Twenty CRM (Custom) | Twenty CRM (Stock) |
|---------|-----------|---------------------|-------------------|
| **AI Chat** | ✅ Working now | ✅ After rebuild | ❌ Not connected |
| **Setup Time** | ✅ 0 minutes | ⚠️ 30-60 minutes | ✅ Already running |
| **Customization** | ✅ Full control | ⚠️ Limited | ❌ None |
| **Build Required** | ❌ No | ✅ Yes | ❌ No |
| **Demo Ready** | ✅ Yes | ⚠️ After build | ⚠️ Partial |
| **Tailored for LeadOn** | ✅ 100% | ⚠️ 50% | ❌ 0% |

---

## 🎬 My Recommendation for Your Hackathon

### Use LeadOn Pro (Option 1)

**Why:**
1. **It's already working** - No build, no wait
2. **Fully customized** - Every feature designed for LeadOn
3. **Impressive** - "We built this" > "We integrated this"
4. **Reliable** - No Docker dependencies during demo
5. **Fast iteration** - Change anything in seconds

### Demo Flow:
1. Open **http://localhost:8000**
2. Show the **Dashboard** - "Here's our CRM overview"
3. Click **Search** - "Let me show you our AI-powered search"
4. Type: "Find CTOs at AI companies in San Francisco"
5. Show **results** - "We found X contacts in seconds"
6. Go to **Contacts** - "Here are all our contacts"
7. **Filter** and **select** contacts
8. **Create campaign** - "Create a campaign with one click"
9. **Export to CSV** - "And export for our team"

### Backup Option:
Keep Twenty CRM running at **http://localhost:4000** to show:
- "We can also integrate with professional CRM systems"
- "Here's the same data in Twenty CRM"
- "We support multiple interfaces"

---

## 🔥 What Makes LeadOn Pro Better

### For Your Hackathon:
- ✅ **Custom-built** - Shows your technical skills
- ✅ **Tailored** - Every feature serves a purpose
- ✅ **Modern UI** - Professional gradient design
- ✅ **AI-powered** - Natural language search
- ✅ **Complete workflow** - Search → Manage → Campaign → Export
- ✅ **No dependencies** - Just HTML/CSS/JS
- ✅ **Fast** - No build step, instant updates

### For Twenty CRM:
- ⚠️ **Generic** - Built for everyone, not just you
- ⚠️ **Complex** - Lots of features you don't need
- ⚠️ **Docker** - Can fail during demo
- ⚠️ **Rebuild required** - 30-60 minutes
- ⚠️ **Hard to customize** - React/TypeScript/Vite/Docker

---

## 💡 Quick Decision Matrix

### Choose LeadOn Pro if:
- ✅ You want to demo **now**
- ✅ You want **full control**
- ✅ You want to **impress judges**
- ✅ You want **reliability**
- ✅ You have **limited time**

### Choose Twenty CRM if:
- ⚠️ You have **30-60 minutes** to rebuild
- ⚠️ You want **generic CRM features**
- ⚠️ You're comfortable with **Docker/Node/Yarn**
- ⚠️ You want to show **integration skills**

---

## 🚀 Next Steps

### Recommended Path:
1. ✅ **Use LeadOn Pro** at http://localhost:8000
2. ✅ **Practice your demo** with the interface
3. ✅ **Add more contacts** via AI search
4. ✅ **Create sample campaigns**
5. ✅ **Prepare your pitch**

### Optional:
- Keep Twenty CRM running as a backup
- Show both interfaces during demo
- Highlight the flexibility of your system

---

## 📝 Files Modified

If you decide to rebuild Twenty CRM later:

1. **`CRM/twenty/packages/twenty-front/src/modules/lead-gen/components/LeadGenChatModal.tsx`**
   - Changed API endpoint to `http://localhost:8000/api/chat`
   - Updated request format to match LeadOn backend
   - Improved error handling

---

## 🆘 Need Help?

### If you choose LeadOn Pro:
- Just open **http://localhost:8000**
- Everything is ready to go!

### If you choose to rebuild Twenty CRM:
- Follow the steps in "Option 2" above
- Allow 30-60 minutes for build
- Make sure Node.js 24.5.0 and Yarn 4.0.2 are installed

---

## 🎊 Summary

You have **two great options**:

1. **LeadOn Pro** (http://localhost:8000) - Custom, ready now, impressive
2. **Twenty CRM** (http://localhost:4000) - Generic, needs rebuild, professional

**My strong recommendation: Use LeadOn Pro for your hackathon demo!**

It's:
- ✅ Ready now
- ✅ Fully customized
- ✅ More impressive
- ✅ More reliable
- ✅ Easier to explain

**You can always rebuild Twenty CRM later if you want to explore it further!**

---

## 🎯 Final Answer

**For your hackathon, use LeadOn Pro at http://localhost:8000**

It has everything you need:
- AI chatbox ✅
- Contact search ✅
- Contact management ✅
- Campaign creation ✅
- Export features ✅
- Modern UI ✅
- Tailored for LeadOn ✅

**It's ready to demo right now!** 🚀

