.. _extensions:

Aspects Extensions
#####################

Aspects is a project that comes with a set of extensions that can be used to
extend the different parts of the project.

Superset Assets
================

Aspects allows to programatically define custom Superset assets, such as custom data sources, queries, reports, and dashboards, via a Tutor patch.
Developers can use an tutor inline plugin with the patch `superset-extra-assets`
and those will be imported at initialization.

An example of such a plugin is the following:

.. code-block:: yaml

    name: custom-inline-plugin
    version: 0.1.0
    patches:
    superset-extra-assets: |
        - _file_name: my-dashboard.yaml
        dashboard_title: "..."
        ...
        - _file_name: my-chart.yaml
        slice_name: "..."
        ...
        - _file_name: my-database.yaml
        database_name: "..."
        ...
        - _file_name: my-dataset.yaml
        table_name: "..."
        ...

The patch is expected to be a list of assets with an extra attribute called **_file_name**,
which uniquely identifies the asset entry. This file does not need to exist anywhere;
it will be created with the rest of the yaml in that stanza as part of the init process.
Each asset is expected to be a valid yaml file with the attributes that Superset expects
for each asset type. See `assets.yaml <https://github.com/openedx/tutor-contrib-aspects/blob/main/tutoraspects/templates/aspects/apps/superset/pythonpath/assets.yaml>`_ 
for examples of asset yaml declarations.

Override Superset Default Assets
================================

Aspects allows to override the default Superset assets by creating an Superset extra asset
as explained above using the same UUID as the default asset. The UUID of the default assets
can be found in the `assets.yaml`

Changing Superset Language Settings
===================================

Superset localization is a work in progress, but you can change the default language and
set alternate languages from the currently supported list by changing the following tutor
configuration variables:

.. code-block:: yaml

    SUPERSET_DEFAULT_LOCALE: en
    SUPERSET_SUPPORTED_LANGUAGES:
      en:
        flag: us
        name: English
      es:
        flag: es
        name: Spanish
      it:
        flag: it
        name: Italian
      fr:
        flag: fr
        name: French
      zh:
        flag: cn
        name: Chinese
      ja:
        flag: jp
        name: Japanese
      de:
        flag: de
        name: German
      pt:
        flag: pt
        name: Portuguese
      pt_BR:
        flag: br
        name: Brazilian Portuguese
      ru:
        flag: ru
        name: Russian
      ko:
        flag: kr
        name: Korean
      sk:
        flag: sk
        name: Slovak
      sl:
        flag: si
        name: Slovenian
      nl:
        flag: nl
        name: Dutch

Where the first key is the abbreviation of the language to use, "flag" is which flag
icon is displayed in the user interface for choosing the language, and "name" is the
displayed name for that language. The mapping above shows all of the current languages
supported by Superset, but please note that different languages have different levels
of completion and support at this time.

Custom Row Level Security Filters to Superset
=============================================
If you add new datasources, tables, or datasets to Superset, you may want to add new
row level security filters to restrict access to that data based on things like user
roles, or organization. To apply custom row level security filters to Superset,
you can use the patch `superset-row-level-security`. This patch expects a list of python
dictionaries with the following structure:

.. code-block:: yaml

    superset-row-level-security: |
        {
            "schema": "{{ASPECTS_XAPI_DATABASE}}",
            "table_name": "{{ASPECTS_XAPI_TABLE}}",
            "role_name": "{{SUPERSET_ROLES_MAPPING.instructor}}",
            "group_key": "{{SUPERSET_ROW_LEVEL_SECURITY_XAPI_GROUP_KEY}}",
            "clause": {% raw %}'{{can_view_courses(current_username(), "splitByChar(\'/\', course_id)[-1]")}}',{% endraw %}
            "filter_type": "Regular",
        },

You can find more information about Superset RLSF in the `Superset documentation <https://superset.apache.org/docs/security/#row-level-security>`_.

Custom Jinja Filters
====================
Aspects allows to add custom jinja filters to Superset. To do so, you can use the patch
`superset-jinja-filters`. which you can use to define new filters like the **can_view_courses**
clause used above. This patch expects valid python code, and the function should return an SQL 
fragment as a string, e.g:

