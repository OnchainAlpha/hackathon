# Apollo.io Contact Scraper - LeadOn CRM

A powerful CLI tool for searching and enriching contact data using the Apollo.io API.

## 🚀 Features

- **Contact Search**: Find contacts by keywords, job titles, locations, and companies
- **Contact Enrichment**: Get detailed information including emails and phone numbers
- **Organization Search**: Find companies by various criteria
- **Interactive Mode**: User-friendly prompts for easy searching
- **Export Options**: Save results to JSON or CSV
- **Rate Limiting**: Built-in rate limiting to respect API limits
- **Error Handling**: Robust retry logic and error handling

## 📋 Prerequisites

- Python 3.8+
- Apollo.io API key (already configured in `.env`)

## 🔧 Installation

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

2. **Verify API key** (already set in `.env`):
```bash
# Your API key is: F--Az_2MyIh9U0Gg_m4yZQ
```

## 💻 Usage

### Interactive Mode (Recommended for beginners)

Simply run the search command and follow the prompts:

```bash
python -m cli.search_contacts search
```

### Command-Line Mode

#### Search for contacts:

```bash
# Basic search
python -m cli.search_contacts search -q "artificial intelligence"

# Search with filters
python -m cli.search_contacts search \
  -q "AI startup" \
  -t "CEO,CTO,Founder" \
  -l "San Francisco, CA, USA" \
  -n 50

# Search and export to JSON
python -m cli.search_contacts search \
  -q "venture capital" \
  -t "Partner,Investor" \
  --json

# Search and export to CSV
python -m cli.search_contacts search \
  -q "machine learning" \
  -t "Data Scientist,ML Engineer" \
  --csv
```

#### Enrich a contact:

```bash
# Enrich by email
python -m cli.search_contacts enrich --email john@example.com

# Enrich by LinkedIn URL
python -m cli.search_contacts enrich --linkedin "https://linkedin.com/in/johndoe"

# Enrich by name and company
python -m cli.search_contacts enrich \
  --first-name John \
  --last-name Doe \
  --domain example.com
```

#### Show help:

```bash
python -m cli.search_contacts --help
python -m cli.search_contacts search --help
python -m cli.search_contacts enrich --help
```

## 📊 Example Workflows

### 1. Find AI Investors in San Francisco

```bash
python -m cli.search_contacts search \
  -q "artificial intelligence venture capital" \
  -t "Partner,Managing Partner,Investor" \
  -l "San Francisco, CA, USA" \
  -n 30 \
  --json
```

### 2. Find CTOs at AI Companies

```bash
python -m cli.search_contacts search \
  -q "artificial intelligence" \
  -t "CTO,Chief Technology Officer" \
  -n 50 \
  --csv
```

### 3. Find Contacts at Specific Companies

```bash
python -m cli.search_contacts search \
  -c "Anthropic,OpenAI,Google DeepMind" \
  -t "CEO,CTO,VP Engineering" \
  -n 25
```

### 4. Enrich Existing Contact

```bash
python -m cli.search_contacts enrich \
  --email dario@anthropic.com \
  --reveal-email \
  --reveal-phone
```

## 🔗 Integration with Job Scraper

Your teammate is building job site scrapers. Here's how to integrate:

### Workflow Example:

1. **Job Scraper finds**: "Anthropic is hiring ML Engineer"
2. **Apollo enriches company**: Get company details, funding, size
3. **Apollo finds contacts**: Search for decision-makers at Anthropic
4. **CRM stores**: All contacts with tags ["anthropic", "ai_company", "hiring_ml"]
5. **LinkedIn bot**: Engages with contacts

### Code Integration:

```python
from scrapers.apollo_scraper import ApolloClient

# Initialize client
client = ApolloClient()

# When job scraper finds a company
company_name = "Anthropic"

# 1. Search for decision-makers at that company
result = client.search_people(
    company_names=[company_name],
    titles=["CEO", "CTO", "Head of AI", "VP Engineering"],
    per_page=25
)

# 2. Enrich each contact
for contact in result.contacts:
    enriched = client.enrich_person(
        email=contact.email,
        reveal_personal_emails=True,
        reveal_phone_number=True
    )
    # Save to CRM...
```

