.. _remote-clickhouse:

Connect to external Clickhouse database
***************************************

Connect to Clickhouse Cloud
###########################

Aspects can be connected with Clickhouse Cloud following the steps below:


1. Disable the Clickhouse service:

.. code-block:: yaml

    RUN_CLICKHOUSE: false

2. Create a Clickhouse Cloud account and a cluster, and get the credentials.

3. Once you get the credentials, set the following variables in your **config.yaml** file:

.. code-block:: yaml

    CLICKHOUSE_HOST: <clickhouse_host>
    CLICKHOUSE_SECURE_CONNECTION: true
    CLICKHOUSE_ADMIN_USER: <clickhouse_admin_user>
    CLICKHOUSE_ADMIN_PASSWORD: <clickhouse_admin_password>

4. Apply the changes by running the following command:

.. code-block:: bash

    tutor config save

5. Depending on how you have configured your ClickHouse user, you may need to bootstrap the default
   user with permissions required to run the Aspects init. The current permissions required to
   successfully init are listed below, but please note that you may need to replace the users and
   databases based on your configuration:

.. code-block:: sql

    CREATE USER IF NOT EXISTS ch_admin IDENTIFIED WITH sha256_password BY '-your-password-';

    GRANT CREATE USER, ALTER USER, CREATE FUNCTION, DROP FUNCTION, CREATE DATABASE, CREATE TEMPORARY TABLE, S3
        ON *.* to ch_admin;

    -- Needed for running cluster sync operations on clustered environments
    GRANT SYSTEM SYNC REPLICA ON *.* TO ch_admin;

    CREATE DATABASE IF NOT EXISTS xapi;
    GRANT ALTER UPDATE, ALTER COLUMN, DROP COLUMN, RENAME COLUMN, ALTER RENAME COLUMN, CREATE DICTIONARY,
          DROP DICTIONARY, DROP TABLE, CREATE TABLE, CREATE VIEW, DROP VIEW, SELECT, INSERT, DELETE, OPTIMIZE,
          dictGet
      ON xapi.* to ch_admin WITH GRANT OPTION;

    CREATE DATABASE IF NOT EXISTS openedx;
    GRANT ALTER UPDATE, ALTER COLUMN, DROP COLUMN, RENAME COLUMN, ALTER RENAME COLUMN, CREATE DICTIONARY,
          DROP DICTIONARY, DROP TABLE, CREATE TABLE, CREATE VIEW, DROP VIEW, SELECT, INSERT, DELETE, OPTIMIZE,
          dictGet
      ON openedx.* to ch_admin WITH GRANT OPTION;

    CREATE DATABASE IF NOT EXISTS event_sink;
    GRANT ALTER UPDATE, ALTER COLUMN, DROP COLUMN, RENAME COLUMN, ALTER RENAME COLUMN, CREATE DICTIONARY,
          DROP DICTIONARY, DROP TABLE, CREATE TABLE, CREATE VIEW, DROP VIEW, SELECT, INSERT, DELETE, OPTIMIZE,
          dictGet
      ON event_sink.* to ch_admin WITH GRANT OPTION;

    CREATE DATABASE IF NOT EXISTS reporting;
    GRANT ALTER UPDATE, ALTER COLUMN, DROP COLUMN, RENAME COLUMN, ALTER RENAME COLUMN, CREATE DICTIONARY,
          DROP DICTIONARY, DROP TABLE, CREATE TABLE, CREATE VIEW, DROP VIEW, SELECT, INSERT, DELETE, OPTIMIZE,
          dictGet
      ON reporting.* to ch_admin WITH GRANT OPTION;

    -- These are used for the ClickHouse status reports in the operator dashboard
    GRANT SELECT ON system.asynchronous_metrics TO ch_admin WITH GRANT OPTION;
    GRANT SELECT ON system.disks TO ch_admin WITH GRANT OPTION;
    GRANT SELECT ON system.events TO ch_admin WITH GRANT OPTION;
    GRANT SELECT ON system.metrics TO ch_admin WITH GRANT OPTION;
    GRANT SELECT ON system.replication_queue TO ch_admin WITH GRANT OPTION;

    -- This is used in SQL query performance testing
    GRANT SELECT ON system.query_log to ch_admin WITH GRANT OPTION;


6. Restart your local or production environment. After this change, you need to run the initialization
   tasks. To do so, run the following command according to your environment:

.. code-block:: bash

    tutor [local|dev|k8s] do init -l aspects

Connect to on Premise Clickhouse
################################

Aspects provide several configuration parameters that can be customized to connect to an on premise
Clickhouse instance. To do so, set the following variables in your **config.yaml** file:

.. code-block:: yaml

    CLICKHOUSE_HOST: <clickhouse_host>
    CLICKHOUSE_SECURE_CONNECTION: true|false
    CLICKHOUSE_ADMIN_USER: <clickhouse_admin_user>
    CLICKHOUSE_ADMIN_PASSWORD: <clickhouse_admin_password>
    CLICKHOUSE_HOST_HTTP_PORT: <clickhouse_http_port> # defaults to 8123 or 8443 for secure TLS connections
    CLICKHOUSE_HOST_NATIVE_PORT: <clickhouse_client_port> # default to 9000 | 9440 used by initialization tasks

Additionally, there are some other variables that are calculated based on the above variables, but
can be customized if needed:

.. code-block:: yaml

    CLICKHOUSE_REPORT_SQLALCHEMY_URI: <clickhouse_url> # used by superset to perform queries
    CLICKHOUSE_ADMIN_SQLALCHEMY_URI: <clickhouse_url> # used by initialization tasks to create tables and views
