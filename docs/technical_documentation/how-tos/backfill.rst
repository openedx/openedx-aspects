.. _backfill:

Backfill old or missing data
****************************

If you are bootstrapping a new Open edX platform with Aspects or experiencing service
downtime in Ralph or Vector, you may need to backfill the old data. This guide will
provide you with step-by-step instructions on how to perform the backfill process.

Backfill xAPI data from tracking logs
#####################################

Event routing backends provide a management command to backfill old or missing
data. The command is called ``transform_tracking_logs``, learn more about it in the
`Event Routing Backends documentation <https://event-routing-backends.readthedocs.io/en/latest/technical_documentation/how-tos/how_to_bulk_transform.html>`_.

.. warning::

    In many Tutor deployments tracking logs are not available to Tutor job images. In this case
    the script below will show an empty file instead of finding your existing tracking log file.
    You can get around this limitation by either shelling into a running LMS or CMS container
    and running the management command directly as detailed in the documentation above.

    You can also add the mount point for tracking logs to the lms-job Docker Compose file on a Tutor
    local or Tutor dev install:

    Edit:

    ``$TUTOR_ROOT/env/[local or dev]/docker-compose.jobs.yml``

    Add the following line to the ``lms-job`` → ``volumes`` key right above the ``depends_on`` line:

    ``- ../../data/lms:/openedx/data``

    Now running ``transform_tracking_logs`` should find the correct file if you are using Tutor
    defaults. This change will be overwritten the next time you ``tutor config save``.

tutor-contrib-aspects provides a wrapper around this command that is compatible with
Ralph and Vector. You can view the help for the command with:

.. code-block:: console

    tutor [dev|local|k8s] do transform-tracking-logs --help

A simple example that will find tracking logs from a Tutor local or dev environment and send them
to Ralph if it is running:

.. code-block:: console

    tutor local do transform-tracking-logs --source_provider LOCAL --source_config '{"key": "/openedx/data/", "prefix": "tracking.log", "container": "logs"}' --destination_provider LRS --transformer_type xapi

A more complicated example using tracking logs from S3 and transforming to Ralph is:

.. code-block:: console

    tutor k8s do transform-tracking-logs --source_provider S3 --source_config '{"key": "aws-key", "secret": "aws-secret", "region": "bucket-region", "container": "bucket-name", "prefix":"any-prefix"}' --destination_provider LRS --transformer_type xapi

Which will run the LMS management command:

.. code-block:: console

    ./manage.py lms transform-tracking-logs --transformer_type xapi --source_provider S3 --source_config '{"key": "aws-key", "secret": "aws-secret", "region": "bucket-region", "container": "bucket-name", "prefix":"any-prefix"}' --destination_provider LRS --transformer_type xapi


This will create a k8s job that will send all the tracking logs from S3 bucket to the configured
LRS. Vector will read the logs from the k8s job and send them to Clickhouse.

Backfilling a large amount of old data can take a very long time. It is possible to speed things up
by:

- Segmenting your tracking log files and running several backfill processes
- Turning off console logging of the xAPI events
- Adjusting your batch size to be very large and sleep time to be very short (at the potential cost
  to your LMS performance)

If you are running into repeated problems, you may wish to transform the tracking logs to file(s) on
S3 or Minio that can be loaded directly into the ClickHouse raw xAPI table
(``openedx.xapi_events_all`` for Vector, ``xapi.xapi_events_all`` for Ralph) using the ClickHouse
S3 table function.


.. _backfill_s3:

Restore xAPI data from the Vector S3 backup
###########################################

If you have enabled the Vector S3 sink (see :ref:`quick-start-vector`), every xAPI event is also
written to your bucket as it is ingested. Those files can be loaded back into ClickHouse without
replaying tracking logs, which is much faster and is useful for:

- Restoring data after a ClickHouse outage or data loss
- Importing data from another environment that writes to the same bucket
- Re-processing historical events

The ``xapi_block_storage_backfill`` command runs on the ClickHouse service and inserts the matching
files directly into the raw xAPI table using the ClickHouse S3 table function. It uses the
``ASPECTS_XAPI_S3_*`` settings for the bucket, endpoint, and credentials.

.. code-block:: console

    # Import every file in the bucket
    tutor [dev|local|k8s] do xapi_block_storage_backfill

    # Filter by date, from year down to hour (24 hour clock). Single and double
    # digit values are equivalent.
    tutor local do xapi_block_storage_backfill --year 2026 --month 3
    tutor local do xapi_block_storage_backfill --year 2026 --month 03 --day 19
    tutor local do xapi_block_storage_backfill --year 2026 --month 03 --day 19 --hour 14

    # Or give a glob path inside the bucket directly. This cannot be combined
    # with the date options.
    tutor local do xapi_block_storage_backfill --path 'xapi/2026/03/19/14/*.log.zst'

Events restored this way may already exist in ClickHouse, so the command can optionally run an
``OPTIMIZE TABLE ... FINAL`` on the raw table and the main downstream tables afterwards to collapse
duplicates:

.. code-block:: console

    tutor local do xapi_block_storage_backfill --year 2026 --month 3 --deduplicate

.. warning::

    ``OPTIMIZE TABLE FINAL`` can be resource intensive on large tables. Run it during low traffic
    periods if you have a large dataset.


.. _backfill_course_blocks:

Backfill course blocks
######################

Aspects keeps a synchronized copy of some course metadata in Clickhouse. This copy is used to
generate reports and to provide a fast way to query the courses. The copy is updated
every time a course is published. However, if a course is published before Aspects
is installed, the course will not be copied to Clickhouse.

Aspects provides a wrapper around the command ``dump-data-to-clickhouse`` that
will backfill any missing courses. To learn more about the command including some important,
options, read the
`Platform Plugin Aspects documentation <https://github.com/openedx/platform-plugin-aspects?tab=readme-ov-file#commands>`_.

To backfill the courses, run:

.. code-block:: console

    # If you already have some courses in your clickhouse sink, its better to
    # drop "--force" as it will create duplicates of the pre-existing courses.
    tutor [dev|local|k8s] do dump-data-to-clickhouse --service cms --options "--object course_overviews --force"


.. _backfill_pii:

Backfill User PII
#################

If you have user PII turned on this data can also be backfilled using the
``dump-data-to-clickhouse`` command as above.

To backfill the user profile and external ids needed to identify users variations on this command
can be run (again please see the documentation for details and other important options):

.. code-block:: console

    tutor [dev|local|k8s] do dump-data-to-clickhouse --service lms --options "--object user_profile"
    tutor [dev|local|k8s] do dump-data-to-clickhouse --service lms --options "--object external_id"
