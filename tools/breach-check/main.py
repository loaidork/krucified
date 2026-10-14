"""
Breach self-check.

- Password check uses the Have I Been Pwned "Pwned Passwords" range API with
  k-anonymity: only the first 5 chars of the SHA-1 hash ever leave this machine,
  so the password itself is never sent. No API key required.
- Email check uses the HIBP v3 API if you export HIBP_API_KEY; otherwise it opens
  the HIBP web page for that address.

Use only to check your OWN accounts/passwords.
"""
import os
import sys
import hashlib
import getpass
import webbrowser
import urllib.parse
import requests
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console()
TIMEOUT = 10
UA = "krucified-breach-check"


def check_password():
    pw = getpass.getpass("  password (hidden input) >> ")
    if not pw:
        console.print("[bold #cfcfcf][!] Empty. Cancelled.[/bold #cfcfcf]")
        return
    sha1 = hashlib.sha1(pw.encode("utf-8")).hexdigest().upper()
    prefix, suffix = sha1[:5], sha1[5:]
    try:
        resp = requests.get(
            f"https://api.pwnedpasswords.com/range/{prefix}",
            headers={"User-Agent": UA, "Add-Padding": "true"}, timeout=TIMEOUT,
        )
        resp.raise_for_status()
    except requests.RequestException as e:
        console.print(f"[bold #cfcfcf][!] Network error: {e}[/bold #cfcfcf]")
        return

    count = 0
    for line in resp.text.splitlines():
        h, _, c = line.partition(":")
        if h.strip() == suffix:
            count = int(c.strip() or "0")
            break

    console.print()
    if count > 0:
        console.print(Panel(
            f"[bold white]  This password appears in known breaches "
            f"[bold #cfcfcf]{count:,}[/bold #cfcfcf] time(s).[/bold white]\n"
            f"[dim]  Stop using it everywhere and rotate it.[/dim]",
            border_style="#808080", box=box.DOUBLE_EDGE,
        ))
    else:
        console.print(Panel(
            "[bold #cfcfcf]  Not found in any known breach corpus.[/bold #cfcfcf]\n"
            "[dim]  (Absence here is not proof it is safe.)[/dim]",
            border_style="#808080", box=box.DOUBLE_EDGE,
        ))
    console.print()


def check_email():
    email = console.input(
        "[bold #cfcfcf][[/bold #cfcfcf][bold white]=[/bold white][bold #cfcfcf]][/bold #cfcfcf] email: "
    ).strip()
    if not email or "@" not in email:
        console.print("[bold #cfcfcf][!] Invalid email.[/bold #cfcfcf]")
        return

    key = os.environ.get("HIBP_API_KEY")
    if not key:
        url = "https://haveibeenpwned.com/account/" + urllib.parse.quote(email)
        console.print("\n[dim]  No HIBP_API_KEY set — opening the HIBP web page instead."
                      "\n  For inline results:  export HIBP_API_KEY=...[/dim]")
        try:
            webbrowser.open(url)
        except Exception:
            pass
        console.print(f"[dim]  {url}[/dim]\n")
        return

    try:
        resp = requests.get(
            "https://haveibeenpwned.com/api/v3/breachedaccount/"
            + urllib.parse.quote(email) + "?truncateResponse=false",
            headers={"hibp-api-key": key, "User-Agent": UA}, timeout=TIMEOUT,
        )
    except requests.RequestException as e:
        console.print(f"[bold #cfcfcf][!] Network error: {e}[/bold #cfcfcf]")
        return

    if resp.status_code == 404:
        console.print("\n[bold #cfcfcf]  No breaches found for this address.[/bold #cfcfcf]\n")
        return
    if resp.status_code != 200:
        console.print(f"[bold #cfcfcf][!] API returned {resp.status_code}[/bold #cfcfcf]")
        return

    breaches = resp.json()
    table = Table(
        title=f"[bold #cfcfcf]Breaches[/bold #cfcfcf] — [bold white]{email}[/bold white]",
        box=box.DOUBLE_EDGE, border_style="#808080", header_style="bold #cfcfcf", show_lines=True,
    )
    table.add_column("Name", style="bold white")
    table.add_column("Date", style="#a8a8a8", width=12)
    table.add_column("Exposed data", style="#a8a8a8")
    for b in breaches:
        table.add_row(
            b.get("Name", "?"),
            b.get("BreachDate", "?"),
            ", ".join(b.get("DataClasses", []))[:60],
        )
    console.print()
    console.print(table)
    console.print()


if __name__ == "__main__":
    try:
        console.print()
        console.print("  [#9aa0a6]> [bold #cfcfcf]breach self-check[/]")
        console.print("[#262626]  " + "─" * 48)
        console.print("\n  [bold #cfcfcf][1][/bold #cfcfcf] check a password   "
                      "[bold #cfcfcf][2][/bold #cfcfcf] check an email\n")
        choice = console.input("  >> ").strip()
        if choice == "1":
            check_password()
        elif choice == "2":
            check_email()
        else:
            console.print("[bold #cfcfcf][!] Cancelled.[/bold #cfcfcf]")
    except (KeyboardInterrupt, EOFError):
        console.print("\n[bold #cfcfcf][!] Interrupted.[/bold #cfcfcf]")
