.. _superset-row-level-security:

Superset extra row level security
*********************************

To apply custom row level security filters to Superset, you can use the patch 
``superset-row-level-security``. This patch can overwrite the `default list <https://github.com/openedx/tutor-contrib-aspects/blob/main/tutoraspects/templates/aspects/apps/superset/pythonpath/openedx/create_row_level_security.py#L18-L46>`_ of roles
or use ``append`` to add additional dictionaries.

Overwrite existing:

.. code-block::

    SECURITY_FILTERS = [
            {
                "schema": "{{ASPECTS_XAPI_DATABASE}}",
                "table_name": "{{ASPECTS_XAPI_TABLE}}",
                "role_name": "{{SUPERSET_ROLES_MAPPING.instructor}}",
                "group_key": "{{SUPERSET_ROW_LEVEL_SECURITY_XAPI_GROUP_KEY}}",
                "clause": {% raw %}'{{can_view_courses(current_username(), "splitByChar(\'/\', course_id)[-1]")}}',{% endraw %}
                "filter_type": "Regular",
            },
    ]

Add to existing:

.. code-block::

    SECURITY_FILTERS.append(
            {
                "schema": "{{ASPECTS_XAPI_DATABASE}}",
                "table_name": "{{ASPECTS_XAPI_TABLE}}",
                "role_name": "{{SUPERSET_ROLES_MAPPING.instructor}}",
                "group_key": "{{SUPERSET_ROW_LEVEL_SECURITY_XAPI_GROUP_KEY}}",
                "clause": {% raw %}'{{can_view_courses(current_username(), "splitByChar(\'/\', course_id)[-1]")}}',{% endraw %}
                "filter_type": "Regular",
            },
    )

You can find more information about Superset RLSF in the `Superset documentation <https://superset.apache.org/docs/security/#row-level-security>`_.
