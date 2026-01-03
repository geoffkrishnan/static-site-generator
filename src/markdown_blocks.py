import re
from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    # regex substitutes \n with one or more spaces after it with \n effectively removing the tabs created after newlines
    return [
        re.sub(r"\n\s+", "\n", block.strip())
        for block in markdown.split("\n\n")
        if block.strip()
    ]


def is_ordered_list(block):
    split_lines = block.split("\n")
    line_number = 1
    for line in split_lines:
        ol_pattern = r"^(\d+)\. "
        match = re.match(ol_pattern, line)
        if not match:
            return False
        if int(match.group(1)) != line_number:
            return False
        line_number += 1
    return True


def block_to_blocktype(block):
    heading_pattern = r"^#{1,6} "
    if re.match(heading_pattern, block):
        return BlockType.HEADING

    if block == "``````":
        return BlockType.CODE

    if (
        block.startswith("```")
        and not block.startswith("````")
        and block.endswith("```")
        and not block.endswith("````")
    ):
        return BlockType.CODE

    lines = block.split("\n")
    quote_pattern = r"^> "
    if all(re.match(quote_pattern, line) for line in lines):
        return BlockType.QUOTE

    ul_pattern = r"^- "
    if all(re.match(ul_pattern, line) for line in lines):
        return BlockType.UNORDERED_LIST

    if is_ordered_list(block):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
