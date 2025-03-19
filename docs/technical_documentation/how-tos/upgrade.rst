.. upgrade-aspects:

How-to Upgrade Aspects
**********************

At least in the early phases of existence, Aspects is intended to have a faster upgrade cycle than Open edX named releases. It's expected that many operators will want to upgrade between releases to get features as they become available, but the upgrade process should be the same whether it's happening as part of a named release upgrade or in between.

As for any upgrade you should take a backup snapshot of your environment before beginning, especially make sure you have a recent backup of your ClickHouse database. Then follow these steps, which are basically the same as installation:

- Install the version you would like from tutor-contrib-aspects, or for the latest: ``pip install --upgrade tutor-contrib-aspects``
- To prevent orphan Superset assets from being left behind, you should remove the existing Superset assets from your Tutor environment before saving the configuration: ``rm -rf env/plugins/aspects/build/aspects-superset/openedx-assets/assets``
- Save your tutor configuration: ``tutor config save``
- Build your Docker images: ``tutor images build openedx aspects aspects-superset --no-cache``
- Initialize Aspects to get the latest schema and reports, for a tutor local install: ``tutor local do init -l aspects``

In a case where the release has special instructions, such as when new xAPI transforms have been added and you may need to replay tracking logs, they will be included in the release announcement.


Major Version Upgrades
----------------------

When upgrading between major versions of Aspects, such as from 1.x to 2.x, take special note that there *will* be breaking changes and there may be new limitations on compatibility with older versions of Open edX. For instance Aspects version 1 was designed to work with Open edX named releases Nutmeg through Redwood, while Aspects version 2 is designed to work with Redwood and later. If you are upgrading from Aspects 1.x to 2.x, you must have compatible versions of Tutor and Open edX installed.


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

1.x to 2.x Upgrade Process
==========================

For most cases the upgrade process is simply:

- Update the version of the ``tutor-contrib-aspects`` plugin.
- Optionally delete the ``/env/plugins/aspects/build/aspects-superset/`` from your Tutor directory to ensure that any old assets are removed. This depends on the version of the plugin you are upgrading from, but usually manifests as having the wrong language assets showing up in the Superset charts and dashboards.
- ``tutor config save``
- ``tutor images build aspects aspects-superset --no-cache``
- ``tutor [dev|local|k8s] do init -l aspects``
- ``tutor [dev|local|k8s] do dbt -c 'run-operation remove_deprecated_models' --only_changed False``

Larger installations with 10s or 100s of millions of xAPI events should try this process on an identical staging environment before running in production as there are a large number of factors that can affect the upgrade process such as ClickHouse configuration, the version you are upgrading from, and the size of your data set.

If you run into trouble, please reach out to the Open edX community for help. The `Data Working Group forum <https://discuss.openedx.org/c/working-groups/data/34>`_ is the best place to start.
