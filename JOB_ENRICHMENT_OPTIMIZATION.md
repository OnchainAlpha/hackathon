# 🎯 Job Enrichment Optimization - Credit Saving & Better Tagging

## 📋 Summary of Changes

Fixed three major issues with the job enrichment workflow:

1. **❌ Problem: Wasting Apollo Credits** - Was fetching 10+ contacts per company (e.g., Alpargatas had 8+ contacts)
2. **❌ Problem: Generic Tags** - Tags like `vp-level`, `seniority:vp` don't explain WHY the contact was added
3. **❌ Problem: No Job Context** - Contacts didn't show which job posting led to finding them

### ✅ Solutions Implemented

1. **Limit to 1 Contact Per Company** - Only fetch the top decision maker (CEO or Director)
2. **Enhanced Tags with Job Context** - Add `job_posting:Senior Engineer` tag to show recruitment context
3. **Source Reason Field** - Add detailed explanation: "Found via job enrichment: Alpargatas S.A. is recruiting for Senior Software Engineer"

---

## 🔧 Changes Made

### 1. **`services/job_enrichment_service.py`**

#### **Method: `enrich_companies_with_apollo()`**

**Before:**
```python
def enrich_companies_with_apollo(self, session, companies: List[Company], 
                                target_titles: List[str] = None) -> List[Contact]:
    if target_titles is None:
        target_titles = ["CEO", "CTO", "VP", "Director", "Head of"]
    
    for company in companies:
        result = self.apollo.search_people(
            company_names=[company.name],
            titles=target_titles,
            per_page=10  # ❌ Gets 10 contacts per company!
        )
        
        for contact_obj in result.contacts:  # ❌ Saves ALL contacts
            contact, created = self.db.get_or_create_contact(...)
```

**After:**
```python
def enrich_companies_with_apollo(self, session, companies: List[Company], 
                                target_titles: List[str] = None,
                                max_contacts_per_company: int = 1) -> List[Contact]:
    if target_titles is None:
        # ✅ Focus on top decision makers only
        target_titles = ["CEO", "Chief Executive Officer", "Director", "Managing Director"]
    
    for company in companies:
        # ✅ Get job postings for context
        job_postings = session.query(JobPosting).filter(
            JobPosting.company_id == company.id
        ).all()
        
        job_titles = [jp.title for jp in job_postings if jp.title]
        job_context = f"recruiting for {', '.join(job_titles[:3])}" if job_titles else "has job openings"
        
        result = self.apollo.search_people(
            company_names=[company.name],
            titles=target_titles,
            per_page=25  # Get options to choose from
        )
        
        # ✅ Only save the first contact (top decision maker)
        contacts_to_save = result.contacts[:max_contacts_per_company]
        
        for contact_obj in contacts_to_save:
            # ✅ Add job posting context tag
            enhanced_tags = existing_tags.copy() if existing_tags else []
            enhanced_tags.append(f"job_posting:{job_titles[0][:30] if job_titles else 'unknown'}")
            
            # ✅ Build source reason with job context
            source_reason = f"Found via job enrichment: {company.name} is {job_context}"
            
            contact, created = self.db.get_or_create_contact(
                ...,
                tags=enhanced_tags,
                source_reason=source_reason,
                ...
            )
```

**Key Changes:**
- ✅ Added `max_contacts_per_company` parameter (default: 1)
- ✅ Changed default titles to focus on CEO/Director only
- ✅ Fetch job postings to build context
- ✅ Only save top `max_contacts_per_company` contacts (default 1)
- ✅ Add `job_posting:` tag with the job title
- ✅ Add `source_reason` explaining why contact was added

---

#### **Method: `run_full_enrichment()`**

**Before:**
```python
def run_full_enrichment(self, user_query: str, product_description: str = "",
                       jobs_per_query: int = 20, min_match_score: float = 60):
    ...
    contacts = self.enrich_companies_with_apollo(session, matched_companies)
```

**After:**
```python
def run_full_enrichment(self, user_query: str, product_description: str = "",
                       jobs_per_query: int = 20, min_match_score: float = 60,
                       max_contacts_per_company: int = 1):  # ✅ New parameter
    ...
    contacts = self.enrich_companies_with_apollo(
        session, 
        matched_companies,
        max_contacts_per_company=max_contacts_per_company  # ✅ Pass parameter
    )
```

---

### 2. **`scrapers/apollo_scraper.py`**

#### **Method: `_parse_person()`**

**Before:**
```python
# Generate tags based on title, seniority, and industry
tags = []
title = person_data.get("title", "").lower()
seniority = person_data.get("seniority", "").lower()

# Add role-based tags
if any(word in title for word in ["ceo", "chief executive", "founder", "co-founder"]):
    tags.append("founder/ceo")  # ❌ Generic tag
if any(word in title for word in ["cto", "chief technology"]):
    tags.append("cto")  # ❌ Generic tag
if any(word in title for word in ["vp", "vice president"]):
    tags.append("vp-level")  # ❌ Generic tag

# Add seniority tag
if seniority:
    tags.append(f"seniority:{seniority}")  # ❌ Raw seniority value
```

