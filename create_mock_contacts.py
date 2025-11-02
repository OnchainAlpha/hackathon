"""
Mock contact data generator for hackathon demo.
Creates realistic contact data when Apollo.io API is not available.
"""

import json
import random
from datetime import datetime
from pathlib import Path
from typing import List

import typer
from rich.console import Console
from rich.table import Table

from scrapers.schemas import Contact

app = typer.Typer()
console = Console()

# Mock data pools
FIRST_NAMES = [
    "James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda",
    "William", "Elizabeth", "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica",
    "Thomas", "Sarah", "Charles", "Karen", "Christopher", "Nancy", "Daniel", "Lisa",
    "Matthew", "Betty", "Anthony", "Margaret", "Mark", "Sandra", "Donald", "Ashley"
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
    "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
    "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Thompson", "White",
    "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker", "Young"
]

TITLES = {
    "executive": ["CEO", "CTO", "CFO", "COO", "Chief Executive Officer", "Chief Technology Officer", "President", "VP Engineering"],
    "director": ["Director of Engineering", "Director of Sales", "Director of Marketing", "Product Director", "Engineering Director"],
    "manager": ["Engineering Manager", "Product Manager", "Sales Manager", "Marketing Manager", "Operations Manager"],
    "senior": ["Senior Software Engineer", "Senior Data Scientist", "Senior Product Manager", "Senior Designer"],
    "investor": ["Partner", "Managing Partner", "Venture Partner", "Investment Partner", "Angel Investor"]
}

COMPANIES = {
    "ai": ["Anthropic", "OpenAI", "DeepMind", "Cohere", "Hugging Face", "Stability AI", "Midjourney", "Character.AI"],
    "tech": ["Google", "Microsoft", "Amazon", "Meta", "Apple", "Netflix", "Uber", "Airbnb"],
    "vc": ["Sequoia Capital", "Andreessen Horowitz", "Kleiner Perkins", "Accel", "Greylock Partners", "Benchmark"],
    "startup": ["Stripe", "Notion", "Figma", "Linear", "Vercel", "Supabase", "Replicate", "Modal"]
}

CITIES = [
    ("San Francisco", "CA", "USA"),
    ("New York", "NY", "USA"),
    ("Los Angeles", "CA", "USA"),
    ("Seattle", "WA", "USA"),
    ("Austin", "TX", "USA"),
    ("Boston", "MA", "USA"),
    ("Chicago", "IL", "USA"),
    ("Denver", "CO", "USA"),
    ("Miami", "FL", "USA"),
    ("Portland", "OR", "USA")
]


def generate_email(first_name: str, last_name: str, company: str) -> str:
    """Generate realistic email address."""
    domain = company.lower().replace(" ", "").replace(".", "")
    if "capital" in domain or "partners" in domain:
        domain = domain.replace("capital", "").replace("partners", "") + "vc"
    
    first = first_name.lower()
    last = last_name.lower()
    
    patterns = [
        f"{first}.{last}@{domain}.com",
        f"{first}@{domain}.com",
        f"{first[0]}{last}@{domain}.com",
    ]
    
    return random.choice(patterns)


def generate_linkedin_url(first_name: str, last_name: str) -> str:
    """Generate LinkedIn URL."""
    return f"https://linkedin.com/in/{first_name.lower()}-{last_name.lower()}-{random.randint(1000, 9999)}"


def generate_phone() -> str:
    """Generate US phone number."""
    area_code = random.randint(200, 999)
    exchange = random.randint(200, 999)
    number = random.randint(1000, 9999)
    return f"+1{area_code}{exchange}{number}"


def generate_contact(category: str = "tech") -> Contact:
    """
    Generate a single mock contact.
    
    Args:
        category: Category of contact (ai, tech, vc, startup, investor)
    """
    first_name = random.choice(FIRST_NAMES)
    last_name = random.choice(LAST_NAMES)
    name = f"{first_name} {last_name}"
    
    # Select title based on category
    if category == "investor":
        title = random.choice(TITLES["investor"])
        company = random.choice(COMPANIES["vc"])
        tags = ["investor", "vc", "fundraising_target"]
    else:
        title_category = random.choice(["executive", "director", "manager", "senior"])
        title = random.choice(TITLES[title_category])
        company = random.choice(COMPANIES.get(category, COMPANIES["tech"]))
        tags = [category, title_category, company.lower().replace(" ", "_")]
    
    city, state, country = random.choice(CITIES)
    
    contact = Contact(
        name=name,
        title=title,
        company=company,
        email=generate_email(first_name, last_name, company),
        linkedin_url=generate_linkedin_url(first_name, last_name),
        phone=generate_phone(),
        city=city,
        state=state,
        country=country,
        tags=tags,
        source="mock_data",
        relationship_stage="new_lead",
        created_at=datetime.now(),
        last_updated=datetime.now()
    )
    
    return contact


