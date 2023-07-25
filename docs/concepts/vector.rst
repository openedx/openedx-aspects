Vector
##################################

Vector is lightweight and ultra-fast tool for building observability pipelines.
In the Aspects project it can optionally be used as a replacement for Ralph to capture xAPI learner statements in the ClickHouse database, and/or as a way to store raw tracking log statements. It can be used as a general purpose log collector and forwarder.
a general purpose log collector.


Vector Components
-----------------

Vector consists of the following components:

- `Sources <https://vector.dev/docs/reference/sources/>`_ - Collects data from a source and sends it to Vector.
- `Transforms <https://vector.dev/docs/reference/transforms/>`_ - Modifies events as they pass through Vector.
- `Sinks <https://vector.dev/docs/reference/sinks/>`_ - Sends events to a destination.

Vector can be deployed in two roles:

- `Agent <https://vector.dev/docs/setup/deployment/roles/#agent>`_ - Collects, transforms, and sends data to a destination.
- `Aggregator <https://vector.dev/docs/setup/deployment/roles/#aggregator>`_ - Receives data from Vector agents and sends it to a destination.


We use the role `Agent` to collect tracking logs and xAPI events from the lms and send it to the clickhouse sink.

To learn more about Vector, see the `documentation <https://vector.dev/docs/>`_.
