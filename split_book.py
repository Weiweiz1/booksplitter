import os
import re
import sys

def split_markdown_by_chapters(filename):
    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        return

    base_name = os.path.splitext(os.path.basename(filename))[0]
    output_dir = f"Chapters_{base_name}"
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    current_chapter_title = "Preface"
    current_chapter_content = []
    
    chapter_pattern = re.compile(r'^(##\s+第.+章|#\s+后记|#\s+附录)')

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
    if len(sys.argv) < 2:
        print("Usage: python split_book.py <your_file_name.md>")
    else:
        target_file = sys.argv[1]
        split_markdown_by_chapters(target_file)