import os
import sys
import re
import requests
from django.test.runner import DiscoverRunner
from django.test import TestCase
import django
from django.conf import settings
from django.core.management import call_command
from unittest import TestSuite

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
    issue_pattern = r"(\w+)/(#\d+)-"
    match = re.search(issue_pattern, branch_name)
    if not match:
        sys.exit(f"Issue number not found in branch name {branch_name}")
    return match.group(2)


def get_test_issue_names(issue_number):
    url = f"https://api.github.com/repos/{repo}/issues?labels=test"
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json",
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        sys.exit(f"Failed to fetch issues: {response.status_code}\nurl = {url}")

    test_issue_pattern = rf"TEST: {issue_number}-([\w\s]+)"
    print(f"Fetching test cases for issue: {issue_number}")

    testcase_names = []
    for issue in response.json():
        match = re.match(test_issue_pattern, issue["title"])
        if match:
            testcase_names.append(match.group(1))
    print(f"Test cases found: {testcase_names}")
    return testcase_names


class PRTestRunner(DiscoverRunner):
    def __init__(self, testcase_names=None, **kwargs):
        self.testcase_names = testcase_names or []
        super().__init__(**kwargs)

    def build_suite(self, test_labels=None, extra_tests=None, **kwargs):
        suite = super().build_suite(test_labels, extra_tests)
        if self.testcase_names:
            return self.filter_suite(suite)
        return suite

    def filter_suite(self, suite):
        filtered_tests = []
        for test in suite:
            if isinstance(test, TestCase):
                if test.__class__.__name__ in self.testcase_names:
                    filtered_tests.append(test)
            elif isinstance(test, TestSuite):
                filtered_suite = self.filter_suite(test)
                if filtered_suite.countTestCases() > 0:
                    filtered_tests.extend(filtered_suite)

        if not filtered_tests:
            print("No tests found for this issue")
            return suite.__class__()

        print(f"Running tests for: {', '.join(self.testcase_names)}")
        new_suite = suite.__class__()
        new_suite.addTests(filtered_tests)
        return new_suite

    def run_tests(self, test_labels, extra_tests=None, **kwargs):
        self.setup_test_environment()
        suite = self.build_suite(test_labels, extra_tests)
        if self.testcase_names:
            suite = self.filter_suite(suite)
        result = self.run_suite(suite)
        self.teardown_test_environment()
        return self.suite_result(suite, result)

    def split_suite(self, suite):
        # Django 3.2 이상에서 필요한 메서드
        return self.reorder_suite(suite)


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

        test_runner = PRTestRunner(
            testcase_names=testcase_names, verbosity=2, interactive=False
        )
        failures = test_runner.run_tests(
            []
        )  # 여기서 "account"는 테스트를 실행할 앱 이름입니다. 필요에 따라 변경하세요.

        if failures:
            print(f"Some tests failed. Number of failures: {failures}")
            sys.exit(1)
        else:
            print("All tests passed successfully.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
