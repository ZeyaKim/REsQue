from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings


class Command(BaseCommand):
    help = "Runs the test suite for the specified test type"

    def add_arguments(self, parser):
        parser.add_argument(
            "type",
            choices=["unit", "integration", "."],
            default=".",
            help="Specify the type of tests to run (unit/integration/all)",
        )
        # 추가 인자를 전달하기 위한 옵션
        parser.add_argument("test_labels", nargs="*")

    def handle(self, *args, **options):
        test_type = options["type"]
        test_labels = options["test_labels"]

        if test_type == "unit":
            settings.TEST_RUNNER = "core.utils.test_runners.UnitTestRunner"
        elif test_type == "integration":
            settings.TEST_RUNNER = "core.utils.test_runners.IntegrationTestRunner"
        else:  # 'all'
            settings.TEST_RUNNER = "django.test.runner.DiscoverRunner"

        # Django의 기본 test 명령어 호출
        call_command("test", *test_labels)
