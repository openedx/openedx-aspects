Ralph
******

Ralph is the default option to send xAPI events to Clickhouse. To run it
make sure to enable the `RUN_RALPH` option in the `config.yml` file.

.. code-block:: yaml

    RUN_RALPH: True

Aspects provides the following configuration options:

.. code-block:: yaml
    
    RALPH_ENABLE_PUBLIC_URL: False # If True, the public URL ralph.{{LMS_HOST}} will be used instead of the internal one
    RALPH_PORT: 8100
    RALPH_SENTRY_DSN: ""
    RALPH_EXECUTION_ENVIRONMENT: "production"
    RALPH_SENTRY_CLI_TRACES_SAMPLE_RATE: 1.0
    RALPH_SENTRY_LRS_TRACES_SAMPLE_RATE: 0.1
    RALPH_SENTRY_IGNORE_HEALTH_CHECKS: True
    RALPH_EXTRA_SETTINGS: {} # Any extra setting for Ralph such backends or cache settings
    RALPH_ADMIN_USERNAME: "admin"
    RALPH_ADMIN_PASSWORD: "secure-password"
    RALPH_LMS_USERNAME: "lms"
    RALPH_LMS_PASSWORD: "secure-password"


To connect an external Ralph instance, you can use the following configuration:

.. code-block:: yaml

    RALPH_HOST: "ralph.example.com"
    RALPH_RUN_HTTPS: False # If True, Ralph will use HTTPS instead of HTTP
