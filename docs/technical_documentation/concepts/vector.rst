.. _vector:

Vector
******

Vector is lightweight and ultra-fast tool for building observability pipelines.
As of Aspects version 5.0, Vector is the default tool used to
capture xAPI learner statements in the ClickHouse database, and/or as a way to
store raw tracking log statements. It can be used as a general purpose log collector
and forwarder.


Vector Components
#################

Vector consists of the following components:

- `Sources <https://vector.dev/docs/reference/configuration/sources/>`_ - Collects data from a source
  and sends it to Vector.
- `Transforms <https://vector.dev/docs/reference/configuration/transforms//>`_ - Modifies events as they
  pass through Vector.
- `Sinks <https://vector.dev/docs/reference/configuration/sinks/>`_ - Sends events to a destination.

Vector can be deployed in two roles:

- `Agent <https://vector.dev/docs/setup/deployment/roles/#agent>`_ - Collects, transforms,
  and sends data to a destination.
- `Aggregator <https://vector.dev/docs/setup/deployment/roles/#aggregator>`_ - Receives data
  from Vector agents and sends it to a destination.

Aspects uses both roles, depending on the deployment type:

- In Tutor ``local`` and ``dev`` (Docker Compose) deployments a single ``vector`` container runs as an
  Agent. It reads the Docker logs of the LMS, CMS, worker, and job containers, transforms the events,
  and writes them directly to the configured sinks.
- In Tutor ``k8s`` deployments a ``vector-agent`` DaemonSet runs one Agent pod per node. The agents
  read the Kubernetes pod logs for the Open edX containers and forward the raw log lines to a
  ``vector-aggregator`` StatefulSet. The aggregator does the parsing and transforms and writes to the
  configured sinks, using a persistent volume for disk buffers so events are not lost if a sink is
  temporarily unavailable.

Aspects has Sources configured for xAPI logging statements (generated in-process by
event-routing-backends), and for tracking log statements. Each of these have their own Transforms,
which validate that the log statements are JSON and forward them to Sinks which store them in
ClickHouse tables.

Those tables are controlled by the variables:

.. code-block:: yaml

    ASPECTS_VECTOR_DATABASE: "openedx"
    ASPECTS_VECTOR_RAW_TRACKING_LOGS_TABLE: "_tracking"
    ASPECTS_RAW_XAPI_TABLE: "xapi_events_all"

Optionally, xAPI events can also be written to an S3 compatible bucket at the same time they are
written to ClickHouse. This provides a backup that can be restored with the
``xapi_block_storage_backfill`` command, see :ref:`backfill_s3` for details.

Configuration options for both the sinks and the aggregator are described in the
:ref:`Quick Start - Vector guide <quick-start-vector>`.

To learn more about Vector, see the `Vector documentation <https://vector.dev/docs/>`_.
