import re
from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    valid_markdown_delimiters = {
        "#",
        "##",
        "###",
        "####",
        "#####",
        "######",  # Headers
        "**",
        "__",  # Bold
        "*",
        "_",  # Italic (also used for bold when doubled)
        "***",
        "___",  # Bold + Italic
        "`",  # Inline code
        "~~",  # Strikethrough
    }

    if delimiter not in valid_markdown_delimiters:
        raise ValueError("Invalid markdown delimiter")
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        if old_node.text.count(delimiter) % 2 != 0:
            raise ValueError(f"Unpaired delimiter: '{delimiter}'")
        split_node = old_node.text.split(delimiter)
        for index, string in enumerate(split_node):
            if string == "":
                continue
            if index % 2 == 0:
                new_node = TextNode(string, TextType.TEXT)
                new_nodes.append(new_node)
            else:
                new_node = TextNode(string, text_type)
                new_nodes.append(new_node)
    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    """
    using negative lookbehind to only match link if it isn't preceded with a !
    so images aren't mistaken for links.
    """
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
