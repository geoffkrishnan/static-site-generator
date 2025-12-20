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


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        text = old_node.text
        current_pos = 0
        for match in extract_markdown_links(text):
            text_before_link = text[current_pos : match.start()]
            new_text = TextNode(text_before_link, TextType.TEXT)
            new_nodes.append(new_text)

            alt_text = match.group("alt")
            url = match.group("url")
            new_link = TextNode(alt_text, TextType.LINK, url)
            new_nodes.append(new_link)

            current_pos = match.end()
        text_after_link = text[current_pos:]
        new_text = TextNode(text_after_link, TextType.TEXT)
    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        text = old_node.text
        current_pos = 0
        for match in extract_markdown_images(text):
            text_before_image = text[current_pos : match.start()]
            new_text = TextNode(text_before_image, TextType.TEXT)
            new_nodes.append(new_text)

            alt_text = match.group("alt")
            url = match.group("url")
            new_img = TextNode(alt_text, TextType.IMAGE, url)
            new_nodes.append(new_img)

            current_pos = match.end()
        text_after_image = text[current_pos:]
        new_text = TextNode(text_after_image, TextType.TEXT)
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


def main():
    node = TextNode(
        "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.TEXT,
    )
    new_nodes = split_nodes_link([node])
    print(new_nodes)


if __name__ == "__main__":
    main()
