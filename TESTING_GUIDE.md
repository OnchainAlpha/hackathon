# 🧪 Testing Guide - LeadOn CRM Job Enrichment

## Quick Start (3 Steps)

### Step 1: Start the Server

Open a terminal and run:
```bash
python crm_integration\chat_api.py
```

You should see:
```
============================================================
🚀 LeadOn Chat CRM API starting...
============================================================
   Claude API:    ✅ Configured
   Apollo API:    ✅ Configured (real data)
   Twenty CRM:    ✅ Configured

   📚 API Docs:   http://localhost:8000/docs
   💬 Chat UI:    http://localhost:8000
============================================================
```

### Step 2: Open the Browser

Navigate to: **http://localhost:8000**

### Step 3: Run Tests

---

## 🧪 Test Scenarios

### Test 1: Normal Apollo Search (Without Job Enrichment)

**Purpose**: Test the basic Apollo search functionality

**Steps**:
1. Enter query: `Find CTOs at AI companies in San Francisco`
2. Leave "Enrich with Job Postings" **UNCHECKED**
3. Click "Search Contacts"

**Expected Result**:
- Should return contacts from Apollo.io
- Response: "I found X contacts matching your criteria"
- Contacts table shows: Name, Title, Company, Email, LinkedIn
- Data source: "(Data from Apollo.io)"

**What to verify**:
- ✅ Contacts are real (from Apollo)
- ✅ Titles match "CTO"
- ✅ Companies are AI-related
- ✅ Locations are San Francisco area

---

### Test 2: Job Enrichment (Basic)

**Purpose**: Test the complete job enrichment workflow

**Steps**:
1. Enter query: `Find companies that need sales automation`
2. **CHECK** "Enrich with Job Postings" ✅
3. Enter product description: `Sales automation platform for B2B companies`
4. Click "Search Contacts"

**Expected Result**:
```
Found 15 companies and 47 contacts!

📊 Enrichment Stats:
• 60 job postings analyzed
• 15 companies matched (score ≥ 60)
• 47 decision-makers found

The companies have been scored based on their fit for your product.
Check the database for detailed match reasoning!
```

**What to verify**:
- ✅ Job postings were scraped from LinkedIn
- ✅ Companies were extracted from job postings
- ✅ Companies have match scores (60-100)
- ✅ Contacts are decision-makers (CEO, VP, Director)
- ✅ Response time: 30-60 seconds (due to scraping)

**Note**: This test will take longer because it:
1. Generates job search queries with Claude
2. Scrapes LinkedIn job postings (20 per query)
3. Analyzes companies with Claude
4. Searches Apollo for contacts

---

### Test 3: Job Enrichment (Specific Product)

**Purpose**: Test AI matching with specific product description

**Steps**:
1. Enter query: `Find companies I can sell my marketing automation tool to`
2. **CHECK** "Enrich with Job Postings" ✅
3. Enter product: `Email marketing and automation platform for SaaS companies`
4. Click "Search Contacts"

**Expected Result**:
- Companies hiring for marketing roles
- High match scores for companies with active marketing hiring
- Contacts: Marketing VPs, CMOs, Growth leads

**What to verify**:
- ✅ Job postings are marketing-related
- ✅ Companies are SaaS/tech companies
- ✅ Match reasoning mentions marketing needs

---

### Test 4: Compare Results

**Purpose**: Compare normal search vs job enrichment

**Test A - Normal Search**:
1. Query: `Find companies in the AI space`
2. Enrichment: **OFF**
3. Note the results

**Test B - Job Enrichment**:
1. Query: `Find companies in the AI space`
2. Enrichment: **ON**
3. Product: `AI development tools and APIs`
4. Note the results

**Compare**:
- Normal search: Broader results, faster
- Job enrichment: More targeted, companies actively hiring, slower

---

## 🔍 Verify Database

After running tests, check the database:

