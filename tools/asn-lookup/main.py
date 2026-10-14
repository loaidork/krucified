"""ASN / IP-prefix lookup — autonomous-system intel via RIPEstat (public API)."""
import requests
from rich.console import Console
from rich.table import Table
from rich import box

console = Console()
TIMEOUT = 15
API = "https://stat.ripe.net/data"
UA = "krucified/1.0"


def header():
    console.print()
    console.print("  [#9aa0a6]> [bold #cfcfcf]asn lookup[/]")
    console.print("[#262626]  " + "─" * 48)


def get(path, resource):
    r = requests.get(f"{API}/{path}/data.json", params={"resource": resource},
                     headers={"User-Agent": UA}, timeout=TIMEOUT)
    r.raise_for_status()
    return r.json().get("data", {})


def show_asn(asn):
    ov = get("as-overview", f"AS{asn}")
    t = Table(box=box.DOUBLE_EDGE, border_style="#808080",
              header_style="bold #cfcfcf", show_lines=True,
              title=f"[bold #cfcfcf]AS{asn}[/bold #cfcfcf] — [#f5f5f5]{ov.get('holder','?')}[/#f5f5f5]")
    t.add_column("field", style="bold #f5f5f5", width=16)
    t.add_column("value", style="#b8b8b8")
    t.add_row("holder", str(ov.get("holder") or "—"))
    t.add_row("announced", "yes" if ov.get("announced") else "no")
    t.add_row("type", str(ov.get("type") or "—"))
    block = ov.get("block") or {}
    t.add_row("rir block", str(block.get("desc") or "—"))
    t.add_row("resource", str(ov.get("resource") or "—"))
    console.print()
    console.print(t)

    pref = get("announced-prefixes", f"AS{asn}")
    plist = pref.get("prefixes", []) or []
    v4 = [p["prefix"] for p in plist if ":" not in p.get("prefix", "")]
    v6 = [p["prefix"] for p in plist if ":" in p.get("prefix", "")]
    console.print(f"  [#808080]announced prefixes: [#f5f5f5]{len(v4)}[/#f5f5f5] IPv4 · [#f5f5f5]{len(v6)}[/#f5f5f5] IPv6[/#808080]")
    for p in v4[:15]:
        console.print(f"    [#9aa0a6]>[/#9aa0a6] [#b8b8b8]{p}[/#b8b8b8]")
    if len(v4) > 15:
        console.print(f"    [dim]… +{len(v4) - 15} more[/dim]")
    console.print()


def show_ip(ip):
    ni = get("network-info", ip)
    prefix = ni.get("prefix")
    asns = ni.get("asns", []) or []
    console.print()
    console.print(f"  [#808080]prefix   [/#808080][#f5f5f5]{prefix or '—'}[/#f5f5f5]")
    console.print(f"  [#808080]asns     [/#808080][#b8b8b8]{', '.join('AS' + str(a) for a in asns) or '—'}[/#b8b8b8]")
    if prefix:
        po = get("prefix-overview", prefix)
        for a in (po.get("asns") or []):
            console.print(f"  [#808080]holder   [/#808080][#b8b8b8]AS{a.get('asn','?')} — {a.get('holder') or '?'}[/#b8b8b8]")
        block = po.get("block") or {}
        if block:
            console.print(f"  [#808080]rir block[/#808080][dim] {block.get('desc') or ''}[/dim]")
    console.print()


if __name__ == "__main__":
    try:
        header()
        console.print("[dim]  enter an ASN (e.g. 13335 or AS13335) or an IP address[/dim]")
        console.print()
        raw = console.input("  [#9aa0a6][=][/#9aa0a6] asn/ip: ").strip()
        if not raw:
            console.print("  [bold #cfcfcf][!] empty.[/bold #cfcfcf]")
            raise SystemExit(0)
        try:
            q = raw.upper().removeprefix("AS")
            if q.isdigit():
                show_asn(q)
            else:
                show_ip(raw)
        except requests.RequestException as e:
            console.print(f"  [bold #cfcfcf][!] lookup failed: {e}[/bold #cfcfcf]")
    except (KeyboardInterrupt, EOFError):
        console.print("\n  [#9aa0a6]> interrupted.[/#9aa0a6]")
