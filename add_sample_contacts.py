"""
Add sample contacts to test the new CRM interface
"""

from database.db_manager import get_db_manager
from database.models import Contact, Company
from datetime import datetime, timedelta
import random

def add_sample_contacts():
    """Add sample contacts to the database"""
    
    db = get_db_manager()
    session = db.get_session()
    
    # Sample data
    sample_contacts = [
        {
            "name": "Sarah Chen",
            "email": "sarah.chen@techcorp.com",
            "title": "Chief Technology Officer",
            "company_name": "TechCorp AI",
            "phone": "+1 (415) 555-0123",
            "linkedin_url": "https://linkedin.com/in/sarahchen",
            "city": "San Francisco",
            "state": "CA",
            "country": "USA",
            "seniority": "Executive"
        },
        {
            "name": "Michael Rodriguez",
            "email": "m.rodriguez@innovate.io",
            "title": "VP of Engineering",
            "company_name": "Innovate Labs",
            "phone": "+1 (650) 555-0456",
            "linkedin_url": "https://linkedin.com/in/mrodriguez",
            "city": "Palo Alto",
            "state": "CA",
            "country": "USA",
            "seniority": "VP"
        },
        {
            "name": "Emily Watson",
            "email": "emily.watson@datastream.com",
            "title": "Head of Product",
            "company_name": "DataStream Inc",
            "phone": "+1 (408) 555-0789",
            "linkedin_url": "https://linkedin.com/in/emilywatson",
            "city": "San Jose",
            "state": "CA",
            "country": "USA",
            "seniority": "Director"
        },
        {
            "name": "James Kim",
            "email": "james@startupxyz.com",
            "title": "Founder & CEO",
            "company_name": "StartupXYZ",
            "phone": "+1 (415) 555-0321",
            "linkedin_url": "https://linkedin.com/in/jameskim",
            "city": "San Francisco",
            "state": "CA",
            "country": "USA",
            "seniority": "C-Suite"
        },
        {
            "name": "Lisa Anderson",
            "email": "l.anderson@cloudtech.io",
            "title": "VP of Sales",
            "company_name": "CloudTech Solutions",
            "phone": "+1 (650) 555-0654",
            "linkedin_url": "https://linkedin.com/in/lisaanderson",
            "city": "Mountain View",
            "state": "CA",
            "country": "USA",
            "seniority": "VP"
        },
        {
            "name": "David Park",
            "email": "david.park@aiventures.com",
            "title": "Director of Engineering",
            "company_name": "AI Ventures",
            "phone": "+1 (415) 555-0987",
            "linkedin_url": "https://linkedin.com/in/davidpark",
            "city": "San Francisco",
            "state": "CA",
            "country": "USA",
            "seniority": "Director"
        },
        {
            "name": "Rachel Green",
            "email": "rachel@fintech.co",
            "title": "Chief Product Officer",
            "company_name": "FinTech Innovations",
            "phone": "+1 (408) 555-0147",
            "linkedin_url": "https://linkedin.com/in/rachelgreen",
            "city": "San Jose",
            "state": "CA",
            "country": "USA",
            "seniority": "C-Suite"
        },
        {
            "name": "Tom Wilson",
            "email": "tom.wilson@saascompany.com",
            "title": "VP of Marketing",
            "company_name": "SaaS Company",
            "phone": "+1 (650) 555-0258",
            "linkedin_url": "https://linkedin.com/in/tomwilson",
            "city": "Redwood City",
            "state": "CA",
            "country": "USA",
            "seniority": "VP"
        },
        {
            "name": "Jennifer Lee",
            "email": "jennifer@blockchain.io",
            "title": "Head of Operations",
            "company_name": "Blockchain Dynamics",
            "phone": "+1 (415) 555-0369",
            "linkedin_url": "https://linkedin.com/in/jenniferlee",
            "city": "San Francisco",
            "state": "CA",
            "country": "USA",
            "seniority": "Director"
        },
        {
            "name": "Robert Taylor",
            "email": "robert.taylor@cybersec.com",
            "title": "CTO",
            "company_name": "CyberSec Pro",
            "phone": "+1 (408) 555-0741",
            "linkedin_url": "https://linkedin.com/in/roberttaylor",
            "city": "Santa Clara",
            "state": "CA",
            "country": "USA",
            "seniority": "C-Suite"
        }
    ]
    
    added = 0
    skipped = 0
    
    print("\n🔄 Adding sample contacts to database...\n")
    
    for contact_data in sample_contacts:
        # Check if contact already exists
        existing = session.query(Contact).filter(
            Contact.email == contact_data["email"]
        ).first()
        
        if existing:
            print(f"⏭️  Skipped: {contact_data['name']} (already exists)")
            skipped += 1
            continue
        
        # Create or get company
        company = session.query(Company).filter(
            Company.name == contact_data["company_name"]
        ).first()
        
        if not company:
            company = Company(
                name=contact_data["company_name"],
                source="sample_data",
                created_at=datetime.utcnow()
            )
            session.add(company)
            session.flush()
        
        # Create contact
        contact = Contact(
            name=contact_data["name"],
            email=contact_data["email"],
            title=contact_data["title"],
            company_id=company.id,
            company_name=contact_data["company_name"],
            phone=contact_data.get("phone"),
            linkedin_url=contact_data.get("linkedin_url"),
            city=contact_data.get("city"),
            state=contact_data.get("state"),
            country=contact_data.get("country"),
            seniority=contact_data.get("seniority"),
            source="sample_data",
            created_at=datetime.utcnow() - timedelta(days=random.randint(0, 30))
        )
        
        session.add(contact)
        print(f"✅ Added: {contact_data['name']} - {contact_data['title']} at {contact_data['company_name']}")
        added += 1
    
    session.commit()
    session.close()
    
    print(f"\n{'='*60}")
    print(f"✅ Successfully added {added} contacts")
    print(f"⏭️  Skipped {skipped} existing contacts")
    print(f"{'='*60}")
    print(f"\n🎉 Your CRM now has sample data!")
    print(f"📊 View at: http://localhost:8000/crm")
    print(f"\n")


if __name__ == "__main__":
    add_sample_contacts()

