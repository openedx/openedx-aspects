13. Clickhouse experimental and beta features
#############################################

Status
******

Accepted

Context
*******

When the Aspects project started, Clickhouse was working on a JSON column type and expected to have it out of
"experimental" status by Sep 2023. However, Clickhouse revealed that the feature development is stuck in limbo, and may
never be completed.

Clickhouse documentation warns that `experimental features`_ may never become accepted into the general feature list,
may be removed at any time, and are not supported by the Clickhouse development team. Additionally, "experimental"
features may not be available on all Clickhouse hosting providers.

By contrast, `beta features`_ are on track to becoming generally-available features, and so though they may change, they
are fully supported by the Clickhouse team, and will eventually be available on all Clickhouse hosting providers.

Decision
********

**Avoid experimental features**

Find alternative solutions and avoid enabling experimental features in Clickhouse.

**Use beta features with caution**

Use Clickhouse `beta features`_ only if no alternative solution can be found.

Plan a feature flag to disable functionality that depends on beta features, to avoid breaking deployments where
Clickhouse beta features are not available.

Consequences
************

#. Remove JSON field types from Clickhouse table schemas, and remove references to the flag that enables them
   (``allow_experimental_object_type``).

Rejected Alternatives
*********************

None

References
**********

* `tutor-contrib-aspects#376`_ Feat: Remove JSON column from xapi_events_all

.. _beta features: https://clickhouse.com/docs/en/beta-and-experimental-features#beta-features
.. _experimental features: https://clickhouse.com/docs/en/beta-and-experimental-features#experimental-features
.. _tutor-contrib-aspects#376: https://github.com/openedx/tutor-contrib-aspects/issues/376
