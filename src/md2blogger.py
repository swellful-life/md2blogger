import argparse
import json
from src.utils.markdown_to_html import MdToHtml
from src.utils.blogger_uploader import BloggerUploader


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert markdown files to Blogger format")
    parser.add_argument("--files", type=str, required=True, help="JSON array of changed files")
    parser.add_argument("--github_url", type=str, required=True, help="GitHub repository")
    parser.add_argument("--blogger_client_id", type=str, required=True, help="Blogger client ID")
    parser.add_argument("--blogger_client_secret", type=str, required=True, help="Blogger client secret")
    parser.add_argument("--blogger_refresh_token", type=str, required=True, help="Blogger refresh token")
    parser.add_argument("--blogger_blog_id", type=str, required=True, help="Blogger blog ID")
    args = parser.parse_args()

    try:
        changed_files = json.loads(args.files)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        exit(1)

    md_files = [file.replace(" ", "_") for file in changed_files]
    repo_url = args.github_url

    print(md_files)

    for md_file in md_files:
        md = MdToHtml(md_file, args.github_url)
        properties, html_content = md._convert_md_to_html()

        uploader = BloggerUploader(
            client_id=args.blogger_client_id,
            client_secret=args.blogger_client_secret,
            refresh_token=args.blogger_refresh_token,
            blog_id=args.blogger_blog_id,
        )
        uploader.upload_post(properties, html_content)
