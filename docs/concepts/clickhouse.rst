Clickhouse
##################################

ClickHouse is a high-performance, column-oriented SQL database management system (DBMS) 
for online analytical processing (OLAP). It is used as the backend storage for the Aspects 
project that powers Superset.

Connect to Clickhouse Cloud
***************************

Aspects can be connected with Clickhouse Cloud following the steps below:


1. Disable the Clickhouse service:

.. code-block:: yaml

    RUN_CLICKHOUSE: false

2. Create a Clickhouse Cloud account and a cluster, and get the credentials.

3. Once you get the credentials set the following variables in your **config.yaml** file:

.. code-block:: yaml

    CLICKHOUSE_HOST: <clickhouse_host>
    CLICKHOUSE_SECURE_CONNECTION: true
    CLICKHOUSE_ADMIN_USER: <clickhouse_admin_user>
    CLICKHOUSE_ADMIN_PASSWORD: <clickhouse_admin_password>

4. Apply the changes by running the following command:

.. code-block:: bash

    tutor config save

5. Restart your local or production environment. After this change you need to run the initialization
   tasks. To do so, run the following command according to your environment:

.. code-block:: bash

    tutor [local|dev|k8s] do init -l aspects

Connect to on Premise Clickhouse
********************************

Aspects provide several configuration parameters that can be customized to connect to an on premise
Clickhouse instance. To do so, set the following variables in your **config.yaml** file:

.. code-block:: yaml

    CLICKHOUSE_HOST: <clickhouse_host>
    CLICKHOUSE_SECURE_CONNECTION: true|false
    CLICKHOUSE_ADMIN_USER: <clickhouse_admin_user>
    CLICKHOUSE_ADMIN_PASSWORD: <clickhouse_admin_password>
    CLICKHOUSE_CLIENT_PORT: <clickhouse_client_port> # default to 9000 | 9440 used by initialization tasks
    CLICKHOUSE_PORT: <clickhouse_port> # default to 8123 | 8443 used by other services such as ralph and the lms

Additionally there are some other variables that are calculated based on the above variables, but
can be customized if needed:

.. code-block:: yaml

    CLICKHOUSE_REPORT_SQLALCHEMY_URI: <clickhouse_url> # used by superset to perform queries
    CLICKHOUSE_ADMIN_SQLALCHEMY_URI: <clickhouse_url> # used by initialization tasks to create tables and views

Clickhouse Migrations
****************************

Clickhouse migrations are handled by `Alembic <https://alembic.sqlalchemy.org/en/latest/>`_.
To learn more about `Alembic`_ and how to use it, please refer to the ADR :ref:`clickhouse-migrations`.

Clickhouse Structure
************************

Clickhouse is used to store the data ingested by the Aspects project via Ralph or Vector. The data is stored
in a single database controlled by the variable **ASPECTS_XAPI_DATABASE** and a single table controlled by
the variable **ASPECTS_RAW_XAPI_TABLE**:

.. code-block:: yaml

    ASPECTS_XAPI_DATABASE: "xapi"
    ASPECTS_RAW_XAPI_TABLE: "xapi_events_all"

From here, the main table is split into different tables and views for performance and reporting purposes:

- Tables group xAPI statements by type (video, problem, enrollment, etc.)

- Materialized views transform the xAPI statements into tables that are structured for performance.

- Views are created on top of these tables to generate specific reports such as "Video Views" 
  and "Enrollments by Day"
