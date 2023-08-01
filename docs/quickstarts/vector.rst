.. _quick-start-vector:

Vector
******

Vector is an alternative option to send xAPI events to Clickhouse. It can be
run along with Ralph, but to optimize resources we encourage you to only use one.

To configure Vector as the xAPI event handler, you can use the following
configuration:

.. code-block:: yaml

    # Disable ralph
    RUN_RALPH: False
    # Enable vector
    RUN_VECTOR: True
    # Change the xAPI database
    ASPECTS_XAPI_DATABASE: "openedx" # default is "xapi"


Aspects provides the following configuration options:

.. code-block:: yaml
    
    ASPECTS_CLICKHOUSE_VECTOR_USER: "vector"
    ASPECTS_CLICKHOUSE_VECTOR_PASSWORD: "secure-password"
    # The default name is used to keep backwards compatibility with Cairn
    ASPECTS_VECTOR_RAW_TRACKING_LOGS_TABLE: "_tracking"