```python
from database.db_manager import get_db_manager

db = get_db_manager()
session = db.get_session()

# Check companies
from database.models import Company
companies = session.query(Company).all()
print(f"Total companies: {len(companies)}")

# Check top matched companies
top_companies = db.get_top_matched_companies(session, limit=10)
for company in top_companies:
    print(f"\n{company.name}")
    print(f"  Score: {company.match_score}/100")
    print(f"  Reasoning: {company.match_reasoning}")
    print(f"  Contacts: {len(company.contacts)}")
    print(f"  Job Postings: {len(company.job_postings)}")

# Check contacts
from database.models import Contact
contacts = session.query(Contact).all()
print(f"\nTotal contacts: {len(contacts)}")

# Check job postings
from database.models import JobPosting
jobs = session.query(JobPosting).all()
print(f"Total job postings: {len(jobs)}")

session.close()
```

---

## 🐛 Troubleshooting

### Issue: Server won't start

**Error**: `Address already in use`

**Solution**:
```bash
# Find process on port 8000
netstat -ano | findstr :8000

# Kill the process
taskkill /F /PID <PID>
```

### Issue: Claude API errors

**Error**: `404 - model not found`

**Check**: Make sure you're using `claude-3-haiku-20240307`

**Solution**: Already fixed in the code!

### Issue: Apollo API errors

**Error**: `403 Forbidden`

**Check**: Your API key is set correctly in `.env`

**Current key**: `E0-borDrTehbfPZN5P4i5Q`

### Issue: LinkedIn scraping fails

**Error**: Rate limiting or blocked requests

**Reasons**:
- LinkedIn detects automated scraping
- Too many requests in short time
- IP address blocked

**Solutions**:
1. Reduce `jobs_per_query` from 20 to 10
2. Add longer delays between requests
3. Use proxies (advanced)
4. Test with smaller queries first

### Issue: Job enrichment takes too long

**Expected**: 30-60 seconds for full enrichment

**If longer**:
- Reduce `jobs_per_query` in the service
- Reduce number of queries generated
- Check network connection

---

## 📊 Expected Performance

### Normal Apollo Search:
- **Time**: 1-3 seconds
- **Results**: 10-100 contacts
- **Data source**: Apollo.io API

### Job Enrichment:
- **Time**: 30-60 seconds
- **Steps**:
  - Query generation: 2-3 seconds
  - Job scraping: 20-30 seconds (20 jobs × 3 queries)
  - Company analysis: 5-10 seconds
  - Apollo enrichment: 5-10 seconds
- **Results**: 10-50 companies, 20-100 contacts

---

## ✅ Success Criteria

After testing, you should have:

1. ✅ Server running on http://localhost:8000
2. ✅ Normal Apollo search working (fast, broad results)
3. ✅ Job enrichment working (slower, targeted results)
4. ✅ Database populated with:
   - Companies with match scores
   - Contacts linked to companies
   - Job postings with relevance scores
5. ✅ UI showing enrichment stats
6. ✅ All API keys working (Claude + Apollo)

---

## 🎯 Next Steps After Testing

Once testing is successful:

1. **Optimize scraping**: Adjust `jobs_per_query` based on needs
2. **Add more sources**: Indeed, Google Jobs, Glassdoor
3. **Implement caching**: Cache job postings to avoid re-scraping
4. **Add filters**: Company size, industry, location filters
5. **Export functionality**: Export results to CSV
6. **Campaign management**: Track multiple campaigns
7. **Analytics**: Visualize match scores and conversion rates

---

## 📝 Test Checklist

Use this checklist while testing:

- [ ] Server starts without errors
- [ ] UI loads at http://localhost:8000
- [ ] Normal Apollo search works
- [ ] Job enrichment checkbox appears
- [ ] Product description field shows when checked
- [ ] Job enrichment completes successfully
- [ ] Results show enrichment stats
- [ ] Database contains companies
- [ ] Database contains contacts
- [ ] Database contains job postings
- [ ] Companies have match scores
- [ ] Match reasoning is populated
- [ ] Contacts are linked to companies
- [ ] Job postings are linked to companies

---

## 🚀 Ready to Test!

Start with **Test 1** (Normal Apollo Search) to verify basic functionality, then move to **Test 2** (Job Enrichment) for the full workflow.

**Good luck!** 🎉

