.. _production_configuration:

Configure Aspects for Production
********************************

Choosing an xAPI Pipeline
#########################

Aspects can be configured to send xAPI events to ClickHouse in several different ways. Which one you choose depends on your specific organization's needs, deployment infrastructure, scale, and familiarity with different technology. The `event-routing-backends docs`_ have more details on the configuration options outline here.

At a high level the options are:

**Celery tasks without batching (default)**

Each tracking log event that has an xAPI transform gets queued as a task. The task performs the xAPI transform and queues a second task to send the event to Ralph. Ralph checks for the existence of the event in ClickHouse before inserting. Events deemed "`business critical`_" can be configured to be retried upon failure.

Pros:

- Celery is a familiar technology for Open edX site operators and can be configured to run in a highly available and scalable way with multiple workers and things like AWS SQS as a backend
- Uses exiting systems and processes, so has the least configuration
- This is the best tested path and least likely to have surprising bugs in v1

Cons:

- The duplication of tasks combined with the high volume of tasks and latency of making network requests for each event can quickly overwhelm Celery workers, requiring many workers to be run and causing delays for other Celery tasks
- Other processes that spawn many or slow Celery tasks, such as re-grading a large course, or many successive course publish events for large courses, can delay event delivery
- Downstream outages in Ralph of ClickHouse can exacerbate these issues with many pending retries piling up
- ClickHouse is much less efficient with many small inserts, resulting in the possibility of insert delays or even errors if there are many simultaneous single row inserts

Recommended for:

Development, testing, or very small deployments.


**Celery tasks with batching**

Event-routing-backends can be configured to `batch requests`_ to Ralph, mitigating many of the issues above while still keeping the simplicity of configuration. Batching is accomplished by a "this many or this long" check, so even on low traffic deployments events will only be delayed by a fixed amount of time. In load testing, batching at up to 1000 events allowed for loads over 50 events/sec on a single worker, which is enough for most production instances.

Pros:

- The same as Celery above
- Far fewer Celery tasks, reducing issues around worker contention and task delays, and greatly improved performance
- Downstream outages have less impact
- Much better resource utilization for ClickHouse

Cons:

- Transformed events are stored in redis while waiting to be sent, increasing redis traffic and potential loss of events in a redis outage
- Batching is not as well tested (as of Redwood) and may have edge cases until it has been used in production

Recommended for:

This is a reasonable choice for most production use cases for small-to-medium sized production deployments and has been load tested up to significant levels.


**Vector**

Vector is a log forwarding service that monitors the logs from docker containers or Kubernetes pods. It writes events directly to ClickHouse and automatically batches events based on volume. The LMS can be configured to transform and log xAPI events in-process and Vector will pick them up by reading the logs.

Pros:

- Removes the need to run or scale Ralph
- Automatic batching adjustments
- Fastest delivery times to ClickHouse
- Vector failures do not impact other systems

Cons:

- It is a new service for most operators
- Events are not de-duplicated before insert, which can result in some (mostly temporary) incorrect data in a disaster recovery
- Disaster recovery hasn't been tested with Aspects yet
- Needs a pod run for every LMS or CMS Kubernetes worker
- When run in-process, adds a small amount of overhead to any LMS request that sends an xAPI statement

Recommended for:

Resource constrained Tutor local environments, experienced operators on larger deployments.


**Event Bus (experimental)**

Open edX has had event bus capabilities with redis and Kafka backends since Palm. In Redwood the event-tracking and event-routing-backends libraries have been updated to support `using the event bus`_ as a replacement for Celery. It has the advantage of being able to remove Celery contention and maintain better delivery guarantees while still supporting Ralph deduplication and other advanced use cases (such as real-time streaming xAPI events to other reporting or backup services).

Pros:

- Can use completely separate hardware from Celery, providing better performance domain boundaries
- Can use the same batching mechanisms as Celery for improved performance, with the same costs and tradeoffs
- Has better delivery guarantees than Celery (in most configurations), allowing operators to recover from event bus consumer outages or upgrades without having to replay tracking logs
- Can support advanced use cases for sending the xAPI events to other sinks with the same near real-time delivery guarantees as Aspects
- (redis) Can scale down to use the same redis instance as edx-platform, or use a separate / hosted redis for better isolation and performance
- (Kafka) Can scale up to handle extremely high volumes of data and handle long-term outages better than any other option, can be run hosted
- (Kafka) Can potentially `integrate directly`_ with ClickHouse removing the need for both a separate event consumer and Ralph.

Cons:

- Many parts are new and may not have extensive production testing

Recommended for:

