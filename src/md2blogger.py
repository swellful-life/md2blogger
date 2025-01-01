import argparse
import json


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert markdown files to Blogger format")
    parser.add_argument('--files', type=str, required=True, help="JSON array of changed files")
    args = parser.parse_args()

    try:
        changed_files = json.loads(args.files)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        exit(1)

    md_files = [file.replace(" ", "_") for file in changed_files]

    print(md_files)
    print(json.dumps(md_files, ensure_ascii=False, indent=2))