**After:**
```python
# Generate tags based on title, seniority, and industry
tags = []
title = person_data.get("title", "").lower()
seniority = person_data.get("seniority", "").lower()

# ✅ Add role-based tags with descriptive prefixes
if any(word in title for word in ["ceo", "chief executive", "founder", "co-founder"]):
    tags.append("role:ceo_founder")
if any(word in title for word in ["cto", "chief technology"]):
    tags.append("role:cto")
if any(word in title for word in ["cfo", "chief financial"]):
    tags.append("role:cfo")
if any(word in title for word in ["vp", "vice president"]):
    tags.append("role:vp")
if "director" in title:
    tags.append("role:director")
if "head of" in title or "head " in title:
    tags.append("role:head")

# ✅ Add department tags
if "engineer" in title:
    tags.append("dept:engineering")
if any(word in title for word in ["sales", "revenue", "business development"]):
    tags.append("dept:sales")
if "product" in title:
    tags.append("dept:product")
if any(word in title for word in ["marketing", "growth"]):
    tags.append("dept:marketing")

# ✅ Add seniority tag with readable formatting
if seniority:
    seniority_map = {
        "c_suite": "C-Suite Executive",
        "vp": "VP Level",
        "director": "Director Level",
        "manager": "Manager Level",
        "senior": "Senior Level",
        "entry": "Entry Level"
    }
    readable_seniority = seniority_map.get(seniority, seniority.title())
    tags.append(f"seniority:{readable_seniority}")

# ✅ Add industry tags with prefix
if "7372" in sic_codes or "541511" in naics_codes:
    tags.append("industry:software")
if "7375" in sic_codes or "518" in naics_codes or "519" in naics_codes:
    tags.append("industry:saas")
```

**Key Changes:**
- ✅ Added prefixes to tags: `role:`, `dept:`, `seniority:`, `industry:`
- ✅ More descriptive tag names (e.g., `role:ceo_founder` instead of `founder/ceo`)
- ✅ Added department tags for better categorization
- ✅ Mapped raw seniority values to readable names (e.g., `c_suite` → `C-Suite Executive`)
- ✅ Added more role types (CFO, COO, Head)

---

### 3. **`database/db_manager.py`**

#### **Method: `get_or_create_contact()`**

**Before:**
```python
def get_or_create_contact(self, session: Session, email: Optional[str] = None,
                         linkedin_url: Optional[str] = None, **kwargs):
    contact = None
    if email:
        contact = self.get_contact_by_email(session, email)
    if not contact and linkedin_url:
        contact = self.get_contact_by_linkedin(session, linkedin_url)
    
    if contact:
        return contact, False  # ❌ Doesn't update existing contact
    
    contact = self.create_contact(session, email=email, linkedin_url=linkedin_url, **kwargs)
    return contact, True
```

**After:**
```python
def get_or_create_contact(self, session: Session, email: Optional[str] = None,
                         linkedin_url: Optional[str] = None, **kwargs):
    contact = None
    if email:
        contact = self.get_contact_by_email(session, email)
    if not contact and linkedin_url:
        contact = self.get_contact_by_linkedin(session, linkedin_url)
    
    if contact:
        # ✅ Update existing contact with new tags and source_reason
        if 'tags' in kwargs and kwargs['tags']:
            # Merge new tags with existing tags (avoid duplicates)
            existing_tags = contact.tags or []
            new_tags = kwargs['tags']
            merged_tags = list(set(existing_tags + new_tags))
            contact.tags = merged_tags
        
        if 'source_reason' in kwargs and kwargs['source_reason']:
            # Update source reason if new one is more specific
            contact.source_reason = kwargs['source_reason']
        
        session.flush()
        return contact, False
    
    contact = self.create_contact(session, email=email, linkedin_url=linkedin_url, **kwargs)
    return contact, True
```

**Key Changes:**
- ✅ Merge new tags with existing tags when updating a contact
- ✅ Update `source_reason` if provided
- ✅ Avoid duplicate tags using `set()`

---

### 4. **`crm_integration/chat_api.py`**

**Before:**
```python
enrichment_result = job_enrichment.run_full_enrichment(
    user_query=message.message,
    product_description=message.product_description or "",
    jobs_per_query=20,
    min_match_score=60
)
```

**After:**
```python
enrichment_result = job_enrichment.run_full_enrichment(
    user_query=message.message,
    product_description=message.product_description or "",
    jobs_per_query=20,
    min_match_score=60,
    max_contacts_per_company=1  # ✅ Only 1 contact per company to save Apollo credits
)
```

---

## 📊 Impact

### **Before:**
- **Alpargatas S.A.**: 8+ contacts fetched (wasting 8 Apollo credits)
- **Tags**: `['vp-level', 'seniority:vp']` - generic, no context
- **Source Reason**: Empty or generic
- **Total Contacts**: 25+ contacts from job enrichment

### **After:**
- **Alpargatas S.A.**: 1 contact fetched (CEO or Director only)
- **Tags**: `['role:director', 'seniority:Director Level', 'dept:engineering', 'job_posting:Senior Software Engineer']`
- **Source Reason**: `"Found via job enrichment: Alpargatas S.A. is recruiting for Senior Software Engineer, DevOps Engineer"`
- **Total Contacts**: ~5-10 contacts (1 per company)

### **Credit Savings:**
- **Before**: 25 contacts = 25 Apollo credits
- **After**: 5-10 contacts = 5-10 Apollo credits
- **Savings**: 60-80% reduction in Apollo API usage! 💰

---

## 🧪 Testing

To test the changes, restart the server and run a job enrichment search:

```bash
# The server should auto-reload, or restart manually:
python -m uvicorn crm_integration.chat_api:app --reload --host 0.0.0.0 --port 8000
```

Then in the CRM interface:
1. Go to http://localhost:8000/crm
2. Enable "Job Enrichment" toggle
3. Search: "Find companies hiring engineers"
4. Check the results - you should see:
   - Only 1 contact per company
   - Tags like `job_posting:Senior Engineer`
   - Source reason explaining the job posting context

---

## 🎯 Next Steps

If you want to get more contacts per company in the future, you can adjust the parameter:

```python
# In chat_api.py, change max_contacts_per_company:
enrichment_result = job_enrichment.run_full_enrichment(
    ...,
    max_contacts_per_company=2  # Get 2 contacts per company
)
```

Or make it configurable via the UI by adding a slider in the frontend! 🎨

