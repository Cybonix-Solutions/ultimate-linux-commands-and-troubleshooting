import os
import json

# Configuration
CONTENT_DIRS = ["commands", "cheatsheets", "troubleshooting"]
OUTPUT_FILE = "site/search_index.json"
ROOT_DIR = "."

def get_title(file_path):
    """Extracts the first H1 or text line as title."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith("# "):
                    return line[2:]
                if line and not line.startswith("#"):
                    return line
    except Exception:
        pass
    return os.path.basename(file_path)

def generate_index():
    index = []
    
    # Ensure site directory exists
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    for directory in CONTENT_DIRS:
        dir_path = os.path.join(ROOT_DIR, directory)
        if not os.path.exists(dir_path):
            continue
            
        for root, _, files in os.walk(dir_path):
            for file in files:
                if file.endswith(".md") and file != "README.md":
                    full_path = os.path.join(root, file)
                    relative_path = os.path.relpath(full_path, ROOT_DIR)
                    
                    try:
                        with open(full_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            
                        entry = {
                            "title": get_title(full_path),
                            "path": "../" + relative_path, # Relative to site/index.html
                            "category": directory,
                            "content": content
                        }
                        index.append(entry)
                    except Exception as e:
                        print(f"Skipping {full_path}: {e}")

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=2)
    
    print(f"Generated index with {len(index)} entries at {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_index()
