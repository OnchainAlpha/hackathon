"""Load demo contacts into the database"""
import json
import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from database.db_manager import DatabaseManager
from database.models import Contact, Company
from scrapers.schemas import Contact as ContactSchema


def load_demo_data():
    """Load demo contacts from JSON file into database"""
    
    # Load demo data
    demo_file = Path(__file__).parent / "exports" / "demo_contacts.json"
    
    if not demo_file.exists():
        print(f"❌ Demo file not found: {demo_file}")
        return
    
    with open(demo_file, 'r') as f:
        contacts_data = json.load(f)
    
    print(f"📂 Loaded {len(contacts_data)} contacts from {demo_file}")
    
    # Initialize database
    db_manager = DatabaseManager()
    session = db_manager.get_session()
    
    added_count = 0
    skipped_count = 0
    
    try:
        for contact_data in contacts_data:
            # Check if contact already exists
            existing = session.query(Contact).filter(
                (Contact.email == contact_data.get('email')) |
                (Contact.linkedin_url == contact_data.get('linkedin_url'))
            ).first()
            
            if existing:
                skipped_count += 1
                continue
            
            # Get or create company
            company = None
            company_name = contact_data.get('company')
            if company_name:
                company = session.query(Company).filter(Company.name == company_name).first()
                if not company:
                    company = Company(
                        name=company_name,
                        created_at=datetime.utcnow()
                    )
                    session.add(company)
                    session.flush()
            
            # Create contact
            contact = Contact(
                name=contact_data.get('name'),
                email=contact_data.get('email'),
                phone=contact_data.get('phone'),
                title=contact_data.get('title'),
                company_id=company.id if company else None,
                company_name=company_name,
                linkedin_url=contact_data.get('linkedin_url'),
                city=contact_data.get('city'),
                state=contact_data.get('state'),
                country=contact_data.get('country'),
                tags=json.dumps(contact_data.get('tags', [])),
                source=contact_data.get('source', 'demo_data'),
                source_reason=f"Demo data - {', '.join(contact_data.get('tags', []))}",
                workflow_stage='new',
                next_action='Send connection request',
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            
            session.add(contact)
            added_count += 1
        
        session.commit()
        
        print(f"\n✅ Successfully loaded demo data!")
        print(f"   • Added: {added_count} contacts")
        print(f"   • Skipped (duplicates): {skipped_count} contacts")
        print(f"\n🚀 Open http://localhost:8000/crm to view your contacts!")
        
    except Exception as e:
        session.rollback()
        print(f"❌ Error loading demo data: {e}")
        import traceback
        traceback.print_exc()
    finally:
        session.close()


if __name__ == "__main__":
    load_demo_data()

