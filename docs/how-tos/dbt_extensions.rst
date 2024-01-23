.. _dbt-extensions:

Extending dbt
*************

As noted in `Concepts: dbt <dbt concepts>`_, you can install your own custom dbt packages to apply your own transforms
to the event data in Aspects.

To change which dbt packages are installed, use the following Tutor variables:

- **EXTRA_DBT_PACKAGES**: A list of pip dbt packages for Aspects to install. Add your custom dbt packages here.
- **DBT_REPOSITORY**: A git repository URL to clone and use as the main Aspects dbt project.
- **DBT_BRANCH**: The branch to use when cloning ``DBT_REPOSITORY``.

To change how the ``dbt`` packages are configured, use these Tutor variables:

- **DBT_PROFILE_\***: variables used in the ``dbt/profiles.yml`` file, including several Clickhouse connection settings


.. _dbt concepts: ../concepts/dbt.html
