import logging

import pytest

# 미 설정 시 py4j debug 로그 출력
logger = logging.getLogger("py4j")
logger.setLevel(logging.WARN)


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