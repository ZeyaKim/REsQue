from django.test import SimpleTestCase
from core.utils.markdown_parser import (
    MarkdownParser,
    SingleHeadingMarkdown,
    MultiHeadingMarkdown,
)

single_heading_markdown = """
# Title_h1
<!-- 주석_h1 -->

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat  nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

## Subtitle_h2
<!-- 주석_h2 -->

sub_content

### Subsubtitle_h3
<!-- 주석_h3 -->

subsub_content

#### Subsubsubtitle_h4

subsubsub_content

### Subsubtitle_h3_2
<!-- 주석_h3_2 -->

subsub_content_2

## Subtitle_h2_2

sub_content_2

## Title_h2_3

## Title_h2_4
<!-- 주석_h2_4 -->

sub_content_3
"""

simple_single_heading_markdown = """
# Title_h1
<!-- 주석_h1 -->

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat  nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

## Subtitle_h2
<!-- 주석_h2 -->

sub_content
"""

multi_heading_markdown = """
## Subtitle_h2

sub_content

### Subsubtitle_h3
<!-- 주석_h3 -->

subsub_content

## Subtitle_h2_2

sub_content_2

## Title_h2_3
<!-- 주석_h2_3 -->

sub_content_3
"""

simple_multi_heading_markdown = """
## Subtitle_h2
<!-- 주석_h2 -->

sub_content

### Subsubtitle_h3

subsub_content

## Subtitle_h2_2

sub_content_2
"""

simple_main_content_with_comment = """
## Subtitle_h2
<!-- 주석_h2 -->

sub_content
"""

simple_main_content_without_comment = """
## Subtitle_h2

sub_content
"""

simple_sub_sections = """
## Subtitle_h2
<!-- 주석_h2 -->

sub_content

### Subsubtitle_h3

subsub_content

## Subtitle_h2_2
<!-- 주석_h2_2 -->

sub_content_2

## Subtitle_h2_3

### Subsubtitle_h3_2

subsub_content_2

## Subtitle_h2_4
<!-- 주석_h2_4 -->
"""


class MarkdownParserTestCase(SimpleTestCase):

    def test_divide_markdown_before_next_section_with_simple_single_heading(self):

        main_content, sub_sections = (
            MarkdownParser._divide_markdown_before_next_section(
                simple_single_heading_markdown
            )
        )

        self.assertTrue(main_content.startswith("# Title_h1"))
        self.assertTrue(sub_sections.startswith("## Subtitle_h2"))

    def test_divide_markdown_before_next_section_with_single_heading(self):

        main_content, sub_sections = (
            MarkdownParser._divide_markdown_before_next_section(single_heading_markdown)
        )

        self.assertTrue(main_content.startswith("# Title_h1"))
        self.assertTrue(sub_sections.startswith("## Subtitle_h2"))

    def test_divide_markdown_before_next_section_with_simple_multi_heading(self):
        main_content, sub_sections = (
            MarkdownParser._divide_markdown_before_next_section(
                simple_multi_heading_markdown
            )
        )

        self.assertEqual(main_content, "")
        self.assertTrue(sub_sections.startswith("## Subtitle_h2"))

    def test_divide_markdown_before_next_section_with_multi_heading(self):
        main_content, sub_sections = (
            MarkdownParser._divide_markdown_before_next_section(multi_heading_markdown)
        )

        self.assertEqual(main_content, "")
        self.assertTrue(sub_sections.startswith("## Subtitle_h2"))

    def test_parse_main_section_without_comment(self):
        main_section = MarkdownParser._parse_main_content(
            simple_main_content_without_comment, level=2
        )

        self.assertEqual(main_section["title"], "Subtitle_h2")
        self.assertEqual(main_section["comment"], None)
        self.assertEqual(main_section["body"], "sub_content")

    def test_parse_main_section_with_comment(self):
        main_section = MarkdownParser._parse_main_content(
            simple_main_content_with_comment, level=2
        )

        self.assertEqual(main_section["title"], "Subtitle_h2")
        self.assertEqual(main_section["comment"], "주석_h2")
        self.assertEqual(main_section["body"], "sub_content")

    def test_split_sub_content(self):

        sub_sections = MarkdownParser._split_sub_content(simple_sub_sections, level=2)

        self.assertEqual(len(sub_sections), 4)
        self.assertEqual(
            all(section.startswith("## ") for section in sub_sections), True
        )

    def test_parse_single_heading_markdown(self):
        markdown = MarkdownParser.parse(single_heading_markdown)

        self.assertEqual(markdown["Title_h1"].title, "Title_h1")
        self.assertIsInstance(markdown, SingleHeadingMarkdown)
        self.assertEqual(markdown.parsed_markdown.comment, "주석_h1")

    def test_parse_multi_heading_markdown(self):
        markdown = MarkdownParser.parse(multi_heading_markdown)

        self.assertEqual(markdown["Subtitle_h2"].title, "Subtitle_h2")
        self.assertIsInstance(markdown, MultiHeadingMarkdown)
        self.assertEqual(markdown.parsed_markdown.get("comment"), None)
