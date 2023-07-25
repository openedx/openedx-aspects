.. _dbt-extensions:

DBT extensions
#####################

To extend the DBT project, you can use the following Tutor variables:

- **DBT_REPOSITORY**: A git repository URL to clone and use as the DBT project.
- **DBT_BRANCH**: The branch to use when cloning the DBT project.
- **DBT_PROJECT_DIR**: The directory to use as the DBT project.
- **EXTRA_DBT_PACKAGES**: A list of python packages for the DBT project to install.
- **DBT_ENABLE_OVERRIDE**: Whether to enable the DBT project override feature, which allows you
  to override the **dbt_project.yml** and **packages.yml** files. Those files can be modified by using
  the following tutor patches: `dbt-packages` and `dbt-project`.
