import requests
from src.utils.markdown_to_html import MetaData


class BloggerUploader:
    def __init__(self, client_id, client_secret, refresh_token, blog_id):
        self._client_id = client_id
        self._client_secret = client_secret
        self._refresh_token = refresh_token
        self._blog_id = blog_id
        self._access_token = self._get_access_token()

    def _get_access_token(self):
        token_url = "https://oauth2.googleapis.com/token"
        data = {
            "client_id": self._client_id,
            "client_secret": self._client_secret,
            "refresh_token": self._refresh_token,
            "grant_type": "refresh_token",
        }

        response = requests.post(token_url, data=data)
        if response.status_code == 200:
            return response.json().get("access_token")
        else:
            raise Exception(f"Failed to get access token: {response.json()}")

    def _get_blog_info(self):
        url = f"https://www.googleapis.com/blogger/v3/blogs/{self._blog_id}"
        headers = {"Authorization": f"Bearer {self._access_token}"}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to get blog info: {response.status_code}, {response.text}")

    def upload_post(self, properties: MetaData, html_content: str):
        """
        Create or update a blog post on Blogger.

        :param properties: MetaData object containing post metadata (title, tags, etc.)
        :param html_content: HTML content of the blog post
        """
        # Skip upload if specified
        if properties.skip_upload:
            print(f"Skipping upload for post: {properties.title}")
            return None

        # Check if a post with the given title already exists
        search_url = f"https://www.googleapis.com/blogger/v3/blogs/{self._blog_id}/posts"
        headers = {"Authorization": f"Bearer {self._access_token}"}
        params = {
            "q": properties.title,
            "fetchBodies": False,
        }
        response = requests.get(search_url, headers=headers, params=params)

        if response.status_code != 200:
            raise Exception(f"Failed to search for posts: {response.text}")

        posts = response.json().get("items", [])
        existing_post = next((post for post in posts if post.get("title") == properties.title), None)

        # Prepare the post data
        post_data = {
            "kind": "blogger#post",
            "blog": {"id": self._blog_id},
            "title": properties.title,
            "content": html_content,
            "labels": properties.tags,
            "published": properties.published,
        }

        # Add permalink if specified
        if properties.permalink:
            post_data["customMetaData"] = properties.permalink

        if existing_post:
            # Update the existing post
            post_id = existing_post["id"]
            update_url = f"https://www.googleapis.com/blogger/v3/blogs/{self._blog_id}/posts/{post_id}"
            response = requests.put(update_url, headers=headers, json=post_data)
            action = "updated"
        else:
            # Create a new post
            create_url = f"https://www.googleapis.com/blogger/v3/blogs/{self._blog_id}/posts"
            response = requests.post(create_url, headers=headers, json=post_data)
            action = "created"

        if response.status_code in (200, 201):
            post = response.json()
            print(f"Post {action} successfully: {post.get('url')}")
            return post.get("url")
        else:
            raise Exception(f"Failed to {action} post: {response.text}")
