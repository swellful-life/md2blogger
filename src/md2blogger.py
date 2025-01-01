import argparse
import json

def main():
    parser = argparse.ArgumentParser(description="Filter and transform .md files.")
    parser.add_argument('--files', type=str, required=True, help="JSON array of changed files")
    args = parser.parse_args()

    try:
        changed_files = json.loads(args.files)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return

    md_files = [file.replace(" ", "_") for file in changed_files]

    print(md_files)
    print(json.dumps(md_files, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()