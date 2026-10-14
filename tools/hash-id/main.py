"""Hash identifier — guesses the algorithm of a hash by shape (fully local)."""
import re
from rich.console import Console
from rich.table import Table
from rich import box

console = Console()

# (regex, candidate algorithms) — ordered, most specific first
PATTERNS = [
    (re.compile(r"^[a-f0-9]{32}$", re.I),            ["MD5", "NTLM", "MD4", "LM-half"]),
    (re.compile(r"^[a-f0-9]{40}$", re.I),            ["SHA-1", "RIPEMD-160"]),
    (re.compile(r"^[a-f0-9]{56}$", re.I),            ["SHA-224", "SHA3-224"]),
    (re.compile(r"^[a-f0-9]{64}$", re.I),            ["SHA-256", "SHA3-256", "BLAKE2s"]),
    (re.compile(r"^[a-f0-9]{96}$", re.I),            ["SHA-384", "SHA3-384"]),
    (re.compile(r"^[a-f0-9]{128}$", re.I),           ["SHA-512", "SHA3-512", "BLAKE2b", "Whirlpool"]),
    (re.compile(r"^\$2[aby]\$\d{2}\$[./A-Za-z0-9]{53}$"), ["bcrypt"]),
    (re.compile(r"^\$1\$[./A-Za-z0-9]{1,8}\$[./A-Za-z0-9]{22}$"), ["md5crypt"]),
    (re.compile(r"^\$5\$"),                          ["sha256crypt"]),
    (re.compile(r"^\$6\$"),                          ["sha512crypt"]),
    (re.compile(r"^\$y\$"),                          ["yescrypt"]),
    (re.compile(r"^\$argon2(id|i|d)\$"),             ["Argon2"]),
    (re.compile(r"^[a-f0-9]{16}$", re.I),            ["MySQL<4.1", "CRC64"]),
    (re.compile(r"^\*[A-F0-9]{40}$"),                ["MySQL 4.1+ (SHA1(SHA1(pw)))"]),
    (re.compile(r"^{SHA}[A-Za-z0-9+/]{27}=$"),       ["LDAP SHA-1 (base64)"]),
]


def header():
    console.print()
    console.print("  [#9aa0a6]> [bold #cfcfcf]hash identifier[/]")
    console.print("[#262626]  " + "─" * 48)


if __name__ == "__main__":
    try:
        header()
        console.print()
        h = console.input("  [#9aa0a6][=][/#9aa0a6] hash: ").strip()
        if not h:
            console.print("  [bold #cfcfcf][!] empty.[/bold #cfcfcf]")
            raise SystemExit(0)

        matches = []
        for rx, algos in PATTERNS:
            if rx.match(h):
                matches.extend(algos)

        t = Table(
            title=f"[bold #cfcfcf]Hash ID[/bold #cfcfcf] — [#b8b8b8]{len(h)} chars[/#b8b8b8]",
            box=box.DOUBLE_EDGE, border_style="#808080", header_style="bold #cfcfcf", show_lines=False,
        )
        t.add_column("Possible algorithm", style="#b8b8b8")
        if matches:
            for m in matches:
                t.add_row(m)
        else:
            t.add_row("[dim]no match — unusual length or encoding[/dim]")

        console.print()
        console.print(t)
        console.print()
    except (KeyboardInterrupt, EOFError):
        console.print("\n  [#9aa0a6]> interrupted.[/#9aa0a6]")
