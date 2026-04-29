.. _upgrade-aspects:

Upgrade Aspects
**********************

Aspects is intended to have a faster upgrade cycle than Open edX named releases since operators might want to upgrade between releases to get features as they become available. The upgrade process is the same whether it's happening as part of a named release upgrade or in between.

As with any upgrade, you should take a backup snapshot of your environment before beginning, especially make sure you have a recent backup of your ClickHouse database. Then follow these steps, which are basically the same as installation.

Upgrade Steps
-------------

    1. Install the version you would like from tutor-contrib-aspects, or for the latest: 

    ``pip install --upgrade tutor-contrib-aspects``

    2. To prevent orphan Superset assets from being left behind, you should remove the existing Superset assets from your Tutor environment before saving the configuration: 

    ``rm -rf env/plugins/aspects/build/aspects-superset/openedx-assets/assets``

    3. Save your tutor configuration: 

    ``tutor config save``

    4. Build your Docker images: 

    ``tutor images build openedx aspects aspects-superset --no-cache``

    5. If using in-context metrics (only available starting in the Teak Open edX release), build also the `mfe` image: 

    ``tutor images build mfe --no-cache``

    6. Initialize Aspects to get the latest schema and reports, for a tutor local install: 

    ``tutor local do init -l aspects``

    7. Remove any deprecated models: 

    ``tutor local do dbt -c 'run-operation remove_deprecated_models' --only_changed False``

Larger installations with 10s or 100s of millions of xAPI events should try this process on an identical staging environment before running in production as there are a large number of factors that can affect the upgrade process such as ClickHouse configuration, the version you are upgrading from, and the size of your data set.

In a case where the release has special instructions, such as when new xAPI transforms have been added and you may need to replay tracking logs, they will be included in the release announcement.

If you run into trouble, please reach out to the Open edX community for help. The `Data Working Group forum <https://discuss.openedx.org/c/working-groups/data/34>`_ is the best place to start.


Major Version Upgrades
----------------------

When upgrading between major versions of Aspects, take special note that there *will* be breaking changes and there may be new limitations on compatibility with older versions of Open edX. If you plan on upgrading, you must have compatible versions of Tutor and Open edX installed.

===============  ======================================
Aspects version  Compatible with Open edX named version
===============  ======================================
v1.x             Nutmeg through Quince
v2.x             Redwood through Teak
v3.x             Ulmo and later
===============  ======================================


Upgrading v3.x to v4.x
-----------------------

Breaking Changes
================

The default data pipeline has changed from Ralph to Vector. This change improves performance and simplifies the architecture by eliminating the need to scale multiple Ralph containers and Celery workers for high-throughput scenarios.

Key changes:

- Vector is now the default for xAPI event ingestion
- The ``ASPECTS_VECTOR_RAW_XAPI_TABLE`` setting has been replaced with ``ASPECTS_RAW_XAPI_TABLE``
- The default database has changed from ``xapi`` (Ralph) to ``openedx`` (Vector)
- A new S3 sink is available to backup xAPI events for recovery

To keep using Ralph as your data pipeline:

.. code-block:: bash

   tutor config save --set ASPECTS_XAPI_SOURCE=ralph
   tutor config save --set RUN_RALPH=True
   tutor config save --set RUN_VECTOR=False

This will configure Aspects to use Ralph with the ``xapi`` database, preserving your existing data.

If you have customized ``ASPECTS_VECTOR_RAW_XAPI_TABLE`` in your configuration, update it to use ``ASPECTS_RAW_XAPI_TABLE`` instead.

For new installations or users switching to Vector, your data will be stored in the ``openedx`` database. You can migrate existing data from the ``xapi`` database to ``openedx`` if needed.


Upgrading v2.5 to v3.x
-----------------------

Breaking Changes
================

In-Context Analytics in Aspects v3.0 uses Paragon v23 which was introduced in Open edX Ulmo. Therefore, Aspects v3.x requires Open edX Ulmo or later. If you are running a named release before Ulmo, you will need to upgrade to Ulmo or later before upgrading Aspects to v3.x.


Upgrading to `v2.5 <https://github.com/openedx/tutor-contrib-aspects/releases/tag/v2.5.0>`_
-------------------------------------------------------------------------------------------

