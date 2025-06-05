from scanner.crawler import crawl_site
from scanner.analyzer import analyze_response
from scanner.issue import Issue
from rich.console import Console
from rich.table import Table

console = Console()

def get_url_from_user():
    console.print("[bold cyan]Enter a URL to scan:[/bold cyan]", end=" ")
    return input().strip()

def display_results(issues: list[Issue]):
    if not issues:
        console.print("[bold green]✓ No issues detected![/bold green]")
        return

    table = Table(title="Scan Results", show_lines=True)

    table.add_column("Severity", style="bold red", justify="center")
    table.add_column("Issue")
    table.add_column("URL", style="cyan")

    for issue in issues:
        severity = getattr(issue, "severity", "MEDIUM")  # default if not set
        table.add_row(severity.upper(), issue.title, issue.url)

    console.print(table)

def main():
    url = get_url_from_user()
    console.print(f"[yellow]Scanning...[/yellow] [italic]{url}[/italic]")

    responses = crawl_site(url)
    all_issues = []

    for response in responses:
        issues = analyze_response(response)
        all_issues.extend(issues)

    console.print(f"\n[bold cyan]Scan complete! Found {len(all_issues)} issue(s).[/bold cyan]")
    display_results(all_issues)

if __name__ == "__main__":
    main()
