import socket
import subprocess
import requests
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console()
TIMEOUT = 6


def run(cmd):
    try:
        return subprocess.run(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=6,
        ).stdout.decode("utf-8", "replace")
    except Exception:
        return ""


def local_addrs():
    rows = []
    out = run(["ip", "-o", "addr", "show"])
    for ln in out.splitlines():
        parts = ln.split()
        if len(parts) >= 4 and parts[2] in ("inet", "inet6"):
            rows.append((parts[1], parts[2], parts[3]))
    return rows


def default_route():
    out = run(["ip", "route", "show", "default"])
    return out.strip().splitlines()[0] if out.strip() else "N/A"


def public_ip():
    try:
        return requests.get("https://api.ipify.org", timeout=TIMEOUT).text.strip()
    except requests.RequestException:
        return "N/A"


if __name__ == "__main__":
    try:
        console.print()
        console.print("  [#9aa0a6]> [bold #cfcfcf]network info[/]")
        console.print("[#262626]  " + "─" * 48)

        t = Table(
            title="[bold #cfcfcf]Local Interfaces[/bold #cfcfcf]",
            box=box.DOUBLE_EDGE, border_style="#808080", header_style="bold #cfcfcf", show_lines=True,
        )
        t.add_column("Interface", style="bold white", width=14)
        t.add_column("Family", style="#a8a8a8", width=8)
        t.add_column("Address", style="#a8a8a8")
        rows = local_addrs()
        if rows:
            for iface, fam, addr in rows:
                t.add_row(iface, fam, addr)
        else:
            t.add_row("[dim]—[/dim]", "", "")
        console.print()
        console.print(t)

        summary = Table(box=box.DOUBLE_EDGE, border_style="#808080", header_style="bold #cfcfcf", show_lines=True)
        summary.add_column("Field", style="bold white", width=16)
        summary.add_column("Value", style="#a8a8a8")
        summary.add_row("Hostname", socket.gethostname())
        summary.add_row("Default route", default_route())
        summary.add_row("Public IP", public_ip())
        console.print()
        console.print(summary)
        console.print()

    except (KeyboardInterrupt, EOFError):
        console.print("\n[bold #cfcfcf][!] Interrupted.[/bold #cfcfcf]")
