.. _quick-start-vector:

Vector
******

Installation instructions for Aspects are available on the plugin site: https://github.com/openedx/tutor-contrib-aspects

Vector is the default option to send xAPI events to Clickhouse in Aspects. It is enabled by default with the following settings:

.. code-block:: yaml

    # Default settings
    RUN_VECTOR: True
    RUN_RALPH: False
    ASPECTS_XAPI_SOURCE: vector

When ``ASPECTS_XAPI_SOURCE`` is set to ``vector``, the xAPI data will be stored in the database defined by ``ASPECTS_VECTOR_DATABASE`` (defaults to ``openedx``).


Aspects provides the following configuration options:

.. code-block:: yaml

    # ClickHouse credentials used by Vector, generated automatically by Tutor
    ASPECTS_CLICKHOUSE_VECTOR_USER: "ch_vector"
    ASPECTS_CLICKHOUSE_VECTOR_PASSWORD: "secure-password"

    # Which pipelines to run. Tracking logs contain PII and are off by default.
    ASPECTS_VECTOR_STORE_XAPI: True
    ASPECTS_VECTOR_STORE_TRACKING_LOGS: False

    # Database and tables that Vector writes to
    ASPECTS_VECTOR_DATABASE: "openedx"
    ASPECTS_RAW_XAPI_TABLE: "xapi_events_all"
    # The default name is used to keep backwards compatibility with Cairn
    ASPECTS_VECTOR_RAW_TRACKING_LOGS_TABLE: "_tracking"

    # Path to the Docker socket that Vector reads container logs from in
    # Tutor local / dev. Only used with Docker Compose.
    ASPECTS_DOCKER_HOST_SOCK_PATH: "/var/run/docker.sock"


S3 backup sink
##############

Vector can write a copy of every xAPI event to an S3 compatible bucket (AWS S3, MinIO, etc.) at
the same time it writes to ClickHouse. This is a backup, not a fallback: events go to both sinks
in parallel. The S3 copy can later be restored into ClickHouse with the
``xapi_block_storage_backfill`` command, see :ref:`backfill_s3`.

The sink is disabled until ``ASPECTS_XAPI_S3_BUCKET`` is set:

.. code-block:: yaml

    ASPECTS_XAPI_S3_BUCKET: "xapi-events"
    ASPECTS_XAPI_S3_REGION: "us-east-1"
    # Only needed for non-AWS S3 compatible services, such as MinIO
    ASPECTS_XAPI_S3_ENDPOINT: "http://minio:9000"
    # If both are left empty Vector will use the default AWS credential chain
    ASPECTS_XAPI_S3_ACCESS_KEY: ""
    ASPECTS_XAPI_S3_SECRET_KEY: ""

    # Batching: a file is written when either limit is reached. Setting the
    # timeout too low will create many small files in S3.
    ASPECTS_XAPI_S3_SINK_MAX_EVENTS: "10000"
    ASPECTS_XAPI_S3_SINK_TIMEOUT_SECS: "600"

Files are written as zstd compressed, newline delimited JSON under the prefix
``xapi/<year>/<month>/<day>/<hour>/`` in the bucket.


Kubernetes aggregator
#####################

In Tutor ``k8s`` deployments Vector runs as a ``vector-agent`` DaemonSet plus a
``vector-aggregator`` StatefulSet (see :ref:`vector`). The following settings control the
aggregator:

.. code-block:: yaml

    # Port the agents send events to the aggregator on
    ASPECTS_VECTOR_AGGREGATOR_PORT: "6000"
    # Number of aggregator pods
    ASPECTS_VECTOR_AGGREGATOR_REPLICAS: 1
    # Maximum size in bytes of the on-disk buffer for each sink (default 1 GiB).
    # When the buffer is full Vector will block until the sink recovers.
    ASPECTS_VECTOR_AGGREGATOR_BUFFER_MAX_SIZE: "1073741824"
    # Size of the persistent volume claim backing the disk buffers
    ASPECTS_VECTOR_AGGREGATOR_STORAGE_SIZE: "2Gi"

``ASPECTS_VECTOR_AGGREGATOR_BUFFER_MAX_SIZE`` is also used for the disk buffer of the
single ``vector`` container in Docker Compose deployments. Make sure
``ASPECTS_VECTOR_AGGREGATOR_STORAGE_SIZE`` is large enough to hold the buffers for every
enabled sink.

Any additional Vector configuration can be added with the ``vector-common-toml`` Tutor patch.
