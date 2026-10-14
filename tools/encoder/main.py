"""Encoder / decoder — base64, hex, URL, ROT13 (fully local)."""
import base64
import codecs
import hashlib
import urllib.parse
from rich.console import Console
from rich.table import Table
from rich import box

console = Console()


def header():
    console.print()
    console.print("  [#9aa0a6]> [bold #cfcfcf]encoder / decoder[/]")
    console.print("[#262626]  " + "─" * 48)


def transform(op, text):
    b = text.encode("utf-8", "surrogatepass")
    if op == "1":  return base64.b64encode(b).decode()
    if op == "2":  return base64.b64decode(text + "=" * (-len(text) % 4)).decode("utf-8", "replace")
    if op == "3":  return b.hex()
    if op == "4":  return bytes.fromhex(text.strip().replace(" ", "")).decode("utf-8", "replace")
    if op == "5":  return urllib.parse.quote(text, safe="")
    if op == "6":  return urllib.parse.unquote(text)
    if op == "7":  return codecs.encode(text, "rot_13")
    if op == "8":  return hashlib.md5(b).hexdigest()
    if op == "9":  return hashlib.sha1(b).hexdigest()
    if op == "10": return hashlib.sha256(b).hexdigest()
    return None


OPS = [
    ("1", "base64 encode"), ("2", "base64 decode"),
    ("3", "hex encode"),    ("4", "hex decode"),
    ("5", "url encode"),    ("6", "url decode"),
    ("7", "rot13"),         ("8", "md5"),
    ("9", "sha1"),          ("10", "sha256"),
]


if __name__ == "__main__":
    try:
        header()
        t = Table(box=box.SIMPLE, border_style="#808080", header_style="bold #cfcfcf")
        t.add_column("#", style="bold #cfcfcf", width=3)
        t.add_column("op", style="#b8b8b8")
        for i in range(0, len(OPS), 2):
            a = OPS[i]; b = OPS[i + 1] if i + 1 < len(OPS) else ("", "")
            t.add_row(a[0], f"{a[1]:<16}" + (f"[#4d4d4d]{b[0]:>3}[/#4d4d4d]  {b[1]}" if b[0] else ""))
        console.print(t)

        op = console.input("  [#9aa0a6][=][/#9aa0a6] op #: ").strip()
        if op not in {o[0] for o in OPS}:
            console.print("  [bold #cfcfcf][!] invalid op.[/bold #cfcfcf]")
            raise SystemExit(0)
        text = console.input("  [#9aa0a6][=][/#9aa0a6] text: ")
        if not text:
            console.print("  [bold #cfcfcf][!] empty input.[/bold #cfcfcf]")
            raise SystemExit(0)

        try:
            out = transform(op, text)
        except Exception as e:
            console.print(f"  [bold #cfcfcf][!] transform failed: {e}[/bold #cfcfcf]")
            raise SystemExit(0)

        console.print()
        console.print("  [#b8b8b8]result:[/#b8b8b8]")
        console.print(f"  [bold #f5f5f5]{out}[/bold #f5f5f5]")
        console.print()
    except (KeyboardInterrupt, EOFError):
        console.print("\n  [#9aa0a6]> interrupted.[/#9aa0a6]")
