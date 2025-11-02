#!/usr/bin/env python3
"""Check contacts in the database"""

from database.db_manager import get_db_manager
from database.models import Contact, Company

def main():
    db = get_db_manager()
    session = db.get_session()
    
    try:
        # Get counts
        total_contacts = session.query(Contact).count()
        total_companies = session.query(Company).count()
        
        print(f"\n{'='*60}")
        print(f"📊 Database Summary")
        print(f"{'='*60}")
        print(f"Total Contacts:  {total_contacts}")
        print(f"Total Companies: {total_companies}")
        print(f"{'='*60}\n")
        
        # Get all contacts
        contacts = session.query(Contact).order_by(Contact.created_at.desc()).all()
        
        print(f"📋 All Contacts (most recent first):\n")
        for i, contact in enumerate(contacts, 1):
            print(f"{i:2d}. {contact.name:30s} | {contact.title or 'N/A':30s} | {contact.company_name or 'N/A':25s} | {contact.source or 'unknown':10s}")
        
        print(f"\n{'='*60}\n")
        
    finally:
        session.close()

if __name__ == "__main__":
    main()

