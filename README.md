# csv-to-json

Convert a CSV file into a JSON array of objects. Numbers are detected and
converted automatically (int when possible, otherwise float); everything else
stays a string. The CSV dialect (delimiter, quoting) is auto-detected, with an
option to force a delimiter. Output goes to stdout or a file, pretty-printed
by default with a `--minify` option.

## Requirements

Python 3.8+ — no third-party packages.

## Usage

```bash
python3 csv2json.py clients.csv
python3 csv2json.py clients.csv --out clients.json
python3 csv2json.py clients.csv --out clients.min.json --minify
python3 csv2json.py data.txt --delimiter ";"
```

## Example

Input `clients.csv`:

```csv
name,age,city,score
Aisha,29,Jaipur,8.5
Bruno,41,Goa,9.0
```

Command:

```bash
python3 csv2json.py clients.csv
```

Output (also printed: `2 row(s) converted.` to stderr):

```json
[
  {
    "name": "Aisha",
    "age": 29,
    "city": "Jaipur",
    "score": 8.5
  },
  {
    "name": "Bruno",
    "age": 41,
    "city": "Goa",
    "score": 9.0
  }
]
```

## Error handling

- A missing or unreadable input file exits with code `2` and a clear message.
- An empty CSV (no usable rows) exits with code `2`.
- Blank rows are skipped automatically.

## Notes

- UTF-8 with BOM is handled transparently.
- Duplicate column names are kept as-is; `csv.Sniffer` auto-detects `,`, `;`,
  tab, and `|` delimiters.
