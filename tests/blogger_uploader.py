import pytest

from src.utils.markdown_to_html import MdToHtml
from src.utils.blogger_uploader import BloggerUploader

@pytest.fixture
def blogger_credentials():
    import json
    with open("../work/secret.json", "r") as f:
        secrets = json.load(f)

    client_id = secrets.get("BLOGGER_CLIENT_ID")
    client_secret = secrets.get("BLOGGER_CLIENT_SECRET")
    refresh_token = secrets.get("BLOGGER_REFRESH_TOKEN")
    blog_id = secrets.get("BLOGGER_BLOG_ID")

    return client_id, client_secret, refresh_token, blog_id


def test_create_blogger_uploader(blogger_credentials):
    client_id, client_secret, refresh_token, blog_id = blogger_credentials
    uploader = BloggerUploader(client_id, client_secret, refresh_token, blog_id)
    print(f"\nAccess Token: {uploader._access_token}")

def test_get_blogger_info(blogger_credentials):
    client_id, client_secret, refresh_token, blog_id = blogger_credentials
    uploader = BloggerUploader(client_id, client_secret, refresh_token, blog_id)
    blog_info = uploader._get_blog_info()
    print(f"\nBlog Info: {blog_info}")

def test_upload_post(blogger_credentials):
    client_id, client_secret, refresh_token, blog_id = blogger_credentials
    uploader = BloggerUploader(client_id, client_secret, refresh_token, blog_id)

    md = MdToHtml("../sample/posts/test/series1/sample2.md", "https://github.com/swellful-life/md2blogger")
    properties, html_content = md._convert_md_to_html()

    uploader.upload_post(properties, html_content)
