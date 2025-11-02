"""
Chat-based CRM API
Conversational interface for scraping and populating Twenty CRM
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import json
from pathlib import Path
from datetime import datetime
import sys
import os
import asyncio
import requests

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from scrapers.schemas import Contact
from scrapers.apollo_scraper import ApolloClient
# Removed Twenty CRM sync - we have our own CRM now!
# from crm_integration.twenty_sync import TwentyCRMSync, sync_apollo_to_twenty
from ai_agent.intent_parser import IntentParser, ScraperOrchestrator
from cli.search_mock import load_mock_contacts, filter_contacts
from database.db_manager import get_db_manager
from services.job_enrichment_service import JobEnrichmentService
from services.agentic_search_service import AgenticSearchService
from services.company_profile_service import CompanyProfileService
from services.company_enrichment_service import CompanyEnrichmentService
from scrapers.linkedin_scraper import get_linkedin_scraper
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = FastAPI(
    title="LeadOn Chat CRM API",
    description="Conversational interface for lead generation and CRM population",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Initialize services
try:
    intent_parser = IntentParser()
    has_claude = True
except Exception as e:
    print(f"⚠️  Claude (Anthropic) not configured: {e}")
    intent_parser = None
    has_claude = False

orchestrator = ScraperOrchestrator() if has_claude else None
# Removed Twenty CRM sync - we have our own CRM now!
# twenty_sync = TwentyCRMSync(api_token=os.getenv("TWENTY_CRM_API_TOKEN"))

# Initialize database and services
db_manager = get_db_manager()
job_enrichment = None
agentic_search = None
company_profile_service = None
company_enrichment_service = None
apollo_company_enrichment = None

if has_claude and os.getenv("APOLLO_API_KEY"):
    try:
        apollo_scraper = ApolloClient()
        job_enrichment = JobEnrichmentService(apollo_scraper, intent_parser, db_manager)
        agentic_search = AgenticSearchService(apollo_scraper, db_manager)
        company_profile_service = CompanyProfileService(os.getenv("ANTHROPIC_API_KEY"))
        company_enrichment_service = CompanyEnrichmentService(os.getenv("ANTHROPIC_API_KEY"))

        # Import and initialize Apollo company enrichment
        from services.apollo_company_enrichment import ApolloCompanyEnrichment
        apollo_company_enrichment = ApolloCompanyEnrichment(apollo_scraper)

        logger.info("✅ Job enrichment service initialized")
        logger.info("✅ Agentic search service initialized")
        logger.info("✅ Company profile service initialized")
        logger.info("✅ Company enrichment service initialized")
        logger.info("✅ Apollo company enrichment service initialized")
    except Exception as e:
        logger.warning(f"⚠️  Services not available: {e}")

# Storage
chat_history: List[Dict[str, Any]] = []
contacts_db: List[Contact] = []


# Models
class ChatMessage(BaseModel):
    """Chat message model"""
    message: str
    website_url: Optional[str] = None
    campaign_objective: Optional[str] = None
    enrich_with_jobs: bool = False  # Enable job postings enrichment
    product_description: Optional[str] = None  # Product/service description for AI matching
    max_contacts: int = 25  # Maximum contacts to find (Apollo credits control)


class ChatResponse(BaseModel):
    """Chat response model"""
    response: str
    contacts_found: int
    contacts_added: int
    intent: Optional[Dict[str, Any]] = None
    timestamp: datetime


class ContactsResponse(BaseModel):
    """Contacts list response"""
    contacts: List[Contact]
    total: int
    timestamp: datetime


# Endpoints
@app.get("/")
async def root():
    """Serve LeadOn Pro frontend"""
    html_path = Path(__file__).parent / "frontend" / "leadon_pro.html"
    if html_path.exists():
        return FileResponse(html_path)

    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>LeadOn CRM</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
            .container { max-width: 1400px; margin: 0 auto; }
            h1 { color: #333; }
            .status { padding: 20px; background: white; border-radius: 8px; margin-bottom: 20px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 LeadOn CRM API</h1>
            <div class="status">
                <h2>Status</h2>
                <p>✅ API is running</p>
                <p>📚 API Docs: <a href="/docs">/docs</a></p>
                <p>💬 Chat Endpoint: POST /api/chat</p>
                <p>📊 Contacts Endpoint: GET /api/contacts</p>
            </div>
        </div>
    </body>
    </html>
    """)


@app.get("/classic")
async def classic():
    """Serve classic chat CRM interface"""
    html_path = Path(__file__).parent / "frontend" / "chat_crm.html"
    if html_path.exists():
        return FileResponse(html_path)
    return HTMLResponse("<h1>Classic interface not found</h1>")


@app.get("/leadon_pro.js")
async def serve_js():
    """Serve the JavaScript file"""
    js_path = Path(__file__).parent / "frontend" / "leadon_pro.js"
    if js_path.exists():
        return FileResponse(js_path, media_type="application/javascript")
    return HTMLResponse("// JS file not found", status_code=404)


@app.get("/crm")
async def serve_crm():
    """Serve the new LeadOn CRM interface"""
    html_path = Path(__file__).parent / "frontend" / "leadon_crm.html"
    if html_path.exists():
        return FileResponse(html_path)
    return HTMLResponse("<h1>CRM interface not found</h1>", status_code=404)


@app.get("/crm/companies")
async def serve_companies():
    """Serve the Companies page"""
    html_path = Path(__file__).parent / "frontend" / "companies.html"
    if html_path.exists():
        return FileResponse(html_path)
    return HTMLResponse("<h1>Companies page not found</h1>", status_code=404)


