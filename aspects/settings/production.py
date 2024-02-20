"""
Production Django settings for Aspects project.
"""


def plugin_settings(settings):
    """
    Set of plugin settings used by the Open Edx platform.
    More info: https://github.com/edx/edx-platform/blob/master/openedx/core/djangoapps/plugins/README.rst
    """
    settings.SUPERSET_CONFIG = getattr(settings, "ENV_TOKENS", {}).get(
        "SUPERSET_CONFIG", settings.SUPERSET_CONFIG
    )
    settings.ASPECTS_INSTRUCTOR_DASHBOARD_UUID = getattr(settings, "ENV_TOKENS", {}).get(
        "ASPECTS_INSTRUCTOR_DASHBOARD_UUID", settings.ASPECTS_INSTRUCTOR_DASHBOARD_UUID
    )
    settings.SUPERSET_EXTRA_FILTERS_FORMAT = getattr(settings, "ENV_TOKENS", {}).get(
        "SUPERSET_EXTRA_FILTERS_FORMAT", settings.SUPERSET_EXTRA_FILTERS_FORMAT
    )
