import re
import subprocess
import platform
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import box

console = Console()

IP_REGEX = re.compile(
    r'^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$'
)


def ping(ip, count=4):
    system = platform.system().lower()
    if system == "windows":
        cmd = ["ping", "-n", str(count), ip]
        encoding = "cp850"
    else:
        cmd = ["ping", "-c", str(count), ip]
        encoding = "utf-8"

    try:
        proc = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=30,
        )
        output = proc.stdout.decode(encoding, errors="replace")
        success = "TTL" in output or "ttl" in output or proc.returncode == 0
        return success, output
    except subprocess.TimeoutExpired:
        return False, "Timeout expired."
    except FileNotFoundError:
        return False, "Ping command not found."
    except Exception as e:
        return False, str(e)


if __name__ == "__main__":
    try:
        console.print()
        console.print("  [#9aa0a6]> [bold #cfcfcf]ip pinger[/]")
        console.print("[#262626]  " + "─" * 48)
        console.print()

        ip = console.input(
            "[bold #cfcfcf][[/bold #cfcfcf][bold white]=[/bold white][bold #cfcfcf]][/bold #cfcfcf] IP address to ping: "
        ).strip()

        if not ip:
            console.print("[bold #cfcfcf][!] Empty address. Cancelled.[/bold #cfcfcf]")
            raise SystemExit(0)

        if not IP_REGEX.match(ip):
            console.print(f"[bold #cfcfcf][!] Invalid IP format:[/bold #cfcfcf] {ip}")
            raise SystemExit(0)

        with Progress(
            SpinnerColumn(spinner_name="dots", style="bold #cfcfcf"),
            TextColumn("[bold white]{task.description}"),
            console=console, transient=True,
        ) as p:
            p.add_task(f"Pinging {ip}...", total=None)
            success, result = ping(ip)

        if success:
            console.print(Panel(
                f"[bold #cfcfcf]  Ping successful to {ip}[/bold #cfcfcf]",
                border_style="#808080", box=box.DOUBLE_EDGE,
            ))
        else:
            console.print(Panel(
                f"[bold #cfcfcf]  Ping failed to {ip}[/bold #cfcfcf]",
                border_style="#808080", box=box.DOUBLE_EDGE,
            ))

        console.print()
        console.print(f"[dim]{result}[/dim]")

    except (KeyboardInterrupt, EOFError):
        console.print("\n[bold #cfcfcf][!] Interrupted.[/bold #cfcfcf]")