@app.get("/crm/campaigns")
async def serve_campaigns():
    """Serve the Campaigns page"""
    html_path = Path(__file__).parent / "frontend" / "campaigns.html"
    if html_path.exists():
        return FileResponse(html_path)
    return HTMLResponse("<h1>Campaigns page not found</h1>", status_code=404)


@app.get("/crm/integrations")
async def serve_integrations():
    """Serve the Integrations page"""
    html_path = Path(__file__).parent / "frontend" / "integrations.html"
    if html_path.exists():
        return FileResponse(html_path)
    return HTMLResponse("<h1>Integrations page not found</h1>", status_code=404)


@app.get("/leadon_crm.js")
async def serve_crm_js():
    """Serve the CRM JavaScript file"""
    js_path = Path(__file__).parent / "frontend" / "leadon_crm.js"
    if js_path.exists():
        return FileResponse(js_path, media_type="application/javascript")
    return HTMLResponse("// JS file not found", status_code=404)


@app.get("/companies.js")
async def serve_companies_js():
    """Serve the Companies JavaScript file"""
    js_path = Path(__file__).parent / "frontend" / "companies.js"
    if js_path.exists():
        return FileResponse(js_path, media_type="application/javascript")
    return HTMLResponse("// JS file not found", status_code=404)


@app.get("/campaigns.js")
async def serve_campaigns_js():
    """Serve the Campaigns JavaScript file"""
    js_path = Path(__file__).parent / "frontend" / "campaigns.js"
    if js_path.exists():
        return FileResponse(js_path, media_type="application/javascript")
    return HTMLResponse("// JS file not found", status_code=404)


@app.get("/integrations.js")
async def serve_integrations_js():
    """Serve the Integrations JavaScript file"""
    js_path = Path(__file__).parent / "frontend" / "integrations.js"
    if js_path.exists():
        return FileResponse(js_path, media_type="application/javascript")
    return HTMLResponse("// JS file not found", status_code=404)


@app.get("/crm/integrations.js")
async def serve_integrations_js_alt():
    """Serve the Integrations JavaScript file (alternate route)"""
    js_path = Path(__file__).parent / "frontend" / "integrations.js"
    if js_path.exists():
        return FileResponse(js_path, media_type="application/javascript")
    return HTMLResponse("// JS file not found", status_code=404)


@app.get("/crm/companies.js")
async def serve_companies_js_alt():
    """Serve the Companies JavaScript file (alternate route)"""
    js_path = Path(__file__).parent / "frontend" / "companies.js"
    if js_path.exists():
        return FileResponse(js_path, media_type="application/javascript")
    return HTMLResponse("// JS file not found", status_code=404)


@app.get("/crm/campaigns.js")
async def serve_campaigns_js_alt():
    """Serve the Campaigns JavaScript file (alternate route)"""
    js_path = Path(__file__).parent / "frontend" / "campaigns.js"
    if js_path.exists():
        return FileResponse(js_path, media_type="application/javascript")
    return HTMLResponse("// JS file not found", status_code=404)


@app.get("/twenty")
async def twenty_with_chat():
    """Serve Twenty CRM with LeadOn chat injected"""
    html_path = Path(__file__).parent / "twenty_chat_injector.html"
    if html_path.exists():
        return FileResponse(html_path)
    return HTMLResponse("<h1>Twenty CRM chat injector not found</h1>", status_code=404)


