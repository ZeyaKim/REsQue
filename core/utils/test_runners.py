from django.test.runner import DiscoverRunner


class UnitTestRunner(DiscoverRunner):
    def build_suite(self, test_labels=None, **kwargs):
        suite = super().build_suite(test_labels, **kwargs)
        tests = [t for t in suite._tests if "unit_test" in str(t).lower()]
        suite._tests = tests
        return suite


class IntegrationTestRunner(DiscoverRunner):
    def build_suite(self, test_labels=None, **kwargs):
        suite = super().build_suite(test_labels, **kwargs)
        tests = [t for t in suite._tests if "integration_test" in str(t).lower()]
        suite._tests = tests
        return suite