Large-to-very-large instances, adventurous site operators, installations that already have Kafka or advanced use cases that can benefit from a multi-consumer architecture.


Setting up the xAPI Pipeline
############################

**Celery**

When in doubt, the simplest place to start with a production configuration is Celery tasks with batching set to 100 events or 5 seconds. You will want to add at least one additional lms-worker to handle the additional load of xAPI events and the event sink pipeline. You will also probably want to add at least one additional cms-worker to handle the new work of the course publishing event sink.

**Vector**

Generally the Aspects created Vector configuration should work in most cases. In Kubernetes environments you will need to make sure that a Vector pod is attached to each LMS/CMS worker.

**Event bus**

Similar to Celery, you should start with at least 2 event bus consumers and configure batching to 100 events or 5 seconds to start with. If you find that the event queue size is growing (see "Monitoring", below), you can add more event bus consumers and/or increase the batch size. We have tested with batch sizes up to 1000 without issue.


Choosing ClickHouse Hosting
###########################

By default Aspects deploys a single ClickHouse Docker container as part of the Tutor install. This is not the preferred way to run a production environment! In most cases, if you can afford it, ClickHouse Cloud is the easiest and most performant way to run the service, and removes the burden of dealing with scaling, security, upgrades, backups, and other potentially difficult database management issues. Axim has been using ClickHouse Cloud for load testing and is designed to work with it.

Altinity Cloud is another hosting service that Aspects has tested with in the past, but may require more hands-on integration as they use a different clustering approach than ClickHouse Cloud.

Another option if you are running in Kubernetes is to use the `clickhouse-operator`_ to deploy and manage a more fault tolerant ClickHouse cluster. Aspects support for ClickHouse clusters is currently experimental, and may not support all cluster configurations without modification.


Setting up ClickHouse
#####################

Tutor local and k8s environments should work out of the box. See Remote ClickHouse <remote-clickhouse> and ClickHouse Cluster <clickhouse-cluster> for more information on setting up hosted services.

.. note::

    Don't forget the usual checklist items! Make sure the server is secured, only accessible from places it needs to be, and backed up!


Setting up Ralph
################

You can deploy `Ralph via Helm chart`_. If you are using a pipeline that involves the Ralph learning record store (Celery or an event bus), you will want to run at least two Ralph servers for fault tolerance. Generally it consumes few resources and is quite stable. If you find that response times from Ralph are high it is usually because there are too many small ClickHouse inserts and you should turn on batching or increase your batch size.


Setting up Superset
###################

While Superset hosting provides such as Preset.io exist, the deep integration that Aspects does with Superset is not expected to work with them. As such we recommend running Superset alongside your Open edX stack.

By default Superset is set to share the Open edX MySQL database and redis servers to save resources. Traditionally services like Aspects are fairly low traffic and this may be acceptable for a production environment, but you may wish to consider setting up separate instances for separation of resources and performance... especially for large sites.

Superset is a Flask application and can be load balanced if need be. Superset also uses Celery workers for asynchronous tasks. You may wish to run more than one of these, though Aspects does not currently make heavy use of them.

.. note::

    Don't forget the usual checklist items! Make sure the server is secured and backed up! Make sure you understand the basics of `superset security configuration`_ and have updated your settings appropriately if necessary. Aspects does a lot with user roles and permissions to support localized dashboards, if you need help understanding how it all fits together please reach on in #aspects on the Open edX Slack!


Important Configuration Considerations
######################################

Personally Identifiable Identification
--------------------------------------

By default Aspects does not store information that can directly link the xAPI learning traces to an individual's name, email address, username, etc. Storing this information has potential legal consequences and should be undertaken with careful consideration.

Setting ``ASPECTS_ENABLE_USER_PII`` to ``True``, then running Tutor init for the Aspects plugin, turns on the ability to send user data to ClickHouse. When turned on this populates the ``event_sink.external_id`` and ``event_sink.user_profile`` tables as new users are created.

However it does not copy over existing users, see "Backfilling Existing Data" below for more information on how to do that.

XAPI User Id Type
-----------------

By default, xAPI statements are sent with a unique UUID for each individual LMS user.  This preserves learner privacy in cases where PII is turned off and is the recommended way of running Aspects. Other options do exist, see <changing_actor_identifier> for more information.

.. note::
    In Nutmeg there is not xAPI anonymous ID type, therefore Aspects uses the LTI type, resulting in a decrease in privacy guarantees since the LTI identifier may be linked to 3rd party systems or visible in ways that the xAPI ID is not. It is up to site operators if this tradeoff is acceptable. Additionally, it means that after upgrading from Nutmeg users will begin to get new identifiers, so data will need to be rebuilt from the tracking logs up in order to preserve correctness.


