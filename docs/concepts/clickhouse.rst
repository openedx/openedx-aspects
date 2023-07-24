Clickhouse
##################################

ClickHouse is a high-performance, column-oriented SQL database management system (DBMS) 
for online analytical processing (OLAP). It is used as the backend storage for the Aspects 
project that powers superset.

Clickhouse Migrations
****************************

Clickhouse migrations are handled by `Alembic <https://alembic.sqlalchemy.org/en/latest/>`_.
To learn more about `Alembic`_ and how to use it, please refer to the ADR :ref:`clickhouse-migrations`..

Clickhouse Tables
************************

Clickhouse tables store the raw data ingested by the Aspects project. Those are used to split the data
by domains such as video and problems events, and to store the data in a columnar format.

Clickhouse Materialized Views
*************************************

ClickHouse materialized views are used to perform transformations on the raw data stored in the tables
in near real time, to make it more suitable for reporting and analytical purposes.
