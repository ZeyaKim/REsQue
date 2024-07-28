import os
import sys
import re
import requests
from django.test.runner import DiscoverRunner
from django.test import TestCase
import django
from django.conf import settings
from django.core.management import call_command


owner = os.getenv("OWNER")
repo = os.getenv("REPO")
branch_name = os.getenv("BRANCH")
github_token = os.getenv("GITHUB_TOKEN")

if not all([owner, repo, branch_name, github_token]):
    sys.exit("Missing required environment variables")

print(f"Current working directory: {os.getcwd()}")
print(f"PYTHONPATH: {os.environ.get('PYTHONPATH')}")
print(f"sys.path: {sys.path}")

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, project_root)
print(f"Updated sys.path: {sys.path}")


def get_issue_number_from_branch():
    """
    브런치 이름에서 이슈 번호를 추출합니다.

    브런치 이름은 다음과 같은 형식이어야 합니다.
    {issue_type}/{issue_number}-{issue_title}
    """
    issue_pattern = r"(\w+)/(#\d+)-"

    match = re.search(issue_pattern, branch_name)

    if not match:
        sys.exit(f"Issue number not found in branch name {branch_name}")

    issue_number = match.group(2)

    return issue_number


def get_test_issue_names(issue_number):
    """
    깃허브 API를 사용하여 이슈에 등록된 테스트 케이스 이름을 가져옵니다.

    이슈에 등록된 테스트 케이스 이름은 다음과 같은 형식이어야 합니다.
    TEST: #{issue_number}-{testcase_name}
    """

    url = f"https://api.github.com/repos/{repo}/issues?labels=test"
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json",
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        sys.exit(f"Failed to fetch issues: {response.status_code}\nurl = {url}")

    test_issue_pattern = rf"TEST: #{issue_number}-([\w\s]+)"

    print(f"Fetching test cases for issue: {issue_number}")

    testcase_names = []
    for issue in response.json():
        match = re.match(test_issue_pattern, issue["title"])
        if match:
            testcase_name = match.group(1)
            testcase_names.append(testcase_name)
    print(f"Test cases found: {testcase_names}")
    return testcase_names


class PRTestRunner(DiscoverRunner):
    @classmethod
    def add_arguments(cls, parser):
        super().add_arguments(parser)
        parser.add_argument(
            "--testcase_names",
            nargs="+",
            type=str,
            help="Specify testcase names to run",
        )

    def __init__(self, testcase_names=None, **kwargs):
        self.testcase_names = testcase_names or []
        super().__init__(**kwargs)

    def build_suite(self, test_labels=None, extra_tests=None, **kwargs):
        suite = super().build_suite(test_labels, extra_tests, **kwargs)
        if self.testcase_names:
            return self.filter_suite(suite)
        return suite

    def filter_suite(self, suite):
        """
        테스트 스위트에서 이슈에 등록된 테스트만 필터링합니다
        """
        filtered_tests = []
        for test in suite:
            if isinstance(test, TestCase) or issubclass(test, TestCase):
                if test.__class__.__name__ in self.testcase_names:
                    filtered_tests.append(test)

        if not filtered_tests:
            sys.exit("No tests found for this issue")
        else:
            print(f"Running tests for: {', '.join(self.testcase_names)}")

        new_suite = suite.__class__()
        new_suite.addTests(filtered_tests)
        return new_suite


def main():
    if not settings.configured:
        django.setup()

    try:
        issue_number = get_issue_number_from_branch()
        testcase_names = get_test_issue_names(issue_number)

        if not testcase_names:
            print("No specific tests found for this issue. Exiting.")
            return

        print(f"Running tests for: {', '.join(testcase_names)}")

        # Django 설정에서 TEST_RUNNER 설정을 임시로 변경
        original_test_runner = settings.TEST_RUNNER
        settings.TEST_RUNNER = "core.utils.issue_related_tests.PRTestRunner"

        # call_command를 사용하여 테스트 실행
        try:
            call_command(
                "test",
                verbosity=2,
                interactive=False,
                testrunner=settings.TEST_RUNNER,
                testcase_names=testcase_names,
            )
            print("Tests completed successfully")
        finally:
            # 원래의 TEST_RUNNER 설정 복구
            settings.TEST_RUNNER = original_test_runner

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
