"""
LAN discovery — lists hosts in the kernel neighbour (ARP) cache, and can run an
active ping sweep of your local subnet with nmap. Local network only.
"""
import re
import socket
import shutil
import subprocess
from rich.console import Console
from rich.table import Table
from rich import box

console = Console()


def header():
    console.print()
    console.print("  [#9aa0a6]> [bold #cfcfcf]lan sweep[/]")
    console.print("[#262626]  " + "─" * 48)


def run(cmd, timeout=6):
    try:
        return subprocess.run(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=timeout,
        ).stdout.decode("utf-8", "replace")
    except Exception:
        return ""


def local_cidr():
    out = run(["ip", "-o", "-f", "inet", "addr", "show"])
    for ln in out.splitlines():
        parts = ln.split()
        if len(parts) >= 4 and parts[2] == "inet" and not parts[3].startswith("127."):
            return parts[1], parts[3]  # iface, a.b.c.d/nn
    return None, None


def neighbours():
    rows = []
    out = run(["ip", "neigh", "show"])
    for ln in out.splitlines():
        m = re.match(r"(\S+)\s+dev\s+(\S+)(?:.*lladdr\s+(\S+))?.*?(\w+)\s*$", ln)
        if m:
            ip, dev, mac, state = m.group(1), m.group(2), m.group(3) or "—", m.group(4)
            rows.append((ip, mac, dev, state))
    return rows


if __name__ == "__main__":
    try:
        header()
        iface, cidr = local_cidr()
        console.print(f"[dim]  interface: {iface or '?'}   subnet: {cidr or '?'}[/dim]")

        rows = neighbours()
        t = Table(
            title="[bold #cfcfcf]Neighbour Cache (ARP)[/bold #cfcfcf]",
            box=box.DOUBLE_EDGE, border_style="#808080", header_style="bold #cfcfcf", show_lines=False,
        )
        t.add_column("IP", style="bold #f5f5f5", width=18)
        t.add_column("MAC", style="#b8b8b8", width=20)
        t.add_column("dev", style="#a8a8a8", width=10)
        t.add_column("state", style="#a8a8a8")
        t.add_column("hostname", style="#b8b8b8")
        for ip, mac, dev, state in rows:
            try:
                host = socket.gethostbyaddr(ip)[0]
            except Exception:
                host = "—"
            t.add_row(ip, mac, dev, state, host)
        if not rows:
            t.add_row("[dim]empty[/dim]", "", "", "", "")
        console.print()
        console.print(t)
        console.print()

        if cidr and shutil.which("nmap"):
            ans = console.input(f"  [#9aa0a6][=][/#9aa0a6] active ping sweep of {cidr} with nmap? [y/N] ").strip().lower()
            if ans == "y":
                cmd = ["nmap", "-sn", cidr]
                console.print(f"[dim]  $ {' '.join(cmd)}[/dim]")
                console.print("[#262626]  " + "─" * 48)
                subprocess.run(cmd)
                console.print()
        elif not shutil.which("nmap"):
            console.print("[dim]  (install nmap for an active ping sweep: sudo pacman -S nmap)[/dim]\n")
    except (KeyboardInterrupt, EOFError):
        console.print("\n  [#9aa0a6]> interrupted.[/#9aa0a6]")
