"""Email validator — syntax check + MX / domain resolution (deliverability hint)."""
import re
import socket
import subprocess
import shutil
from rich.console import Console

console = Console()
SYNTAX = re.compile(r"^[A-Za-z0-9._%+\-]+@([A-Za-z0-9.\-]+\.[A-Za-z]{2,})$")


def header():
    console.print()
    console.print("  [#9aa0a6]> [bold #cfcfcf]email validator[/]")
    console.print("[#262626]  " + "─" * 48)


def mx_records(domain):
    """Return list of MX hosts using `dig` if present, else none."""
    if shutil.which("dig"):
        try:
            out = subprocess.run(["dig", "+short", "MX", domain],
                                 capture_output=True, text=True, timeout=10).stdout
            return [l.split()[-1].rstrip(".") for l in out.splitlines() if l.strip()]
        except Exception:
            return []
    return []


if __name__ == "__main__":
    try:
        header()
        console.print()
        email = console.input("  [#9aa0a6][=][/#9aa0a6] email: ").strip()
        if not email:
            console.print("  [bold #cfcfcf][!] empty.[/bold #cfcfcf]")
            raise SystemExit(0)

        m = SYNTAX.match(email)
        console.print()
        ok = "[#f5f5f5]valid[/#f5f5f5]" if m else "[bold #cfcfcf]INVALID[/bold #cfcfcf]"
        console.print(f"  [#808080]syntax     [/#808080]{ok}")
        if not m:
            console.print()
            raise SystemExit(0)

        domain = m.group(1)
        console.print(f"  [#808080]domain     [/#808080][#b8b8b8]{domain}[/#b8b8b8]")

        # domain resolves?
        try:
            ip = socket.gethostbyname(domain)
            console.print(f"  [#808080]resolves   [/#808080][#b8b8b8]{ip}[/#b8b8b8]")
        except OSError:
            console.print(f"  [#808080]resolves   [/#808080][bold #cfcfcf]no A record[/bold #cfcfcf]")

        mx = mx_records(domain)
        if mx:
            console.print(f"  [#808080]mx hosts   [/#808080][#f5f5f5]{len(mx)}[/#f5f5f5] [dim](can receive mail)[/dim]")
            for h in mx[:8]:
                console.print(f"    [#9aa0a6]>[/#9aa0a6] [#b8b8b8]{h}[/#b8b8b8]")
        elif shutil.which("dig"):
            console.print(f"  [#808080]mx hosts   [/#808080][dim]none — domain likely can't receive mail[/dim]")
        else:
            console.print(f"  [#808080]mx hosts   [/#808080][dim]install `dig` (bind) for MX lookup[/dim]")
        console.print()
        console.print("  [dim]  note: syntax+MX only — does not prove the mailbox exists.[/dim]")
        console.print()
    except (KeyboardInterrupt, EOFError):
        console.print("\n  [#9aa0a6]> interrupted.[/#9aa0a6]")