LMS Embedded Dashboards
-----------------------

.. note::
    The embedded dashboard functionality relies on functionality introduced in Quince and will not work on earlier versions of Open edX.

By default, Aspects enables plugin functionality in the LMS that embeds a defined set of Superset dashboards into the Instructor dashboard of each course. The following settings control the behavior of those dashboards:

- ``ASPECTS_ENABLE_INSTRUCTOR_DASHBOARD_PLUGIN`` - Enables or disables the embedding entirely. ``True`` means the dashboards will be available, ``False`` means they are not.
- ``ASPECTS_INSTRUCTOR_DASHBOARDS`` - A list of dashboards to display. Each dashboard gets an individual tab. You can use this option to add custom embedded dashboards, or to remove or replace the default dashboards.
- ``ASPECTS_COURSE_OVERVIEW_HELP_MARKDOWN`` controls the content of the "Help" tab in the Course Overview dashboard
- ``ASPECTS_INDIVIDUAL_LEARNER_HELP_MARKDOWN`` controls the content of the "Help" tab in the Individual Learner dashboard
- ``ASPECTS_LEARNER_GROUPS_HELP_MARKDOWN`` controls the content of the "Help" tab in the At-Risk Learners dashboard
- ``ASPECTS_OPERATOR_HELP_MARKDOWN`` controls the content of the "Help" tab in the Operator dashboard


Ralph Accessibility
-------------------

By default when Ralph is run it is only made accessible on the internal Docker Compose / Kubernetes networks. Setting ``RALPH_ENABLE_PUBLIC_URL`` to ``True`` allows external access to Ralph for additional xAPI use cases.

.. note::
    This works with the default Tutor dev/local/k8s, but depending on your configuration, more changes may be required.


Superset Localization
---------------------

Superset offers very basic localization options. Aspects builds on those to bring localization to as many pieces of the user interface as is currently technically possible. The following settings impact localization options in Superset:

- ``SUPERSET_SUPPORTED_LANGUAGES`` - This list controls what is displayed in the main Superset UI, which users can select from manually. It only impacts the main Superset user interface (top level menus). Note that these are only language options, and do no include locale specific translations (ex: French is supported, Canadian French is not).
- ``SUPERSET_DASHBOARD_LOCALES`` - This list is for the Aspects language options and include all of the default Open edX languages. Many languages are still being translated, and you may wish to disable some rather than having a mix of localized strings and English being displayed, or add other options. This setting controls the names of dashboards, charts, and columns, as well as some fields returned from the database.
- The patch ``superset-extra-asset-translations`` allows you to augment or replace the default translations provided with Aspects.

Monitoring Superset
-------------------

Super set comes with built in Sentry support. If you set ``SUPERSET_SENTRY_DSN`` you can take advantage of that telemetry data.


Data Lifecycle / TTL
####################

.. warning::

    By default Aspects partitions all stored data by month and will only keep 1 year of data! ClickHouse will automatically drop partitions of older data as they age off.

For learner privacy and performance reasons, Aspects defaults to only storing one year's worth of historical data. This can be changed or turned off entirely via the setting ``ASPECTS_DATA_TTL_EXPRESSION``. See <data-lifecycle-policy> for more information.


Backfilling Existing Data
##########################

If you are setting up Aspects as part of an already established Open edX installation, you will probably want to import existing data. There are several things to keep in mind for this process, especially for large or long-running instances!

Backfilling Course and User Data
--------------------------------

.. warning::

    The commands below will run as fast as possible by default, potentially causing performance issues on live sites. Please review the `dump_data_to_clickhouse arguments`_ to see options for testing the command with one or a few objects, or batching the process with a sleep time so as not to overwhelm the LMS, MySQL, or Celery queues.

There is a management command to populate course data for one, all, or a subset of courses:

.. code-block::

    tutor local run lms ./manage.py lms dump_data_to_clickhouse --object course_overviews


If you are running with ``ASPECTS_ENABLE_USER_PII`` set to ``True`` you will need to populate the user PII data with these commands:

.. code-block::

    tutor local run lms ./manage.py lms dump_data_to_clickhouse --object external_id

.. code-block::

    tutor local run lms ./manage.py lms dump_data_to_clickhouse --object user_profile


Backfilling xAPI Data From Tracking Logs
----------------------------------------

How you get data from tracking logs depends on where they are stored, and how large they are. As much as possible you should trim the log files down to just the events that fall within your data retention policy (see "Data Lifecycle / TTL" above) before loading them to avoid unnecessary load on production systems.

