.. _dbt:

data build tool (dbt)
*********************

``dbt`` is an open source, command-line tool managed by `dbtlabs`_ for generating and maintaining data transformations.

``dbt`` allows engineers to transform data by writing ``SELECT`` statements that reflect business logic which ``dbt``
materializes into tables and views that can be queried efficiently.

``dbt`` also allows engineers to modularize and re-use their transformation code using "packages" that can be shared
across projects or organizations.

dbt in Aspects
##############

Aspects uses the `aspects-dbt`_ package to define the transforms used by the Aspects project. This package creates and
manages macros and materialized views for data tables stored in `Clickhouse`_, and provides some tests.

Operators may create and install their own ``dbt`` packages; see `dbt extensions`_ for details.

`tutor-contrib-aspects`_ also provides a "do" command to proxy running `dbt commands`_ against your deployment; run
``tutor [dev|local] do dbt --help`` for details.

References
##########

* `dbtlabs`_: ``dbt`` documentation
* `dbt-core`_: core ``dbt`` package
* `aspects-dbt`_: Aspects dbt transforms
* `tutor-contrib-aspects`_: Aspects Tutor plugin

.. _aspects-dbt: https://github.com/openedx/aspects-dbt/#aspects-dbt
.. _clickhouse: clickhouse.html
.. _dbtlabs: https://docs.getdbt.com/
.. _dbt-core: https://github.com/dbt-labs/dbt-core
.. _dbt commands: https://docs.getdbt.com/reference/dbt-commands
.. _dbt extensions: ../how-tos/dbt_extensions.html
.. _tutor-contrib-aspects: https://github.com/openedx/tutor-contrib-aspects
