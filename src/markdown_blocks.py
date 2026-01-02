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


"""
return type of blocktype given a block string
will just do regex to identify
"""

"""

"""


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

    code_pattern = r"^```.*```$"
    if re.match(code_pattern, block):
        return BlockType.CODE

    quote_pattern = r"^>"
    if re.match(quote_pattern, block):
        return BlockType.QUOTE

    ul_pattern = r"^- "
    if re.match(ul_pattern, block):
        return BlockType.UNORDERED_LIST

    if is_ordered_list(block):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