@app.command()
def generate(
    count: int = typer.Option(50, "--count", "-n", help="Number of contacts to generate"),
    category: str = typer.Option("tech", "--category", "-c", help="Category: ai, tech, vc, startup, investor"),
    output: str = typer.Option("mock_contacts.json", "--output", "-o", help="Output filename"),
    display: bool = typer.Option(True, "--display/--no-display", help="Display contacts in table")
):
    """
    Generate mock contact data for testing and demos.
    
    Examples:
        python create_mock_contacts.py generate --count 50 --category ai
        python create_mock_contacts.py generate -n 100 -c investor -o investors.json
    """
    console.print(f"\n[cyan]Generating {count} mock contacts in category '{category}'...[/cyan]\n")
    
    # Generate contacts
    contacts = []
    for _ in range(count):
        contact = generate_contact(category)
        contacts.append(contact)
    
    # Save to file
    output_path = Path("exports") / output
    output_path.parent.mkdir(exist_ok=True)
    
    data = [contact.model_dump(mode='json') for contact in contacts]
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, default=str)
    
    console.print(f"[green]✓[/green] Generated {count} contacts")
    console.print(f"[green]✓[/green] Saved to {output_path}\n")
    
    # Display sample
    if display and contacts:
        table = Table(title=f"Sample Contacts (showing first 10)", show_header=True, header_style="bold magenta")
        
        table.add_column("Name", style="cyan")
        table.add_column("Title", style="green")
        table.add_column("Company", style="blue")
        table.add_column("Email", style="yellow")
        table.add_column("Location", style="white")
        
        for contact in contacts[:10]:
            location = f"{contact.city}, {contact.state}"
            table.add_row(
                contact.name,
                contact.title,
                contact.company,
                contact.email,
                location
            )
        
        console.print(table)
        console.print(f"\n[dim]Showing 10 of {count} contacts. See {output_path} for full list.[/dim]\n")


@app.command()
def categories():
    """List available contact categories."""
    console.print("\n[bold cyan]Available Categories:[/bold cyan]\n")
    
    console.print("[bold]ai[/bold] - AI/ML companies")
    console.print("  Companies: " + ", ".join(COMPANIES["ai"][:5]) + "...")
    console.print("  Titles: CEO, CTO, ML Engineer, etc.\n")
    
    console.print("[bold]tech[/bold] - Major tech companies")
    console.print("  Companies: " + ", ".join(COMPANIES["tech"][:5]) + "...")
    console.print("  Titles: Various engineering and product roles\n")
    
    console.print("[bold]vc[/bold] - Venture capital firms")
    console.print("  Companies: " + ", ".join(COMPANIES["vc"][:5]) + "...")
    console.print("  Titles: Partner, Managing Partner, etc.\n")
    
    console.print("[bold]startup[/bold] - Startup companies")
    console.print("  Companies: " + ", ".join(COMPANIES["startup"][:5]) + "...")
    console.print("  Titles: Founder, CEO, early employees\n")
    
    console.print("[bold]investor[/bold] - Individual investors")
    console.print("  Focus: Angel investors and VC partners")
    console.print("  Tags: investor, vc, fundraising_target\n")


@app.command()
def demo():
    """Generate a demo dataset with mixed categories."""
    console.print("\n[bold cyan]Generating Demo Dataset[/bold cyan]\n")
    
    categories_to_generate = [
        ("ai", 20, "AI company contacts"),
        ("investor", 15, "Investors and VCs"),
        ("tech", 10, "Tech company contacts"),
        ("startup", 5, "Startup contacts")
    ]
    
    all_contacts = []
    
    for category, count, description in categories_to_generate:
        console.print(f"[cyan]Generating {count} {description}...[/cyan]")
        for _ in range(count):
            contact = generate_contact(category)
            all_contacts.append(contact)
    
    # Save
    output_path = Path("exports") / "demo_contacts.json"
    output_path.parent.mkdir(exist_ok=True)
    
    data = [contact.model_dump(mode='json') for contact in all_contacts]
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, default=str)
    
    console.print(f"\n[green]✓[/green] Generated {len(all_contacts)} total contacts")
    console.print(f"[green]✓[/green] Saved to {output_path}\n")
    
    # Summary
    console.print("[bold]Summary:[/bold]")
    for category, count, description in categories_to_generate:
        console.print(f"  • {count} {description}")
    
    console.print(f"\n[dim]Use this dataset for your hackathon demo![/dim]\n")


if __name__ == "__main__":
    app()

