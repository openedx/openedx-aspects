"""
Test plugin settings for commond, devstack and production environments
"""

from django.conf import settings
from django.test import TestCase

from aspects.settings import common as common_settings
from aspects.settings import production as production_setttings


class TestPluginSettings(TestCase):
    """
    Tests plugin settings
    """

    def test_common_settings(self):
        """
        Test common settings
        """
        settings.MAKO_TEMPLATE_DIRS_BASE = []
        common_settings.plugin_settings(settings)
        self.assertIn("MAKO_TEMPLATE_DIRS_BASE", settings.__dict__)
        self.assertIn("url", settings.SUPERSET_CONFIG)
        self.assertIn("username", settings.SUPERSET_CONFIG)
        self.assertIn("password", settings.SUPERSET_CONFIG)
        self.assertIn("dashboard_slug", settings.SUPERSET_INSTRUCTOR_DASHBOARD)
        self.assertIn("dashboard_uuid", settings.SUPERSET_INSTRUCTOR_DASHBOARD)
        self.assertIsNotNone(settings.SUPERSET_EXTRA_FILTERS_FORMAT)

    def test_production_settings(self):
        """
        Test production settings
        """
        settings.ENV_TOKENS = {
            "SUPERSET_CONFIG": {
                "url": "http://superset.local.overhang.io:8088",
                "username": "superset",
                "password": "superset",
            },
            "SUPERSET_INSTRUCTOR_DASHBOARD": {
                "dashboard_slug": "instructor-dashboard",
                "dashboard_uuid": "1d6bf904-f53f-47fd-b1c9-6cd7e284d286",
            },
            "SUPERSET_EXTRA_FILTERS_FORMAT": [],
        }
        production_setttings.plugin_settings(settings)
        self.assertEqual(
            settings.SUPERSET_CONFIG, settings.ENV_TOKENS["SUPERSET_CONFIG"]
        )
        self.assertEqual(
            settings.SUPERSET_INSTRUCTOR_DASHBOARD,
            settings.ENV_TOKENS["SUPERSET_INSTRUCTOR_DASHBOARD"],
        )
        self.assertEqual(
            settings.SUPERSET_EXTRA_FILTERS_FORMAT,
            settings.ENV_TOKENS["SUPERSET_EXTRA_FILTERS_FORMAT"],
        )
