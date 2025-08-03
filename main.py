#!/usr/bin/env python3
import sys
import requests
from urllib.parse import urlparse

TIMEOUT = 10  # секунд


def normalize(url: str) -> str:
    url = url.strip()
    if not url:
        return ""
    parsed = urlparse(url)
    if not parsed.scheme:
        url = "http://" + url
    return url


def check(url: str) -> None:
    norm = normalize(url)
    if not norm:
        return
    try:
        resp = requests.head(norm, timeout=TIMEOUT, allow_redirects=True)
        status = resp.status_code
        if status >= 200 and status < 400:
            print(f"{url} -> 200")
            return
        resp = requests.get(norm, timeout=TIMEOUT, allow_redirects=True)
        status = resp.status_code
        if 200 <= status < 400:
            print(f"{url} -> 200")
        else:
            print(f"{url} -> HTTP {status}")
    except requests.exceptions.Timeout:
        print(f"{url} -> Timeout after {TIMEOUT}s")
    except requests.exceptions.InvalidURL:
        print(f"{url} -> Invalid URL")
    except requests.exceptions.ConnectionError as e:
        print(f"{url} -> Connection error: {e}")
    except Exception as e:
        print(f"{url} -> Other error: {e}")


def main():
    input_lines = [line.rstrip("\n") for line in sys.stdin if line.strip()]
    if not input_lines:
        print("No input URL provided.", file=sys.stderr)
        sys.exit(1)
    for line in input_lines:
        check(line)


if __name__ == "__main__":
    main()
