"""MAC / OUI vendor lookup via the public macvendors API."""
import re
import requests
from rich.console import Console
from rich.table import Table
from rich import box

console = Console()
TIMEOUT = 8
MAC_RE = re.compile(r"^[0-9A-Fa-f]{2}([:\-]?[0-9A-Fa-f]{2}){2,5}$")


def header():
    console.print()
    console.print("  [#9aa0a6]> [bold #cfcfcf]mac vendor lookup[/]")
    console.print("[#262626]  " + "─" * 48)


if __name__ == "__main__":
    try:
        header()
        console.print()
        mac = console.input("  [#9aa0a6][=][/#9aa0a6] MAC (ex: 00:1A:2B:3C:4D:5E): ").strip()
        if not mac or not MAC_RE.match(mac):
            console.print("  [bold #cfcfcf][!] invalid MAC format.[/bold #cfcfcf]")
            raise SystemExit(0)

        try:
            resp = requests.get(
                f"https://api.macvendors.com/{mac}",
                headers={"User-Agent": "krucified-mac-lookup"}, timeout=TIMEOUT,
            )
        except requests.RequestException as e:
            console.print(f"  [bold #cfcfcf][!] network error: {e}[/bold #cfcfcf]")
            raise SystemExit(0)

        vendor = resp.text.strip() if resp.status_code == 200 else None

        t = Table(
            box=box.DOUBLE_EDGE, border_style="#808080", header_style="bold #cfcfcf", show_lines=True,
        )
        t.add_column("Field", style="bold #f5f5f5", width=10)
        t.add_column("Value", style="#b8b8b8")
        norm = re.sub(r"[^0-9A-Fa-f]", "", mac).upper()
        t.add_row("MAC", mac)
        t.add_row("OUI", norm[:6] if len(norm) >= 6 else norm)
        t.add_row("Vendor", vendor if vendor else "[dim]not found / unregistered[/dim]")

        console.print()
        console.print(t)
        console.print()
    except (KeyboardInterrupt, EOFError):
        console.print("\n  [#9aa0a6]> interrupted.[/#9aa0a6]")