The management command for bulk importing tracking logs is documented here: `transform_tracking_logs`_


Tracking Log Retention
######################

Aspects is powered by tracking logs, therefore it's important to rotate and store your tracking log files in a place where they can be replayed if necessary in the event of disaster recovery or other outage. Setting up log rotation is outside the scope of this document, but highly suggested as by default Tutor will write to one tracking log file forever.

Monitoring
##########

There are a few key metrics worth monitoring to make sure that Aspects is healthy:

**ClickHouse Lag Time**

This is the time between now and the last xAPI event arriving. The frequency of events depends on a lot of factors, but an unusually long lag can mean that events aren't arriving. An easy way to check this is by querying ClickHouse with a query such as

.. code-block:: sql

    SELECT
        count(*) as ttl_count,
        max(emission_time) as most_recent,
        date_diff('second', max(emission_time), now()) as lag_seconds
    FROM xapi.xapi_events_all
    FINAL
    FORMAT JSON


**Celery Queue Length**

If you are using Celery it's important to make sure that the queue isn't growing uncontrollably due to the influx of new events and other tasks associated with Aspects. For a default install the following Python code will show you the number of tasks waiting to be handled for the LMS and CMS queues:

.. code-block:: python

        from django.conf import settings
        import redis

        r = redis.Redis.from_url(settings.BROKER_URL)
        lms_queue = r.llen("edx.lms.core.default")
        cms_queue = r.llen("edx.cms.core.default")


**Redis Bus Queue Length**

For redis streams you can find the number of pending items using the following Python:

.. code-block:: python

        r = redis.Redis.from_url(settings.EVENT_BUS_REDIS_CONNECTION_URL)

        # "analytics" is the topic, your configuration may vary
        info = r.xinfo_stream("analytics", full=True)

        lag = 0

        # You may prefer to break out the lag here by consumer group
        try:
            for g in info["groups"]:
                lag += g["lag"]
        # Older versions of redis don't have "lag".
        except KeyError:  # pragma: no cover
            pass

        return lag


**Kafka Bus**

If you are running Kafka you likely have other tools for monitoring and managing the service. Generally you are looking for the difference between the low and high watermark offsets for each partition in your configured topic and consumer group to determine how many messages each partition has processed vs the total.

**Superset**

Superset is a fairly standard Flask web application, and should be monitored for the usual metrics. So far the only slowness we have encountered has been with slow ClickHouse queries.


**ClickHouse**

In addition to the usual CPU/Memory/Disk monitoring you can also monitor a few key ClickHouse metrics:

- Uptime: The server uptime in seconds. It includes the time spent for server initialization before accepting connections.
- MaxPartCountForPartition: Maximum number of parts per partition across all partitions of all tables of MergeTree family. Values larger than 300 indicates misconfiguration, overload, or massive data loading.
- StuckReplicationTasks: Replication tasks that were retried or postponed over 100 times.
- Query: Number of executing queries
- DelayedInserts: Number of INSERT queries that are throttled due to high number of active data parts for partition in a MergeTree table.
- DistributedFilesToInsert: Number of pending files to process for asynchronous insertion into Distributed tables. Number of files for every shard is summed.
- cluster default: Free space per cluster node, as percent

These are also captured in the Aspects Operator Dashboard as well as a filterable list of slowest ClickHouse queries to assist with troubleshooting.


.. _business critical: https://event-routing-backends.readthedocs.io/en/latest/getting_started.html#persistence
.. _batch requests: https://event-routing-backends.readthedocs.io/en/latest/getting_started.html#batching-configuration
.. _using the event bus: https://event-routing-backends.readthedocs.io/en/latest/getting_started.html#event-bus-configuration
.. _integrate directly: https://clickhouse.com/docs/en/integrations/kafka
.. _event-routing-backends docs: https://event-routing-backends.readthedocs.io/en/latest/getting_started.html#configuration
.. _clickhouse-operator: https://github.com/Altinity/clickhouse-operator
.. _superset security configuration: https://superset.apache.org/docs/security/
.. _Ralph via Helm chart: https://openfun.github.io/ralph/latest/tutorials/helm/
.. _dump_data_to_clickhouse arguments: https://github.com/openedx/platform-plugin-aspects/blob/951ed84de01dda6bec9923c60fcd96bf80d6fa54/platform_plugin_aspects/management/commands/dump_data_to_clickhouse.py#L91
.. _transform_tracking_logs: https://event-routing-backends.readthedocs.io/en/latest/howto/how_to_bulk_transform.html
