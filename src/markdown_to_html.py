from htmlnode import ParentNode
from markdown_blocks import BlockType, markdown_to_blocks, block_to_blocktype
from textnode import LeafNode, text_node_to_html_node
from inline_markdown import text_to_textnodes


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_nodes = []
    for block in blocks:
        curr_blocktype = block_to_blocktype(block)

        if curr_blocktype == BlockType.HEADING:
            text = block.lstrip("#").strip()
            num_hashtags = len(block) - len(text) - 1

            text_nodes = text_to_textnodes(text)
            child_htmlnodes = [
                text_node_to_html_node(text_node) for text_node in text_nodes
            ]
            heading_parentnode = ParentNode(f"h{num_hashtags}", child_htmlnodes)
            block_nodes.append(heading_parentnode)

        elif curr_blocktype == BlockType.CODE:
            # code blocks
            # <pre>
            # <code>
            #     hello bitch
            # </code>
            # </pre>
            # "```code```"
            text = block.lstrip("`").rstrip("`").lstrip("\n")

            code_node = LeafNode("code", text)
            code_parentnode = ParentNode("pre", [code_node])
            block_nodes.append(code_parentnode)

        elif curr_blocktype == BlockType.UNORDERED_LIST:
            # <ul>
            #     <li>
            #     <li>
            # </ul>tag
            lines = block.split("\n")
            li_nodes = []
            for line in lines:
                # strip the "- " from the start of text line
                text = line[2:]
                text_nodes = text_to_textnodes(text)
                child_htmlnodes = [
                    text_node_to_html_node(text_node) for text_node in text_nodes
                ]
                li_node = ParentNode("li", child_htmlnodes)
                li_nodes.append(li_node)
            ul_node = ParentNode("ul", li_nodes)
            block_nodes.append(ul_node)

        elif curr_blocktype == BlockType.ORDERED_LIST:
            lines = block.split("\n")
            li_nodes = []
            for line in lines:
                # strip the "number. " from the start of text line
                text = line[3:]
                text_nodes = text_to_textnodes(text)
                child_htmlnodes = [
                    text_node_to_html_node(text_node) for text_node in text_nodes
                ]
                li_node = ParentNode("li", child_htmlnodes)
                li_nodes.append(li_node)
            ol_node = ParentNode("ol", li_nodes)
            block_nodes.append(ol_node)
        elif curr_blocktype == BlockType.QUOTE:
            lines = block.split("\n")
            raw_text = []
            for line in lines:
                if line.startswith("> "):
                    raw_text.append(line[2:])
                elif line.startswith(">"):
                    raw_text.append(line[1:])
            text = "".join(raw_text)

            text_nodes = text_to_textnodes(text)
            child_htmlnodes = [
                text_node_to_html_node(text_node) for text_node in text_nodes
            ]

            quote_node = ParentNode("blockquote", child_htmlnodes)
            block_nodes.append(quote_node)
        elif curr_blocktype == BlockType.PARAGRAPH:
            lines = block.split("\n")
            text = " ".join(lines)

            text_nodes = text_to_textnodes(text)
            child_htmlnodes = [
                text_node_to_html_node(text_node) for text_node in text_nodes
            ]

            paragraph_node = ParentNode("p", child_htmlnodes)
            block_nodes.append(paragraph_node)
    return ParentNode("div", block_nodes)
