.. _clickhouse-sql:

Clickhouse extra SQL
###################################

You can execute extra Clickhouse SQL at initialization. To do so, you need to use the
patch `clickhouse-extra-sql`. This patch expects valid Clickhouse SQL code:

.. code-block:: yaml
    
    # Make sure to add a semi-colon at the end of every SQL statements
    clickhouse-extra-sql: |
        CREATE TABLE IF NOT EXISTS {{ASPECTS_XAPI_DATABASE}}.{{ASPECTS_XAPI_TABLE}} (
            ...
        ) ENGINE = MergeTree()
        PARTITION BY toDate(timestamp)
        ORDER BY (timestamp, uuid)
        SETTINGS index_granularity = 8192;
        
        SELECT * from {{ASPECTS_XAPI_DATABASE}}.{{ASPECTS_XAPI_TABLE}} LIMIT 1;
