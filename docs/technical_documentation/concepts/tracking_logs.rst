.. _tracking-logs:

Tracking Logs
*************

The event-tracking library tracks context-aware semi-structured system events. It captures
and stores events with nested data structures in order to truly take advantage of schemaless
data storage systems.

This library produces trackings logs which can be stored in multiple destinations.

In Aspects those trackings logs are captured by Vector and stored in the Clickhouse database.
Those are not really used by the Aspects plugin, but they are there for custom reporting
capabilities.

Note that we use xAPI statements over tracking logs, because those store a lot of
PII data, such as usernames, email addresses, browser data, and IP addresses;
while xAPI statements are more generic.
