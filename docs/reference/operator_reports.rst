.. _operator-reports:

Operator Dashboard Reports
##########################

The Operator Dashboard contains charts that are of interest to site operators and system administrators.

The dashboard is visible to Global Staff and Superusers on Open edX.

.. warning:: 

    The Operator Dashboard is in a beta state and has not received the same amount of polish as the other dashboards. We expect to address the operator dashboard in future versions of Aspects. Please contact us in the #aspects channel on Open edX Slack, or in the Analytics topic in our forums if you would like to offer suggestions or feedback, or participate in upcoming formal feedback sessions about this dashboard!


.. _operator_filters:

Filters
*******

You can filter the data used by these charts by applying various options from the Filters panel.

These filters are configured to apply to specific charts, and so some may show under "out of scope" if they are unused by the current page of charts.

.. note: Ensure that the "Time range" filter is set to the desired date/time range. By default, only the last 90 days of data is shown.


.. _instance-health-tab:

Instance Health
***************

Shows charts and counts useful for monitoring the basic health of the Open edX / Aspects integration.

.. _active_learners:

Active Learners
===============

Shows the number of users who have xAPI events for the selected time range. 


.. _active_courses:

Active Courses
==============

Shows the number of courses that have xAPI events for the selected time range. 

.. _event_activity:

Event Activity
==============

Shows the number of xAPI events for the selected time range.


.. _total-orgs:

Total Organizations
===================

Shows the total number of organizations associated with the Open edX event data.

.. _last-event-received:

Last Received Event
===================

Shows the UTC date/time of the most recently received event from Open edX.

.. _last-course-published:

Last Course Published
=====================

Shows the UTC date/time of the most recently published course.

.. _total-courses:

Total Courses
=============

Shows the total number of courses associated with the Open edX event data stored in Aspects. 

.. note: This may not be every course which exists in the LMS / Studio. Courses populate in Aspects once published, and older courses can be brought into Aspects using the steps outline in `backfill_course_blocks`_


.. _enrollments-tab:

Enrollments
***********

Shows basic enrollments charts.

.. _enrollments-over-time:

Current Active Enrollments By Mode
==================================

Shows the counts of students currently enrolled in each mode for each course. If there are no enrollments for a mode it will be omitted.


.. _org-tab:

Organizations
*************

Shows basic data grouped by Organization.

.. _users-per-org:

Active Users Per Organization
=============================

Shows the total number of users per organization with any activity, whether they are currently enrolled or not.


.. _courses-per-org:

Courses Per Organization
========================

Shows the total number of courses per organization. As above, this may not represent all courses in LMS / Studio, only those which have been published or backfilled to Aspects.


.. _clickhouse-tab:

ClickHouse
**********

Shows charts related to the use of ClickHouse, the Aspects event database.

.. _slowest_clickhouse_queries:

Slowest ClickHouse Queries
==========================

Shows metadata for the 100 slowest queries executed on ClickHouse.

.. _clickhouse-metrics:

Clickhouse Metrics
==================

Table showing some useful metrics from the ClickHouse system tables. See each row's "description" field for details on each metric.


.. _superset-tab:

Superset
********

Charts related to the use of Superset, the Aspects frontend.

.. _superset-active-users:

Superset Active Users
=====================

Shows a count of unique users who performed an action in Superset over the selected time range.

.. _superset-active-users-over-time:

Active Users Over Time
======================

Shows the number of unique users who performed an action in Superset during the selected time range.

.. _superset-registered-users-over-time:

Registered Users Over Time
==========================

Shows the total number of registered users for the selected time range/grain.

.. _superset-user-actions:

User Actions
============

Shows the number of Superset actions taken by each user for the selected time range.

.. _superset-most-used-charts:

Most-used Charts
================

Shows the number of Superset actions taken on each chart during the selected time range.

.. _superset-most-used-dashboards:

Most-used Dashboards
====================

Shows the number of Superset actions taken on each dashboard in the selected time range.
