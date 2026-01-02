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
        if old_node.text_type in (TextType.IMAGE, TextType.LINK):
            new_nodes.append(old_node)
            continue

        if (
            delimiter in ("*", "**", "_", "__", "***", "___")
            and old_node.text_type != TextType.TEXT
        ):
            new_nodes.append(old_node)
            continue

        if delimiter == "`" and old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        if delimiter not in old_node.text:
            new_nodes.append(old_node)
            continue

        if old_node.text_type == text_type:
            new_nodes.append(old_node)
            continue

        if old_node.text.count(delimiter) % 2 != 0:
            raise ValueError(f"Unpaired delimiter: '{delimiter}'")

        split_node = old_node.text.split(delimiter)
        for index, string in enumerate(split_node):
            if string == "":
                continue
            if index % 2 == 0:
                new_node = TextNode(string, old_node.text_type)
                new_nodes.append(new_node)
            else:
                new_node = TextNode(string, text_type)
                new_nodes.append(new_node)
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        text = old_node.text

        if not text:
            new_nodes.append(old_node)
            continue

        matches = list(extract_markdown_links(text))
        # edge case: if no links exist, just append the old node directly
        if not matches:
            new_nodes.append(old_node)
            continue

        current_pos = 0
        for match in extract_markdown_links(text):
            text_before_link = text[current_pos : match.start()]
            if text_before_link:
                new_text = TextNode(text_before_link, TextType.TEXT)
                new_nodes.append(new_text)

            alt_text = match.group("alt")
            url = match.group("url")
            new_link = TextNode(alt_text, TextType.LINK, url)
            new_nodes.append(new_link)

            current_pos = match.end()
        text_after_link = text[current_pos:]
        if text_after_link or current_pos == 0:
            new_text = TextNode(text_after_link, TextType.TEXT)
            new_nodes.append(new_text)
    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        text = old_node.text

        # edge case: empty text
        if not text:
            new_nodes.append(old_node)
            continue

        matches = list(extract_markdown_images(text))
        # edge case: if no images exist, just append the old node directly
        if not matches:
            new_nodes.append(old_node)
            continue

        current_pos = 0
        for match in extract_markdown_images(text):
            text_before_image = text[current_pos : match.start()]
            if text_before_image:
                new_text = TextNode(text_before_image, TextType.TEXT)
                new_nodes.append(new_text)

            alt_text = match.group("alt")
            url = match.group("url")
            new_img = TextNode(alt_text, TextType.IMAGE, url)
            new_nodes.append(new_img)

            current_pos = match.end()
        text_after_image = text[current_pos:]
        if text_after_image:
            new_text = TextNode(text_after_image, TextType.TEXT)
            new_nodes.append(new_text)
    return new_nodes


def extract_markdown_images(text):
    pattern = r"!\[(?P<alt>[^\[\]]*)\]\((?P<url>[^\(\)]*)\)"
    return re.finditer(pattern, text)


def extract_markdown_links(text):
    """
    using negative lookbehind to only match link if it isn't preceded with a !
    so images aren't mistaken for links.
    """
    pattern = r"(?<!!)\[(?P<alt>[^\[\]]*)\]\((?P<url>[^\(\)]*)\)"
    return re.finditer(pattern, text)


def text_to_textnodes(text):
    text_nodes = [TextNode(text, TextType.TEXT)]
    text_nodes = split_nodes_image(text_nodes)
    text_nodes = split_nodes_link(text_nodes)
    text_nodes = split_nodes_delimiter(text_nodes, "**", TextType.BOLD)
    text_nodes = split_nodes_delimiter(text_nodes, "*", TextType.ITALIC)
    text_nodes = split_nodes_delimiter(text_nodes, "`", TextType.CODE)
    return text_nodes


def markdown_to_blocks(markdown):
    # regex substitutes \n with one or more spaces after it with \n effectively removing the tabs created after newlines
    return [
        re.sub(r"\n\s+", "\n", block.strip())
        for block in markdown.split("\n\n")
        if block.strip()
    ]
