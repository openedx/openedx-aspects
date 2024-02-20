"""
Tests for the filters module.
"""

from unittest import TestCase
from unittest.mock import Mock, patch

from aspects.extensions.filters import BLOCK_CATEGORY, AddSupersetTab


class TestFilters(TestCase):
    """
    Test suite for the LimeSurveyXBlock filters.
    """

    def setUp(self) -> None:
        """
        Set up the test suite.
        """
        self.filter = AddSupersetTab(filter_type=Mock(), running_pipeline=Mock())
        self.template_name = "test-template-name"
        self.context = {"course": Mock()}

    @patch("aspects.extensions.filters.generate_superset_context")
    def test_run_filter(self, mock_generate_superset_context):
        """
        Check the filter is not executed when there are no LimeSurvey blocks in the course.

        Expected result:
            - The context is returned without modifications.
        """
        mock_generate_superset_context.return_value = {
            "sections": [],
        }

        context = self.filter.run_filter(self.context, self.template_name)

        self.assertDictContainsSubset(
            {
                "course_id": str(self.context["course"].id),
                "section_key": BLOCK_CATEGORY,
                "section_display_name": BLOCK_CATEGORY.title(),
                "template_path_prefix": "/instructor_dashboard/",
            },
            context["context"]["sections"][0],
        )
