import argparse
import json

def filter_md_files(files):
    return [file for file in files if file.endswith('.md')]

def main():
    parser = argparse.ArgumentParser(description="Filter and process .md files.")
    parser.add_argument('--files', type=str, required=True, help="JSON array of changed files")
    args = parser.parse_args()

    changed_files = json.loads(args.files)
    md_files = filter_md_files(changed_files)
    print(json.dumps(md_files, indent=2))

if __name__ == "__main__":
    main()