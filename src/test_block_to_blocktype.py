import unittest

from markdown_blocks import BlockType, block_to_blocktype


class TestBlockToBlockType(unittest.TestCase):
    def test_heading_happy(self):
        headings = [
            "# Heading 1",
            "## Heading 2",
            "### Heading 3",
            "#### Heading 4",
            "##### Heading 5",
            "###### Heading 6",
        ]
        for heading in headings:
            self.assertEqual(block_to_blocktype(heading), BlockType.HEADING)

    def test_code_happy(self):
        valid_cases = [
            "```code```",
            "``` code ```",
            "``````",
        ]

        for case in valid_cases:
            with self.subTest(case=case):
                self.assertEqual(block_to_blocktype(case), BlockType.CODE)

    def test_ul_happy(self):
        ul = """- First item
- Second item
- Third item"""
        self.assertEqual(block_to_blocktype(ul), BlockType.UNORDERED_LIST)

    def test_ol_happy(self):
        ol = """1. First item
2. Second item
3. Third item"""
        self.assertEqual(block_to_blocktype(ol), BlockType.ORDERED_LIST)

    def test_paragraph_happy(self):
        paragraph = "paragraph blah blah"
        self.assertEqual(block_to_blocktype(paragraph), BlockType.PARAGRAPH)

    def test_bad_headings(self):
        headings = ["#Heading 1", " #Heading 1", "####### Heading 2", ""]
        for heading in headings:
            self.assertNotEqual(block_to_blocktype(heading), BlockType.HEADING)

    def test_bad_code(self):
        invalid_cases = [
            "````code```",
            "``code```",
            "```code",
            "code```",
            "text```code```",
            "```code```text",
            "``code``",
            " ```code```",
            "```code``` ",
            "",
        ]
        for case in invalid_cases:
            with self.subTest(case=case):
                self.assertNotEqual(block_to_blocktype(case), BlockType.CODE)

    # def test_nested_code(self):
    #
    #     code = "``` ```code``` ```"
    #     self.assertEqual(block_to_blocktype(code), BlockType.CODE)
