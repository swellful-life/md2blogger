import argparse
import json
import os


def filter_and_transform_files(files):
    filtered_files = []
    for file in files:
        if file.endswith('.md'):
            transformed_file = file.replace(' ', '_')
            filtered_files.append(transformed_file)
    return filtered_files


def main():
    parser = argparse.ArgumentParser(description="Filter and transform .md files.")
    parser.add_argument('--files', type=str, required=True, help="JSON array of changed files")
    args = parser.parse_args()

    try:
        changed_files = json.loads(args.files)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return

    md_files = filter_and_transform_files(changed_files)

    print(md_files)
    print(json.dumps(md_files, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()