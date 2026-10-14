"""Timestamp converter — unix epoch <-> human time, any timezone. Local."""
from datetime import datetime, timezone
from rich.console import Console

console = Console()


def header():
    console.print()
    console.print("  [#9aa0a6]> [bold #cfcfcf]epoch converter[/]")
    console.print("[#262626]  " + "─" * 48)


def line(label, value):
    console.print(f"  [#808080]{label:<16}[/#808080][#b8b8b8]{value}[/#b8b8b8]")


def show_epoch(ts):
    # auto-detect ms / s
    if ts > 1e12:
        ts = ts / 1000.0
    dt_utc = datetime.fromtimestamp(ts, tz=timezone.utc)
    dt_local = datetime.fromtimestamp(ts)
    console.print()
    line("epoch (s)", f"{ts:.0f}")
    line("utc", dt_utc.strftime("%Y-%m-%d %H:%M:%S UTC"))
    line("local", dt_local.strftime("%Y-%m-%d %H:%M:%S %Z").strip())
    line("iso-8601", dt_utc.isoformat())
    line("weekday", dt_utc.strftime("%A"))
    delta = datetime.now(timezone.utc) - dt_utc
    rel = "in the future" if delta.total_seconds() < 0 else "ago"
    line("relative", f"{abs(delta).days} days {rel}")


if __name__ == "__main__":
    try:
        header()
        now = datetime.now(timezone.utc)
        console.print(f"[dim]  now: {int(now.timestamp())}  ·  {now:%Y-%m-%d %H:%M:%S UTC}[/dim]")
        console.print("[dim]  enter a unix timestamp, or blank for current time[/dim]")
        console.print()
        raw = console.input("  [#9aa0a6][=][/#9aa0a6] epoch: ").strip()
        if not raw:
            show_epoch(now.timestamp())
            console.print()
            raise SystemExit(0)
        try:
            show_epoch(float(raw))
        except ValueError:
            # maybe a date string
            parsed = None
            for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d", "%Y/%m/%d", "%d-%m-%Y"):
                try:
                    parsed = datetime.strptime(raw, fmt).replace(tzinfo=timezone.utc)
                    break
                except ValueError:
                    continue
            if parsed:
                show_epoch(parsed.timestamp())
            else:
                console.print("  [bold #cfcfcf][!] not a timestamp or recognizable date.[/bold #cfcfcf]")
        console.print()
    except (KeyboardInterrupt, EOFError):
        console.print("\n  [#9aa0a6]> interrupted.[/#9aa0a6]")
