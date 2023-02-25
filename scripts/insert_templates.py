#!/usr/bin/env python3
import re
import sys
from pathlib import Path
from typing import Iterator, Optional

PLACEHOLDER_LINE_REGEX = re.compile(r"<!-- tpl: ([a-zA-Z_]+) -->\n")
RENDERED_TEMPLATES_BASE_PATH = Path(".") / "templates" / "rendered"


def iter_rendered_template_lines(template_name: str) -> Iterator[str]:
    template_path = RENDERED_TEMPLATES_BASE_PATH / f"{template_name}.md"
    with open(template_path, "r") as lines:
        yield from lines


def get_template_name_from_line(line: str) -> Optional[str]:
    if match := PLACEHOLDER_LINE_REGEX.match(line):
        return match.group(1)


def iter_output_lines(
    input_file_path: str,
) -> Iterator[str]:
    with open(input_file_path, "r") as input_file:
        for line in input_file:
            template_name = get_template_name_from_line(line)
            if template_name:
                yield from iter_rendered_template_lines(template_name)
            else:
                yield line


def main():
    assert len(sys.argv) == 3
    _, input_file_path, output_file_path = sys.argv
    with open(output_file_path, "w") as output_file:
        for line in iter_output_lines(input_file_path):
            output_file.write(line)


if __name__ == "__main__":
    main()
