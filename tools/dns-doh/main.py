"""DNS-over-HTTPS resolver — queries Cloudflare / Google DoH endpoints."""
import requests
from rich.console import Console
from rich.table import Table
from rich import box

console = Console()
TIMEOUT = 10
RTYPES = ["A", "AAAA", "MX", "NS", "TXT", "CNAME", "SOA", "CAA"]
PROVIDERS = {
    "cloudflare": "https://cloudflare-dns.com/dns-query",
    "google": "https://dns.google/resolve",
}
# numeric type -> name, for pretty output
TYPE_NAMES = {1: "A", 2: "NS", 5: "CNAME", 6: "SOA", 15: "MX", 16: "TXT",
              28: "AAAA", 257: "CAA"}


def header():
    console.print()
    console.print("  [#9aa0a6]> [bold #cfcfcf]dns-over-https[/]")
    console.print("[#262626]  " + "─" * 48)


def query(endpoint, name, rtype):
    r = requests.get(endpoint, params={"name": name, "type": rtype},
                     headers={"accept": "application/dns-json"}, timeout=TIMEOUT)
    r.raise_for_status()
    return r.json()


if __name__ == "__main__":
    try:
        header()
        console.print("[dim]  resolves over encrypted HTTPS — bypasses local resolver[/dim]")
        console.print()
        name = console.input("  [#9aa0a6][=][/#9aa0a6] domain: ").strip()
        if not name:
            console.print("  [bold #cfcfcf][!] empty.[/bold #cfcfcf]")
            raise SystemExit(0)
        prov = console.input("  [#9aa0a6][=][/#9aa0a6] provider (cloudflare/google) [cloudflare]: ").strip().lower() or "cloudflare"
        endpoint = PROVIDERS.get(prov, PROVIDERS["cloudflare"])

        t = Table(
            title=f"[bold #cfcfcf]DoH[/bold #cfcfcf] — [#f5f5f5]{name}[/#f5f5f5] via {prov}",
            box=box.DOUBLE_EDGE, border_style="#808080", header_style="bold #cfcfcf", show_lines=False,
        )
        t.add_column("type", style="bold #f5f5f5", width=8)
        t.add_column("ttl", style="#808080", width=8)
        t.add_column("answer", style="#b8b8b8")
        found = False
        for rt in RTYPES:
            try:
                data = query(endpoint, name, rt)
            except requests.RequestException as e:
                console.print(f"  [bold #cfcfcf][!] {rt}: {e}[/bold #cfcfcf]")
                continue
            for ans in data.get("Answer", []):
                tn = TYPE_NAMES.get(ans.get("type"), str(ans.get("type")))
                t.add_row(tn, str(ans.get("TTL", "")), str(ans.get("data", "")).strip())
                found = True
        console.print()
        if found:
            console.print(t)
        else:
            console.print("  [dim]  no records returned.[/dim]")
        console.print()
    except (KeyboardInterrupt, EOFError):
        console.print("\n  [#9aa0a6]> interrupted.[/#9aa0a6]")
