Ralph
#############

Ralph is an toolbox for Open edX learning analytics. It can be used as a library,
command line interface, or as an API server.

Altough Ralph has usages such as:

- Batch processing tracking logs.
- Convert tracking logs to xAPI statements.
- Fetch xAPI statements from a configured backend.
- Validate xAPI statements.
- Store events to different `backends <https://openfun.github.io/ralph/backends/>`_.

In the aspects project it's used as the API server that connects Open edX and clickhouse
database. Ralph receives the xAPI statements from Open edX and stores them in the clickhouse
database after validating the data.

Ralph is connected to the Open edX platform via event-routing-backends without any filter
and receives all the xAPI statements. To learn more about event-routing-backends, please
refer to the `documentation <https://event-routing-backends.readthedocs.io/en/latest/>`_.
