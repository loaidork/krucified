"""URL expander — follows the redirect chain of a (possibly shortened) link."""
import requests
from rich.console import Console
from rich import box
from rich.table import Table

console = Console()
TIMEOUT = 10
UA = "Mozilla/5.0 (X11; Linux x86_64) krucified/1.0"


def header():
    console.print()
    console.print("  [#9aa0a6]> [bold #cfcfcf]url expander[/]")
    console.print("[#262626]  " + "─" * 48)


if __name__ == "__main__":
    try:
        header()
        console.print()
        url = console.input("  [#9aa0a6][=][/#9aa0a6] url: ").strip()
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

        t = Table(
            title="[bold #cfcfcf]Redirect Chain[/bold #cfcfcf]",
            box=box.DOUBLE_EDGE, border_style="#808080", header_style="bold #cfcfcf", show_lines=True,
        )
        t.add_column("#", style="bold #cfcfcf", width=3)
        t.add_column("code", style="#a8a8a8", width=6)
        t.add_column("url", style="#b8b8b8")
        hops = list(resp.history) + [resp]
        for i, h in enumerate(hops):
            t.add_row(str(i), str(h.status_code), h.url)
        console.print()
        console.print(t)
        console.print(f"  [#b8b8b8]final  [/#b8b8b8][bold #f5f5f5]{resp.url}[/bold #f5f5f5]")
        console.print()
    except (KeyboardInterrupt, EOFError):
        console.print("\n  [#9aa0a6]> interrupted.[/#9aa0a6]")
