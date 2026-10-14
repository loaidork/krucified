"""Wayback Machine — check archive history & newest/oldest snapshots for a URL."""
import requests
from rich.console import Console
from rich import box
from rich.panel import Panel

console = Console()
TIMEOUT = 15
UA = "krucified/1.0"


def header():
    console.print()
    console.print("  [#9aa0a6]> [bold #cfcfcf]wayback machine[/]")
    console.print("[#262626]  " + "─" * 48)


def fmt_ts(ts):
    if not ts or len(ts) < 14:
        return ts or "—"
    return f"{ts[0:4]}-{ts[4:6]}-{ts[6:8]} {ts[8:10]}:{ts[10:12]}:{ts[12:14]} UTC"


if __name__ == "__main__":
    try:
        header()
        console.print()
        url = console.input("  [#9aa0a6][=][/#9aa0a6] url: ").strip()
        if not url:
            console.print("  [bold #cfcfcf][!] empty url.[/bold #cfcfcf]")
            raise SystemExit(0)

        # availability: newest snapshot
        try:
            av = requests.get("https://archive.org/wayback/available",
                              params={"url": url}, headers={"User-Agent": UA},
                              timeout=TIMEOUT).json()
        except requests.RequestException as e:
            console.print(f"  [bold #cfcfcf][!] request failed: {e}[/bold #cfcfcf]")
            raise SystemExit(0)

        snap = (av.get("archived_snapshots") or {}).get("closest") or {}

        # oldest + newest snapshot via cheap limited CDX calls (full counts are slow)
        first_ts, last_ts = None, None
        CDX = "https://web.archive.org/cdx/search/cdx"
        try:
            old = requests.get(CDX, params={"url": url, "output": "json",
                               "fl": "timestamp", "limit": 1},
                               headers={"User-Agent": UA}, timeout=TIMEOUT).json()
            rows = old[1:] if old and old and old[0] == ["timestamp"] else old
            if rows:
                first_ts = rows[0][0]
            new = requests.get(CDX, params={"url": url, "output": "json",
                               "fl": "timestamp", "limit": -1},
                               headers={"User-Agent": UA}, timeout=TIMEOUT).json()
            rows = new[1:] if new and new and new[0] == ["timestamp"] else new
            if rows:
                last_ts = rows[0][0]
        except Exception:
            pass

        archived = bool(snap.get("available") or first_ts or last_ts)
        body = []
        body.append(f"[#808080]archived   [/#808080]" +
                    ("[#f5f5f5]yes[/#f5f5f5]" if archived else "[dim]no snapshots found[/dim]"))
        if first_ts:
            body.append(f"[#808080]first      [/#808080][#b8b8b8]{fmt_ts(first_ts)}[/#b8b8b8]")
        if last_ts:
            body.append(f"[#808080]latest     [/#808080][#b8b8b8]{fmt_ts(last_ts)}[/#b8b8b8]")
        if snap.get("url"):
            body.append(f"[#808080]closest    [/#808080][bold #f5f5f5]{snap['url']}[/bold #f5f5f5]")
        console.print()
        console.print(Panel("\n".join(body),
                            title="[bold #cfcfcf]archive[/bold #cfcfcf]",
                            border_style="#808080", box=box.DOUBLE_EDGE, padding=(0, 1)))
        console.print()
    except (KeyboardInterrupt, EOFError):
        console.print("\n  [#9aa0a6]> interrupted.[/#9aa0a6]")
