import pytest
from unittest.mock import patch, mock_open
from src.utils.markdown_to_html import MdToHtml


sample_text1 = """
---
title: sample posting
permalink: sample-posting    adfad
published: 2025-01-11T14:10:00
tags:
  - aussie
  - english
---

안녕하세요, 이것은 샘플 포스팅입니다.
"""

sample_text2 = """
---
제목: 당신은 행복한가요?
---
구분선2
- 목록1
  - 목록1.1
  - 목록1.2
- 목록2

"""




@patch("builtins.open", new_callable=mock_open, read_data=sample_text1)
def test_md_to_html(mock_file):
    md = MdToHtml("sample.md", "https://github.com/swellful-life/md2blogger")
    md._convert_md_to_html()


@patch("builtins.open", new_callable=mock_open, read_data=sample_text2)
def test_md_to_html2(mock_file):
    md = MdToHtml("sample.md", "https://github.com/swellful-life/md2blogger")
    md._convert_md_to_html()

def test_md_to_html3():
    md = MdToHtml("../sample/posts/test/series1/sample2.md", "https://github.com/swellful-life/md2blogger")
    md._convert_md_to_html()
