import re
from functools import singledispatchmethod


class MarkdownParseError(Exception):
    """마크다운 파싱 중 발생하는 오류를 위한 사용자 정의 예외"""

    pass


class Markdown:
    """마크다운 문서를 파싱하고 조작하는 클래스

    이 마크다운은 다음과 같은 구조를 가집니다:
    1. h1로 시작하는 계층 구조이거나, h2의 집합으로 이루어진 구조
    2. heading 바로 아래에는 comment가 위치
    3. 다음 sub_heading이 나오기 전까지의 내용을 main_content로 간주
    4. sub_heading이 나온 이후의 텍스트는 sub_headings로 분리
    """

    @classmethod
    def parse(cls, markdown_content: str):
        """마크다운 문자열을 파싱하여 Markdown 객체로 변환"""
        try:
            return cls._parse_section(markdown_content)
        except Exception as e:
            raise MarkdownParseError(f"마크다운 파싱 중 오류 발생: {str(e)}")

    @classmethod
    def _parse_section(cls, section_content: str, level: int = 1):
        main_section_pattern = re.compile(
            rf"^(#{{{level}}}[^\n]*(?:\n(?!#{{1,{level}}})[^\n]*)*)",
            re.MULTILINE | re.DOTALL,
        )

        match = main_section_pattern.match(section_content)
        if not match:
            raise MarkdownParseError(
                f"올바른 마크다운 구조를 찾을 수 없습니다. (레벨: {level})"
            )

        main_content = match.group(1).strip()
        sub_sections_content = section_content[match.end() :].strip()

        if main_content:
            return cls(
                **cls._parse_main_content(main_content, level),
                level=level,
                sub_sections=[
                    cls._parse_section(sub_section_content, level + 1)
                    for sub_section_content in cls._split_sub_content(
                        sub_sections_content, level + 1
                    )
                ],
            )

        return main_content, sub_sections_content

    @staticmethod
    def _parse_main_content(main_content: str, level: int = 1):
        """주 내용을 제목, 댓글, 본문으로 파싱"""
        main_content_pattern = re.compile(
            rf"^(?P<title>#{{{level}}}\s.*?)\n(?:(?P<comment><!--.*?-->\n))?\n*(?P<body>(?:(?!^#{{1,{level}}}\s).*\n?)*)",
            re.MULTILINE | re.DOTALL,
        )

        match = main_content_pattern.match(main_content)
        if not match:
            raise MarkdownParseError(
                f"주 섹션의 구조가 올바르지 않습니다. (레벨: {level})"
            )

        title = re.sub(rf"^#{{{level}}}\s+", "", match.group("title").strip())

        comment_match = match.group("comment")
        if comment_match:
            comment = re.sub(r"<!--\s*(.*?)\s*-->", r"\1", comment_match).strip()
        else:
            comment = ""

        body = match.group("body").strip()

        return {
            "title": title,
            "comment": comment,
            "body": body,
        }

    @staticmethod
    def _split_sub_content(sub_contents: str, level: int) -> list[str]:
        """하위 내용을 개별 섹션으로 분할"""
        # level에 따라 '#{level} '로 시작하여 다음 '#{level} ' 전까지의 내용을 캡처하는 패턴
        split_pattern = re.compile(
            rf"(#{{{level}}} .*?(?=\n#{{{level}}} |\Z))", re.MULTILINE | re.DOTALL
        )

        # findall을 사용하여 모든 매치를 찾음
        splitted_sub_contents = split_pattern.findall(sub_contents)

        return splitted_sub_contents

    def __init__(
        self,
        title: str,
        comment: str,
        body: str,
        level: int = 1,
        sub_sections: list["Markdown"] = None,
    ):
        """Markdown 객체 초기화"""
        self.level = level
        self.title = title
        self.comment = comment
        self.body = body
        self.sub_sections = {s.title: s for s in sub_sections} if sub_sections else {}

    @singledispatchmethod
    def __getitem__(self, arg):
        """지원되지 않는 인자 타입에 대한 기본 처리"""
        raise NotImplementedError("Unsupported argument type")

    @__getitem__.register
    def _(self, title: str):
        """제목으로 하위 섹션 접근"""
        return self.sub_sections.get(title)

    @__getitem__.register
    def _(self, path: list):
        """경로로 중첩된 하위 섹션 접근"""
        current_title = path[0]
        remaining_path = path[1:]

        if not remaining_path:
            return self.sub_sections.get(current_title)

        next_section = self.sub_sections.get(current_title)
        return next_section[remaining_path] if next_section else None

    def build(self) -> str:
        """Markdown 객체를 문자열로 변환"""
        main_content = (
            f"{'#'*self.level} {self.title}\n<!-- {self.comment} -->\n\n{self.body}\n"
        )
        sub_content = "\n".join([s.build() for s in self.sub_sections.values()])

        return f"{main_content}\n{sub_content}"


markdown_for_test = """# Title
<!-- Comment -->

Body

## Subtitle 1
<!-- Comment -->

Body

### Sub-subtitle 1
<!-- Comment -->

Body

### Sub-subtitle 2
<!-- Comment -->

Body

## Subtitle 2
<!-- Comment -->

Body

### Sub-subtitle 1
<!-- Comment -->

Body

### Sub-subtitle 2
<!-- Comment -->

Body
"""


print(Markdown.parse(markdown_for_test).build())
print(Markdown.parse(markdown_for_test)["Subtitle 1"].build())
