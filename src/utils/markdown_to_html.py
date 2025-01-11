import os
import re
import yaml
from typing import List, Optional
from dataclasses import dataclass, field, fields
from datetime import datetime
from zoneinfo import ZoneInfo


@dataclass
class MetaData:
    title: Optional[str] = None
    permalink: Optional[str] = None
    published: Optional[str] = None
    tags: Optional[List[str]] = field(default=None)

class MdToHtml:
    PERMALINK_PATTERN = r"^[a-z\-]+$"

    def __init__(self, input_path: str):
        self._input_path = input_path
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
    def _parse_datetime(date_str: str) -> str:
        try:
            utc_datetime = datetime.fromisoformat(date_str)
            kst_datetime = utc_datetime.replace(tzinfo=ZoneInfo("UTC")).astimezone(ZoneInfo("Asia/Seoul"))
            return kst_datetime.isoformat(timespec='seconds')
        except ValueError:
            return datetime.now(ZoneInfo("Asia/Seoul")).isoformat(timespec='seconds')

    def _validate_permalink(self, permalink: str) -> str:
        permalink = permalink.replace(" ", "")
        print(permalink)
        return permalink if re.fullmatch(self.PERMALINK_PATTERN, permalink) else ""

    def extract_metadata(self) -> Optional[MetaData]:
        if not self._properties:
            return MetaData(
            title=os.path.basename(self._input_path).rsplit(".md", 1)[0],
            published = self._parse_datetime(""),
        )

        return MetaData(
            title=self._properties.get("title", os.path.basename(self._input_path).rsplit(".md", 1)[0]),
            permalink=self._validate_permalink(self._properties.get("permalink", None)),
            published=self._parse_datetime(self._properties.get("published", "")),
            tags=list(self._properties.get("tags", [])),
        )

    def _md_to_html(self):
        self._metadata = self.extract_metadata()
        # TODO: Convert markdown in self._body to HTML.
        # TODO: If the title is not set in metadata, derive it from the file name.
        # TODO: Return or store the resulting HTML content.