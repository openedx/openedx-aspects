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

Superset Custom Row Level Security Filters
=============================================

If you add new Databases, tables, or Datasets to Superset, you may want to add new
row level security filters to restrict access to the data based on things like user
roles, or organization.

See :ref:`superset-row-level-security` for more information.

Superset Custom Jinja Filters
=============================

Aspects allows to add custom jinja filters to Superset which can be used to generate SQL
statements based on the current user role or any given input.

In Aspects, those are used to filter the data based on the user course access.

See :ref:`superset-jinja-filters` for more information.

Superset Custom Roles
=====================

Aspects allows to add custom Superset roles which can be seen as groups of permissions,
those are automatically associated at login. 

See :ref:`superset-roles` for more information.

Custom Clickhouse SQL
=====================

Aspects allows to add custom Clickhouse SQL at initialization. 

See :ref:`clickhouse-sql` for more information.

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
