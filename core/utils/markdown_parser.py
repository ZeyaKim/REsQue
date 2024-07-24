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
        """마크다운 문자열을 파싱하여 Markdown 객체로 변환 

        Args:
            markdown_content (str): 마크다운 문자열

        Returns:
            Markdown: 파싱된 마크다운 객체

        Raises:
            MarkdownParseError: 마크다운 파싱 중 오류 발생 시
        """
        try:
            return cls._parse_section(markdown_content)
        except MarkdownParseError as e:
            raise e

    @classmethod
    def _parse_section(cls, section_content: str, level: int = 1):
        """마크다운 문자열을 파싱하여 메인 섹션과 하위 섹션으로 분할

        `#{level} `로 시작하는 섹션을 파싱한 후, `{level+1}`을 기준으로 메인 섹션과 하위 섹션으로 분할한다.
        그 후, 메인 섹션과 하위 섹션을 각각 파싱하여 메인 섹션에서는 제목, 댓글, 본문을 추출하고,
        하위 섹션은 Markdown 객체의 리스트로 변환한 후 마크다운 객체의 생성자에 전달한다.

        Args:
            section_content (str): 파싱할 마크다운 문자열
            level (int): 현재 섹션의 레벨

        Returns:
            Markdown: 파싱된 마크다운 객체

        """
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

        sub_section_objects = [
            cls._parse_section(sub_section_content, level + 1)
            for sub_section_content in cls._split_sub_content(
                sub_sections_content, level + 1
            )
        ]

        if main_content:
            return cls(
                **cls._parse_main_content(main_content, level),
                level=level,
                sub_sections=sub_section_objects,
            )

        return sub_section_objects

    @staticmethod
    def _parse_main_content(main_content: str, level: int = 1):
        """주 내용을 제목, 댓글, 본문으로 파싱

        주 내용은 제목, 댓글, 본문으로 구성되어 있으며, 제목은 `#{level} `로 시작한다.
        댓글은 HTML 주석으로 감싸져 있으며, 본문은 제목과 댓글 사이의 내용이다.

        Args:
            main_content (str): 주 내용
            level (int): 현재 섹션의 레벨

        Returns:
            dict: 파싱된 주 내용의 제목, 댓글, 본문
        """
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
        """하위 내용을 개별 섹션으로 분할

        하위 내용은 `#{level+1} `로 시작하는 섹션으로 구성되어 있으며,
        `#{level} `로 시작하는 섹션을 기준으로 분할한다.

        Args:
            sub_contents (str): 하위 내용
            level (int): 현재 섹션의 레벨

        Returns:
            list[str]: 분할된 하위 내용
        """
        split_pattern = re.compile(
            rf"(#{{{level}}} .*?(?=\n#{{{level}}} |\Z))", re.MULTILINE | re.DOTALL
        )
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
        """제목으로 하위 섹션 접근

        Args:
            title (str): 하위 섹션의 제목

        Returns:
            Markdown: 하위 섹션 객체
        """
        return self.sub_sections.get(title)

    @__getitem__.register
    def _(self, path: list[str]):
        """경로로 중첩된 하위 섹션 접근

        Args:
            path (list[str]): 하위 섹션의 제목 경로

        Returns:
            Markdown: 하위 섹션 객체
        """
        current_title = path[0]
        remaining_path = path[1:]

        if not remaining_path:
            return self.sub_sections.get(current_title)

        next_section = self.sub_sections.get(current_title)
        return next_section[remaining_path] if next_section else None

    def __str__(self) -> str:
        """Markdown 객체를 문자열로 변환"""
        main_content = (
            f"{'#'*self.level} {self.title}\n<!-- {self.comment} -->\n\n{self.body}\n"
        )
        sub_content = "\n".join([s.build() for s in self.sub_sections.values()])

        return f"{main_content}\n{sub_content}"
