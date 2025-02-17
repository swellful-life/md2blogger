import os
import re
import yaml
from typing import List, Optional
from dataclasses import dataclass, field, fields
from datetime import datetime
from zoneinfo import ZoneInfo


@dataclass
class MetaData:
    title: str
    permalink: str
    published: datetime
    tags: List[str] = field(default_factory=list)
    skip_upload: bool = False


class MdToHtml:
    PERMALINK_PATTERN = r"^[a-z\-]+$"

    def __init__(self, input_path: str, repo_url: str):
        self._input_path = input_path
        self._repo_url = repo_url
        self._contents = self._read_file()
        self._properties, self._body = self._parse_contents(self._contents)

    def _read_file(self) -> str:
        try:
            with open(self._input_path, "r") as f:
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {self._input_path}")

    def _parse_contents(self, contents: str) -> tuple:
        contents = contents.lstrip()
        if not contents.startswith("---"):
            return {}, contents

        parts = contents.split("---", 2)
        if len(parts) < 3 or not self._is_valid_yaml(parts[1]):
            return {}, contents
        return yaml.safe_load(parts[1]), parts[2].lstrip()

    @staticmethod
    def _get_valid_keys() -> set:
        return {field.name for field in fields(MetaData)}

    def _is_valid_yaml(self, text: str) -> bool:
        valid_keys = self._get_valid_keys()
        try:
            parsed = yaml.safe_load(text)
            return isinstance(parsed, dict) and set(parsed.keys()).issubset(valid_keys)
        except yaml.YAMLError:
            return False

    @staticmethod
    def _parse_datetime(date_utc: Optional[str]) -> str:
        try:
            if not date_utc:
                return datetime.now(ZoneInfo("Asia/Seoul")).isoformat(timespec="seconds")

            date_utc_obj = datetime.fromisoformat(date_utc)
            kst_datetime = date_utc_obj.replace(tzinfo=ZoneInfo("UTC")).astimezone(ZoneInfo("Asia/Seoul"))
            return kst_datetime.isoformat(timespec="seconds")
        except (ValueError, TypeError):
            return datetime.now(ZoneInfo("Asia/Seoul")).isoformat(timespec="seconds")

    def _validate_permalink(self, permalink: Optional[str]) -> Optional[str]:
        if not permalink:
            return None
        permalink = permalink.replace(" ", "")
        return permalink if re.fullmatch(self.PERMALINK_PATTERN, permalink) else None

    def extract_metadata(self) -> MetaData:
        default_title = os.path.basename(self._input_path).rsplit(".md", 1)[0]

        return MetaData(
            title=self._properties.get("title", default_title),
            permalink=self._validate_permalink(self._properties.get("permalink")),
            published=self._parse_datetime(self._properties.get("published")),
            tags=list(self._properties.get("tags", [])),
            skip_upload=self._properties.get("skip_upload", False),
        )

    def _convert_md_to_html(self):
        from markdown_it import MarkdownIt
        from mdit_py_plugins.tasklists import tasklists_plugin

        self._metadata = self.extract_metadata()

        md_renderer = MarkdownIt("commonmark", {"breaks": True}).use(tasklists_plugin).enable("table")

        raw_html = md_renderer.render(self._body)

        html_w_table_wrapper = re.sub(
            r'(<table(?:.|\n)*?</table>)',
            r'<div class="table-wrapper">\1</div>',
            raw_html,
            flags=re.DOTALL
        )

        self._html = re.sub(
            r'(<img\s+[^>]*src=")(?!http)([^"]+)(")',  # Match <img src="...">
            rf'\1{self._repo_url}/blob/main/\2?raw=true\3 width="100%"',  # Add width="100%"
            html_w_table_wrapper,
        )

        return self._metadata, self._html
