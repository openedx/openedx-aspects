"""
Open edX Filters needed for Aspects integration.
"""

import pkg_resources
from django.conf import settings
from django.template import Context, Template
from openedx_filters import PipelineStep
from web_fragments.fragment import Fragment

from aspects.utils import update_context

TEMPLATE_ABSOLUTE_PATH = "/instructor_dashboard/"
BLOCK_CATEGORY = "superset"


class AddSupersetTab(PipelineStep):
    """Add superset tab to instructor dashboard."""

    def run_filter(
        self, context, template_name
    ):  # pylint: disable=arguments-differ, unused-argument
        """Execute filter that modifies the instructor dashboard context.
        Args:
            context (dict): the context for the instructor dashboard.
            _ (str): instructor dashboard template name.
        """
        course = context["course"]

        instructor_dashboard_config = getattr(
            settings, "SUPERSET_INSTRUCTOR_DASHBOARD", {}
        )
        dashboard_uuid = instructor_dashboard_config.get("dashboard_uuid")

        extra_filters_format = getattr(settings, "SUPERSET_EXTRA_FILTERS_FORMAT", [])

        default_filters = [
            "org = '{course.org}'",
            "course_name = '{course.display_name}'",
            "course_run = '{course.id.run}'",
        ]

        filters = default_filters + extra_filters_format

        context = update_context(
            context, dashboard_uuid=dashboard_uuid, filters=filters
        )
        template = Template(self.resource_string("static/html/superset.html"))

        html = template.render(Context(context))
        frag = Fragment(html)

        frag.add_css(self.resource_string("static/css/superset.css"))
        frag.add_javascript(self.resource_string("static/js/embed_dashboard.js"))

        section_data = {
            "fragment": frag,
            "section_key": BLOCK_CATEGORY,
            "section_display_name": "Aspects",
            "course_id": str(course.id),
            "template_path_prefix": TEMPLATE_ABSOLUTE_PATH,
        }
        context["sections"].append(section_data)
        return {
            "context": context,
        }

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string("aspects", path)
        return data.decode("utf8")
