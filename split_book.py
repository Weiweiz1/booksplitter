import argparse
import os
import re
import sys

PATTERNS = {
    'chinese': r'^(##\s+第.+章|#\s+后记|#\s+附录)',
    'english': r'^##\s+Chapter\s+\d+',
    'h2': r'^##\s+',
}


def split_markdown_by_chapters(filename, pattern, numbered=False, dry_run=False):
    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        sys.exit(1)

    base_name = os.path.splitext(os.path.basename(filename))[0]
    output_dir = f"Chapters_{base_name}"

    if not dry_run and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    chapters = []
    current_chapter_title = "Preface"
    current_chapter_content = []

    chapter_pattern = re.compile(pattern)

    for line in lines:
        match = chapter_pattern.match(line)
        if match:
            if current_chapter_content:
                chapters.append((current_chapter_title, current_chapter_content))
                current_chapter_content = []

            raw_title = line.strip().replace('#', '').strip()
            current_chapter_title = raw_title
            current_chapter_content.append(line)
        else:
            current_chapter_content.append(line)

    if current_chapter_content:
        chapters.append((current_chapter_title, current_chapter_content))

    for index, (title, content) in enumerate(chapters, start=1):
        save_chapter(output_dir, title, content, index if numbered else None, dry_run)

    if dry_run:
        print(f"Dry run: would split '{filename}' into {len(chapters)} chapters in {output_dir}/")
    else:
        print(f"Success! Split '{filename}' into {len(chapters)} chapters in {output_dir}/")

def save_chapter(directory, title, content, index=None, dry_run=False):
    safe_title = re.sub(r'[\\/*?:"<>|]', "", title).replace(" ", "_")
    if index is not None:
        filename = f"{index:02d}_{safe_title}.md"
    else:
        filename = f"{safe_title}.md"
    output_path = os.path.join(directory, filename)

    if dry_run:
        print(f"  {filename}")
    else:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.writelines(content)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Split a markdown book into chapter files.'
    )
    parser.add_argument('filename', help='Path to the markdown file')
    parser.add_argument(
        '--style',
        choices=PATTERNS.keys(),
        default='chinese',
        help='Preset pattern style (default: chinese)'
    )
    parser.add_argument(
        '--pattern',
        help='Custom regex pattern (overrides --style)'
    )
    parser.add_argument(
        '--numbered',
        action='store_true',
        help='Prefix filenames with sequential numbers (01_, 02_, ...)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview chapters without writing files'
    )

    args = parser.parse_args()
    pattern = args.pattern if args.pattern else PATTERNS[args.style]
    split_markdown_by_chapters(args.filename, pattern, args.numbered, args.dry_run)