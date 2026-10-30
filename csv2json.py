#!/usr/bin/env python3
"""csv-to-json: convert a CSV file into a JSON array of objects.

Numbers are converted automatically (int when possible, else float),
everything else stays a string. Dialect (delimiter, quoting) is
auto-detected; use --delimiter to override.
"""

import argparse
import csv
import json
import sys


def convert_value(text):
    """Convert a CSV cell to int/float when it looks numeric."""
    s = text.strip()
    if not s:
        return ""
    for cast in (int, float):
        try:
            return cast(s)
        except ValueError:
            continue
    return s


def load_rows(path, delimiter):
    try:
        fh = open(path, newline="", encoding="utf-8-sig")
    except OSError as exc:
        print(f"Error: cannot open '{path}': {exc.strerror or exc}", file=sys.stderr)
        sys.exit(2)
    with fh:
        sample = fh.read(4096)
        fh.seek(0)
        if delimiter is None:
            try:
                dialect = csv.Sniffer().sniff(sample, delimiters=[",", ";", "\t", "|"])
            except csv.Error:
                dialect = csv.excel
            reader = csv.reader(fh, dialect)
        else:
            reader = csv.reader(fh, delimiter=delimiter)
        rows = [row for row in reader if any(cell.strip() for cell in row)]
    if not rows:
        print(f"Error: '{path}' has no usable rows.", file=sys.stderr)
        sys.exit(2)
    header = [h.strip() or f"col{i+1}" for i, h in enumerate(rows[0])]
    return [{h: convert_value(c) for h, c in zip(header, row)} for row in rows[1:]]


def main():
    parser = argparse.ArgumentParser(
        description="Convert CSV to a JSON array of objects."
    )
    parser.add_argument("input", help="Input CSV file")
    parser.add_argument("--out", help="Write JSON to this file (default: stdout)")
    parser.add_argument(
        "--minify", action="store_true", help="Compact JSON output, no indentation"
    )
    parser.add_argument(
        "--delimiter", help="Force a delimiter (auto-detected if omitted)"
    )
    args = parser.parse_args()

    records = load_rows(args.input, args.delimiter)
    text = json.dumps(records, indent=None if args.minify else 2, ensure_ascii=False)

    if args.out:
        try:
            with open(args.out, "w", encoding="utf-8") as fh:
                fh.write(text + "\n")
        except OSError as exc:
            print(f"Error: cannot write '{args.out}': {exc.strerror or exc}",
                  file=sys.stderr)
            sys.exit(2)
    else:
        print(text)
    print(f"{len(records)} row(s) converted.", file=sys.stderr)


if __name__ == "__main__":
    main()
