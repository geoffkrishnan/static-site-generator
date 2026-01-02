import re


def markdown_to_blocks(markdown):
    # regex substitutes \n with one or more spaces after it with \n effectively removing the tabs created after newlines
    return [
        re.sub(r"\n\s+", "\n", block.strip())
        for block in markdown.split("\n\n")
        if block.strip()
    ]
