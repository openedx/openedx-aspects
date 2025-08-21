.. _troubleshooting_aspects:

Troubleshooting Aspects
#######################

Most common problems with Aspects can be fixed by making sure everything is up to date by deleting
any potentially orphaned Superset assets, rebuilding Docker images, and re-initializing Aspects:

- From your TUTOR_ROOT: ``rm -rf env/plugins/aspects``
- ``tutor config save``
- ``tutor images build openedx aspects aspects-superset``
- ``tutor [dev|local|k8s] do init -l aspects``

  - This may take a long time if you have lots of data!


Common Issues
*************
In some cases things can get into a state which isn't resolved by those steps, below are some
common Aspects problems and how to fix them.


Superset Logo Just Spins
========================

Symptom: In the Instructor Dashboard "Reports" tab, In-Context Metrics in Studio, or in Superset,
some or all Superset dashboards appear to load but the "S" logo just spins and no data appears.

Causes: This most often happens where ClickHouse has no data for filters needed to display a
dashboard.

Solution: Make sure you have published your courses since installing / reinstalling Aspects, or :ref:`backfill course blocks <backfill_course_blocks>` .


Embedded Dashboard Errors
=========================

Symptom: In the Instructor Dashboard "Reports" tab or In-Context Metrics in Studio the dashboards
fail to load, showing only a message like:

- ``Something went wrong with embedded authentication. Check the dev console for details.``
- or ``Error: invalid_request Invalid client_id``

This most often happens when moving between Tutor deployment types (dev/local/k8s) but can also
happen when the hostnames or ports your LMS or Superset change (such as when populating a staging
environment from a production database). This is usually an issue with the OAuth Application entry
not matching the Superset URL. Make sure you ``config.yml`` settings are correct for your
environment (especially ``SUPERSET_HOST`` and ``SUPERSET_PORT``) then:

- Go into the Django admin: ``{LMS_ROOT}/admin/oauth2_provider/application/``
- Delete the Application entries for `superset-sso` and ``superset-sso-dev`` if they exist
- Re-run ``tutor [dev|local|k8s] do init -l aspects`` to recreate the entries


General Troubleshooting
***********************

Logs to check for errors:

When running with the Ralph data pipeline:

- lms-worker
- cms-worker
- ralph

When running with the Vector data pipeline:

- lms
- cms
- vector

When running with the event bus data pipeline:

- lms
- cms
- aspects-consumer
