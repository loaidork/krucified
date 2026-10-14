"""Identity / token generator — UUIDs, API keys, hex/base64 tokens. Local."""
import uuid
import secrets
import base64
from rich.console import Console

console = Console()


def header():
    console.print()
    console.print("  [#9aa0a6]> [bold #cfcfcf]id / token generator[/]")
    console.print("[#262626]  " + "─" * 48)


def line(label, value):
    console.print(f"  [#808080]{label:<14}[/#808080][bold #f5f5f5]{value}[/bold #f5f5f5]")


if __name__ == "__main__":
    try:
        header()
        console.print("[dim]  cryptographically-random values via `secrets` (local)[/dim]")
        console.print()

        console.print("  [bold #cfcfcf]uuids[/bold #cfcfcf]")
        line("uuid4", str(uuid.uuid4()))
        line("uuid4", str(uuid.uuid4()))
        line("uuid1 (time)", str(uuid.uuid1()))

        console.print()
        console.print("  [bold #cfcfcf]tokens[/bold #cfcfcf]")
        line("hex-16", secrets.token_hex(16))
        line("hex-32", secrets.token_hex(32))
        line("urlsafe-32", secrets.token_urlsafe(32))
        line("base64-24", base64.b64encode(secrets.token_bytes(24)).decode())

        console.print()
        console.print("  [bold #cfcfcf]keys[/bold #cfcfcf]")
        # api-key style: prefix + random body
        line("api-key", "sk_live_" + secrets.token_urlsafe(24))
        # bip39-ish numeric pin / otp
        line("numeric-pin", "".join(secrets.choice("0123456789") for _ in range(8)))
        # mac address (locally-administered, unicast)
        mac = [secrets.randbelow(256) for _ in range(6)]
        mac[0] = (mac[0] & 0xFE) | 0x02
        line("random-mac", ":".join(f"{b:02x}" for b in mac))
        console.print()
    except (KeyboardInterrupt, EOFError):
        console.print("\n  [#9aa0a6]> interrupted.[/#9aa0a6]")
