.. _dbt-extensions:

Extending dbt
*************

As noted in :ref:`dbt`, you can install your own custom dbt package to apply your own transforms to the event data in Aspects. 

This guide demonstrates how to create and use a custom dbt package in Aspects by building the `sample-aspects-dbt <https://github.com/openedx/sample-aspects-dbt>`_
repo. 

Step 1. Install dbt core (if needed)
====================================

The easiest way to install dbt core is to use pip in a python3 virtual environment.

See `aspects-dbt requirements.txt <https://github.com/openedx/aspects-dbt/blob/main/requirements.txt>`_ for the specific package versions used by Aspects.

.. code-block:: bash

  # Create and activate a python3 virtual environment
  python3 -m venv venv
  source venv/bin/activate
  pip install --upgrade pip

  # Install the dbt package versions used by Aspects
  pip install dbt-clickhouse==x.x.x dbt-core==x.x.x

See `Install dbt <https://docs.getdbt.com/docs/core/installation-overview>`_ for more ways to install dbt.

Step 2. Set up new dbt package
===============================

#. Create a new repository for your custom dbt package, and clone it to your local machine.

#. In the root of your local repository, create a new dbt package by following the prompts given by the ``dbt init`` tool.

   * .. code-block:: bash

      # Use the profile name from your ``dbt/profiles.yml`` file
      dbt init --profile aspects
      
      # Enter a name for your project (letters, digits, underscore):
      sample_aspects_dbt

      ls sample_aspects_dbt
      # analyses/  dbt_project.yml  macros/  models/  README.md  seeds/  snapshots/  tests/

   * ``dbt_project.yml`` should have the same `profile name <https://github.com/openedx/sample-aspects-dbt/blob/main/dbt_project.yml#L8-L9>`_ as your local profiles file

   * See `About dbt init <https://docs.getdbt.com/reference/commands/init>`_ for more options.

#. In ``dbt_project.yml``, set the location for compiled SQL to match that used by ``aspects``:

   * .. code-block:: yaml

      # directory which will store compiled SQL files
      target-path: "target"


Step 3. Link to aspects-dbt
===========================

Aspects charts depend on the transforms in `aspects-dbt`_, so it's important that your dbt package also installs the same version of aspects-dbt as your version of the Aspects Tutor plugin.

To do this, add a `packages.yml <https://github.com/openedx/sample-aspects-dbt/blob/main/packages.yml>`_ file to your dbt package at the top level where:

* ``git`` url matches the default value of ``DBT_REPOSITORY`` in `tutor-contrib-aspects plugin.py <https://github.com/openedx/tutor-contrib-aspects/blob/main/tutoraspects/plugin.py>`_
* ``revision`` matches the default value of ``DBT_BRANCH`` in `tutor-contrib-aspects plugin.py <https://github.com/openedx/tutor-contrib-aspects/blob/main/tutoraspects/plugin.py>`_

.. code-block:: yaml

  packages:
    - git: "https://github.com/openedx/aspects-dbt.git"
      revision: vX.X.X


Step 4. Test dbt connection
===========================

Before adding your custom transforms, it's a good idea to test that your dbt package can connect to the Clickhouse database and run the base transforms from aspects-dbt.

#. Run ``dbt debug`` to test the connection to your database and the validity of your dbt project.  
#. You might need to run ``dbt deps`` to install the dependencies for your package.
#. Run ``dbt run`` to run the base transforms from aspects-dbt.
#. You may need to run ``dbt run --full-refresh`` if the previous step fails.

Step 5. Create your custom transforms
=====================================

Here is where you will need an understanding of dbt, Clickhouse, Aspects' data schemas, and the specific transforms you
want to create.

If you need any python dependencies beyond what is provided by aspects-dbt, add these to a ``requirements.txt`` file at the top level of your repository.

.. note:: You can use Aspects to debug your custom SQL:

  #. Login to Superset as an Open edX superuser.
  #. Using the menus at the top of the page, navigate to the "SQL -> SQL Lab" UI.
  #. Browse the schemas and run read-only SQL queries on your data.

For this tutorial, we created two new models - `course_enrollments`_ `learner_responses <https://github.com/openedx/sample-aspects-dbt/blob/main/models/learners/learner_responses.sql>`_ and which will be materialized by dbt into a view and materialized view in Clickhouse. (more information on `materialized views <https://docs.getdbt.com/docs/build/materializations#materialized-view>`_.)


