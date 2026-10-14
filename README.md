# krucified

An OSINT & network-reconnaissance toolkit for Linux, with an ashy-gray terminal UI.

This is a clean-room rewrite — not a repackaged leak. There is no installer that
phones home, no auto-opened chat invites, no bundled bot, and no obfuscated code.
Every module is plain, readable Python you can audit before running.

## Modules (41)

**recon**
- OSINT Framework (link)
- IP Lookup — geolocation / org / ASN via ipinfo
- IP Geolocation — geo via ip-api
- IP Operator / ASN
- Reverse DNS — PTR lookup for an IP
- DNS Records — A/AAAA/MX/NS/TXT/CNAME/SOA (`dig`/`nslookup`, socket fallback)
- DNS-over-HTTPS — encrypted resolve via Cloudflare / Google DoH endpoints
- Domain Intel — WHOIS, DNS, subdomains, SSL (crt.sh), VirusTotal, Shodan, URLScan
- Subdomain Enum — passive, via crt.sh certificate-transparency logs
- WHOIS — wraps the system `whois` binary
- ASN Lookup — autonomous-system / prefix intel via RIPEstat (ASN or IP)
- Email Validator — syntax check + domain resolve + MX records
- Username Hunter — opens a username's public profile pages across platforms

**network** (authorized targets only)
- Web Lookup (full) — DNS resolve, HTTP status, geo, common-port scan
- Open Ports Scan — TCP connect scan of common ports
- Nmap Scan — profiles: quick, default, version, full-range, aggressive (-A),
  SYN stealth (-sS), ping sweep; auto-prefixes `sudo` for root-only profiles
- IP Pinger — ICMP ping (cross-platform)
- Traceroute — `traceroute` / `tracepath` / `mtr`
- Packet Capture — tshark (Wireshark CLI) or tcpdump; interface, count, BPF filter
- LAN Sweep — ARP/neighbour cache + optional nmap ping sweep of the local subnet
- Banner Grab — TCP (and TLS) connect to host:port, read the service banner
- Network Info — local interfaces, default route, hostname, public IP
- VPN / Proxy Detector — IPQS, IPHub, AbuseIPDB, Shodan, GreyNoise

**web / tls**
- HTTP Headers — status, redirect chain, response headers, security-header audit
- SSL / TLS Info — certificate issuer, validity, expiry countdown, SANs, protocol
- URL Expander — follows the redirect chain of a shortened link
- Tech Fingerprint — guess server / CMS / framework from headers, cookies & body
- Robots / Sitemap Recon — fetch robots.txt, list disallows, enumerate sitemaps
- Wayback Machine — archive history, oldest & newest snapshot, closest capture

**crypto / utils**
- MAC Vendor Lookup — OUI → vendor via macvendors API
- Hash Lookup — reverse MD5/SHA1/SHA256 via online tables
- Hash Identifier — guess the algorithm by shape (fully local)
- Encoder / Decoder — base64, hex, URL, ROT13, md5/sha1/sha256 (fully local)
- CIDR Calc — subnet math: network, broadcast, host range, counts (fully local)
- JWT Decoder — decode header & payload, flag expiry (no signature verify, local)
- Epoch Converter — unix timestamp ↔ UTC/local/ISO, relative age (fully local)
- ID / Token Generator — UUIDs, hex/base64/urlsafe tokens, API keys, MAC (local)
- Password Strength — entropy + crack-time estimate, hidden input (fully local)
- Password Generator — strong random passwords (uses `SystemRandom`)
- Temp Mail — disposable inbox links
- Breach Self-Check — password check via HIBP k-anonymity (only the first 5 chars of
  the SHA-1 ever leave the machine); email check opens HIBP, or queries the v3 API if
  you `export HIBP_API_KEY=...`

## API credentials

No API credentials are bundled. IP lookup uses IPinfo's unauthenticated
endpoint unless you configure an optional token. For example (bash):

```bash
export IPINFO_TOKEN="your_ipinfo_token"
export HIBP_API_KEY="your_hibp_api_key"  # optional, for email checks
./start.sh
```

With fish, use `set -x IPINFO_TOKEN your_ipinfo_token` instead.
`.env.example` documents supported names; the application does **not**
automatically load `.env` files. Do not commit actual secrets.

## Testing

Run the offline source and security smoke tests with:

```bash
python3 -m unittest discover -s tests -v
```

This does not verify live third-party APIs or external system binaries.

## Optional system tools

Some Network/OSINT modules call external binaries. Install what you want (Arch):

```bash
sudo pacman -S nmap wireshark-cli tcpdump bind traceroute mtr whois
```

Each module degrades gracefully and prints an install hint if its binary is missing.

## Install

```bash
cd /home/$USER/krucified
./setup.sh      # creates .venv and installs deps
./start.sh      # launch
```

Or without a virtualenv:

```bash
pip install -r requirements.txt
python3 krucified.py
```

Requires Python 3.8+ and the `ping` binary (preinstalled on virtually all Linux
distros).

The interface is a single flat module list — pick a module by number, it runs,
you drop back to the list. No animations, no splash screens. The header shows the
version, which optional external binaries are present, and `user@host`.

## Scope / ethics

Use these only against infrastructure you own or are explicitly authorized to
test (pentest engagement, CTF, your own servers). Port scanning and recon of
systems you don't have permission to test may be illegal in your jurisdiction.
See `DISCLAIMER.md`.
