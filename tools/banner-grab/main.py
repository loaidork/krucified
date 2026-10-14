"""Banner grab — TCP connect to host:port and read the service banner."""
import re
import ssl
import socket
from rich.console import Console
from rich.panel import Panel
from rich import box

console = Console()
TIMEOUT = 6
HOST_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9.\-]{0,127}$")
TLS_PORTS = {443, 465, 993, 995, 8443}
HTTP_PORTS = {80, 8080, 8000, 8888, 443, 8443}


def header():
    console.print()
    console.print("  [#9aa0a6]> [bold #cfcfcf]banner grab[/]")
    console.print("[#262626]  " + "─" * 48)


if __name__ == "__main__":
    try:
        header()
        console.print()
        host = console.input("  [#9aa0a6][=][/#9aa0a6] host: ").strip()
        if not host or not HOST_RE.match(host):
            console.print("  [bold #cfcfcf][!] invalid or empty host.[/bold #cfcfcf]")
            raise SystemExit(0)
        try:
            port = int(console.input("  [#9aa0a6][=][/#9aa0a6] port: ").strip())
            assert 1 <= port <= 65535
        except (ValueError, AssertionError):
            console.print("  [bold #cfcfcf][!] invalid port.[/bold #cfcfcf]")
            raise SystemExit(0)

        try:
            sock = socket.create_connection((host, port), timeout=TIMEOUT)
        except (socket.gaierror, socket.timeout, ConnectionError, OSError) as e:
            console.print(f"  [bold #cfcfcf][!] connection failed: {e}[/bold #cfcfcf]")
            raise SystemExit(0)

        data = b""
        try:
            if port in TLS_PORTS:
                ctx = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                sock = ctx.wrap_socket(sock, server_hostname=host)
            sock.settimeout(TIMEOUT)
            if port in HTTP_PORTS:
                sock.sendall(f"HEAD / HTTP/1.0\r\nHost: {host}\r\n\r\n".encode())
            data = sock.recv(2048)
        except Exception:
            pass
        finally:
            try:
                sock.close()
            except Exception:
                pass

        text = data.decode("utf-8", "replace").strip() if data else ""
        console.print()
        console.print(Panel(
            (f"[#b8b8b8]{text}[/#b8b8b8]" if text else "[dim]no banner returned[/dim]"),
            title=f"[bold #cfcfcf]{host}:{port}[/bold #cfcfcf]",
            border_style="#808080", box=box.DOUBLE_EDGE, padding=(0, 1),
        ))
        console.print()
    except (KeyboardInterrupt, EOFError):
        console.print("\n  [#9aa0a6]> interrupted.[/#9aa0a6]")
