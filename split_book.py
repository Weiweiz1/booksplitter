import argparse
import os
import re
import sys

PATTERNS = {
    'chinese': r'^(##\s+第.+章|#\s+后记|#\s+附录)',
    'english': r'^##\s+Chapter\s+\d+',
    'h2': r'^##\s+',
}


def split_markdown_by_chapters(filename, pattern):
    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        sys.exit(1)

    base_name = os.path.splitext(os.path.basename(filename))[0]
    output_dir = f"Chapters_{base_name}"

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    current_chapter_title = "Preface"
    current_chapter_content = []

    chapter_pattern = re.compile(pattern)

    for line in lines:
        match = chapter_pattern.match(line)
        if match:
            if current_chapter_content:
                save_chapter(output_dir, current_chapter_title, current_chapter_content)
                current_chapter_content = []

            raw_title = line.strip().replace('#', '').strip()
            current_chapter_title = raw_title
            current_chapter_content.append(line)
        else:
            current_chapter_content.append(line)

    if current_chapter_content:
        save_chapter(output_dir, current_chapter_title, current_chapter_content)
    
    print(f"Success! Split '{filename}' into folder: {output_dir}/")

def save_chapter(directory, title, content):
    safe_title = re.sub(r'[\\/*?:"<>|]', "", title).replace(" ", "_")
    output_path = os.path.join(directory, f"{safe_title}.md")
    
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

    args = parser.parse_args()
    pattern = args.pattern if args.pattern else PATTERNS[args.style]
    split_markdown_by_chapters(args.filename, pattern)