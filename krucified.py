#!/usr/bin/env python3
"""
 haiii loai here thank you for using krucified also feel 
 free to use this code however you please! after all if i didnt 
 want you to how could i stop you lol anyways enjoy!
"""
import os, sys, time, shutil, subprocess, webbrowser, random, string

from rich.console import Console
from rich.panel   import Panel
from rich.text    import Text
from rich.align   import Align
from rich         import box

console = Console(highlight=False)

C_DEEP   = "#262626"
C_DARK   = "#555555"
C_MID    = "#808080"
C_GREEN  = "#a0a0a0"
C_NEON   = "#cfcfcf"
C_BRIGHT = "#e6e6e6"
C_WHITE  = "#f5f5f5"
C_SILVER = "#b8b8b8"
C_DIM    = "#4d4d4d"
C_ACCENT = "#9aa0a6"
C_GT     = "#9aa0a6"

# EPIGRAMS act as like MOTDs for the tool, they are randomly selected from a list each time the program is run feel free to add your own epigrams to the list below
# Just make sure to keep them short and funny, they will be displayed in the header of the tool and remember to format them as strings in the list below, 
# each string should be enclosed in quotes and separated by commas god i feel like im explaining this to a 5 year old but whatever lol
EPIGRAMS = [
    "fockin skid",
    "is linux like the opsec thing?",
    "omigod guys im such an epic opsec hacker",
    "got root?",
    "Privacy is a human right",
    "nullsec is full of skids",
]
EPIGRAM = random.choice(EPIGRAMS)

HERE  = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.join(HERE, "LOGO_LINES")

# external binaries some modules use — shown in the header status bar
EXT_TOOLS = ["nmap", "tshark", "tcpdump", "dig", "traceroute", "mtr"]


def tool_path(name):
    return os.path.join(TOOLS, name, "main.py")

def cls():
    os.system("clear")

def tw():
    return shutil.get_terminal_size((100, 30)).columns

def th():
    return shutil.get_terminal_size((100, 30)).lines

 #to make a cool ascii art like this i would use https://patorjk.com tons of fonts

def jls_extract_def():
    # i really need to stop adding comments ;_:
    return 


LOGO_LINES = [
    r" ██   ███  ██████▒   ██    ██    ▒████▒   ██████   ████████   ██████   ████████  █████▒",
    r" ██  ▓██   ███████▓  ██    ██   ▓██████   ██████   ████████   ██████   ████████  ███████",
    r" ██ ▒██▒   ██   ▒██  ██    ██  ▒██▒  ░█     ██     ██           ██     ██        ██  ▒██▒",
    r" ██░██▒    ██    ██  ██    ██  ██▓          ██     ██           ██     ██        ██   ▒██",
    r" ████▒     ██   ▒██  ██    ██  ██░          ██     ██           ██     ██        ██   ░██",
    r" ███▓      ███████▒  ██    ██  ██           ██     ███████      ██     ███████   ██    ██",
    r" █████▒    ██████▓   ██    ██  ██           ██     ███████      ██     ███████   ██    ██", # yknow sometimes ascii in a multitool really makes me feel like a skid lol
    r" ██▒▒██    ██  ▓██░  ██    ██  ██░          ██     ██           ██     ██        ██   ░██",
    r" ██  ██▓   ██   ██▓  ██    ██  ██▓          ██     ██           ██     ██        ██   ▒██",
    r" ██  ▒██   ██   ▒██  ██▓  ▓██  ▒██▒  ░█     ██     ██           ██     ██        ██  ▒██▒",
    r" ██   ██▓  ██    ██▒ ▒██████▒   ▓██████   ██████   ██         ██████   ████████  ███████",
    r" ██   ▒██  ██    ███  ▒████▒     ▒████▒   ██████   ██         ██████   ████████  █████▒   by @loai on dc",
    r"                       Open sourced since 10/12/26 <3", 

] # i really need to stop adding comments ;_: = jls_extract_def()

VERSION = "1.2" # see guys python is easy asf


def draw_logo():
    if len(LOGO_LINES[0]) <= tw() - 1:
        for line in LOGO_LINES:
            console.print(Text(line, style=f"{C_MID} bold"))
    else:
        console.print(Text(" krucified", style=f"{C_MID} bold"))


