# 🚀 LeadOn CRM - Quick Reference

## 🌐 URLs

| Interface | URL | Description |
|-----------|-----|-------------|
| **New CRM** | http://localhost:8000/crm | Modern table interface (USE THIS!) |
| Old Interface | http://localhost:8000/ | Original LeadOn Pro |
| API Docs | http://localhost:8000/docs | Interactive API documentation |
| Contacts API | http://localhost:8000/api/contacts | JSON list of contacts |

---

## ⚡ Quick Commands

### Start Server
```bash
python crm_integration/chat_api.py
```

### Add Sample Data
```bash
python add_sample_contacts.py
```

### Check Database
```bash
python -c "from database.db_manager import get_db_manager; db = get_db_manager(); session = db.get_session(); from database.models import Contact; print(f'Contacts: {session.query(Contact).count()}'); session.close()"
```

---

## 🎯 Common Tasks

### Find Contacts with AI
1. Open http://localhost:8000/crm
2. Click "AI Search" button
3. Type query: "Find CTOs at AI companies"
4. Press Enter
5. Wait 15-30 seconds
6. Contacts appear in table!

### Export Contacts
**All contacts:**
- Click "Export" button in top bar

**Selected contacts:**
- Check boxes next to contacts
- Click "Export" in action bar

### Filter Contacts
- Type in search bar at top
- Filters by name, email, company, or title
- Real-time filtering

### Bulk Actions
1. Select contacts with checkboxes
2. Action bar appears at bottom
3. Choose: Campaign, Export, or Delete

---

## 🔑 Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Ctrl + K` | Focus search bar (coming soon) |
| `Enter` | Send AI search query |
| `Esc` | Close chat panel |

---

## 📊 Sample AI Queries

### By Role
```
Find CTOs at AI companies
Get me VPs of Sales at SaaS companies
Find founders in fintech
```

### By Location
```
Find CTOs in San Francisco
Get me VPs of Engineering in New York
Find founders in Austin, Texas
```

### By Company Stage
```
Find CTOs at Series B startups
Get me founders at seed stage companies
Find VPs at enterprise companies
```

### Combined
```
Find CTOs at AI companies in San Francisco
Get me VPs of Sales at Series B SaaS companies in NYC
Find founders at fintech startups in London
```

---

## 🎨 Interface Layout

```
┌─────────────────────────────────────────────────────────────┐
│  [☰] LeadOn                    [AI Search] [Sync] [Create]  │ ← Top Bar
├──────────┬──────────────────────────────────────────────────┤
│          │  Contacts                                         │
│ [👥] Contacts                                                │
│ [🏢] Companies  [Search...........................] [Filter] │
│ [📢] Campaigns                                               │
│ [💼] Jobs       ┌────────────────────────────────────────┐  │
│          │      │ ☑ Name  Links  Title  Company  Email  │  │
│          │      ├────────────────────────────────────────┤  │
│          │      │ ☐ Sarah Chen  🔗  CTO  TechCorp  ...  │  │
│ [👤] Admin      │ ☐ Michael R.  🔗  VP   Innovate  ...  │  │
│          │      │ ☐ Emily W.    🔗  Head DataStream ... │  │
└──────────┴──────┴────────────────────────────────────────┴──┘
    ↑                           ↑
 Sidebar                    Main Table
```

---

## 🔧 Configuration Files

### .env (Environment Variables)
```bash
OPENAI_API_KEY=sk-...          # Required for AI
APOLLO_API_KEY=...             # Required for contacts
```

### Database
- **Location**: `database/leadon.db`
- **Type**: SQLite (no setup needed)
- **Backup**: Just copy the file!

---

## 🐛 Quick Fixes

### Server won't start?
```bash
# Check if port 8000 is in use
netstat -ano | findstr :8000

# Kill process if needed
taskkill /PID <process_id> /F

# Restart server
python crm_integration/chat_api.py
```

### No contacts showing?
```bash
# Add sample data
python add_sample_contacts.py

# Refresh browser
Ctrl + F5
```

### AI Search not working?
1. Check `.env` has API keys
2. Check server logs for errors
3. Try simpler query: "Find CTOs"

---

## 📈 Database Stats

```bash
# Quick stats
python -c "
from database.db_manager import get_db_manager
from database.models import Contact, Company
db = get_db_manager()
session = db.get_session()
print(f'Contacts: {session.query(Contact).count()}')
print(f'Companies: {session.query(Company).count()}')
session.close()
"
```

---

## 🎯 Best Practices

### Finding Contacts
1. **Start specific**: "Find CTOs at AI companies in SF"
2. **Use job enrichment**: Check the box for better results
3. **Limit credits**: Set max contacts to 25-50
4. **Review results**: Check quality before exporting

### Managing Data
1. **Regular exports**: Backup your contacts weekly
2. **Clean duplicates**: Review before campaigns
3. **Tag contacts**: Use campaigns to organize
4. **Update info**: Keep contact details current

### Campaigns
1. **Segment**: Select specific groups
2. **Personalize**: Use contact details in messages
3. **Track**: Monitor response rates
4. **Iterate**: Improve based on results

---

## 📞 Support

### Documentation
- **NEW_CRM_GUIDE.md** - Full usage guide
- **CURRENT_STATUS.md** - Current setup
- **README.md** - Project overview

### API Documentation
- http://localhost:8000/docs

### Logs
- Server logs in terminal
- Browser console (F12) for frontend errors

---

## 🎉 Quick Win Checklist

- [ ] Server running at http://localhost:8000
- [ ] Open http://localhost:8000/crm
- [ ] See 11 sample contacts in table
- [ ] Try search/filter
- [ ] Click "AI Search" button
- [ ] Send query: "Find CTOs at AI companies"
- [ ] Watch contacts populate
- [ ] Select some contacts
- [ ] Export to CSV
- [ ] 🎊 You're a CRM pro!

---

## 💡 Pro Tips

1. **Sidebar collapse**: Click ☰ for more screen space
2. **Pagination**: Navigate with arrows at bottom
3. **Select all**: Checkbox in header selects page
4. **LinkedIn links**: Click 🔗 to open profiles
5. **Email links**: Click email to open mail client
6. **Real-time**: Auto-refreshes every 30 seconds
7. **CSV export**: Opens in Excel/Google Sheets
8. **Job enrichment**: Finds companies hiring

---

## 🚀 You're All Set!

Everything you need is in this one file. Bookmark it! 📌

