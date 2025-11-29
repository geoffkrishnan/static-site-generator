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
            raise ValueError(f"Unpaired delimiter: '{delimiter}' in text")
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


def main():
    node = TextNode("****", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    print(new_nodes)
    """
    new_nodes should become
    [
        TextNode("text with ", TextType.TEXT)
        TextNode("code block", TextType.CODE)
        TextNode("word", TextType.TEXT)
    ]
    """


if __name__ == "__main__":
    main()
