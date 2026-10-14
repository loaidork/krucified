"""CIDR / subnet calculator (fully local, stdlib ipaddress)."""
import ipaddress
from rich.console import Console
from rich.table import Table
from rich import box

console = Console()


def header():
    console.print()
    console.print("  [#9aa0a6]> [bold #cfcfcf]cidr calc[/]")
    console.print("[#262626]  " + "─" * 48)


if __name__ == "__main__":
    try:
        header()
        console.print("[dim]  ex: 192.168.1.0/24  ·  10.0.0.5/8  ·  2001:db8::/48[/dim]")
        console.print()
        raw = console.input("  [#9aa0a6][=][/#9aa0a6] cidr: ").strip()
        if not raw:
            console.print("  [bold #cfcfcf][!] empty.[/bold #cfcfcf]")
            raise SystemExit(0)
        try:
            net = ipaddress.ip_network(raw, strict=False)
        except ValueError as e:
            console.print(f"  [bold #cfcfcf][!] {e}[/bold #cfcfcf]")
            raise SystemExit(0)

        hosts = net.num_addresses - (2 if net.version == 4 and net.prefixlen < 31 else 0)
        hosts = max(hosts, 0)
        first = last = "—"
        it = net.hosts()
        try:
            first = str(next(it))
            last = str(list(net.hosts())[-1])
        except StopIteration:
            pass

        t = Table(
            title=f"[bold #cfcfcf]Subnet[/bold #cfcfcf] — [#f5f5f5]{net.with_prefixlen}[/#f5f5f5]",
            box=box.DOUBLE_EDGE, border_style="#808080", header_style="bold #cfcfcf", show_lines=True,
        )
        t.add_column("Field", style="bold #f5f5f5", width=18)
        t.add_column("Value", style="#b8b8b8")
        t.add_row("Version", f"IPv{net.version}")
        t.add_row("Network", str(net.network_address))
        t.add_row("Netmask", str(net.netmask))
        if net.version == 4:
            t.add_row("Wildcard", str(net.hostmask))
            t.add_row("Broadcast", str(net.broadcast_address))
        t.add_row("First host", first)
        t.add_row("Last host", last)
        t.add_row("Total addrs", f"{net.num_addresses:,}")
        t.add_row("Usable hosts", f"{hosts:,}")
        t.add_row("Private", "yes" if net.is_private else "no")
        console.print()
        console.print(t)
        console.print()
    except (KeyboardInterrupt, EOFError):
        console.print("\n  [#9aa0a6]> interrupted.[/#9aa0a6]")
