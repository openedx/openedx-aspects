"""
Tests for the utils module.
"""

from collections import namedtuple
from unittest import TestCase
from unittest.mock import Mock, patch

from django.conf import settings

from aspects.utils import generate_superset_context

User = namedtuple("User", ["username"])


class TestUtils(TestCase):
    """
    Test utils module
    """

    @patch("aspects.utils.generate_guest_token")
    def test_generate_superset_context(self, mock_generate_guest_token):
        """
        Test generate_superset_context
        """
        course_mock = Mock()
        filter_mock = Mock()
        context = {"course": course_mock}
        mock_generate_guest_token.return_value = ("test-token", "test-dashboard-uuid")

        context = generate_superset_context(
            context,
            dashboard_uuid="test-dashboard-uuid",
            filters=[filter_mock],
        )

        self.assertEqual(context["superset_token"], "test-token")
        self.assertEqual(context["dashboard_uuid"], "test-dashboard-uuid")
        self.assertEqual(context["superset_url"], settings.SUPERSET_CONFIG.get("host"))
        self.assertNotIn("exception", context)

    @patch("aspects.utils.SupersetClient")
    def test_generate_superset_context_with_superset_client_exception(self, mock_superset_client):
        """
        Test generate_superset_context
        """
        course_mock = Mock()
        filter_mock = Mock()
        context = {"course": course_mock}
        mock_superset_client.side_effect = Exception("test-exception")

        context = generate_superset_context(
            context,
            dashboard_uuid="test-dashboard-uuid",
            filters=[filter_mock],
        )

        self.assertIn("exception", context)

    @patch("aspects.utils.SupersetClient")
    @patch("aspects.utils.get_current_user")
    def test_generate_superset_context_succesful(self, mock_get_current_user, mock_superset_client):
        """
        Test generate_superset_context
        """
        course_mock = Mock()
        filter_mock = Mock()
        context = {"course": course_mock}
        response_mock = Mock(status_code=200)
        mock_superset_client.return_value.session.post.return_value = response_mock
        response_mock.json.return_value = {
            "token": "test-token",
        }
        mock_get_current_user.return_value = User(username="test-user")

        context = generate_superset_context(
            context,
            dashboard_uuid="test-dashboard-uuid",
            filters=[filter_mock],
        )

        self.assertEqual(context["superset_token"], "test-token")
        self.assertEqual(context["dashboard_uuid"], "test-dashboard-uuid")
        self.assertEqual(context["superset_url"], settings.SUPERSET_CONFIG.get("host"))

    @patch("aspects.utils.get_current_user")
    def test_generate_superset_context_with_exception(self, mock_get_current_user):
        """
        Test generate_superset_context
        """
        course_mock = Mock()
        filter_mock = Mock()
        mock_get_current_user.return_value = User(username="test-user")
        context = {"course": course_mock}

        context = generate_superset_context(
            context,
            dashboard_uuid="test-dashboard-uuid",
            filters=[filter_mock],
        )

        self.assertIn("exception", context)
