import re
import socket
import shutil
import subprocess
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console()

RECORD_TYPES = ["A", "AAAA", "MX", "NS", "TXT", "CNAME", "SOA"]
DOMAIN_RE = re.compile(r"^[a-zA-Z0-9]([a-zA-Z0-9\-._]{0,251}[a-zA-Z0-9])?$")


def query_dig(domain, rtype):
    try:
        out = subprocess.run(
            ["dig", "+short", rtype, domain],
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=10,
        ).stdout.decode("utf-8", "replace")
        return [ln.strip() for ln in out.splitlines() if ln.strip()]
    except Exception:
        return []


def query_nslookup(domain, rtype):
    try:
        out = subprocess.run(
            ["nslookup", "-type=" + rtype, domain],
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=10,
        ).stdout.decode("utf-8", "replace")
        hits = []
        for ln in out.splitlines():
            ln = ln.strip()
            if any(k in ln for k in ("address:", "mail exchanger", "nameserver",
                                     "text =", "canonical name")):
                hits.append(ln.split("=")[-1].strip() if "=" in ln
                            else ln.split(":")[-1].strip())
        return hits
    except Exception:
        return []


def query_socket(domain, rtype):
    try:
        fam = socket.AF_INET6 if rtype == "AAAA" else socket.AF_INET
        if rtype in ("A", "AAAA"):
            infos = socket.getaddrinfo(domain, None, fam)
            return sorted({i[4][0] for i in infos})
    except Exception:
        pass
    return []


def resolve(domain, rtype):
    if shutil.which("dig"):
        return query_dig(domain, rtype)
    if shutil.which("nslookup"):
        return query_nslookup(domain, rtype)
    return query_socket(domain, rtype)


if __name__ == "__main__":
    try:
        console.print()
        console.print("  [#9aa0a6]> [bold #cfcfcf]dns lookup[/]")
        console.print("[#262626]  " + "─" * 48)
        console.print()

        if not (shutil.which("dig") or shutil.which("nslookup")):
            console.print("[dim]  note: dig/nslookup not found — falling back to A/AAAA only."
                          "\n  install:  sudo pacman -S bind[/dim]\n")

        domain = console.input(
            "[bold #cfcfcf][[/bold #cfcfcf][bold white]=[/bold white][bold #cfcfcf]][/bold #cfcfcf] Domain: "
        ).strip().rstrip(".")

        if not domain or not DOMAIN_RE.match(domain):
            console.print(f"[bold #cfcfcf][!] Invalid or empty domain.[/bold #cfcfcf]")
            raise SystemExit(0)

        table = Table(
            title=f"[bold #cfcfcf]DNS Records[/bold #cfcfcf] — [bold white]{domain}[/bold white]",
            box=box.DOUBLE_EDGE, border_style="#808080",
            header_style="bold #cfcfcf", show_lines=True,
        )
        table.add_column("Type", style="bold white", width=8)
        table.add_column("Records", style="#a8a8a8")

        for rtype in RECORD_TYPES:
            recs = resolve(domain, rtype)
            table.add_row(rtype, "\n".join(recs) if recs else "[dim]—[/dim]")

        console.print()
        console.print(table)
        console.print()

    except (KeyboardInterrupt, EOFError):
        console.print("\n[bold #cfcfcf][!] Interrupted.[/bold #cfcfcf]")
