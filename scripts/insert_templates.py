#!/usr/bin/env python3
import sys
import re
from pathlib import Path
from typing import Dict, Iterator, List, Optional

PLACEHOLDER_LINE_REGEX = re.compile(r"<!-- tpl: ([a-zA-Z_]+) -->\n")


def get_rendered_templates() -> Dict[str, List[str]]:
    result = {}
    rendered_dir = Path(".") / "rendered"
    for file_path in rendered_dir.glob("*.md"):
        result[file_path.stem] = open(file_path).readlines()
    return result


def get_template_name_from_line(line: str) -> Optional[str]:
    if match := PLACEHOLDER_LINE_REGEX.match(line):
        return match.group(1)


def _iter_lines(
    input_file_path: str,
    rendered_templates: Dict[str, List[str]],
) -> Iterator[str]:
    with open(input_file_path, "r") as input_file:
        for line in input_file:
            template_name = get_template_name_from_line(line)
            if template_name:
                rendered_lines = rendered_templates.get(template_name)
                if rendered_lines:
                    yield from rendered_lines
                    continue
            yield line


def main():
    assert len(sys.argv) == 3
    _, input_file_path, output_file_path = sys.argv
    rendered_templates = get_rendered_templates()
    with open(output_file_path, "w") as output_file:
        output_file.writelines(
            _iter_lines(
                input_file_path=input_file_path,
                rendered_templates=rendered_templates,
            )
        )


if __name__ == "__main__":
    main()