def header_status(): # this is the status bar at the top of the menu, shows version, host, user, and which external binaries are present
    present = [t for t in EXT_TOOLS if shutil.which(t)]
    try:
        host = os.uname().nodename
    except Exception:
        host = "localhost"
    user = os.environ.get("USER") or "op"
    t = Text("  ")
    t.append("discord.gg/Qxs4eFe2Bv", style=C_DIM)
    t.append(f"  v{VERSION}", style=C_DARK)
    t.append("    bins ", style=C_DIM)
    t.append(" ".join(present) if present else "none", style=C_MID)
    miss = len(EXT_TOOLS) - len(present)
    if miss:
        t.append(f" (+{miss} missing)", style=C_DIM)
    t.append(f"    {user}@{host}", style=C_DARK)
    return t


def draw_header():
    cls()
    console.print()
    draw_logo()
    console.print(header_status())
    console.print(Text.from_markup(f"  [{C_GT}]> {EPIGRAM}"))
    console.print(f"[{C_DEEP}] " + "─" * (tw() - 2))


def make_cell(key, label):
    if not key.strip():
        return Text("")
    t = Text()
    t.append(key, style=f"{C_NEON} bold")
    t.append("  ", style=C_DIM)
    t.append(label, style=C_SILVER)
    return t


def _cell_len(key, label):
    return 0 if not key.strip() else len(key) + 2 + len(label)


