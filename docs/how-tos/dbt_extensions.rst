.. _dbt-extensions:

Extending dbt
*************

As noted in :ref:`dbt`, you can install your own custom dbt package to apply your own transforms to the event data
in Aspects.

This guide demonstrates how to create and use a custom dbt package in Aspects by building the `aspects-dbt-example`_
repo. See `aspects-dbt-example#1`_ to follow along with each of these steps.

See `Building dbt packages`_ and `Best practice guides`_ for dbt's official documentation.

Step 0. Install dbt core
========================

The easiest way to install dbt core is to use pip in a python3 virtual environment.

See `aspects/requirements.txt`_ for the specific package versions used by Aspects.

.. code-block:: bash

  # Create and activate a python3 virtual environment
  python3 -m venv venv
  source venv/bin/activate
  pip install --upgrade pip

  # Install the dbt package versions used by Aspects
  pip install dbt-clickhouse==1.7.1 dbt-core==1.7.0

See `Install dbt`_ for more ways to install dbt.

Step 1. Initialize your dbt package
===================================

Create a new dbt package by following the prompts given by the ``dbt init`` tool.

.. code-block:: bash

  dbt init
  # Enter a name for your project (letters, digits, underscore): aspects_dbt_example
  # Which database would you like to use? [1] clickhouse

  ls aspects_dbt_example
  # analyses/  dbt_project.yml  macros/  models/  README.md  seeds/  snapshots/  tests/


See `About dbt init`_ for more options.

Step 2. Use the Aspects profile
===============================

Update the generated ``dbt_project.yml`` to use the ``aspects`` profile:

.. code-block:: yaml

  # This setting configures which "profile" dbt uses for this project.
  profile: 'aspects'

Step 3. Link to aspects-dbt
===========================

Aspects charts depend on the transforms in `aspects-dbt`_, so it's important that your dbt package also installs
the same version of `aspects-dbt`_ as your version of the Aspects Tutor plugin.

To do this, add a ``packages.yml`` file to your dbt package at the top level where:

* ``git`` url matches the default value of ``DBT_REPOSITORY`` in `tutor-contrib-aspects plugin.py`_
* ``revision`` matches the default value of ``DBT_BRANCH`` in `tutor-contrib-aspects plugin.py`_

.. code-block:: yaml

  packages:
    - git: "https://github.com/openedx/aspects-dbt.git"
      revision: v3.4.1

Step 4. Add your custom transforms
==================================

Here is where you will need an understanding of dbt, Clickhouse, Aspects' data schemas, and the specific transforms you
want to create.

.. note:: You can use Aspects to debug your custom SQL:

  #. Login to Superset as an Open edX superuser.
  #. Using the menus at the top of the page, navigate to the "SQL -> SQL Lab" UI.
  #. Browse the schemas and run read-only SQL queries on your data.

For this tutorial, we added a new model which will be materialized by dbt into a view in Clickhouse.
Our new model calculates the average number of attempts made by users on each problem by referencing the
`int_problem_results` model created by the base aspects-dbt package (see `dbt ref`_):

.. code-block::

  select
      problem_id, AVG(attempts) as average_attempts
  from
      (
          select
              problem_id,
              max(attempts) as attempts
          from
              {{ ref('int_problem_results') }}
          group by
              actor_id,
              problem_id
      )
  group by problem_id

Next, make sure your model is configured in the ``db_project.yml``. If you forget this step, dbt will warn you when
running your package.

.. code-block:: yaml

   models:
    problem_responses:
      # Config indicated by + and applies to all files under models/problem_responses/
      +materialized: view


See `About dbt models`_ to learn more.

Step 5. Add tests
=================

Writing tests for your transforms is important:  not only can tests validate and document your intended changes, they
can be used to guard against data edge cases and regressions from future code changes.

dbt generic tests are defined as SQL files, where the goal of the SQL statement is to return zero records.

Because our new `average_attempts` model aggregates on `actor_id` and `problem_id`, it should only have 1 entry for each
`problem_id`. So our test can be:

