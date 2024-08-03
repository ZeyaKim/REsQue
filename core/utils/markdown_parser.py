import re


class MarkdownParser:
    @classmethod
    def parse(cls, markdown_content: str) -> "Markdown":
        try:
            parsed_markdown = cls._parse_section(markdown_content)
            if isinstance(parsed_markdown, dict):
                return MultiHeadingMarkdown(parsed_markdown)
            return SingleHeadingMarkdown(parsed_markdown)

        except MarkdownParseError as e:
            raise e

    @staticmethod
    def _parse_section(section_content: str, level: int = 1):
        (
            main_content,
            sub_sections_string,
        ) = MarkdownParser._divide_markdown_before_next_section(section_content, level)

        main_section = None
        if main_content:
            main_section = MarkdownSection(
                **MarkdownParser._parse_main_content(main_content, level), level=level
            )

        if not sub_sections_string:
            return main_section

        splitted_sub_sections = MarkdownParser._split_sub_content(
            sub_sections_string, level + 1
        )

        sub_sections = [
            MarkdownParser._parse_section(sub_section_content, level + 1)
            for sub_section_content in splitted_sub_sections
        ]

        if main_section:
            main_section.insert_sub_sections(sub_sections)
            return main_section

        return {sub_section.title: sub_section for sub_section in sub_sections}

    @staticmethod
    def _divide_markdown_before_next_section(markdown_content: str, level=1):
        """
        마크다운 문자열을 현재 레벨의 섹션과 다음 레벨의 섹션으로 나눕니다.
        둘 중 하나가 없을 수 있습니다.
        """
        pattern = rf"^#{{{level+1}}}\s"  # 예: 레벨이 1일 때 "## "를 찾음

        match = re.search(pattern, markdown_content, re.MULTILINE)

        if not match:
            pattern = rf"^#{{{level}}}\s"  # 예: 레벨이 1일 때 "# "를 찾음

            match = re.search(pattern, markdown_content, re.MULTILINE)

            if not match:
                raise MarkdownParseError(
                    f"주 섹션 또는 서브 섹션을 찾을 수 없습니다. (레벨: {level})\n{markdown_content}"
                )

            return markdown_content, ""

        split_point = match.start()
        main_section = markdown_content[:split_point].strip()
        sub_sections = markdown_content[split_point:].strip()

        return main_section, sub_sections

    @staticmethod
    def _parse_main_content(main_content: str, level: int = 1):
        main_content_pattern = re.compile(
            rf"^(?P<title>#{{{level}}}\s[^\n]+)(?:\n(?P<comment><!--.*?-->))?(?P<body>(?:\n\n[\s\S]*)?)",
            re.MULTILINE,
        )

        match = main_content_pattern.match(main_content.strip())
        if not match:
            raise MarkdownParseError(f"주 섹션의 구조가 올바르지 않습니다. (레벨: {level})")

        title = match.group("title").strip()
        comment = match.group("comment")
        body = match.group("body").strip()

        title = title.replace(f"{'#'*level} ", "")
        comment = (
            comment.replace("<!-- ", "").replace(" -->", "").strip()
            if comment
            else None
        )

        return {
            "title": title,
            "comment": comment,
            "body": body,
        }

    @staticmethod
    def _split_sub_content(sub_contents: str, level: int) -> list[str]:
        """
        서브 섹션을 분할합니다.
        """
        pattern = rf"^#{{{level}}} "
        matches = list(re.finditer(pattern, sub_contents, re.MULTILINE))

        if not matches:
            return [sub_contents] if sub_contents.strip() else []

        result = []
        for i, match in enumerate(matches):
            start = match.start()
            end = matches[i + 1].start() if i + 1 < len(matches) else None
            result.append(sub_contents[start:end].strip())

        return result


class MarkdownParseError(Exception):
    """마크다운 파싱 중 발생하는 오류를 위한 사용자 정의 예외"""

    pass


class Markdown:
    def __init__(self, parsed_markdown):
        self.parsed_markdown = parsed_markdown

    def __str__(self) -> str:
        raise NotImplementedError("Not implemented")


class SingleHeadingMarkdown(Markdown):
    def __init__(self, parsed_markdown):
        self.parsed_markdown: MarkdownSection = parsed_markdown

    def __str__(self) -> str:
        return str(self.parsed_markdown)

    def __getitem__(self, heading: str):
        if heading != self.parsed_markdown.title:
            return None
        return self.parsed_markdown


class MultiHeadingMarkdown(Markdown):
    def __str__(self) -> str:
        return "\n\n".join(str(s) for s in self.parsed_markdown.values())

    def __getitem__(self, title: str):
        return self.parsed_markdown[title]


class MarkdownSection:
    def __init__(
        self,
        title: str,
        comment: str,
        body: str,
        level: int,
    ):
        self.title = title
        self.comment = comment
        self.body = body
        self.level = level

        self.sub_sections = None

    def __getitem__(self, title: str):
        if not self.sub_sections:
            return None

        return self.sub_sections[title]

    def __str__(self) -> str:
        main_content = (
            f"{'#' * self.level} {self.title}\n<!-- {self.comment} -->\n\n{self.body}"
        )
        sub_content = "\n\n".join(str(s) for s in self.sub_sections.values())
        return f"{main_content}\n\n{sub_content}".strip()

    def insert_sub_sections(self, sub_sections):
        if not self.sub_sections:
            self.sub_sections = {}

        self.sub_sections.update({s.title: s for s in sub_sections})
