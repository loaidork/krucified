"""JWT decoder — decodes header & payload (no signature verification). Local."""
import json
import base64
from datetime import datetime, timezone
from rich.console import Console
from rich.panel import Panel
from rich import box

console = Console()
TIME_CLAIMS = {"exp": "expires", "iat": "issued at", "nbf": "not before"}


def header():
    console.print()
    console.print("  [#9aa0a6]> [bold #cfcfcf]jwt decoder[/]")
    console.print("[#262626]  " + "─" * 48)


def b64url(seg):
    seg += "=" * (-len(seg) % 4)
    return base64.urlsafe_b64decode(seg.encode())


def show(title, obj):
    body = json.dumps(obj, indent=2, ensure_ascii=False)
    console.print(Panel(
        f"[#b8b8b8]{body}[/#b8b8b8]",
        title=f"[bold #cfcfcf]{title}[/bold #cfcfcf]",
        border_style="#808080", box=box.DOUBLE_EDGE, padding=(0, 1),
    ))


if __name__ == "__main__":
    try:
        header()
        console.print("[dim]  signature is NOT verified — decode only[/dim]")
        console.print()
        token = console.input("  [#9aa0a6][=][/#9aa0a6] jwt: ").strip()
        parts = token.split(".")
        if len(parts) < 2:
            console.print("  [bold #cfcfcf][!] not a JWT (need header.payload.signature).[/bold #cfcfcf]")
            raise SystemExit(0)

        try:
            hdr = json.loads(b64url(parts[0]))
            pay = json.loads(b64url(parts[1]))
        except Exception as e:
            console.print(f"  [bold #cfcfcf][!] decode failed: {e}[/bold #cfcfcf]")
            raise SystemExit(0)

        console.print()
        show("header", hdr)
        show("payload", pay)

        for claim, label in TIME_CLAIMS.items():
            if isinstance(pay.get(claim), (int, float)):
                ts = datetime.fromtimestamp(pay[claim], tz=timezone.utc)
                note = ""
                if claim == "exp":
                    note = "  [dim](EXPIRED)[/dim]" if ts < datetime.now(timezone.utc) else "  [dim](valid)[/dim]"
                console.print(f"  [#808080]{label:<10}[/#808080][#b8b8b8]{ts:%Y-%m-%d %H:%M:%S UTC}[/#b8b8b8]{note}")
        console.print()
    except (KeyboardInterrupt, EOFError):
        console.print("\n  [#9aa0a6]> interrupted.[/#9aa0a6]")
