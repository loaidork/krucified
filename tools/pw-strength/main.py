"""Password strength analyzer — entropy + crack-time estimate. Fully local."""
import math
import getpass
from rich.console import Console
from rich import box
from rich.panel import Panel

console = Console()

COMMON = {
    "password", "123456", "123456789", "qwerty", "12345678", "111111",
    "1234567", "password1", "12345", "123123", "admin", "letmein",
    "welcome", "monkey", "iloveyou", "dragon", "sunshine", "princess",
    "football", "1234", "passw0rd", "root", "toor", "changeme",
}
# rough offline guesses/sec for a well-resourced attacker (slow hash budget)
GUESSES_PER_SEC = 1e10


def header():
    console.print()
    console.print("  [#9aa0a6]> [bold #cfcfcf]password strength[/]")
    console.print("[#262626]  " + "─" * 48)


def charset_size(pw):
    size = 0
    if any(c.islower() for c in pw): size += 26
    if any(c.isupper() for c in pw): size += 26
    if any(c.isdigit() for c in pw): size += 10
    if any(c in " !@#$%^&*()_+-=[]{}|;:,.<>?/~`'\"\\" for c in pw): size += 33
    return size or 1


def human_time(seconds):
    if seconds < 1:
        return "instant"
    units = [("years", 31557600), ("days", 86400), ("hours", 3600),
             ("minutes", 60), ("seconds", 1)]
    for name, size in units:
        if seconds >= size:
            v = seconds / size
            if name == "years" and v > 1e6:
                return f"{v/1e6:,.0f} million years"
            return f"{v:,.1f} {name}"
    return "instant"


def verdict(bits):
    if bits < 28:   return "very weak", "#808080"
    if bits < 36:   return "weak", "#9aa0a6"
    if bits < 60:   return "fair", "#b8b8b8"
    if bits < 128:  return "strong", "#e6e6e6"
    return "very strong", "#f5f5f5"


if __name__ == "__main__":
    try:
        header()
        console.print("[dim]  runs 100% offline — nothing is sent or stored[/dim]")
        console.print()
        try:
            pw = getpass.getpass("  [=] password (hidden): ")
        except Exception:
            pw = console.input("  [#9aa0a6][=][/#9aa0a6] password: ")
        if not pw:
            console.print("  [bold #cfcfcf][!] empty.[/bold #cfcfcf]")
            raise SystemExit(0)

        size = charset_size(pw)
        bits = len(pw) * math.log2(size)
        seconds = (2 ** bits) / GUESSES_PER_SEC / 2  # expected = half the space
        label, col = verdict(bits)

        notes = []
        if pw.lower() in COMMON:
            notes.append("appears in common-password lists — treat as cracked")
        if len(pw) < 12:
            notes.append("under 12 chars — extend it")
        if len(set(pw)) < len(pw) / 2:
            notes.append("many repeated characters")
        if pw.isalpha():
            notes.append("letters only — add digits & symbols")
        if pw.isdigit():
            notes.append("digits only — very low entropy")

        body = []
        body.append(f"[#808080]length     [/#808080][#b8b8b8]{len(pw)}[/#b8b8b8]")
        body.append(f"[#808080]charset    [/#808080][#b8b8b8]{size} symbols[/#b8b8b8]")
        body.append(f"[#808080]entropy    [/#808080][#b8b8b8]{bits:.1f} bits[/#b8b8b8]")
        body.append(f"[#808080]crack time [/#808080][#b8b8b8]{human_time(seconds)}[/#b8b8b8] [dim](@1e10/s)[/dim]")
        body.append(f"[#808080]verdict    [/#808080][bold {col}]{label.upper()}[/bold {col}]")
        console.print()
        console.print(Panel("\n".join(body), title="[bold #cfcfcf]analysis[/bold #cfcfcf]",
                            border_style="#808080", box=box.DOUBLE_EDGE, padding=(0, 1)))
        if notes:
            console.print()
            for n in notes:
                console.print(f"  [#9aa0a6]>[/#9aa0a6] [dim]{n}[/dim]")
        console.print()
    except (KeyboardInterrupt, EOFError):
        console.print("\n  [#9aa0a6]> interrupted.[/#9aa0a6]")
