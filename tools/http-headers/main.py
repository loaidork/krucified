"""HTTP header / banner grab — inspect response headers and security posture."""
import requests
from rich.console import Console
from rich.table import Table
from rich import box

console = Console()
TIMEOUT = 10
UA = "Mozilla/5.0 (X11; Linux x86_64) krucified/1.0"
SEC_HEADERS = [
    "Strict-Transport-Security", "Content-Security-Policy", "X-Frame-Options",
    "X-Content-Type-Options", "Referrer-Policy", "Permissions-Policy",
]


def header():
    console.print()
    console.print("  [#9aa0a6]> [bold #cfcfcf]http headers[/]")
    console.print("[#262626]  " + "─" * 48)


if __name__ == "__main__":
    try:
        header()
        console.print()
        url = console.input("  [#9aa0a6][=][/#9aa0a6] url (ex: example.com): ").strip()
        if not url:
            console.print("  [bold #cfcfcf][!] empty url.[/bold #cfcfcf]")
            raise SystemExit(0)
        if not url.startswith(("http://", "https://")):
            url = "https://" + url

        try:
            resp = requests.get(url, headers={"User-Agent": UA}, timeout=TIMEOUT, allow_redirects=True)
        except requests.RequestException as e:
            console.print(f"  [bold #cfcfcf][!] request failed: {e}[/bold #cfcfcf]")
            raise SystemExit(0)

        console.print()
        console.print(f"  [#b8b8b8]final url  [/#b8b8b8][#f5f5f5]{resp.url}[/#f5f5f5]")
        console.print(f"  [#b8b8b8]status     [/#b8b8b8][bold #cfcfcf]{resp.status_code}[/bold #cfcfcf]")
        if len(resp.history) > 0:
            console.print(f"  [#b8b8b8]redirects  [/#b8b8b8]" +
                          " -> ".join(str(h.status_code) for h in resp.history) + f" -> {resp.status_code}")

        t = Table(
            title="[bold #cfcfcf]Response Headers[/bold #cfcfcf]",
            box=box.DOUBLE_EDGE, border_style="#808080", header_style="bold #cfcfcf", show_lines=True,
        )
        t.add_column("Header", style="bold #f5f5f5", width=28)
        t.add_column("Value", style="#b8b8b8")
        for k, v in resp.headers.items():
            t.add_row(k, v)
        console.print()
        console.print(t)

        sec = Table(
            title="[bold #cfcfcf]Security Headers[/bold #cfcfcf]",
            box=box.DOUBLE_EDGE, border_style="#808080", header_style="bold #cfcfcf", show_lines=True,
        )
        sec.add_column("Header", style="bold #f5f5f5", width=28)
        sec.add_column("Present", style="#b8b8b8")
        for h in SEC_HEADERS:
            present = h in resp.headers
            sec.add_row(h, "[#cfcfcf]yes[/#cfcfcf]" if present else "[dim]missing[/dim]")
        console.print()
        console.print(sec)
        console.print()
    except (KeyboardInterrupt, EOFError):
        console.print("\n  [#9aa0a6]> interrupted.[/#9aa0a6]")
