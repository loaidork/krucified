"""
Passive subdomain enumeration via crt.sh (Certificate Transparency logs).
No scanning of the target — just reads public CT log data.
"""
import re
import requests
from rich.console import Console
from rich.table import Table
from rich import box

console = Console()
TIMEOUT = 20
DOMAIN_RE = re.compile(r"^[a-zA-Z0-9]([a-zA-Z0-9\-._]{0,251}[a-zA-Z0-9])?$")


def header():
    console.print()
    console.print("  [#9aa0a6]> [bold #cfcfcf]subdomain enum[/]")
    console.print("[#262626]  " + "─" * 48)


if __name__ == "__main__":
    try:
        header()
        console.print("[dim]  source: crt.sh certificate transparency logs[/dim]")
        console.print()
        domain = console.input("  [#9aa0a6][=][/#9aa0a6] domain (ex: example.com): ").strip().rstrip(".")
        if not domain or not DOMAIN_RE.match(domain):
            console.print("  [bold #cfcfcf][!] invalid or empty domain.[/bold #cfcfcf]")
            raise SystemExit(0)

        try:
            resp = requests.get(
                "https://crt.sh/", params={"q": f"%.{domain}", "output": "json"},
                headers={"User-Agent": "krucified-subdomain-enum"}, timeout=TIMEOUT,
            )
            resp.raise_for_status()
            data = resp.json()
        except requests.RequestException as e:
            console.print(f"  [bold #cfcfcf][!] network error: {e}[/bold #cfcfcf]")
            raise SystemExit(0)
        except ValueError:
            console.print("  [bold #cfcfcf][!] unexpected response from crt.sh.[/bold #cfcfcf]")
            raise SystemExit(0)

        subs = set()
        for row in data:
            for name in str(row.get("name_value", "")).splitlines():
                name = name.strip().lstrip("*.").lower()
                if name.endswith(domain):
                    subs.add(name)
        subs.discard(domain)

        table = Table(
            title=f"[bold #cfcfcf]Subdomains[/bold #cfcfcf] — [#f5f5f5]{domain}[/#f5f5f5]  "
                  f"([#b8b8b8]{len(subs)}[/#b8b8b8])",
            box=box.DOUBLE_EDGE, border_style="#808080",
            header_style="bold #cfcfcf", show_lines=False,
        )
        table.add_column("Subdomain", style="#b8b8b8")
        for s in sorted(subs):
            table.add_row(s)
        if not subs:
            table.add_row("[dim]none found[/dim]")

        console.print()
        console.print(table)
        console.print()
    except (KeyboardInterrupt, EOFError):
        console.print("\n  [#9aa0a6]> interrupted.[/#9aa0a6]")
