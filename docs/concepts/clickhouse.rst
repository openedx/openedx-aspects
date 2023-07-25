Clickhouse
##################################

ClickHouse is a high-performance, column-oriented SQL database management system (DBMS) 
for online analytical processing (OLAP). It is used as the backend storage for the Aspects 
project that powers Superset.

Aspects is compatible with Clickhouse Cloud and on premise Clickhouse instances.

See :ref:`remote-clickhouse` for more information.

Clickhouse Migrations
****************************

Clickhouse migrations are handled by `Alembic <https://alembic.sqlalchemy.org/en/latest/>`_.
To learn more about `Alembic`_ and how to use it, please refer to the ADR :ref:`clickhouse-migrations`.

Clickhouse Structure
************************

Clickhouse is used to store the data ingested by the Aspects project via Ralph or Vector. The data is stored
in a single database controlled by the variable **ASPECTS_XAPI_DATABASE**, and a single table controlled by
the variable **ASPECTS_RAW_XAPI_TABLE**:

.. code-block:: yaml

    ASPECTS_XAPI_DATABASE: "xapi"
    ASPECTS_RAW_XAPI_TABLE: "xapi_events_all"

From here, the main table is split into different tables and views for performance and reporting purposes:

- Tables group xAPI statements by type (video, problem, enrollment, etc.)

- Materialized views transform the xAPI statements into tables that are structured for performance.

- Views are created on top of these tables to generate specific reports such as "Video Views" 
  and "Enrollments by Day".
