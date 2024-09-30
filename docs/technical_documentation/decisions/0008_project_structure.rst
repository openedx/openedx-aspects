8. Project Structure
####################

Status
******

Accepted

Context
*******

The Aspects Analytics system (Aspects) consists of several pieces of technology working together via
some configuration and scripting. Decisions around where to store data and configuration need to be
made so that developers understand where to make changes and look for the causes of issues. These
decisions can have wide ranging impact on things such as extensibility and configurability of the
system as a whole.

This ADR offers guiding principles to address these issues:

* The number of plugins and systems in play can make it difficult to know where to look for
  configuration or add new features.
* Initialization steps for the third-party systems are sometimes intricate and dependent on other
  systems, so Aspects deployment needs to control exactly what happens when.
* In the future, Aspects will offer a non-Tutor deployment option for experienced operators.

Decisions
*********

**Aspects repo**

This repo (`openedx-aspects`_) remains the primary Aspects repository where the project decisions
and documentation are stored.

This repo should also be used to store any common code or configuration between Tutor and non-Tutor
Aspects deployments.

**Single Aspects Tutor plugin**

All of the third-party services that Aspects requires can be deployed and configured by a single
`tutor-contrib-aspects`_ plugin.

This plugin employs the following structure to delineate the different areas of responsibility::

    tutoraspects/
    ├── patches
    └── templates
        ├── aspects
        │   ├── apps
        │   │   ├── aspects
        │   │   ├── clickhouse
        │   │   ├── ralph
        │   │   ├── superset
        │   │   └── vector
        │   ├── build
        │   │   ├── aspects
        │   │   └── aspects-superset
        │   │       └── openedx-assets
        │   └── jobs
        │       └── init
        │           ├── aspects
        │           ├── clickhouse
        │           ├── lms
        │           ├── mysql
        │           └── superset
        └── openedx-assets

This structure is guided by the following principles:

* Configuration or functionality specific to a single service should live under a directory named
  for that service.

  E.g. `templates/aspects/apps/clickhouse` contains deployment templates related to Clickhouse,
  and `templates/aspects/jobs/init/clickhouse` contains the Clickhouse initialization scripts.

* Configuration or functionality that spans multiple services should live under an `aspects` directory.

  E.g. `templates/aspects/apps/aspects` contains Aspects-specific database migrations (Clickhouse
  migrations handled by Alembic) and dbt profiles (data transformation layer).

* Templates for Superset assets (dashboards, charts, etc.) live under the
  `templates/aspects/build/aspects-superset/openedx-assets` directory to facilitate localization of
  this user-facing content.

  These asset templates utilize shared, non-localized files stored under `templates/openedx-assets`.

**LMS plugins**

Aspects depends on specific versions of a few Django plugins to move events from the LMS into its
processing pipeline (currently `openedx-event-sink-clickhouse`_ and `event-routing-backends`_).
These plugins should live in their own repositories, and be installed to the LMS/CMS as "extra
requirements", using the chosen deployment's best practices. For example, the Tutor plugin installs
these dependencies to the LMS+CMS using the `OPENEDX_EXTRA_PIP_REQUIREMENTS` variable.

Consequences
************

* The service-based Tutor plugins (``tutor-contrib-clickhouse``, ``tutor-contrib-ralph``, ``tutor-contrib-superset``) are consolidated into `tutor-contrib-aspects`_ and archived under `openedx-unsupported`_.

Rejected Alternatives
*********************

**Separate plugins for each third-party service**

Supercedes `ADR 6 Areas of responsibility`_.

.. _ADR 6 Areas of responsibility: 0006_areas_of_responsibility.html
.. _event-routing-backends: https://github.com/openedx/event-routing-backends
.. _openedx-aspects: https://github.com/openedx/openedx-aspects
.. _openedx-event-sink-clickhouse: https://github.com/openedx/openedx-event-sink-clickhouse
.. _openedx-unsupported: https://github.com/openedx-unsupported
.. _tutor-contrib-aspects: https://github.com/openedx/tutor-contrib-aspects