def draw_tree(title, items):
    if title:
        console.print(Text.from_markup(f"  [{C_DIM}]{title}"))
    for e in items:
        kind = e[0]
        if kind == "cat":
            console.print()
            console.print(Text.from_markup(f"  [{C_MID} bold]{e[1]}"))
        elif kind == "cols":
            pairs = e[1]
            col_w = max(28, (tw() - 8) // 2)
            for j in range(0, len(pairs), 2):
                L = pairs[j]
                R = pairs[j + 1] if j + 1 < len(pairs) else None
                line = Text("    ")
                line.append_text(make_cell(*L))
                line.append(" " * max(2, col_w - _cell_len(*L)))
                if R:
                    line.append_text(make_cell(*R))
                console.print(line)
        elif kind in ("nav", "navlast"):
            console.print()
            console.print(Text.from_markup(
                f"  [{C_DIM}]▶ [{C_NEON} bold]{e[1]}[/] [{C_DIM}]{e[2]}"
            ))
    console.print()


def prompt(loc): # this is the prompt at the bottom of the menu edit as you please, just make sure to keep the ansi codes in there so it looks cool
    # ansi: bold ash "scriptkiddie" + dim "~>"
    raw = input("\033[1m\033[38;2;207;207;207mscriptkiddie\033[0m\033[38;2;77;77;77m ~>\033[0m ").strip()
    return raw


def show(loc, title, items):
    draw_header()
    draw_tree(title, items)
    return prompt(loc)


def run_tool(name):
    src = tool_path(name)
    if not os.path.exists(src):
        console.print(f"[{C_NEON} bold]  [!] module not found: {name}")
    else:
        try:
            subprocess.run([sys.executable, src])
        except Exception as exc:
            console.print(f"[{C_NEON} bold]  [!] error: {exc}")
    input("\033[38;2;77;77;77m  [enter]\033[0m")


def _ansi(h):
    hx = h.lstrip("#")
    r, g, b = int(hx[0:2], 16), int(hx[2:4], 16), int(hx[4:6], 16)
    return f"\033[38;2;{r};{g};{b}m"


def _panel(title, desc):
    console.print()
    console.print(Text.from_markup(
        f"  [{C_GT}]> [{C_MID} bold]{title.lower()}[{C_DIM}]  —  {desc}"))
    console.print(f"[{C_DEEP}]  " + "─" * (min(70, tw()) - 4))


def _open_links(pairs):
    for name, url in pairs:
        t = Text("    ")
        t.append(f"{name:<16}", style=C_SILVER)
        t.append(url, style=C_MID)
        console.print(t)
        try:
            webbrowser.open(url)
            time.sleep(0.05)
        except Exception:
            pass
    console.print()
    input("\033[38;2;77;77;77m  [enter]\033[0m")


# inline tools that are just a bunch of links to public services, no local binaries needed
def tool_username_hunter():
    _panel("USERNAME HUNTER", "Check a username across public platforms")
    u = input(f"{_ansi(C_MID)}  username >> \033[0m").strip()
    if not u:
        return
    console.print(Text.from_markup(f"[{C_MID} bold]  Results for : {u}"))
    _open_links([
        ("GitHub",    f"https://github.com/{u}"),
        ("Twitter/X", f"https://x.com/{u}"),
        ("Instagram", f"https://instagram.com/{u}"),
        ("TikTok",    f"https://tiktok.com/@{u}"),
        ("Reddit",    f"https://reddit.com/u/{u}"),
        ("Twitch",    f"https://twitch.tv/{u}"),
        ("YouTube",   f"https://youtube.com/@{u}"),
        ("Steam",     f"https://steamcommunity.com/id/{u}"),
        ("Medium",    f"https://medium.com/@{u}"),
        ("Telegram",  f"https://t.me/{u}"),
    ])


def tool_domain_intel():
    _panel("DOMAIN INTEL", "WHOIS · DNS · SSL · Shodan · VirusTotal")
    d = input(f"{_ansi(C_MID)}  domain (ex: example.com) >> \033[0m").strip()
    if not d:
        return
    console.print(Text.from_markup(f"[{C_MID} bold]  Intel for : {d}"))
    _open_links([
        ("WHOIS",      f"https://who.is/whois/{d}"),
        ("DNS Lookup", f"https://dnschecker.org/#A/{d}"),
        ("Subdomains", f"https://subdomainfinder.c99.nl/?domain={d}"),
        ("SSL Cert",   f"https://crt.sh/?q={d}"),
        ("VirusTotal", f"https://virustotal.com/gui/domain/{d}"),
        ("Shodan",     f"https://shodan.io/search?query=hostname%3A{d}"),
        ("URLScan",    f"https://urlscan.io/search/#domain%3A{d}"),
    ])


def tool_vpn_detector():
    _panel("VPN / PROXY DETECTOR", "Check VPN · Proxy · Tor · abuse history on an IP")
    ip = input(f"{_ansi(C_MID)}  IP address >> \033[0m").strip()
    if not ip:
        return
    console.print(Text.from_markup(f"[{C_MID} bold]  VPN Check : {ip}"))
    _open_links([
        ("IPQualityScore", f"https://ipqualityscore.com/free-ip-lookup-proxy-vpn-test/lookup/{ip}"),
        ("IPHub",          f"https://iphub.info/ip/{ip}"),
        ("AbuseIPDB",      f"https://abuseipdb.com/check/{ip}"),
        ("Shodan",         f"https://shodan.io/host/{ip}"),
        ("GreyNoise",      f"https://viz.greynoise.io/ip/{ip}"),
    ])


def tool_hash_lookup():
    _panel("HASH LOOKUP", "Reverse MD5 · SHA1 · SHA256 via online rainbow tables")
    h = input(f"{_ansi(C_MID)}  hash >> \033[0m").strip()
    if not h:
        return
    console.print(Text.from_markup(f"[{C_MID} bold]  Hash : {h[:40]}{'...' if len(h) > 40 else ''}"))
    _open_links([
        ("CrackStation", "https://crackstation.net/"),
        ("Hashes.com",   "https://hashes.com/en/decrypt/hash"),
        ("MD5Decrypt",   "https://md5decrypt.net/"),
    ])


def tool_password_gen():
    _panel("PASSWORD GENERATOR", "Generate strong random passwords")
    try:
        length = int(input(f"{_ansi(C_MID)}  length (default 20) >> \033[0m").strip() or "20")
    except ValueError:
        length = 20
    length = max(4, min(length, 256))
    charset = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?"
    rng = random.SystemRandom()
    console.print()
    console.print(Text.from_markup(f"[{C_MID} bold]  8 passwords  ·  length {length}"))
    for i in range(8):
        pwd = ''.join(rng.choices(charset, k=length))
        t = Text()
        t.append(f" │   [{i + 1:02d}] ", style=C_DEEP)
        t.append(pwd, style=f"{C_WHITE} bold")
        console.print(t)
    console.print()
    input("\033[38;2;77;77;77m  [enter]\033[0m")


def tool_temp_mail():
    _panel("TEMP MAIL", "Disposable inbox services")
    console.print(Text.from_markup(f"[{C_MID} bold]  Temp Mail Services"))
    _open_links([
        ("10MinuteMail",   "https://10minutemail.com/"),
        ("Guerrilla Mail", "https://guerrillamail.com/"),
        ("TempMail",       "https://temp-mail.org/"),
    ])


# the main menu deck, each entry is either a category or a row of two tools
DECK = [
    ("cat", "osint"),
    ("cols", [
        ("01", "doxbin"), ("02", "ip lookup"),
        ("03", "ip geolocation"),  ("04", "ip operator / asn"),
        ("05", "reverse dns"),     ("06", "dns records"),
        ("07", "dns-over-https"),  ("08", "domain intel"),
        ("09", "subdomain enum"),  ("10", "whois"),
        ("11", "asn lookup"),      ("12", "email validator"),
        ("13", "username hunter"), ("  ", ""),
    ]),
    ("cat", "network and like portscanning"),
    ("cols", [
        ("14", "web lookup (full)"), ("15", "open ports scan"),
        ("16", "nmap scan"),         ("17", "ip pinger"),
        ("18", "traceroute"),        ("19", "packet capture"),
        ("20", "lan sweep"),         ("21", "banner grab"),
        ("22", "network info"),      ("23", "vpn / proxy check"),
    ]),
    ("cat", "interwebs tools"),
    ("cols", [
        ("24", "http headers"),     ("25", "ssl / tls info"),
        ("26", "url expander"),     ("27", "tech fingerprint"),
        ("28", "robots / sitemap"), ("29", "wayback machine"),
    ]),
    ("cat", "general utils"),
    ("cols", [
        ("30", "mac vendor lookup"),  ("31", "hash lookup"),
        ("32", "hash identifier"),    ("33", "encoder / decoder"),
        ("34", "cidr calc"),          ("35", "jwt decoder"),
        ("36", "epoch converter"),    ("37", "id / token gen"),
        ("38", "password strength"),  ("39", "password generator"),
        ("40", "temp mail"),          ("41", "breach self-check"),
    ]),
    ("navlast", "Q", "quit"),
]

ACTIONS = {
    "01": lambda: webbrowser.open("https://doxbin.com/"),
    "02": lambda: run_tool("ip-lookup"),
    "03": lambda: run_tool("ip-localisation"),
    "04": lambda: run_tool("ip-operator"),
    "05": lambda: run_tool("reverse-dns"),
    "06": lambda: run_tool("dns-lookup"),
    "07": lambda: run_tool("dns-doh"),
    "08": tool_domain_intel,
    "09": lambda: run_tool("subdomain-enum"),
    "10": lambda: run_tool("whois"),
    "11": lambda: run_tool("asn-lookup"),
    "12": lambda: run_tool("email-check"),
    "13": tool_username_hunter,
    "14": lambda: run_tool("ip-all-lookup"),
    "15": lambda: run_tool("ip-open-ports"),
    "16": lambda: run_tool("nmap-scan"),
    "17": lambda: run_tool("ip-pinger"),
    "18": lambda: run_tool("traceroute"),
    "19": lambda: run_tool("packet-capture"),
    "20": lambda: run_tool("lan-sweep"),
    "21": lambda: run_tool("banner-grab"),
    "22": lambda: run_tool("net-info"),
    "23": tool_vpn_detector,
    "24": lambda: run_tool("http-headers"),
    "25": lambda: run_tool("ssl-info"),
    "26": lambda: run_tool("url-expander"),
    "27": lambda: run_tool("tech-detect"),
    "28": lambda: run_tool("robots-recon"),
    "29": lambda: run_tool("wayback"),
    "30": lambda: run_tool("mac-lookup"),
    "31": tool_hash_lookup,
    "32": lambda: run_tool("hash-id"),
    "33": lambda: run_tool("encoder"),
    "34": lambda: run_tool("cidr-calc"),
    "35": lambda: run_tool("jwt-decode"),
    "36": lambda: run_tool("epoch"),
    "37": lambda: run_tool("gen-id"),
    "38": lambda: run_tool("pw-strength"),
    "39": tool_password_gen,
    "40": tool_temp_mail,
    "41": lambda: run_tool("breach-check"),
}


def main_menu():
    while True:
        o = show("krx", "select ur tool skid", DECK)
        s = o.strip()
        if s.upper() == "Q":
            cls()
            console.print(f"[{C_GT}]  > baiii\n")
            sys.exit(0)
        action = ACTIONS.get(s.zfill(2) if s.isdigit() else s.upper())
        if action:
            action()
        # unknown input just redraws the deck


if __name__ == "__main__":
    try:
        sys.stdout.write("\x1b]2;krucified\x07")
        main_menu()
    except (KeyboardInterrupt, EOFError):
        console.print(f"\n[{C_GT}]  > cya later!")
        sys.exit(0) 
