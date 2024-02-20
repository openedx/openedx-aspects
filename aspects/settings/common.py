"""
Common Django settings for eox_hooks project.
For more information on this file, see
https://docs.djangoproject.com/en/2.22/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.22/ref/settings/
"""
from aspects import ROOT_DIRECTORY


def plugin_settings(settings):
    """
    Set of plugin settings used by the Open Edx platform.
    More info: https://github.com/edx/edx-platform/blob/master/openedx/core/djangoapps/plugins/README.rst
    """
    settings.MAKO_TEMPLATE_DIRS_BASE.append(ROOT_DIRECTORY / "templates")
    settings.SUPERSET_CONFIG = {
        "url": "http://superset.local.overhang.io:8088",
        "username": "superset",
        "password": "superset",
    }
    settings.SUPERSET_INSTRUCTOR_DASHBOARD = {
        "dashboard_slug": "instructor-dashboard",
        "dashboard_uuid": "1d6bf904-f53f-47fd-b1c9-6cd7e284d286",
    }
    settings.SUPERSET_EXTRA_FILTERS_FORMAT = []
