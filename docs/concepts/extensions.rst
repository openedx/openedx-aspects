.. _extensions:

Aspects Extensions
#####################

Aspects is a project that comes with a set of extensions that can be used to
extend the different parts of the project.

Superset Assets
================

Aspects allows site operators to programatically define custom Superset assets, such as 
Databases, Datases, Slices or Dashboard, and override default ones.

See :ref:`superset-extra-assets` for more information.

Superset Language
===================================

Superset localization is a work in progress, but you can change the default language and
set alternate languages from the currently supported list.

See :ref:`superset-language-settings` for more information.

Custom Row Level Security Filters to Superset
=============================================
If you add new Databases, tables, or Datasets to Superset, you may want to add new
row level security filters to restrict access to the data based on things like user
roles, or organization.

See :ref:`superset-row-level-security` for more information.

Custom Jinja Filters
====================
Aspects allows to add custom jinja filters to Superset which can be used to generate SQL
statements based on the current user role or any given input.

In Aspects, those are used to filter the data based on the user course access.

See :ref:`superset-jinja-filters` for more information.

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
