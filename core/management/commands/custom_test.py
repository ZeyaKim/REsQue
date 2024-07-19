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

    def run_from_argv(self, argv):
        """
        Override the run_from_argv to use parse_known_args()
        """
        parser = self.create_parser(argv[0], argv[1])
        options, unknown = parser.parse_known_args(argv[2:])
        cmd_options = vars(options)
        args = cmd_options.pop("args", ())
        handle_args = (args,) + tuple(unknown)
        self.execute(*handle_args, **cmd_options)

    def handle(self, *args, **options):
        test_type = options.pop("type")

        if test_type == "unit":
            settings.TEST_RUNNER = "core.utils.test_runners.UnitTestRunner"
        elif test_type == "integration":
            settings.TEST_RUNNER = "core.utils.test_runners.IntegrationTestRunner"
        else:  # 'all'
            settings.TEST_RUNNER = "django.test.runner.DiscoverRunner"

        # Django의 기본 test 명령어 호출
        # 알려지지 않은 인자들을 포함한 모든 추가 인자를 그대로 전달합니다.
        call_command("test", *args)
