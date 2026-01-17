---
name: split-book
description: Split a markdown book into separate chapter files
---

# Split Book Skill

Split a markdown book into separate chapter files.

## Usage

```
/split-book <filename> [--style STYLE] [--pattern PATTERN]
```

## Arguments

- `filename` (required): Path to the markdown file to split
- `--style`: Preset pattern style - `chinese`, `english`, or `h2` (default: `chinese`)
- `--pattern`: Custom regex pattern (overrides `--style`)

## Instructions

When this skill is invoked:

1. **Parse the arguments** from the skill invocation:
   - Extract the filename (required)
   - Check for `--style` option (chinese/english/h2, default: chinese)
   - Check for `--pattern` option (custom regex, overrides style)

2. **Determine the chapter pattern** based on arguments:
   - `chinese`: `^(##\s+第.+章|#\s+后记|#\s+附录)`
   - `english`: `^##\s+Chapter\s+\d+`
   - `h2`: `^##\s+`
   - Or use the custom `--pattern` if provided

3. **Read the markdown file** using the Read tool

4. **Create the output directory** named `Chapters_<basename>/` where `<basename>` is the filename without extension

5. **Split the content into chapters**:
   - Process the file line by line
   - When a line matches the chapter pattern, start a new chapter
   - The chapter title is extracted by removing `#` characters and trimming whitespace
   - Content before the first chapter match is saved as "Preface"

6. **Write each chapter to a separate file**:
   - Sanitize the chapter title for use as filename (remove `\ / * ? : " < > |` and replace spaces with underscores)
   - Save as `<output_dir>/<sanitized_title>.md`

7. **Report the results** to the user:
   - List all chapter files created
   - Confirm the output directory location

## Example Invocations

```
/split-book mybook.md
/split-book mybook.md --style english
/split-book mybook.md --style h2
/split-book mybook.md --pattern "^##\s+Part\s+\d+"
```
