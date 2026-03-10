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

    ASPECTS_CLICKHOUSE_VECTOR_USER: "vector"
    ASPECTS_CLICKHOUSE_VECTOR_PASSWORD: "secure-password"
    # The default name is used to keep backwards compatibility with Cairn
    ASPECTS_VECTOR_RAW_TRACKING_LOGS_TABLE: "_tracking"