.. code-block:: yaml

    superset-jinja-filters: |
        ALL_COURSES = "1 = 1"
        NO_COURSES = "1 = 0"
        def can_view_courses(username, field_name="course_id"):
            """
            Returns SQL WHERE clause which restricts access to the courses the current user has staff access to.
            """
            from superset.extensions import security_manager
            user = security_manager.get_user_by_username(username)
            if user:
                user_roles = security_manager.get_user_roles(user)
            else:
                user_roles = []

            # Users with no roles don't get to see any courses
            if not user_roles:
                return NO_COURSES

            # Superusers and global staff have access to all courses
            for role in user_roles:
                if str(role) == "Admin" or str(role) == "Alpha":
                    return ALL_COURSES

            # Everyone else only has access if they're staff on a course.
            courses = security_manager.get_courses(username)

            # TODO: what happens when the list of courses grows beyond what the query will handle?
            if courses:
                course_id_list = ", ".join(f"'{course_id}'" for course_id in courses)
                return f"{field_name} in ({course_id_list})"
            else:
                # If you're not course staff on any courses, you don't get to see any.
                return NO_COURSES

Once the custom jinja filter is defined is necessary to register it using **SUPERSET_EXTRA_JINJA_FILTERS** 
in the config.yaml file. It's a dictionary that expects a key for the name of the filter and the name of underlying function:

.. code-block:: yaml

    SUPERSET_EXTRA_JINJA_FILTERS:
        can_view_courses: can_view_courses


Custom Superset Roles
=====================
Aspects allows to add custom Superset roles. To do so, you can use the patch
`superset-extra-roles` which you can use to define new roles. This patch expects valid JSON objects
with the following structure:

.. code-block:: yaml

    ## Add a comma before the new role
    superset-extra-roles: |
        ,
        {
            "name": "my_custom_role",
            "permissions": [
                {
                    "name": "can_read",
                    "view_menu": {
                        "name": "Superset",
                        "category": "Security",
                        "category_label": "Security",
                        "category_icon": "fa-bar-chart",
                    },
                }
            ],
        }

Once you have defined your custom roles you probably want to assign them to users
automatically at login. You can do so by using the patch **superset-sso-assignment-rules**.
This patch expects valid python code and should return a list of roles:

.. code-block:: python

    if "edunext" in username:
        return ["admin"]
    else:
        return []

In the context of the code you can access to the following variables:

- **self**: OpenEdxSsoSecurityManager instance.
- **username**: username of the user.
- **decoded_access_token**: decoded JWT token of the user (can be used to perform API calls)

Custom Clickhouse SQL
=====================

Aspects allows to add custom Clickhouse SQL at initialization. To do so, you can use the patch
`clickhouse-extra-sql` which you can use to define new SQL. This patch expects valid Clickhouse SQL
code:

.. code-block:: yaml
    
    # Make sure to add a semi-colon at the end of every SQL statements
    clickhouse-extra-sql: |
        CREATE TABLE IF NOT EXISTS {{ASPECTS_XAPI_DATABASE}}.{{ASPECTS_XAPI_TABLE}} (
            ...
        ) ENGINE = MergeTree()
        PARTITION BY toDate(timestamp)
        ORDER BY (timestamp, uuid)
        SETTINGS index_granularity = 8192;
        
        SELECT * from {{ASPECTS_XAPI_DATABASE}}.{{ASPECTS_XAPI_TABLE}} LIMIT 1;

Extending DBT
=============

To extend the DBT project you can use the following tutor settings:

- **DBT_REPOSITORY**: A git repository URL to clone and use as the DBT project.
- **DBT_BRANCH**: The branch to use when cloning the DBT project.
- **DBT_PROJECT_DIR**: The directory to use as the DBT project.
- **EXTRA_DBT_PACKAGES**: A list of python packages for the DBT project to install.
- **DBT_ENABLE_OVERRIDE**: Whether to enable the DBT project override feature, which allows you
  to override the dbt_project.yml and packages.yml files. Those files can be modified by using
  the following tutor patches: `dbt-packages` and `dbt-project`.
