"""WHOIS lookup — wraps the system `whois` binary."""
import re
import shutil
import subprocess
from rich.console import Console

console = Console()
TARGET_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9.\-:]{0,127}$")


def header():
    console.print()
    console.print("  [#9aa0a6]> [bold #cfcfcf]whois[/]")
    console.print("[#262626]  " + "─" * 48)


if __name__ == "__main__":
    try:
        header()
        console.print()
        if not shutil.which("whois"):
            console.print("  [bold #cfcfcf][!] whois is not installed.[/bold #cfcfcf]")
            console.print("[dim]  install:  sudo pacman -S whois[/dim]\n")
            raise SystemExit(0)

        target = console.input("  [#9aa0a6][=][/#9aa0a6] domain or IP: ").strip()
        if not target or not TARGET_RE.match(target):
            console.print("  [bold #cfcfcf][!] invalid or empty target.[/bold #cfcfcf]")
            raise SystemExit(0)

        console.print(f"[dim]  $ whois {target}[/dim]")
        console.print("[#262626]  " + "─" * 48)
        try:
            out = subprocess.run(
                ["whois", target], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=30,
            ).stdout.decode("utf-8", "replace")
        except subprocess.TimeoutExpired:
            console.print("  [bold #cfcfcf][!] whois timed out.[/bold #cfcfcf]")
            raise SystemExit(0)

        for line in out.splitlines():
            s = line.strip()
            if not s or s.startswith(("%", "#", ">>>")):
                console.print(f"[dim]{line}[/dim]")
            elif ":" in s and not s.startswith("http"):
                k, _, v = line.partition(":")
                console.print(f"[#808080]{k}:[/#808080][#b8b8b8]{v}[/#b8b8b8]")
            else:
                console.print(f"[#b8b8b8]{line}[/#b8b8b8]")
        console.print()
    except (KeyboardInterrupt, EOFError):
        console.print("\n  [#9aa0a6]> interrupted.[/#9aa0a6]")
