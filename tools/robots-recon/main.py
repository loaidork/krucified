"""robots.txt / sitemap recon — fetch a site's robots.txt and enumerate sitemaps."""
import re
import requests
from rich.console import Console

console = Console()
TIMEOUT = 12
UA = "Mozilla/5.0 (X11; Linux x86_64) krucified/1.0"


def header():
    console.print()
    console.print("  [#9aa0a6]> [bold #cfcfcf]robots / sitemap recon[/]")
    console.print("[#262626]  " + "─" * 48)


def base(url):
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    return url.rstrip("/")


def fetch(url):
    r = requests.get(url, headers={"User-Agent": UA}, timeout=TIMEOUT)
    return r


if __name__ == "__main__":
    try:
        header()
        console.print()
        site = console.input("  [#9aa0a6][=][/#9aa0a6] site: ").strip()
        if not site:
            console.print("  [bold #cfcfcf][!] empty.[/bold #cfcfcf]")
            raise SystemExit(0)
        root = base(site)

        try:
            r = fetch(f"{root}/robots.txt")
        except requests.RequestException as e:
            console.print(f"  [bold #cfcfcf][!] request failed: {e}[/bold #cfcfcf]")
            raise SystemExit(0)

        console.print()
        console.print(f"  [#808080]GET {root}/robots.txt → [#f5f5f5]{r.status_code}[/#f5f5f5]")
        if r.status_code != 200 or not r.text.strip():
            console.print("  [dim]  no robots.txt.[/dim]\n")
            raise SystemExit(0)

        disallows, allows, sitemaps, agents = [], [], [], []
        for line in r.text.splitlines():
            s = line.strip()
            if not s or s.startswith("#"):
                continue
            low = s.lower()
            if low.startswith("disallow:"):
                disallows.append(s.split(":", 1)[1].strip())
            elif low.startswith("allow:"):
                allows.append(s.split(":", 1)[1].strip())
            elif low.startswith("sitemap:"):
                sitemaps.append(s.split(":", 1)[1].strip())
            elif low.startswith("user-agent:"):
                agents.append(s.split(":", 1)[1].strip())

        console.print(f"  [#808080]user-agents: [#b8b8b8]{', '.join(dict.fromkeys(agents)) or '—'}[/#b8b8b8]")
        console.print()
        if disallows:
            console.print(f"  [bold #cfcfcf]disallow[/bold #cfcfcf] [dim]({len(disallows)})[/dim] — [dim]paths the owner hides from crawlers[/dim]")
            for p in disallows[:40]:
                console.print(f"    [#9aa0a6]>[/#9aa0a6] [#b8b8b8]{p or '/'}[/#b8b8b8]")
            if len(disallows) > 40:
                console.print(f"    [dim]… +{len(disallows) - 40} more[/dim]")
        if allows:
            console.print(f"\n  [bold #cfcfcf]allow[/bold #cfcfcf] [dim]({len(allows)})[/dim]")
            for p in allows[:15]:
                console.print(f"    [#808080]>[/#808080] [#b8b8b8]{p}[/#b8b8b8]")

        # discover sitemaps (declared or default)
        if not sitemaps:
            sitemaps = [f"{root}/sitemap.xml"]
        console.print(f"\n  [bold #cfcfcf]sitemaps[/bold #cfcfcf]")
        for sm in dict.fromkeys(sitemaps):
            try:
                sr = fetch(sm)
                n = len(re.findall(r"<loc>", sr.text)) if sr.status_code == 200 else 0
                tag = f"[#f5f5f5]{sr.status_code}[/#f5f5f5]"
                extra = f" [dim]({n} urls)[/dim]" if n else ""
                console.print(f"    [#9aa0a6]>[/#9aa0a6] {tag} [#b8b8b8]{sm}[/#b8b8b8]{extra}")
            except requests.RequestException:
                console.print(f"    [dim]>  err  {sm}[/dim]")
        console.print()
    except (KeyboardInterrupt, EOFError):
        console.print("\n  [#9aa0a6]> interrupted.[/#9aa0a6]")