.. code-block: sql

  -- average_attempts should only have one record for each problem_id.
  select
      count(*) as num_rows
  from
      {{ ref('average_attempts') }}
  group by
      problem_id
  having num_rows > 1


See `Writing data tests`_ for more examples.


Step 6. Install and use your dbt package
========================================

Once you've pushed all the changes to your custom dbt package repo, now we're ready to use it.

Use ``tutor config save`` to update the following Tutor variables to use your custom package instead of the Aspects
default.

- ``DBT_REPOSITORY``: A git repository URL to clone and use as the dbt project.

  Set this to the URL for your custom dbt package.

  Default: ``https://github.com/openedx/aspects-dbt``
- ``DBT_BRANCH``: The branch to use when cloning the dbt project.

  Set this to the hash/branch/tag of the custom dbt package that you wish to use.

  Default: varies between versions of Aspects.
- ``EXTRA_DBT_PACKAGES``: Add any python packages that your dbt project requires here.

  Default: ``[]``
- ``DBT_PROFILE_*``: variables used in the Aspects ``dbt/profiles.yml`` file, including several Clickhouse connection settings.

- ``DBT_SSH_KEY``: The private SSH key to use when cloning the dbt project. Only necessary if you are using a private repository.

Once your package is configured in Tutor, you can run dbt commands directly on your deployment.

See `dbt commands`_ for a full list of available commands.

.. code-block:: bash

  # Build and test your package
  tutor dev do dbt -c "build"

  # Deploy your customizations
  tutor dev do dbt -c "run"

  # Run tests on the data
  tutor dev do dbt -c "test"


Step 7. Troubleshooting
=======================

You may need to repeat steps 4-6 a few times to resolve any warnings or errors that dbt reports with your package.

Don't forget to push your changes to your repo before running the tutor dbt command: it fetches a clean copy of your
configured package repo + branch each time it runs.

See `dbt debugging`_ for more information on how to debug issues with your package.


References
##########

* `Building dbt packages`_: dbt's guide to building packages
* `Best practice guides`_: dbt's guidelines on project structure, style, and setup.
* `About dbt models`_: dbt's guide to creating SQL or Python model transforms
* `Writing data tests`_: dbt's guide to writing package tests
* `dbt commands`_: list of all dbt commands
* `dbt debugging`_: guide for debugging issues with dbt
* `aspects-dbt`_: Aspects' dbt package
* `aspects-dbt-example`_: the demo custom dbt package used in this tutorial.
* `eduNEXT/dbt-aspects-unidigital`_: a real custom dbt package running in production Aspects

.. _aspects-dbt: https://github.com/openedx/aspects-dbt
.. _aspects-dbt-example: https://github.com/open-craft/aspects-dbt-example
.. _aspects-dbt-example#1: https://github.com/open-craft/aspects-dbt-example/pull/1
.. _aspects/requirements.txt: https://github.com/openedx/tutor-contrib-aspects/blob/main/tutoraspects/templates/aspects/build/aspects/requirements.txt
.. _About dbt init: https://docs.getdbt.com/reference/commands/init
.. _About dbt models: https://docs.getdbt.com/docs/build/models
.. _Best practice guides: https://docs.getdbt.com/best-practices
.. _dbt commands: https://docs.getdbt.com/reference/dbt-commands
.. _dbt debugging: https://docs.getdbt.com/guides/debug-errors
.. _dbt ref: https://docs.getdbt.com/reference/dbt-jinja-functions/ref
.. _eduNEXT/dbt-aspects-unidigital: https://github.com/eduNEXT/dbt-aspects-unidigital
.. _Building dbt packages: https://docs.getdbt.com/guides/building-packages
.. _Install dbt: https://docs.getdbt.com/docs/core/installation-overview
.. _Writing data tests: https://docs.getdbt.com/best-practices/writing-custom-generic-tests
.. _tutor-contrib-aspects plugin.py: https://github.com/openedx/tutor-contrib-aspects/blob/main/tutoraspects/plugin.py
