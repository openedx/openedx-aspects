.. _ralph:

Ralph
*****

Ralph is a toolbox for Open edX learning analytics. It can be used as a library,
command line interface, or as an API server.

Although Ralph has usages such as:

- Batch processing tracking logs.
- Convert tracking logs to xAPI statements.
- Fetch xAPI statements from a configured backend.
- Validate xAPI statements.
- Store events to different backends.

In the aspects project, Ralph is optionally used as the API server that connects Open edX
and Clickhouse database. Ralph receives the xAPI statements from Open edX and stores them
in the Clickhouse database after validating the data.

By default, Ralph is connected to the Open edX platform via Event Routing Backends without any filter
and receives all the xAPI statements. To learn more about event-routing-backends, please
refer to the `documentation <https://event-routing-backends.readthedocs.io/en/latest/>`_.
