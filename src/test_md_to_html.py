import unittest
from markdown_to_html import markdown_to_html_node


class TestMDtoHTML(unittest.TestCase):
    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_headings(self):
        self.maxDiff = None
        md = """
        # This is a heading

        ## This is a heading

        ### This is a heading

        #### This is a heading

        ##### This is a heading

        ###### This is a heading

        ####### this is not a heading
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is a heading</h1><h2>This is a heading</h2><h3>This is a heading</h3><h4>This is a heading</h4><h5>This is a heading</h5><h6>This is a heading</h6><p>####### this is not a heading</p></div>",
        )

    def test_quote(self):
        md = """
        > blah

        > blahblah

        > blah
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>blah</blockquote><blockquote>blahblah</blockquote><blockquote>blah</blockquote></div>",
        )

    def test_ul(self):
        md = """
        - one
        - two
        - three
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html, "<div><ul><li>one</li><li>two</li><li>three</li></ul></div>"
        )

    def test_ol(self):
        md = """
        1. one
        2. two
        3. three
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html, "<div><ol><li>one</li><li>two</li><li>three</li></ol></div>"
        )
