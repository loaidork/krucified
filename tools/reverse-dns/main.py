import re
import socket
from rich.console import Console
from rich.table import Table
from rich import box

console = Console()
IP_RE = re.compile(r'^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')


def header():
    console.print()
    console.print("  [#9aa0a6]> [bold #cfcfcf]reverse dns[/]")
    console.print("[#262626]  " + "─" * 48)


if __name__ == "__main__":
    try:
        header()
        console.print()
        ip = console.input("  [#9aa0a6][=][/#9aa0a6] IP address: ").strip()
        if not ip or not IP_RE.match(ip):
            console.print("  [bold #cfcfcf][!] invalid or empty IP.[/bold #cfcfcf]")
            raise SystemExit(0)

        table = Table(
            title=f"[bold #cfcfcf]Reverse DNS[/bold #cfcfcf] — [#f5f5f5]{ip}[/#f5f5f5]",
            box=box.DOUBLE_EDGE, border_style="#808080",
            header_style="bold #cfcfcf", show_lines=True,
        )
        table.add_column("Field", style="bold #f5f5f5", width=14)
        table.add_column("Value", style="#b8b8b8")
        try:
            host, aliases, addrs = socket.gethostbyaddr(ip)
            table.add_row("PTR", host)
            table.add_row("Aliases", ", ".join(aliases) if aliases else "[dim]—[/dim]")
            table.add_row("Addresses", ", ".join(addrs))
        except socket.herror:
            table.add_row("PTR", "[dim]no record[/dim]")
        except socket.gaierror as e:
            table.add_row("error", str(e))

        console.print()
        console.print(table)
        console.print()
    except (KeyboardInterrupt, EOFError):
        console.print("\n  [#9aa0a6]> interrupted.[/#9aa0a6]")
