"""TLS certificate inspector — connects to host:port and shows the cert."""
import ssl
import socket
from datetime import datetime, timezone
from rich.console import Console
from rich.table import Table
from rich import box

console = Console()
TIMEOUT = 10


def header():
    console.print()
    console.print("  [#9aa0a6]> [bold #cfcfcf]ssl / tls info[/]")
    console.print("[#262626]  " + "─" * 48)


def name_tuple(seq):
    out = {}
    for rdn in seq or ():
        for k, v in rdn:
            out[k] = v
    return out


if __name__ == "__main__":
    try:
        header()
        console.print()
        host = console.input("  [#9aa0a6][=][/#9aa0a6] host (ex: example.com): ").strip()
        if not host:
            console.print("  [bold #cfcfcf][!] empty host.[/bold #cfcfcf]")
            raise SystemExit(0)
        port_raw = console.input("  [#9aa0a6][=][/#9aa0a6] port (default 443): ").strip()
        try:
            port = int(port_raw) if port_raw else 443
        except ValueError:
            port = 443

        ctx = ssl.create_default_context()
        try:
            with socket.create_connection((host, port), timeout=TIMEOUT) as sock:
                with ctx.wrap_socket(sock, server_hostname=host) as ss:
                    cert = ss.getpeercert()
                    proto = ss.version()
                    cipher = ss.cipher()
        except ssl.SSLCertVerificationError as e:
            console.print(f"  [bold #cfcfcf][!] certificate verify failed:[/bold #cfcfcf] {e.verify_message}")
            raise SystemExit(0)
        except (socket.gaierror, socket.timeout, ConnectionError, OSError) as e:
            console.print(f"  [bold #cfcfcf][!] connection error: {e}[/bold #cfcfcf]")
            raise SystemExit(0)

        subj = name_tuple(cert.get("subject"))
        issuer = name_tuple(cert.get("issuer"))
        fmt = "%b %d %H:%M:%S %Y %Z"
        not_after = cert.get("notAfter", "")
        days_left = "?"
        try:
            exp = datetime.strptime(not_after, fmt).replace(tzinfo=timezone.utc)
            days_left = (exp - datetime.now(timezone.utc)).days
        except Exception:
            pass
        sans = [v for k, v in cert.get("subjectAltName", ()) if k == "DNS"]

        t = Table(
            title=f"[bold #cfcfcf]TLS Certificate[/bold #cfcfcf] — [#f5f5f5]{host}:{port}[/#f5f5f5]",
            box=box.DOUBLE_EDGE, border_style="#808080", header_style="bold #cfcfcf", show_lines=True,
        )
        t.add_column("Field", style="bold #f5f5f5", width=18)
        t.add_column("Value", style="#b8b8b8")
        t.add_row("Protocol", f"{proto}  ({cipher[0] if cipher else '?'})")
        t.add_row("Subject CN", subj.get("commonName", "—"))
        t.add_row("Issuer", issuer.get("commonName", issuer.get("organizationName", "—")))
        t.add_row("Valid from", cert.get("notBefore", "—"))
        t.add_row("Valid until", f"{not_after}   ([#b8b8b8]{days_left} days left[/#b8b8b8])")
        t.add_row("Serial", str(cert.get("serialNumber", "—")))
        t.add_row("SAN", ", ".join(sans) if sans else "—")

        console.print()
        console.print(t)
        console.print()
    except (KeyboardInterrupt, EOFError):
        console.print("\n  [#9aa0a6]> interrupted.[/#9aa0a6]")
