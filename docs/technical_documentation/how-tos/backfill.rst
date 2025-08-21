Backfill old or missing data
*****************************

If you are bootstrapping a new Open edX platform with Aspects or experiencing service
downtime in Ralph or Vector, you may need to backfill the old data. This guide will
provide you with step-by-step instructions on how to perform the backfill process.

Backfill xAPI data from tracking logs
######################################

Event routing backends provide a management command to backfill old or missing
data. The command is called ``transform_tracking_logs``, learn more about it in the
`Event Routing Backends documentation <https://event-routing-backends.readthedocs.io/en/latest/howto/how_to_bulk_transform.html>`_.

tutor-contrib-aspects provides a wrapper around this command that is compatible with
Ralph and Vector. Run it with:

.. code-block:: console

    tutor [dev|local|k8s] do transform-tracking-logs --options "..."

The ``--options`` argument is passed directly to the management command. For example,

.. code-block:: console

    tutor k8s do transform-tracking-logs --options "--source_provider S3 --source_config '{\"key\": \"aws-key\", \"secret\": \"aws-secret\", \"region\": \"bucket-region\" ,\"container\": \"bucket-name\", \"prefix\":\"any-prefix\"}' --destination_provider LRS --transformer_type xapi"

Which will run the command:

.. code-block:: console

    ./manage.py --transformer_type xapi --source_provider S3 --source_config '{"key": "aws-key", "secret": "aws-secret", "region": "bucket-region" ,"container": "bucket-name", "prefix":"any-prefix"}' --destination_provider LRS --transformer_type xapi


This will create a k8s job that will send all the tracking logs from S3 bucket to the configured
LRS. Vector will read the logs from the k8s job and send them to Clickhouse.


.. _backfill_course_blocks:

Backfill course blocks
#######################

Aspects keeps a synchronized copy of some course metadata in Clickhouse. This copy is used to
generate reports and to provide a fast way to query the courses. The copy is updated
every time a course is published. However, if a course is published before Aspects
is installed, the course will not be copied to Clickhouse.

Aspects provides a wrapper around the command ``dump_data_to_clickhouse`` that
will backfill any missing courses. To learn more about the command including some important,
options, read the
`Event Sink Clickhouse documentation <https://github.com/openedx/openedx-event-sink-clickhouse#commands>`_.

To backfill the courses, run:

.. code-block:: console

    tutor [dev|local|k8s] do dump_data_to_clickhouse --service cms --object course_overviews


.. _backfill_pii:

Backfill User PII
#################

If you have user PII turned on this data can also be backfilled using the
``dump_data_to_clickhouse`` as above.

To backfill the user profile and external ids needed to identify users variations on this command
can be run (again please see the documentation for details and other important options):

.. code-block:: console

    tutor [dev|local|k8s] do dump_data_to_clickhouse --service lms --object user_profile
    tutor [dev|local|k8s] do dump_data_to_clickhouse --service lms --object external_id
