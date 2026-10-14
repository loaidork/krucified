"""
Packet capture — the Wireshark CLI family.

Prefers tshark (Wireshark's terminal capture tool); falls back to tcpdump.
Live capture needs root or CAP_NET_RAW, so this prefixes sudo when needed.
Capture only on networks you are authorized to monitor.
"""
import os
import re
import shutil
import subprocess
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console()
IFACE_RE = re.compile(r"^[A-Za-z0-9._@\-]{1,32}$")
FILTER_RE = re.compile(r"^[A-Za-z0-9 .:/()\-_&|=<>!]{0,120}$")


def list_interfaces():
    names = []
    try:
        out = subprocess.run(
            ["ip", "-o", "link", "show"],
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=5,
        ).stdout.decode("utf-8", "replace")
        for ln in out.splitlines():
            parts = ln.split(":")
            if len(parts) >= 2:
                name = parts[1].strip().split("@")[0]
                if name:
                    names.append(name)
    except Exception:
        pass
    return names


if __name__ == "__main__":
    try:
        console.print()
        console.print("  [#9aa0a6]> [bold #cfcfcf]packet capture[/]")
        console.print("[#262626]  " + "─" * 48)
        console.print()

        tshark = shutil.which("tshark")
        tcpdump = shutil.which("tcpdump")
        if not tshark and not tcpdump:
            console.print("[bold #cfcfcf][!] Neither tshark nor tcpdump is installed.[/bold #cfcfcf]")
            console.print("[dim]  install:  sudo pacman -S wireshark-cli   (or)  sudo pacman -S tcpdump[/dim]\n")
            raise SystemExit(0)
        engine = "tshark" if tshark else "tcpdump"
        console.print(f"[dim]  engine: {engine}[/dim]")

        ifaces = list_interfaces()
        if ifaces:
            table = Table(box=box.SIMPLE, border_style="#808080", header_style="bold #cfcfcf")
            table.add_column("Interface", style="white")
            for n in ifaces:
                table.add_row(n)
            console.print(table)

        iface = console.input("[bold #cfcfcf][=][/bold #cfcfcf] interface (e.g. eth0, wlan0, any) >> ").strip()
        if not iface or not IFACE_RE.match(iface):
            console.print("[bold #cfcfcf][!] Invalid interface.[/bold #cfcfcf]")
            raise SystemExit(0)

        try:
            count = int(console.input("[bold #cfcfcf][=][/bold #cfcfcf] packet count (default 20) >> ").strip() or "20")
        except ValueError:
            count = 20
        count = max(1, min(count, 100000))

        bpf = console.input("[bold #cfcfcf][=][/bold #cfcfcf] BPF filter (optional, e.g. 'tcp port 443') >> ").strip()
        if bpf and not FILTER_RE.match(bpf):
            console.print("[bold #cfcfcf][!] Filter contains unsupported characters.[/bold #cfcfcf]")
            raise SystemExit(0)

        if engine == "tshark":
            cmd = ["tshark", "-i", iface, "-c", str(count)]
            if bpf:
                cmd += ["-f", bpf]
        else:
            cmd = ["tcpdump", "-i", iface, "-c", str(count), "-nn"]
            if bpf:
                cmd += bpf.split()

        if os.geteuid() != 0:
            if shutil.which("sudo"):
                console.print("[dim]  live capture needs root — prefixing sudo[/dim]")
                cmd = ["sudo"] + cmd
            else:
                console.print("[bold #cfcfcf][!] Live capture needs root; re-run as root.[/bold #cfcfcf]")
                raise SystemExit(0)

        console.print()
        console.print(f"[dim]  $ {' '.join(cmd)}[/dim]\n")
        console.print("[bold #cfcfcf] ── capture "
                      "──────────────────────────────────────────[/bold #cfcfcf]\n")
        subprocess.run(cmd)
        console.print("\n[bold #cfcfcf] ── end ─────────────────────────────────────"
                      "──────────[/bold #cfcfcf]")

    except (KeyboardInterrupt, EOFError):
        console.print("\n[bold #cfcfcf][!] Interrupted.[/bold #cfcfcf]")
