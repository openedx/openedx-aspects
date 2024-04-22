.. _data-lifecycle-policy:

Data Lifecycle Policy
*********************

What it is
##########

Aspects is a data pipeline that captures, transforms, and aggregates tracking logs from the Open edX platform into xAPI statements and stores them in a ClickHouse database.
However, the data is not stored indefinitely by default. The data is keep for 1 year by default, but this can be adjusted by the site operator via the setting `ASPECTS_DATA_TTL_EXPRESSION` in the tutor plugin.

The setting value is a ClickHouse expression that defines the time-to-live policy (TTL) for the data. The expression is evaluated for each row in the table and should return a date. Rows with a date in the past are deleted. You can read more about the TTL policy in the ClickHouse documentation: https://clickhouse.tech/docs/en/engines/table-engines/mergetree-family/mergetree/#ttl

The data is partioned by month this way the TLL policy is applied per partition. Make sure to set the TTL policy to a date that is compatible with the partitioning policy. e.g. `ASPECTS_DATA_TTL_EXPRESSION: toDateTime(emission_time) + INTERVAL 2 MONTH` or `ASPECTS_DATA_TTL_EXPRESSION: toDateTime(emission_time) + INTERVAL 2 YEAR`.
