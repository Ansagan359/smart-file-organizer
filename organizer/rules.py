"""Category rules: which extensions map to which folder."""

from __future__ import annotations

import json
from pathlib import Path

# Default extension → category mapping. Override with a custom JSON via --config.
DEFAULT_RULES: dict[str, list[str]] = {
    "Images": ["jpg", "jpeg", "png", "gif", "bmp", "svg", "webp", "heic", "tiff", "ico"],
    "Documents": ["pdf", "doc", "docx", "txt", "md", "rtf", "odt", "xls", "xlsx", "ppt", "pptx", "csv"],
    "Audio": ["mp3", "wav", "flac", "aac", "ogg", "m4a"],
    "Video": ["mp4", "mkv", "mov", "avi", "webm", "flv", "wmv"],
    "Archives": ["zip", "rar", "7z", "tar", "gz", "bz2", "xz"],
    "Code": ["py", "js", "ts", "tsx", "jsx", "java", "c", "cpp", "cs", "go", "rs", "rb", "php", "html", "css", "json", "yaml", "yml", "sh"],
    "Executables": ["exe", "msi", "dmg", "appimage", "deb", "rpm"],
    "Fonts": ["ttf", "otf", "woff", "woff2"],
}

OTHER = "Other"


def extension_to_category(rules: dict[str, list[str]]) -> dict[str, str]:
    """Invert the rules into a flat ``ext -> category`` lookup."""
    mapping: dict[str, str] = {}
    for category, extensions in rules.items():
        for ext in extensions:
            mapping[ext.lower().lstrip(".")] = category
    return mapping


def load_rules(path: Path | None) -> dict[str, list[str]]:
    """Load custom rules from a JSON file, or fall back to the defaults."""
    if path is None:
        return DEFAULT_RULES
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Rules file must be a JSON object of {category: [extensions]}.")
    return data
