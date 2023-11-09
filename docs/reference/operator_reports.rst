.. _operator-reports:

Operator Reports
################

The Operator Dashboard contains charts that are of interest to site operators and system administrators.

The dashboard is visible to Global Staff and Superusers on Open edX.

.. _operator_filters:

Filters
*******

You can filter the data used by these charts by applying various options from the Filters panel.

These filters are configured to apply to specific charts, and so some may show under "out of scope" if they are unused by the current page of charts.

.. note: Ensure that the "Time range" filter is set to the desired date/time range. By default, only the previous quarter of data is shown.


.. _instance-health-tab:

Instance Health
***************

Shows charts and counts useful for monitoring the basic health of the Open edX / Aspects integration.

.. _users-over-time:

Active Users Over Time
======================

Shows the total number of unique users on Open edX.

.. _events-over-time:

xAPI Events Over Time
=====================

Shows the total number of xAPI events received from Open edX.

.. _instance-information:

Instance Information
====================

Shows the current running versions of Aspects and the systems that underly it.

.. _total-users:

Total Unique Users
==================

Shows the total number of unique users associated with the Open edX event data.

.. _total-courses:

Total Courses
=============

Shows the total number of courses associated with the Open edX event data.

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


.. _enrollments-tab:

Enrollments
***********

Shows basic enrollments charts.

.. _enrollments-over-time:

Course Enrollments Over Time
============================

Shows the total of unique enrolled learners at the end of each day of the selected time range.

If a learner was enrolled previously, but has left the course since, they are not counted as of the date they left. If they re-enroll in the course they will be counted again.

.. _enrollments-by-type:

Enrollments by Type
===================

Shows the current count of active enrollments grouped by their most recent enrollment mode (audit, verified, etc).

For example, if a learner upgraded from Audit to Verified they will only be counted once as Verified. Learners who have un-enrolled in the course are not counted.

.. _courses-tab:

Courses
*******

Shows basic course data.

.. _active-courses:

Most Active Courses Per Day
===========================

Shows the courses with the most events per day.


.. _org-tab:

Organizations
*************

Shows basic data grouped by Organization.

.. _courses-per-org:

Courses Per Organization
========================

Shows the total number of courses per organization.

.. _users-per-org:

Active Users Per Organization
=============================

Shows the total number of users per organization.


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

Active Users
============

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

.. _superset-chart-count:

Chart Count
===========

Shows the number of Superset charts created during the selected time range.

.. _superset-most-used-charts:

Most-used Charts
================

Shows the number of Superset actions taken on each chart during the selected time range.

.. _superset-charts-by-type:

Charts by Type
==============

Shows which types of Superset charts were in use over the selected time range.

.. _superset-dashboard-count:

Dashboard Count
===============

Shows the number of dashboards created in Superset over the selected time period.

.. _superset-most-used-dashboards:

Most-used Dashboards
====================

Shows the number of Superset actions taken on each dashboard in the selected time range.
