import os
import re
import shutil
import subprocess
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console()

# label -> (nmap flags, needs_root)
PROFILES = {
    "1": ("Quick scan (top 100 ports)",      ["-T4", "-F"],                 False),
    "2": ("Default scan (top 1000 ports)",   ["-T4"],                       False),
    "3": ("Service / version detection",     ["-T4", "-sV"],                False),
    "4": ("Full TCP port range (1-65535)",   ["-T4", "-p-"],                False),
    "5": ("Aggressive (-A: OS, ver, scripts)", ["-T4", "-A"],               True),
    "6": ("SYN stealth scan (-sS)",          ["-T4", "-sS"],                True),
    "7": ("Ping sweep (host discovery, -sn)", ["-sn"],                      False),
}

TARGET_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9.\-:/]{0,127}$")


if __name__ == "__main__":
    try:
        console.print()
        console.print("  [#9aa0a6]> [bold #cfcfcf]nmap scan[/]")
        console.print("[#262626]  " + "─" * 48)
        console.print()

        if not shutil.which("nmap"):
            console.print("[bold #cfcfcf][!] nmap is not installed.[/bold #cfcfcf]")
            console.print("[dim]  install:  sudo pacman -S nmap[/dim]\n")
            raise SystemExit(0)

        table = Table(box=box.SIMPLE, border_style="#808080", header_style="bold #cfcfcf")
        table.add_column("#", style="bold #cfcfcf", width=3)
        table.add_column("Profile", style="white")
        table.add_column("Root", style="dim", width=6)
        for k, (label, _flags, root) in PROFILES.items():
            table.add_row(k, label, "yes" if root else "")
        console.print(table)
        console.print()

        choice = console.input("[bold #cfcfcf][=][/bold #cfcfcf] profile # >> ").strip()
        if choice not in PROFILES:
            console.print("[bold #cfcfcf][!] Invalid profile.[/bold #cfcfcf]")
            raise SystemExit(0)
        label, flags, needs_root = PROFILES[choice]

        target = console.input(
            "[bold #cfcfcf][=][/bold #cfcfcf] target (IP / host / CIDR) >> "
        ).strip()
        if not target or not TARGET_RE.match(target):
            console.print("[bold #cfcfcf][!] Invalid or empty target.[/bold #cfcfcf]")
            raise SystemExit(0)

        cmd = ["nmap"] + flags + [target]
        if needs_root and os.geteuid() != 0:
            if shutil.which("sudo"):
                console.print("[dim]  this profile needs root — prefixing sudo[/dim]")
                cmd = ["sudo"] + cmd
            else:
                console.print("[bold #cfcfcf][!] This profile needs root; re-run as root.[/bold #cfcfcf]")
                raise SystemExit(0)

        console.print()
        console.print(f"[dim]  $ {' '.join(cmd)}[/dim]\n")
        console.print("[bold #cfcfcf] ── nmap output "
                      "──────────────────────────────────────[/bold #cfcfcf]\n")
        subprocess.run(cmd)
        console.print("\n[bold #cfcfcf] ── end ─────────────────────────────────────────"
                      "──────[/bold #cfcfcf]")

    except (KeyboardInterrupt, EOFError):
        console.print("\n[bold #cfcfcf][!] Interrupted.[/bold #cfcfcf]")
