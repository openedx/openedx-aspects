.. _dbt-extensions:

Extending dbt
*************

As noted in :ref:`dbt`, you can install your own custom ``dbt`` package to apply your own transforms to the event data
in Aspects.

**Step 1. Create your dbt package**

See `Building dbt packages`_ for details.

**Step 2. Link to aspects-dbt**

Aspects charts depend on the transforms in `aspects-dbt`_, so it's important that your ``dbt`` package also installs
`aspects-dbt`_.

To do this, add a ``packages.yml`` file to your ``dbt`` package at the top level, with content like this:

.. code-block:: yaml

  packages:
    - git: "https://github.com/openedx/aspects-dbt.git"
      revision: v2.2

**Step 3. Install and run your dbt package**

Update the following Tutor variables to use your package instead of the Aspects default.

- **DBT_REPOSITORY**: A git repository URL to clone and use as the ``dbt`` project.

  Default: ``https://github.com/openedx/aspects-dbt``
- **DBT_BRANCH**: The branch to use when cloning the ``dbt`` project.

  Default: varies between versions of Aspects.
- **DBT_PROJECT_DIR**: The directory to use as the ``dbt`` project.

  Default: ``aspects-dbt``
- **EXTRA_DBT_PACKAGES**: Add any python packages that your ``dbt`` project requires here.

  Default: ``[]``
- **DBT_PROFILE_\***: variables used in the Aspects ``dbt/profiles.yml`` file, including several Clickhouse connection settings.

Once your package is configured in Tutor, you can run ``dbt`` commands directly on your deployment; run ``tutor [dev|local] do dbt --help`` for details.

.. _aspects-dbt: https://github.com/openedx/aspects-dbt
.. _Building dbt packages: https://docs.getdbt.com/guides/building-packages
