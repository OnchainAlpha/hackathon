"""
Quick test script for Apollo.io integration.
Run this to verify your setup is working correctly.
"""

from rich.console import Console
from rich.panel import Panel
from scrapers.apollo_scraper import ApolloClient

console = Console()


def test_connection():
    """Test basic connection to Apollo.io API."""
    console.print(Panel.fit(
        "[bold cyan]Testing Apollo.io Connection[/bold cyan]",
        border_style="cyan"
    ))
    
    try:
        # Initialize client
        console.print("\n[cyan]1. Initializing Apollo.io client...[/cyan]")
        client = ApolloClient()
        console.print("[green]✓[/green] Client initialized successfully")
        
        # Test simple search
        console.print("\n[cyan]2. Testing people search...[/cyan]")
        result = client.search_people(
            query="CEO",
            per_page=5
        )
        console.print(f"[green]✓[/green] Search successful! Found {result.total_results} total results")
        console.print(f"   Retrieved {len(result.contacts)} contacts")
        
        # Display first contact
        if result.contacts:
            contact = result.contacts[0]
            console.print("\n[cyan]3. Sample contact:[/cyan]")
            console.print(f"   Name: {contact.name}")
            console.print(f"   Title: {contact.title}")
            console.print(f"   Company: {contact.company}")
            console.print(f"   Email: {contact.email or 'N/A'}")
            console.print(f"   Location: {contact.city}, {contact.state}, {contact.country}")
        
        console.print("\n[bold green]✓ All tests passed![/bold green]")
        console.print("\n[dim]Your Apollo.io integration is working correctly.[/dim]")
        console.print("[dim]You can now use the CLI tool: python -m cli.search_contacts search[/dim]")
        
        return True
        
    except ValueError as e:
        console.print(f"\n[bold red]✗ Configuration Error:[/bold red] {e}")
        console.print("\n[yellow]Please check your .env file and ensure APOLLO_API_KEY is set.[/yellow]")
        return False
        
    except Exception as e:
        console.print(f"\n[bold red]✗ Test Failed:[/bold red] {e}")
        console.print("\n[yellow]Check your internet connection and API key.[/yellow]")
        return False


if __name__ == "__main__":
    test_connection()

