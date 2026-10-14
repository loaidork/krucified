import re
import os
import requests
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import box

console = Console()

IPINFO_TOKEN = os.environ.get("IPINFO_TOKEN")
TIMEOUT = 8
IP_REGEX = re.compile(
    r'^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$'
)


def lookup_ip(ip):
    url = f"https://ipinfo.io/{ip}"
    params = {"token": IPINFO_TOKEN} if IPINFO_TOKEN else None
    resp = requests.get(url, params=params, timeout=TIMEOUT)
    resp.raise_for_status()
    return resp.json()


def display(ip, data):
    table = Table(
        title=f"[bold #cfcfcf]IP Lookup[/bold #cfcfcf] — [bold white]{ip}[/bold white]",
        box=box.DOUBLE_EDGE,
        border_style="#808080",
        header_style="bold #cfcfcf",
        show_lines=True,
    )
    table.add_column("Field", style="bold white", width=20)
    table.add_column("Value", style="#a8a8a8")

    table.add_row("IP",           data.get("ip",       "N/A"))
    table.add_row("City",         data.get("city",     "N/A"))
    table.add_row("Region",       data.get("region",   "N/A"))
    table.add_row("Country",      data.get("country",  "N/A"))
    table.add_row("Postal Code",  data.get("postal",   "N/A"))
    table.add_row("Coordinates",  data.get("loc",      "N/A"))
    table.add_row("Organization", data.get("org",      "N/A"))
    table.add_row("Timezone",     data.get("timezone", "N/A"))
    table.add_row("Hostname",     data.get("hostname", "N/A"))

    console.print()
    console.print(table)
    console.print()


if __name__ == "__main__":
    try:
        console.print()
        console.print("  [#9aa0a6]> [bold #cfcfcf]ip lookup[/]")
        console.print("[#262626]  " + "─" * 48)
        console.print()

        ip = console.input(
            "[bold #cfcfcf][[/bold #cfcfcf][bold white]=[/bold white][bold #cfcfcf]][/bold #cfcfcf] IP Address: "
        ).strip()

        if not ip:
            console.print("[bold #cfcfcf][!] Empty address. Cancelled.[/bold #cfcfcf]")
            raise SystemExit(0)

        if not IP_REGEX.match(ip):
            console.print(f"[bold #cfcfcf][!] Invalid IP format:[/bold #cfcfcf] {ip}")
            raise SystemExit(0)

        with Progress(
            SpinnerColumn(spinner_name="dots", style="bold #cfcfcf"),
            TextColumn("[bold white]{task.description}"),
            console=console, transient=True,
        ) as p:
            p.add_task("Fetching information...", total=None)
            data = lookup_ip(ip)

        display(ip, data)

    except requests.HTTPError as e:
        console.print(f"[bold #cfcfcf][!] API error: {e}[/bold #cfcfcf]")
    except requests.RequestException as e:
        console.print(f"[bold #cfcfcf][!] Network error: {e}[/bold #cfcfcf]")
    except (KeyboardInterrupt, EOFError):
        console.print("\n[bold #cfcfcf][!] Interrupted.[/bold #cfcfcf]")
