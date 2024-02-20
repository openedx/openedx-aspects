Pipelines
**********

Aspects provide two Pipelines which are detailed below.

Ralph Pipeline
##############

The Ralph pipeline is the default pipeline, and is the most robust. It will retry the
most important failed events, and will catch most duplicates before they hit the database.
This pipeline consist of a plugin in the LMS (`event-routing-backends`) that will send
through HTTP the events to the Ralph API.

Ralph will validate the events and send them to the configured backends. Clickhouse is
the only Ralph backend supported by the Aspects plugin.

Ralph is for sharing xAPI data using the LRS standard.

To learn more about Ralph, see the `Ralph documentation <https://openfun.github.io/ralph/>`_.

To configure Ralph as your pipeline, see the :ref:`Quick Start - Ralph guide <quick-start-ralph>`.

Vector Pipeline
###############

The Vector pipeline instead works by capturing the standard output from the LMS logs
and sending them directly to configured "sinks" or data destinations. It implements two
similar pipelines, one for xAPI data and one for tracking logs.

Vector is lighter weight, and generally data will arrive a little faster, but doesn’t retry.
It can also be a good choice if you want to add other listeners for that data
(ex: to store xAPI statements to S3).

To learn more about Vector, see the `Vector documentation <https://vector.dev/docs/>`_.

To configure Vector as your pipeline, see the :ref:`Quick Start - Vector guide <quick-start-vector>`.
