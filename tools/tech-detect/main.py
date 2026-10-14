"""Tech fingerprint — guess server stack / CMS / frameworks from HTTP response."""
import re
import requests
from rich.console import Console

console = Console()
TIMEOUT = 12
UA = "Mozilla/5.0 (X11; Linux x86_64) krucified/1.0"

# header -> label
HEADER_HINTS = {
    "server": "server",
    "x-powered-by": "powered-by",
    "x-aspnet-version": "ASP.NET",
    "x-generator": "generator",
    "via": "proxy/cdn",
    "x-drupal-cache": "Drupal",
    "x-shopify-stage": "Shopify",
    "x-github-request-id": "GitHub Pages",
    "cf-ray": "Cloudflare",
    "x-served-by": "Fastly/Varnish",
    "x-vercel-id": "Vercel",
    "x-amz-cf-id": "AWS CloudFront",
}
# body regex -> label
BODY_HINTS = [
    (r"wp-content|wp-includes", "WordPress"),
    (r"/sites/default/files|Drupal\.settings", "Drupal"),
    (r"Joomla!", "Joomla"),
    (r"cdn\.shopify\.com", "Shopify"),
    (r"__NEXT_DATA__|/_next/", "Next.js"),
    (r"window\.__NUXT__", "Nuxt.js"),
    (r"ng-version=", "Angular"),
    (r"data-reactroot|react(?:\.production)?\.min\.js", "React"),
    (r"csrf-token|rails", "Ruby on Rails"),
    (r"laravel_session", "Laravel"),
    (r"wix\.com|X-Wix", "Wix"),
    (r"squarespace", "Squarespace"),
    (r"jquery[.-]", "jQuery"),
    (r"bootstrap(?:\.min)?\.css", "Bootstrap"),
]


def header():
    console.print()
    console.print("  [#9aa0a6]> [bold #cfcfcf]tech fingerprint[/]")
    console.print("[#262626]  " + "─" * 48)


if __name__ == "__main__":
    try:
        header()
        console.print()
        url = console.input("  [#9aa0a6][=][/#9aa0a6] url: ").strip()
        if not url:
            console.print("  [bold #cfcfcf][!] empty.[/bold #cfcfcf]")
            raise SystemExit(0)
        if not url.startswith(("http://", "https://")):
            url = "https://" + url

        try:
            r = requests.get(url, headers={"User-Agent": UA}, timeout=TIMEOUT)
        except requests.RequestException as e:
            console.print(f"  [bold #cfcfcf][!] request failed: {e}[/bold #cfcfcf]")
            raise SystemExit(0)

        console.print()
        console.print(f"  [#808080]final url  [/#808080][#b8b8b8]{r.url}[/#b8b8b8]")
        console.print(f"  [#808080]status     [/#808080][#f5f5f5]{r.status_code}[/#f5f5f5]")

        found = {}
        for h, label in HEADER_HINTS.items():
            if h in r.headers:
                found[label] = r.headers[h]
        # cookie-based hints
        for c in r.cookies:
            cl = c.name.lower()
            if "phpsessid" in cl:
                found.setdefault("PHP", "PHPSESSID cookie")
            if "asp.net" in cl:
                found.setdefault("ASP.NET", c.name)
            if "laravel" in cl:
                found.setdefault("Laravel", c.name)

        body = r.text[:200000]
        detected = [label for rx, label in BODY_HINTS if re.search(rx, body, re.I)]

        console.print()
        console.print("  [bold #cfcfcf]headers[/bold #cfcfcf]")
        if found:
            for label, val in found.items():
                console.print(f"    [#9aa0a6]>[/#9aa0a6] [#f5f5f5]{label}[/#f5f5f5] [dim]— {val}[/dim]")
        else:
            console.print("    [dim]nothing notable disclosed[/dim]")

        console.print()
        console.print("  [bold #cfcfcf]body signatures[/bold #cfcfcf]")
        if detected:
            for d in dict.fromkeys(detected):
                console.print(f"    [#9aa0a6]>[/#9aa0a6] [#f5f5f5]{d}[/#f5f5f5]")
        else:
            console.print("    [dim]no known fingerprints matched[/dim]")
        console.print()
    except (KeyboardInterrupt, EOFError):
        console.print("\n  [#9aa0a6]> interrupted.[/#9aa0a6]")
