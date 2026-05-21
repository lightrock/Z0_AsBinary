"""Fetch the official NIST CODATA 2014 all-values ASCII file.

This is deliberately separate from the local source-to-binary build step so the
repo can preserve chain of custody:

1. Fetch official NIST raw source into data/codata/raw/.
2. Review/normalize into docs/codata/pre-2019-codata-2014-source.md.
3. Rebuild the binary and bits-only derived files.

The script is optional and network-dependent. Generated analysis must not depend
on a live network call at test time.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import urllib.request

NIST_CODATA_2014_ALL_ASCII_URL = "https://physics.nist.gov/cuu/Constants/ArchiveASCII/allascii_2014.txt"


def fetch(url: str, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url, timeout=30) as response:
        body = response.read()
    destination.write_bytes(body)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default=NIST_CODATA_2014_ALL_ASCII_URL)
    parser.add_argument(
        "--destination",
        type=Path,
        default=Path("data/codata/raw/allascii_2014.txt"),
    )
    args = parser.parse_args()
    fetch(args.url, args.destination)
    print(f"Fetched {args.url} -> {args.destination}")


if __name__ == "__main__":
    main()