@app.post("/api/chat", response_model=ChatResponse)
async def chat(message: ChatMessage, background_tasks: BackgroundTasks):
    """
    Process chat message and scrape contacts.

    User sends natural language request like:
    - "Find CTOs at AI companies in San Francisco"
    - "Get investors in the FinTech space"
    - "Partnership outreach to SaaS CEOs"

    System:
    1. Parses intent using AI
    2. Calls Apollo API to get real contacts (or uses mock data as fallback)
    3. Saves contacts to CRM database
    4. Syncs to Twenty CRM in background
    5. Returns friendly response
    """
    if not has_claude:
        # Fallback: Simple keyword-based parsing
        return await _simple_chat_handler(message)

    try:
        # Parse intent using AI
        intent = intent_parser.parse_intent(
            message.message,
            message.website_url
        )

        logger.info(f"Parsed intent: {intent.campaign_objective}")
        logger.info(f"  Titles: {intent.titles}")
        logger.info(f"  Locations: {intent.locations}")
        logger.info(f"  Companies: {intent.companies}")

        # Check if job enrichment is requested
        if message.enrich_with_jobs and job_enrichment:
            logger.info("🎯 Job enrichment enabled - running full workflow...")

            try:
                enrichment_result = job_enrichment.run_full_enrichment(
                    user_query=message.message,
                    product_description=message.product_description or "",
                    jobs_per_query=20,
                    min_match_score=60,
                    max_contacts_per_company=1  # Only 1 contact per company to save Apollo credits
                )

                # Convert database models to Contact schema for response
                results = []
                for contact in enrichment_result['contacts']:
                    results.append(Contact(
                        name=contact.name,
                        email=contact.email,
                        title=contact.title,
                        company=contact.company_name,
                        linkedin_url=contact.linkedin_url,
                        phone=contact.phone,
                        city=contact.city,
                        state=contact.state,
                        country=contact.country
                    ))

                using_apollo = True
                logger.info(f"✅ Job enrichment complete: {enrichment_result['stats']}")

                # Generate enhanced response with stats
                response_text = f"""Found {len(enrichment_result['companies'])} companies and {len(results)} contacts!

📊 Enrichment Stats:
• {enrichment_result['stats']['total_jobs_scraped']} job postings analyzed
• {enrichment_result['stats']['matched_companies']} companies matched (score ≥ 60)
• {enrichment_result['stats']['total_contacts']} decision-makers found

The companies have been scored based on their fit for your product. Check the database for detailed match reasoning!"""

                # Skip normal Apollo search
                contacts_added = len(results)

            except Exception as e:
                logger.error(f"❌ Job enrichment failed: {e}")
                # Fall back to normal Apollo search
                message.enrich_with_jobs = False

        # Normal Apollo search (if job enrichment not used or failed)
        if not message.enrich_with_jobs:
            # Try to use agentic search if available
            results = []
            using_apollo = False

            if agentic_search:
                try:
                    logger.info("🤖 Using agentic search to find contacts...")

                    # Run agentic search workflow
                    # Calculate parameters based on max_contacts
                    max_contacts = min(message.max_contacts, 100)  # Cap at 100
                    min_results = min(max_contacts // 2, 10)  # At least half of max, but max 10
                    max_results_per_query = min(max_contacts, 25)  # Per query limit

                    agentic_result = agentic_search.run_agentic_search(
                        user_query=message.message,
                        product_description=message.product_description or "",
                        max_iterations=3,
                        min_results=min_results,
                        max_results_per_query=max_results_per_query
                    )

                    # Convert to Contact objects
                    results = []
                    contacts_without_company = []

                    for contact_dict in agentic_result['contacts']:
                        contact = Contact(
                            name=contact_dict.get('name', ''),
                            email=contact_dict.get('email', ''),
                            title=contact_dict.get('title', ''),
                            company=contact_dict.get('company', ''),  # Contact schema uses 'company', not 'organization_name'
                            linkedin_url=contact_dict.get('linkedin_url', ''),
                            phone=contact_dict.get('phone', ''),
                            city=contact_dict.get('city', ''),
                            state=contact_dict.get('state', ''),
                            country=contact_dict.get('country', '')
                        )
                        results.append(contact)

                        # Track contacts without company for LinkedIn enrichment
                        if not contact.company and contact.linkedin_url:
                            contacts_without_company.append(contact)

                    # Enrich contacts without company names using LinkedIn (limit to first 5 to avoid rate limiting)
                    if contacts_without_company:
                        logger.info(f"🔍 {len(contacts_without_company)} contacts missing company names - enriching from LinkedIn (first 5)...")
                        linkedin_scraper = get_linkedin_scraper()

                        for contact in contacts_without_company[:5]:  # Limit to 5 to avoid rate limiting
                            try:
                                linkedin_data = linkedin_scraper.extract_company_from_profile(contact.linkedin_url)
                                if linkedin_data and linkedin_data.get('company'):
                                    contact.company = linkedin_data['company']
                                    logger.info(f"  ✅ Enriched {contact.name}: {linkedin_data['company']}")
                            except Exception as e:
                                logger.warning(f"  ⚠️  Failed to enrich {contact.name}: {e}")

                    using_apollo = True
                    logger.info(f"✅ Agentic search found {len(results)} contacts")
                    logger.info(f"   Iterations: {agentic_result['iterations']}")
                    logger.info(f"   Companies: {len(agentic_result['companies'])}")

                    # Generate enhanced response with stats
                    response_text = f"""Found {len(results)} contacts from {len(agentic_result['companies'])} companies!

🤖 Agentic Search Stats:
• {agentic_result['iterations']} search iterations
• {agentic_result['stats']['queries_executed']} queries executed
• {agentic_result['stats']['total_companies']} unique companies
• Avg {agentic_result['stats']['avg_results_per_query']:.1f} results per query

The AI iteratively refined searches to find the best matches for your query."""

                except Exception as e:
                    logger.warning(f"⚠️  Agentic search failed: {e}")
                    logger.info("📦 Falling back to mock data...")
                    using_apollo = False

            # Fallback to mock data if agentic search not available
            if not using_apollo:
                logger.info("📦 Using mock data (Apollo API key not set or failed)")
                all_contacts = load_mock_contacts()

                # Filter based on intent
                filtered_contacts = filter_contacts(
                    all_contacts,
                    query=intent.query,
                    titles=intent.titles,
                    companies=intent.companies,
                    locations=intent.locations,
                    tags=intent.tags
                )

                results = filtered_contacts[:intent.max_results]
                logger.info(f"✅ Found {len(results)} contacts from mock data")

                # Generate normal response for mock data
                response_text = intent_parser.generate_response(intent, len(results))
                response_text += " (Using demo data - set APOLLO_API_KEY for real results)"
            elif 'response_text' not in locals():
                # Generate normal response for Apollo data (if not already generated by agentic search)
                response_text = intent_parser.generate_response(intent, len(results))
                response_text += " (Data from Apollo.io)"

        # Save contacts to database (deduplicate by email or LinkedIn URL) - only if not job enrichment
        if not message.enrich_with_jobs or 'contacts_added' not in locals():
            contacts_added = 0
            session = db_manager.get_session()

            try:
                logger.info(f"📝 Processing {len(results)} contacts for database insertion...")
                for i, contact in enumerate(results, 1):
                    # Debug: Log contact details with tags
                    tags_str = ", ".join(contact.tags) if contact.tags else "no tags"
                    logger.info(f"  [{i}/{len(results)}] {contact.name} | Company: {contact.company or 'NONE'} | Tags: [{tags_str}]")

                    # Skip contacts without email or LinkedIn (can't deduplicate)
                    if not contact.email and not contact.linkedin_url:
                        logger.warning(f"  ⚠️  Skipping {contact.name} - no email or LinkedIn URL")
                        continue

                    # Skip Apollo's placeholder emails - treat as if no email
                    email_to_save = contact.email
                    if email_to_save and 'email_not_unlocked' in email_to_save:
                        logger.info(f"  🔒 Email locked for {contact.name} - using LinkedIn URL only")
                        email_to_save = None

                    # If no real email and no LinkedIn, skip
                    if not email_to_save and not contact.linkedin_url:
                        logger.warning(f"  ⚠️  Skipping {contact.name} - no real email or LinkedIn URL")
                        continue

                    # Generate source reason with tags
                    tags_str = ", ".join(contact.tags) if contact.tags else "no tags"
                    source_reason = f"Found via AI search. Tags: {tags_str}"

                    # Save to database (get_or_create handles deduplication)
                    db_contact, created = db_manager.get_or_create_contact(
                        session,
                        email=email_to_save,
                        linkedin_url=contact.linkedin_url,
                        name=contact.name,
                        title=contact.title,
                        company_name=contact.company,
                        phone=contact.phone,
                        city=contact.city,
                        state=contact.state,
                        country=contact.country,
                        source='apollo',
                        tags=contact.tags,
                        source_reason=source_reason,
                        search_query=message.message[:500],  # Store the user's search query
                        workflow_stage='new',  # Set initial workflow stage
                        next_action='Send connection request'  # Set initial next action
                    )

                    if created:
                        contacts_added += 1
                        logger.info(f"  ✅ Added: {contact.name} at {contact.company or 'Unknown'} ({email_to_save or contact.linkedin_url})")
                    else:
                        logger.info(f"  ⏭️  Skipped (duplicate): {contact.name} - already in database")

                    # Also add to in-memory list for backward compatibility
                    exists = any(
                        (c.email and contact.email and c.email == contact.email) or
                        (c.linkedin_url and contact.linkedin_url and c.linkedin_url == contact.linkedin_url)
                        for c in contacts_db
                    )
                    if not exists:
                        contacts_db.append(contact)

                session.commit()
                logger.info(f"💾 Added {contacts_added} new contacts to database")

            except Exception as e:
                session.rollback()
                logger.error(f"Error saving contacts to database: {e}")
            finally:
                session.close()

        # Removed Twenty CRM sync - contacts are already in our database!
        # All contacts are automatically saved to our SQLite database above

        # Generate response (if not already generated by job enrichment)
        if 'response_text' not in locals():
            response_text = intent_parser.generate_response(intent, len(results))

            # Add data source info to response
            if using_apollo:
                response_text += " (Data from Apollo.io)"
            else:
                response_text += " (Using demo data - set APOLLO_API_KEY for real results)"

        # Save to chat history
        chat_entry = {
            "user_message": message.message,
            "ai_response": response_text,
            "contacts_found": len(results),
            "contacts_added": contacts_added,
            "using_apollo": using_apollo,
            "intent": intent.model_dump(),
            "timestamp": datetime.now().isoformat()
        }
        chat_history.append(chat_entry)

        return ChatResponse(
            response=response_text,
            contacts_found=len(results),
            contacts_added=contacts_added,
            intent=intent.model_dump(),
            timestamp=datetime.now()
        )

    except Exception as e:
        logger.error(f"❌ Error processing chat: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


async def _simple_chat_handler(message: ChatMessage) -> ChatResponse:
    """Simple fallback handler without OpenAI"""
    # Extract keywords
    text = message.message.lower()
    
    titles = []
    if "cto" in text: titles.append("CTO")
    if "ceo" in text: titles.append("CEO")
    if "vp" in text or "vice president" in text: titles.append("VP")
    if "founder" in text: titles.append("Founder")
    
    tags = []
    if "investor" in text or "vc" in text: tags.append("investor")
    if "ai" in text or "artificial intelligence" in text: tags.append("ai")
    if "saas" in text: tags.append("tech")
    
    # Load and filter contacts
    all_contacts = load_mock_contacts()
    filtered = filter_contacts(
        all_contacts,
        titles=titles if titles else None,
        tags=tags if tags else None
    )
    
    results = filtered[:50]
    
    # Add to storage
    for contact in results:
        if contact not in contacts_db:
            contacts_db.append(contact)
    
    response_text = f"Found {len(results)} contacts matching your criteria. Added to CRM!"
    
    return ChatResponse(
        response=response_text,
        contacts_found=len(results),
        contacts_added=len(results),
        intent={"titles": titles, "tags": tags},
        timestamp=datetime.now()
    )


@app.get("/api/contacts", response_model=ContactsResponse)
async def get_contacts(
    limit: int = 1000,
    tags: Optional[str] = None,
    title: Optional[str] = None
):
    """
    Get all contacts from CRM database.

    Query params:
    - limit: Maximum number of contacts to return (default: 1000)
    - tags: Filter by tags (comma-separated) - NOT IMPLEMENTED YET
    - title: Filter by job title
    """
    session = db_manager.get_session()

    try:
        # Get contacts from database
        from database.models import Contact as DBContact
        query = session.query(DBContact)

        # Apply title filter if provided
        if title:
            query = query.filter(DBContact.title.ilike(f'%{title}%'))

        # Get results with limit
        db_contacts = query.limit(limit).all()

        # Convert database models to Contact schema
        results = []
        for db_contact in db_contacts:
            # Handle email validation - Contact schema requires valid email or None
            email_value = db_contact.email if db_contact.email else None

            # Parse tags from JSON if available
            tags = db_contact.tags if db_contact.tags else []
            if isinstance(tags, str):
                import json
                try:
                    tags = json.loads(tags)
                except:
                    tags = []

            results.append(Contact(
                id=str(db_contact.id),  # Include the database ID!
                name=db_contact.name,
                email=email_value,
                title=db_contact.title or None,
                company=db_contact.company_name or None,
                linkedin_url=db_contact.linkedin_url or None,
                phone=db_contact.phone or None,
                city=db_contact.city or None,
                state=db_contact.state or None,
                country=db_contact.country or None,
                tags=tags,
                source=db_contact.source or "apollo.io",
                relationship_stage="new_lead",  # Default value since DB doesn't have this field
                workflow_stage=db_contact.workflow_stage or None,
                last_action=db_contact.last_action or None,
                last_action_date=db_contact.last_action_date or None,
                next_action=db_contact.next_action or None,
                next_action_date=db_contact.next_action_date or None,
                automation_notes=db_contact.automation_notes or None,
                created_at=db_contact.created_at,
                last_updated=db_contact.updated_at  # DB uses 'updated_at' not 'last_updated'
            ))

        logger.info(f"📊 Retrieved {len(results)} contacts from database")

        return ContactsResponse(
            contacts=results,
            total=len(results),
            timestamp=datetime.now()
        )

    except Exception as e:
        logger.error(f"Error retrieving contacts from database: {e}")
        # Fallback to in-memory list
        filtered = contacts_db.copy()

        if title:
            filtered = [c for c in filtered if c.title and title.lower() in c.title.lower()]

        results = filtered[:limit]

        return ContactsResponse(
            contacts=results,
            total=len(results),
            timestamp=datetime.now()
        )
    finally:
        session.close()


@app.get("/api/chat/history")
async def get_chat_history():
    """Get chat history"""
    return {"history": chat_history, "total": len(chat_history)}


@app.post("/api/contacts/create")
async def create_contact_manually(contact_data: Dict[str, Any]):
    """Create a contact manually"""
    try:
        db_manager = get_db_manager()
        session = db_manager.get_session()

        # Extract tags if provided
        tags = contact_data.pop('tags', [])
        if isinstance(tags, str):
            tags = [t.strip() for t in tags.split(',') if t.strip()]

        # Convert tags list to JSON string for SQLite
        import json
        contact_data['tags'] = json.dumps(tags) if tags else None

        # Create contact
        db_contact, created = db_manager.get_or_create_contact(
            session,
            **contact_data
        )

        session.commit()

        if created:
            logger.info(f"✅ Manually created contact: {db_contact.name}")
            return {"message": "Contact created successfully", "id": db_contact.id}
        else:
            logger.info(f"⏭️  Contact already exists: {db_contact.name}")
            return {"message": "Contact already exists", "id": db_contact.id}

    except Exception as e:
        logger.error(f"Error creating contact: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()


@app.put("/api/contacts/{contact_id}")
async def update_contact(contact_id: int, contact_data: Dict[str, Any]):
    """Update an existing contact"""
    try:
        db_manager = get_db_manager()
        session = db_manager.get_session()

        from database.models import Contact

        # Get the contact
        contact = session.query(Contact).filter(Contact.id == contact_id).first()
        if not contact:
            raise HTTPException(status_code=404, detail="Contact not found")

        # Extract and process tags if provided
        if 'tags' in contact_data:
            tags = contact_data.pop('tags')
            if isinstance(tags, str):
                tags = [t.strip() for t in tags.split(',') if t.strip()]
            import json
            contact_data['tags'] = json.dumps(tags) if tags else None

        # Update contact fields
        for key, value in contact_data.items():
            if value is not None and hasattr(contact, key):
                setattr(contact, key, value)

        session.commit()
        session.refresh(contact)

        logger.info(f"✅ Updated contact: {contact.name}")
        return {"message": "Contact updated successfully", "id": contact.id}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating contact: {e}")
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()


@app.delete("/api/contacts")
async def clear_contacts():
    """Clear all contacts"""
    global contacts_db
    count = len(contacts_db)
    contacts_db = []
    return {"message": f"Cleared {count} contacts"}


@app.get("/api/companies")
async def get_companies():
    """Get all companies from database"""
    try:
        db_manager = get_db_manager()
        session = db_manager.get_session()

        # Get all companies with contact count
        from database.models import Company, Contact
        from sqlalchemy import func

        companies = session.query(
            Company,
            func.count(Contact.id).label('contact_count')
        ).outerjoin(
            Contact, Company.id == Contact.company_id
        ).group_by(Company.id).all()

        results = []
        for company, contact_count in companies:
            # Parse JSON fields if they're strings
            pain_points = company.pain_points
            if pain_points and isinstance(pain_points, str):
                import json
                try:
                    pain_points = json.loads(pain_points)
                except:
                    pain_points = []

            tags = company.tags
            if tags and isinstance(tags, str):
                import json
                try:
                    tags = json.loads(tags)
                except:
                    tags = []

            technologies = company.technologies
            if technologies and isinstance(technologies, str):
                import json
                try:
                    technologies = json.loads(technologies)
                except:
                    technologies = []

            results.append({
                'id': company.id,
                'name': company.name,
                'website': company.website,
                'industry': company.industry,
                'description': company.description,
                'employee_count': company.employee_count,
                'location': company.location,
                'linkedin_url': company.linkedin_url,
                'contact_count': contact_count,
                'created_at': company.created_at.isoformat() if company.created_at else None,
                # Apollo enrichment fields
                'apollo_id': company.apollo_id,
                'founded_year': company.founded_year,
                'funding_stage': company.funding_stage,
                'total_funding': company.total_funding,
                'technologies': technologies,
                # CRM fields
                'tags': tags,
                'relationship_stage': company.relationship_stage,
                # AI Enrichment fields
                'industry_analysis': company.industry_analysis,
                'pain_points': pain_points,
                'value_proposition': company.value_proposition,
                'enrichment_notes': company.enrichment_notes,
                'last_enriched_at': company.last_enriched_at.isoformat() if company.last_enriched_at else None
            })

        logger.info(f"📊 Retrieved {len(results)} companies from database")

        return {
            'companies': results,
            'total': len(results)
        }

    except Exception as e:
        logger.error(f"Error retrieving companies: {e}")
        return {'companies': [], 'total': 0}
    finally:
        session.close()


@app.post("/api/companies/sync-contacts")
async def sync_contacts_for_companies():
    """Sync contacts for all companies using Apollo API"""
    try:
        if not job_enrichment:
            return {"error": "Job enrichment service not available", "contacts_added": 0, "companies_processed": 0}

        db_manager = get_db_manager()
        session = db_manager.get_session()

        from database.models import Company

        # Get all companies
        companies = session.query(Company).all()

        if not companies:
            return {"message": "No companies found", "contacts_added": 0, "companies_processed": 0}

        logger.info(f"🔄 Syncing contacts for {len(companies)} companies...")

        # Use the job enrichment service to find contacts
        contacts = job_enrichment.enrich_companies_with_apollo(
            session,
            companies,
            max_contacts_per_company=1  # Only 1 contact per company
        )

        # Commit changes
        session.commit()

        logger.info(f"✅ Synced {len(contacts)} contacts for {len(companies)} companies")

        return {
            "message": f"Successfully synced {len(contacts)} contacts",
            "contacts_added": len(contacts),
            "companies_processed": len(companies)
        }

    except Exception as e:
        logger.error(f"Error syncing contacts: {e}")
        session.rollback()
        return {"error": str(e), "contacts_added": 0, "companies_processed": 0}
    finally:
        session.close()


@app.get("/api/campaigns")
async def get_campaigns():
    """Get all campaigns from database"""
    try:
        db_manager = get_db_manager()
        session = db_manager.get_session()

        from database.models import Campaign

        campaigns = session.query(Campaign).all()

        results = []
        for campaign in campaigns:
            results.append({
                'id': campaign.id,
                'name': campaign.name,
                'description': campaign.description,
                'status': campaign.status,
                'contact_count': 0,  # TODO: Count contacts in campaign
                'sent_count': 0,  # TODO: Track sent messages
                'replied_count': 0,  # TODO: Track replies
                'created_at': campaign.created_at.isoformat() if campaign.created_at else None
            })

        logger.info(f"📊 Retrieved {len(results)} campaigns from database")

        return {
            'campaigns': results,
            'total': len(results)
        }

    except Exception as e:
        logger.error(f"Error retrieving campaigns: {e}")
        return {'campaigns': [], 'total': 0}
    finally:
        session.close()


@app.get("/api/stats")
async def get_stats():
    """Get CRM statistics"""
    total_contacts = len(contacts_db)
    
    # Count by tags
    tags_count = {}
    for contact in contacts_db:
        for tag in contact.tags:
            tags_count[tag] = tags_count.get(tag, 0) + 1
    
    # Count by title
    titles_count = {}
    for contact in contacts_db:
        if contact.title:
            titles_count[contact.title] = titles_count.get(contact.title, 0) + 1
    
    # Count by company
    companies_count = {}
    for contact in contacts_db:
        if contact.company:
            companies_count[contact.company] = companies_count.get(contact.company, 0) + 1
    
    return {
        "total_contacts": total_contacts,
        "total_chats": len(chat_history),
        "tags": tags_count,
        "titles": dict(sorted(titles_count.items(), key=lambda x: x[1], reverse=True)[:10]),
        "companies": dict(sorted(companies_count.items(), key=lambda x: x[1], reverse=True)[:10]),
        "timestamp": datetime.now().isoformat()
    }


# ==================== Company Profile & Enrichment Endpoints ====================

@app.post("/api/profile/create")
async def create_company_profile(data: Dict[str, Any]):
    """Create company profile from website URL"""
    try:
        if not company_profile_service:
            raise HTTPException(status_code=503, detail="Company profile service not available")

        website_url = data.get('website_url')
        if not website_url:
            raise HTTPException(status_code=400, detail="website_url is required")

        logger.info(f"📝 Creating company profile from {website_url}")

        # Create profile from website
        profile_data = company_profile_service.create_profile_from_website(website_url)

        if 'error' in profile_data:
            raise HTTPException(status_code=500, detail=profile_data['error'])

        # Save to database
        session = db_manager.get_session()
        try:
            success = company_profile_service.save_profile_to_db(session, profile_data)
            if not success:
                raise HTTPException(status_code=500, detail="Failed to save profile")

            return {"message": "Profile created successfully", "profile": profile_data}
        finally:
            session.close()

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating company profile: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/profile")
async def get_company_profile():
    """Get current company profile"""
    try:
        if not company_profile_service:
            raise HTTPException(status_code=503, detail="Company profile service not available")

        session = db_manager.get_session()
        try:
            profile = company_profile_service.get_profile_from_db(session)
            if not profile:
                return {"profile": None, "message": "No profile found"}
            return {"profile": profile}
        finally:
            session.close()

    except Exception as e:
        logger.error(f"Error getting company profile: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/companies/{company_id}/enrich")
async def enrich_single_company(company_id: int):
    """Enrich a single company with AI-powered insights"""
    try:
        if not company_enrichment_service or not company_profile_service:
            raise HTTPException(status_code=503, detail="Enrichment services not available")

        session = db_manager.get_session()
        try:
            # Get our company profile
            our_profile = company_profile_service.get_profile_from_db(session)
            if not our_profile:
                raise HTTPException(status_code=400, detail="Please create your company profile first")

            # Enrich the company
            success = company_enrichment_service.enrich_and_save(session, company_id, our_profile)

            if not success:
                raise HTTPException(status_code=500, detail="Failed to enrich company")

            return {"message": "Company enriched successfully", "company_id": company_id}
        finally:
            session.close()

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error enriching company: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/companies/enrich-all")
async def enrich_all_companies(data: Optional[Dict[str, Any]] = None):
    """Enrich all companies with AI-powered insights"""
    try:
        if not company_enrichment_service or not company_profile_service:
            raise HTTPException(status_code=503, detail="Enrichment services not available")

        limit = data.get('limit') if data else None

        session = db_manager.get_session()
        try:
            # Get our company profile
            our_profile = company_profile_service.get_profile_from_db(session)
            if not our_profile:
                raise HTTPException(status_code=400, detail="Please create your company profile first")

            # Enrich all companies
            result = company_enrichment_service.enrich_all_companies(session, our_profile, limit)

            return {
                "message": f"Enriched {result['success']} companies",
                "total": result['total'],
                "success": result['success'],
                "failure": result['failure']
            }
        finally:
            session.close()

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error enriching companies: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/companies/{company_id}/enrich-apollo")
async def enrich_company_with_apollo(company_id: int):
    """Enrich a single company with Apollo API data"""
    try:
        if not apollo_company_enrichment:
            raise HTTPException(status_code=503, detail="Apollo enrichment service not available")

        session = db_manager.get_session()
        try:
            from database.models import Company

            # Get company from database
            company = session.query(Company).filter(Company.id == company_id).first()

            if not company:
                raise HTTPException(status_code=404, detail="Company not found")

            # Enrich the company
            success = apollo_company_enrichment.enrich_company(session, company)

            if not success:
                raise HTTPException(status_code=500, detail="Failed to enrich company with Apollo")

            return {"message": "Company enriched successfully with Apollo", "company_id": company_id}
        finally:
            session.close()

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error enriching company with Apollo: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/companies/enrich-all-apollo")
async def enrich_all_companies_with_apollo(data: Optional[Dict[str, Any]] = None):
    """Enrich all companies with Apollo API data"""
    try:
        if not apollo_company_enrichment:
            raise HTTPException(status_code=503, detail="Apollo enrichment service not available")

        limit = data.get('limit') if data else None

        session = db_manager.get_session()
        try:
            from database.models import Company

            # Get all companies
            companies = session.query(Company).all()

            # Enrich companies
            result = apollo_company_enrichment.enrich_multiple_companies(session, companies, limit)

            return {
                "message": f"Enriched {result['success']} companies with Apollo",
                "total": result['total'],
                "success": result['success'],
                "failure": result['failure']
            }
        finally:
            session.close()

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error enriching companies with Apollo: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/api/companies/{company_id}")
async def update_company(company_id: int, data: Dict[str, Any]):
    """Update company fields (tags, relationship_stage, etc.)"""
    try:
        session = db_manager.get_session()
        try:
            from database.models import Company
            import json

            company = session.query(Company).filter(Company.id == company_id).first()

            if not company:
                raise HTTPException(status_code=404, detail="Company not found")

            # Update allowed fields
            if 'tags' in data:
                company.tags = json.dumps(data['tags']) if isinstance(data['tags'], list) else data['tags']

            if 'relationship_stage' in data:
                company.relationship_stage = data['relationship_stage']

            if 'description' in data:
                company.description = data['description']

            session.commit()

            return {"message": "Company updated successfully", "company_id": company_id}
        finally:
            session.close()

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating company: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ==================== Integrations API ====================

@app.get("/api/integrations")
async def get_integrations():
    """Get all integrations"""
    try:
        db_manager = get_db_manager()
        session = db_manager.get_session()

        try:
            from database.models import Integration

            integrations = session.query(Integration).all()

            results = []
            for integration in integrations:
                # Parse config JSON
                config = {}
                if integration.config:
                    try:
                        config = json.loads(integration.config) if isinstance(integration.config, str) else integration.config
                    except:
                        config = {}

                results.append({
                    'id': integration.id,
                    'platform': integration.platform,
                    'status': integration.status,
                    'account_name': integration.account_name,
                    'account_id': integration.account_id,
                    'account_email': integration.account_email,
                    'messages_sent': integration.messages_sent,
                    'connections_made': integration.connections_made,
                    'last_used_at': integration.last_used_at.isoformat() if integration.last_used_at else None,
                    'connected_at': integration.connected_at.isoformat() if integration.connected_at else None,
                    'created_at': integration.created_at.isoformat() if integration.created_at else None,
                    'config': config
                })

            return {
                'integrations': results,
                'total': len(results)
            }
        finally:
            session.close()

    except Exception as e:
        logger.error(f"Error getting integrations: {e}")
        raise HTTPException(status_code=500, detail=str(e))


class LinkedInConnectRequest(BaseModel):
    email: str
    password: str


@app.post("/api/integrations/linkedin/connect")
async def connect_linkedin(request: LinkedInConnectRequest):
    """Connect LinkedIn account"""
    try:
        db_manager = get_db_manager()
        session = db_manager.get_session()

        try:
            from database.models import Integration

            # Check if LinkedIn integration already exists
            existing = session.query(Integration).filter(
                Integration.platform == 'linkedin'
            ).first()

            if existing:
                # Update existing integration
                existing.status = 'connected'
                existing.account_email = request.email
                existing.account_name = request.email.split('@')[0]
                existing.connected_at = datetime.utcnow()
                existing.updated_at = datetime.utcnow()
                # Note: In production, encrypt the password!
                existing.access_token = request.password  # This should be encrypted

                session.commit()
                logger.info(f"✅ Updated LinkedIn integration for {request.email}")
            else:
                # Create new integration
                integration = Integration(
                    platform='linkedin',
                    status='connected',
                    account_email=request.email,
                    account_name=request.email.split('@')[0],
                    access_token=request.password,  # This should be encrypted
                    connected_at=datetime.utcnow(),
                    created_at=datetime.utcnow()
                )
                session.add(integration)
                session.commit()
                logger.info(f"✅ Created LinkedIn integration for {request.email}")

            return {
                'message': 'LinkedIn connected successfully',
                'platform': 'linkedin',
                'account': request.email
            }
        finally:
            session.close()

    except Exception as e:
        logger.error(f"Error connecting LinkedIn: {e}")
        raise HTTPException(status_code=500, detail=str(e))


class TelegramConnectRequest(BaseModel):
    bot_token: str


@app.post("/api/integrations/telegram/connect")
async def connect_telegram(request: TelegramConnectRequest):
    """Connect Telegram bot"""
    try:
        db_manager = get_db_manager()
        session = db_manager.get_session()

        try:
            from database.models import Integration

            # Validate bot token by making a test API call
            import requests
            test_response = requests.get(f"https://api.telegram.org/bot{request.bot_token}/getMe")

            if not test_response.ok:
                raise HTTPException(status_code=400, detail="Invalid bot token")

            bot_info = test_response.json()
            if not bot_info.get('ok'):
                raise HTTPException(status_code=400, detail="Invalid bot token")

            bot_username = bot_info['result']['username']
            bot_name = bot_info['result']['first_name']

            # Check if Telegram integration already exists
            existing = session.query(Integration).filter(
                Integration.platform == 'telegram'
            ).first()

            if existing:
                # Update existing integration
                existing.status = 'connected'
                existing.account_name = bot_name
                existing.account_id = bot_username
                existing.connected_at = datetime.utcnow()
                existing.updated_at = datetime.utcnow()
                # Note: In production, encrypt the token!
                existing.access_token = request.bot_token  # This should be encrypted

                session.commit()
                logger.info(f"✅ Updated Telegram integration for @{bot_username}")
            else:
                # Create new integration
                integration = Integration(
                    platform='telegram',
                    status='connected',
                    account_name=bot_name,
                    account_id=bot_username,
                    access_token=request.bot_token,  # This should be encrypted
                    connected_at=datetime.utcnow(),
                    created_at=datetime.utcnow()
                )
                session.add(integration)
                session.commit()
                logger.info(f"✅ Created Telegram integration for @{bot_username}")

            return {
                'message': 'Telegram bot connected successfully',
                'platform': 'telegram',
                'bot_name': bot_name,
                'bot_username': bot_username
            }
        finally:
            session.close()

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error connecting Telegram: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/integrations/{platform}/disconnect")
async def disconnect_integration(platform: str):
    """Disconnect an integration"""
    try:
        db_manager = get_db_manager()
        session = db_manager.get_session()

        try:
            from database.models import Integration

            integration = session.query(Integration).filter(
                Integration.platform == platform
            ).first()

            if not integration:
                raise HTTPException(status_code=404, detail=f"{platform} integration not found")

            integration.status = 'disconnected'
            integration.updated_at = datetime.utcnow()

            session.commit()
            logger.info(f"✅ Disconnected {platform} integration")

            return {
                'message': f'{platform} disconnected successfully',
                'platform': platform
            }
        finally:
            session.close()

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error disconnecting integration: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.on_event("startup")
async def startup_event():
    """Initialize on startup"""
    print("\n" + "="*60)
    print("🚀 LeadOn CRM API starting...")
    print("="*60)
    print(f"   Claude API:    {'✅ Configured' if has_claude else '❌ Not configured (using fallback)'}")
    print(f"   Apollo API:    {'✅ Configured (real data)' if os.getenv('APOLLO_API_KEY') else '❌ Not configured (using mock data)'}")
    print(f"   Database:      ✅ SQLite (leadon.db)")
    print(f"\n   📚 API Docs:   http://localhost:8000/docs")
    print(f"   🎯 New CRM:    http://localhost:8000/crm")
    print(f"   💬 Old UI:     http://localhost:8000/")
    print("="*60 + "\n")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

