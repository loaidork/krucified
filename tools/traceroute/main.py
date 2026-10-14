import re
import shutil
import subprocess
from rich.console import Console
from rich.panel import Panel
from rich import box

console = Console()
TARGET_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9.\-:]{0,127}$")


if __name__ == "__main__":
    try:
        console.print()
        console.print("  [#9aa0a6]> [bold #cfcfcf]traceroute[/]")
        console.print("[#262626]  " + "─" * 48)
        console.print()

        tool = None
        for cand in ("traceroute", "tracepath", "mtr"):
            if shutil.which(cand):
                tool = cand
                break
        if not tool:
            console.print("[bold #cfcfcf][!] No traceroute tool found.[/bold #cfcfcf]")
            console.print("[dim]  install:  sudo pacman -S traceroute   (or)  mtr[/dim]\n")
            raise SystemExit(0)
        console.print(f"[dim]  engine: {tool}[/dim]")

        target = console.input("[bold #cfcfcf][=][/bold #cfcfcf] target (IP / host) >> ").strip()
        if not target or not TARGET_RE.match(target):
            console.print("[bold #cfcfcf][!] Invalid or empty target.[/bold #cfcfcf]")
            raise SystemExit(0)

        if tool == "mtr":
            cmd = ["mtr", "--report", "--report-cycles", "5", target]
        else:
            cmd = [tool, target]

        console.print()
        console.print(f"[dim]  $ {' '.join(cmd)}[/dim]\n")
        subprocess.run(cmd)
        console.print()

    except (KeyboardInterrupt, EOFError):
        console.print("\n[bold #cfcfcf][!] Interrupted.[/bold #cfcfcf]")