Step 6. Add dbt tests
=====================

Writing tests for your transforms is important to validate and document your intended changes, and guard against data edge cases and regressions from future code changes.

There are two types of dbt tests; `data tests <https://docs.getdbt.com/best-practices/writing-custom-generic-tests>`_ and `unit tests <https://docs.getdbt.com/docs/build/unit-tests>`_.

Run ``dbt test`` to run both the data and unit tests for your package.

Data tests
------------
Data tests can be defined in the `schema.yml <https://github.com/openedx/sample-aspects-dbt/blob/main/models/enrollment/schema.yml#L18-L20>`_ file for each model, and are used to validate properties of the data such as types, accepted values, uniqueness, and relationships between tables.

Data tests can also be defined in a `SQL file <https://github.com/openedx/sample-aspects-dbt/blob/main/tests/test_course_enrollments.sql>`_, where the goal of the SQL statement is to return zero records. 

Unit tests
----------
Unit tests are used to validate the logic of your dbt models in isolation from the underlying data. They are defined in a `unit_tests.yaml <https://github.com/openedx/sample-aspects-dbt/blob/main/models/response/unit_tests.yaml>`_ file within the ``models`` directory.

Other unit test resources:
- `dbt Unit Testing: Why You Need Them, Tutorial & Best Practices <https://dagster.io/guides/dbt-unit-testing-why-you-need-them-tutorial-best-practices>`_
- `dbt unit testing best practices <https://www.datafold.com/blog/dbt-unit-testing-definitions-best-practices-2024>`_


Step 7. Install and use your dbt package
========================================

Once you've pushed all the changes to your custom dbt package repo, now we're ready to use it.

Use ``tutor config save`` to update the following Tutor variables to use your custom package instead of the Aspects default.

  - ``DBT_REPOSITORY``: The git repository URL of your custom dbt package.

    Default: ``https://github.com/openedx/aspects-dbt``

  - ``DBT_BRANCH``: The hash/branch/tag of your custom dbt package that you wish to use.

    Default: the latest tagged version of aspects-dbt

  - ``EXTRA_DBT_PACKAGES``: Add any python packages that your dbt project requires here.

  - ``DBT_PROFILE_*``: variables used in the Aspects ``dbt/profiles.yml`` file, including several Clickhouse connection settings.

  - ``DBT_SSH_KEY``: The private SSH key to use when cloning the dbt project. Only necessary if you are using a private repository.

Once your package is configured in Tutor, you can run dbt commands directly on your deployment.

See `dbt commands <https://docs.getdbt.com/reference/dbt-commands>`_ for a full list of available commands.

.. code-block:: bash

  # Build and test your package
  tutor dev do dbt -c "build"

  # Deploy your customizations
  tutor dev do dbt -c "run"

  # Run data tests on the data
  tutor dev do dbt -c "test"

  # Run unit tests on the data
  tutor dev do dbt -c "test --selector unit_tests"

  # To push your new transformations to Superset SQL Lab
  tutor dev do import-assets


Troubleshooting
===============
- Tutor commands may need to be run with ``--only_changed False`` to force a full dbt run if you have made changes to your dbt package that are not being picked up.

- Don't forget to push your changes to your repo before running the tutor dbt command: it fetches a clean copy of your configured package repo + branch each time it runs.


References
==========

* `aspects-dbt <https://github.com/openedx/aspects-dbt>`_: Aspects' dbt package
* `sample-aspects-dbt <https://github.com/openedx/sample-aspects-dbt>`_: the demo custom dbt package used in this tutorial
* `Building dbt packages <https://docs.getdbt.com/guides/building-packages>`_: dbt's guide to building packages
* `Best practice guides <https://docs.getdbt.com/best-practices>`_: dbt's guidelines on project structure, style, and setup
* `About dbt models <https://docs.getdbt.com/docs/build/models>`_: dbt's guide to creating SQL or Python model transforms
* `dbt debugging <https://docs.getdbt.com/guides/debug-errors>`_: guide for debugging issues with dbt
* `The missing guide to debug() in dbt <https://docs.getdbt.com/blog/guide-to-jinja-debug>`_: detailed advice for debugging issues with dbt