## 📁 Output Files

Exported files are saved to the `exports/` directory:

- **JSON**: `exports/contacts_<query>_<page>.json`
- **CSV**: `exports/contacts_<query>_<page>.csv`

## 🎯 Use Cases for Your CRM

### 1. Lead Generation
- Search for target personas (e.g., "VCs investing in AI")
- Export to CRM with appropriate tags
- LinkedIn bot engages automatically

### 2. Company Intelligence
- Job scraper finds companies hiring
- Apollo enriches company data
- Find multiple contacts at each company (multi-threading)

### 3. Contact Enrichment
- Periodically refresh CRM contacts
- Verify emails before campaigns
- Update job titles and companies

### 4. Lead Scoring
- Use Apollo's company data (funding, size, growth)
- Score leads automatically
- Prioritize high-value prospects

### 5. Relationship Mapping
- Find multiple contacts at target companies
- Map organizational structure
- Multi-threaded outreach strategy

## 🔍 Apollo.io API Capabilities

### People Search Filters:
- Keywords
- Job titles
- Locations
- Seniority levels
- Company names
- Industries
- Company size (employee ranges)

### People Enrichment:
- Email addresses (work + personal)
- Phone numbers
- LinkedIn URLs
- Social media profiles
- Current company and title
- Location details

### Organization Search Filters:
- Company name
- Locations
- Employee count ranges
- Industries
- Funding stages
- Technologies used

### Organization Enrichment:
- Company details
- Funding information
- Employee count
- Revenue estimates
- Technologies
- Social media

## ⚙️ Configuration

Edit `.env` file to customize:

```bash
# Apollo.io API
APOLLO_API_KEY=F--Az_2MyIh9U0Gg_m4yZQ

# Rate Limiting
APOLLO_REQUESTS_PER_MINUTE=60

# Logging
LOG_LEVEL=INFO
```

## 📝 Logging

Logs are saved to `logs/scraper_<timestamp>.log` with:
- Request/response details
- Error messages and stack traces
- Rate limiting information
- Performance metrics

## 🚨 Rate Limits

Apollo.io uses fixed-window rate limiting. Default: 60 requests/minute.

The scraper automatically:
- Tracks request timestamps
- Waits when limit is reached
- Retries failed requests (3 attempts)
- Logs rate limit information

## 🛠️ Troubleshooting

### "Apollo API key is required"
- Check `.env` file exists
- Verify `APOLLO_API_KEY` is set correctly

### "No contacts found"
- Try broader search terms
- Remove some filters
- Check spelling of locations/titles

### Rate limit errors
- Wait a few minutes
- Reduce `per_page` parameter
- Increase `APOLLO_REQUESTS_PER_MINUTE` in `.env`

## 🔮 Future Enhancements

- [ ] Direct CRM database integration
- [ ] Bulk enrichment (10 contacts at once)
- [ ] Advanced query parsing with NLP
- [ ] Automated tagging based on data
- [ ] Integration with LinkedIn automation
- [ ] Real-time contact monitoring
- [ ] Webhook support for new contacts

## 📚 API Documentation

Full Apollo.io API docs: https://docs.apollo.io/reference/

## 🤝 Team Integration

This scraper is part of **Team 1 (Scraper Team)** for the LeadOn CRM project.

**Integration Points**:
- **Team 2 (CRM)**: Use Contact schema from `scrapers/schemas.py`
- **Team 3 (LinkedIn)**: Contacts include LinkedIn URLs for automation
- **Job Scraper**: Share company names for cross-referencing

## 📞 Support

For issues or questions, check:
1. This README
2. `context.md` for project overview
3. Apollo.io API docs
4. Log files in `logs/` directory

---

**Built for LeadOn CRM Hackathon Project** 🚀

