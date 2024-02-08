.. _dbt-extensions:

Extending dbt
*************

As noted in :ref:`dbt`, you can install your own custom dbt package to apply your own transforms to the event data
in Aspects.

**Step 1. Create your dbt package**

Create a new dbt package using `dbt init`_.

Update the generated ``dbt_project.yml`` to use the ``aspects`` profile:

.. code-block:: yaml

  # This setting configures which "profile" dbt uses for this project.
  profile: 'aspects'

See `Building dbt packages`_ for more details, and `Writing data tests`_ for how to validate your transformations.

**Step 2. Link to aspects-dbt**

Aspects charts depend on the transforms in `aspects-dbt`_, so it's important that your dbt package also installs
the same version of `aspects-dbt`_ as your Aspects Tutor plugin.

To do this, add a ``packages.yml`` file to your dbt package at the top level, where:

* ``git`` url matches the default value of ``DBT_REPOSITORY`` in `tutor-contrib-aspects plugin.py`_
* ``revision`` matches the default value of ``DBT_BRANCH`` in `tutor-contrib-aspects plugin.py`_

.. code-block:: yaml

  packages:
    - git: "https://github.com/openedx/aspects-dbt.git"
      revision: v2.2

**Step 3. Install and run your dbt package**

Update the following Tutor variables to use your package instead of the Aspects default.

- ``DBT_REPOSITORY``: A git repository URL to clone and use as the dbt project.

  Set this to the URL for your custom dbt package.

  Default: ``https://github.com/openedx/aspects-dbt``
- ``DBT_BRANCH``: The branch to use when cloning the dbt project.

  Set this to the hash/branch/tag of your custom dbt package that you wish to use.

  Default: varies between versions of Aspects.
- ``DBT_PROJECT_DIR``: The directory to use as the dbt project.

  Set this to the name of your dbt package repository.

  Default: ``aspects-dbt``
- ``EXTRA_DBT_PACKAGES``: Add any python packages that your dbt project requires here.

  Default: ``[]``
- ``DBT_PROFILE_*``: variables used in the Aspects ``dbt/profiles.yml`` file, including several Clickhouse connection settings.

- ``DBT_SSH_KEY``: The private SSH key to use when cloning the dbt project. Only necessary if you are using a private repository.

Once your package is configured in Tutor, you can run dbt commands directly on your deployment; run ``tutor [dev|local] do dbt --help`` for details.

References
##########

* `Building dbt packages`_: dbt's guide to building packages
* `Writing data tests`_: dbt's guide to writing package tests
* `aspects-dbt`_: Aspects' dbt package
* `eduNEXT/dbt-aspects-unidigital`_: a custom dbt packages running in production Aspects

.. _aspects-dbt: https://github.com/openedx/aspects-dbt
.. _dbt init: https://docs.getdbt.com/reference/commands/init
.. _eduNEXT/dbt-aspects-unidigital: https://github.com/eduNEXT/dbt-aspects-unidigital
.. _Building dbt packages: https://docs.getdbt.com/guides/building-packages
.. _Writing data tests: https://docs.getdbt.com/best-practices/writing-custom-generic-tests
.. _tutor-contrib-aspects plugin.py: https://github.com/openedx/tutor-contrib-aspects/blob/main/tutoraspects/plugin.py
