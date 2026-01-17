# booksplitter

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A command-line tool to split markdown books into separate chapter files.

## Installation

```bash
git clone https://github.com/Weiweiz1/booksplitter.git
cd booksplitter
```

No dependencies required - uses Python standard library only.

## Usage

```bash
python split_book.py <filename> [options]
```

### Options

| Option | Description |
|--------|-------------|
| `--style` | Preset pattern: `chinese`, `english`, or `h2` (default: `chinese`) |
| `--pattern` | Custom regex pattern (overrides `--style`) |
| `--numbered` | Prefix filenames with sequential numbers (`01_`, `02_`, ...) |
| `--dry-run` | Preview chapters without writing files |
| `-v, --verbose` | Show progress as chapters are saved |

### Preset Patterns

- **chinese** - Matches `## 第X章`, `# 后记`, `# 附录`
- **english** - Matches `## Chapter 1`, `## Chapter 2`, etc.
- **h2** - Matches any level-2 heading (`## ...`)

### Examples

```bash
# Split a Chinese book (default)
python split_book.py mybook.md

# Split an English book
python split_book.py mybook.md --style english

# Split by any h2 heading
python split_book.py mybook.md --style h2

# Use a custom pattern
python split_book.py mybook.md --pattern "^##\s+Part\s+\d+"

# Preview what chapters would be created
python split_book.py mybook.md --dry-run

# Output with numbered prefixes (01_Preface.md, 02_Chapter1.md, ...)
python split_book.py mybook.md --numbered
```

## Output

Creates a folder named `Chapters_<filename>/` containing individual markdown files for each chapter. Content before the first chapter match is saved as `Preface.md`.