There were multiple changes to dbt views which will need to be manually refreshed. Do this by running:

.. code-block:: bash

    tutor [local/dev/k8s] do dbt --only_changed False -c 'run --full-refresh --select dim_problem_responses+ fact_video_segments+ dim_course_blocks+ fact_navigation_completion+ fact_pageview_engagement+ problem_events+ dim_learner_last_response+ dim_problem_results+ dim_subsection_problem_results+ fact_problem_engagement+ dim_problem_coursewide_avg+ dim_subsection_performance+'


Upgrading v1.x to v2.x
----------------------

Breaking Changes
================

- v2 of Aspects drops support for named releases before Redwood. If you are running a named release before Redwood, you will need to upgrade to Redwood or later before upgrading Aspects to v2.x.

- Several potentially large data migrations are done in the upgrade from to 2.x. See below for details.

Migrations
==========

One of the main efforts of the v2 release was to normalize the use of data model names and schemas to make the database more consistent and easier to work with. Our ongoing performance work has also yielded about an average 9% ClickHouse memory improvement and 3.5% chart loading time.

These changes require several data migrations to be run to update the database schema. Most of these migrations are run automatically when you upgrade to v2.x. They may take a long time to run, depending on the size of your data set. It is recommended to run these migrations on a test copy of your database before upgrading production to understand how long your upgrade may take and flush out any potential problems in advance.

If you have custom data models that rely on the Aspects schema, be aware that some of the changes may require you to update your custom models to work with the new schema. The specific changes are:

==========  ==============================  ==========  ====================================
old schema  old table name                  new schema  new table name
==========  ==============================  ==========  ====================================
event_sink  course_block_names              reporting   dim_course_block_names
event_sink  course_names                    event_sink  dim_course_names
event_sink  course_tags                     reporting   dim_most_recent_course_tags
reporting   dim_course_blocks_extended      DEPRECATED
reporting   fact_enrollment_status          reporting   dim_most_recent_enrollment
xapi        fact_instance_enrollments       reporting   fact_instance_enrollments
reporting   fact_learner_course_grade       reporting   dim_learner_most_recent_course_grade
reporting   fact_learner_course_status      reporting   dim_learner_most_recent_course_state
xapi        fact_learner_last_course_visit  reporting   dim_learner_last_course_visit
reporting   fact_navigation                 DEPRECATED
reporting   fact_problem_responses          DEPRECATED
reporting   fact_student_status             reporting   dim_student_status
reporting   int_pages_per_subsection        DEPRECATED
reporting   int_problem_hints               DEPRECATED
reporting   int_problem_results             reporting   fact_learner_response_attempts
reporting   int_problems_per_subsection     DEPRECATED
reporting   int_videos_per_subsection       reporting   fact_videos_per_subsection
event_sink  most_recent_course_blocks       event_sink  dim_most_recent_course_blocks
reporting   most_recent_course_tags         DEPRECATED
event_sink  most_recent_object_tags         event_sink  dim_most_recent_object_tags
event_sink  most_recent_tags                event_sink  dim_most_recent_tags
event_sink  most_recent_taxonomies          event_sink  dim_most_recent_taxonomies
xapi        responses                       reporting   dim_learner_response_attempt
xapi        section_page_engagement         reporting   fact_section_page_engagement
xapi        section_problem_engagement      reporting   fact_section_problem_engagement
xapi        section_video_engagement        reporting   fact_section_video_engagement
xapi        subsection_page_engagement      reporting   fact_subsection_page_engagement
xapi        subsection_problem_engagement   reporting   fact_subsection_problem_engagement
xapi        subsection_video_engagement     reporting   fact_subsection_video_engagement
reporting   watched_video_duration          reporting   fact_watched_video_duration
==========  ==============================  ==========  ====================================


These model updates are done as part of the dbt step of init, or can be executed manually or even individually by running different forms of the dbt command. Moved or deprecated models will not have their old versions deleted as part of this upgrade, which should allow for a more seamless transition.

Once the Superset assets are updated (the last step in the Aspects init process) the old models can and should be safely dropped. This can be done by running the following command:

``tutor [dev|local|k8s] do dbt -c 'run-operation remove_deprecated_models' --only_changed False``
