12. Clickhouse vs dbt
#####################

Status
******

Accepted

Context
*******

Most of the use cases for Aspects require complex transformations to be performed on the data stored in
:ref:`clickhouse` before it can be displayed in :ref:`superset`. :ref:`xapi-concepts` is a good format for communicating
learning-related events as they happen, but in order to analyse them and draw conclusions for what these events signify
over time, Aspects needs views of the data that are designed specifically for the queries performed.

:ref:`clickhouse` provides some features for transforming complex data, but creating efficient views and managing schema
changes over time can be difficult. Plus, some of these features (like named collections) are not available on all
hosted :ref:`clickhouse` services.

This ADR describes the division of responsibilities in Aspects between the :ref:`clickhouse` database and :ref:`dbt`, a
data transformation tool.

Decision
********

**Store in Clickhouse, transform with dbt**

Raw event and event sink data tables should continue to be created using :ref:`clickhouse-migrations`.

Data transformations on this raw data should be made with :ref:`dbt`, including:

* materialized views
* partitions
* dictionaries
* fields extracted from event JSON

Note that while we use dbt to manage these data transformations, the transformations themselves 

Consequences
************

#. Contribute upstream to `dbt-clickhouse`_ where support for required features is missing.
#. Move transformations made by the "query" and "dataset" Aspects Superset assets to `aspects-dbt`_.
#. Move dictionaries and partitions originally created using :ref:`clickhouse-migrations` to `aspects-dbt`_.
#. Squash remaining alembic migrations.

Rejected Alternatives
*********************

**Use native Clickhouse transforms instead of dbt**

This option was rejected for maintainability reasons:  :ref:`dbt` was designed to manage data transformations with its
package and test framework, and so is more modular and reusable, and better suited to Aspects' long-term goals.

References
**********

* `tutor-contrib-aspects#546`_ Only recreate materialized views when necessary
* `tutor-contrib-aspects#565`_ Add dictionary support to dbt-clickhouse

.. _aspects-dbt: https://github.com/openedx/aspects-dbt
.. _dbt-clickhouse: https://github.com/ClickHouse/dbt-clickhouse
.. _tutor-contrib-aspects#546: https://github.com/openedx/tutor-contrib-aspects/issues/546
.. _tutor-contrib-aspects#565: https://github.com/openedx/tutor-contrib-aspects/issues/565
