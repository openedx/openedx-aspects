.. _aspects-overview:

Aspects Overview
****************

What it is
##########

Aspects captures learning events and transforms them into data visualizations. When a learner enrolls in a course, that event is captured in a database and displayed back to the course instructor as a graph of learner enrollments over time. When an instructor adds a new problem to their course and publishes it, the course data is refreshed in the database so that it can immediately begin showing information about how learners answer the question.

Aspects is being built to help Open edX users answer questions like:

- How many learners were active in a specified time period?
- How many learners are participating in forum discussions?
- How often was this problem answered correctly vs incorrectly?
- How much of each video is watched, and which sections were re-watched most?

By default Aspects focuses on learner privacy and does not include the ability to identify learners in the reports. This type of functionality can be added via plugins if desirable, but can have negative performance and user interface issues for large courses.

How it works
############

Many actions in the Open edX platform generate :ref:`tracking-logs`, which are captured by the event-routing-backends plugin, transformed into :ref:`xAPI <xapi-concepts>` statements, and either forwarded to the :ref:`Ralph <ralph>` learning record store or sent to the :ref:`Vector <vector>` log statement forwarder (depending on configuration). Either option will save the xAPI statement to a :ref:`ClickHouse <clickhouse>` analytic database. Once in the database, the statement can be transformed and aggregated in many different ways using different types of views or intermediate tables to generate data that is then displayed using :ref:`Superset <superset>`.

See the :download:`Data Flow PDF </_static/AspectsDataFlows.pdf>` for more details.

For Course Teams
~~~~~~~~~~~~~~~~

Course teams have access to several dashboards, as configured by their site operators. 

See :ref:`Course Team <course_team>` for detailed information on how course teams can interact with Asepcts.

For Analysts
~~~~~~~~~~~~

Data Analysts don't yet have specific roles that we can pull from the Open edX installation, but we hope to be able to do that soon. For now, you should be able to get appropriate permissions assigned to you by a site operator or administrator with the necessary permissions. In addition to being able to see the Instructor Reports you may get access to the Operator Reports and the ability to use the SQL Lab to run queries directly against the different ClickHouse data sources.

See the `Superset <https://superset.apache.org/docs/intro>`_. documentation for more information on how to use the advanced Superset features.

For Operators
~~~~~~~~~~~~~

Site operators have full administrative access to Superset as well as a dashboard :ref:`Operator Reports <operator-reports>` of metrics to monitor instance-wide health and activity. See the `Superset <https://superset.apache.org/docs/intro>`_. documentation for more information on how to use the advanced Superset features. You can also create new dashboards and charts.

For Developers
~~~~~~~~~~~~~~

Developers can :ref:`extend <extensions>` Aspects in numerous ways to work with the many ways Open edX can be configured and unique reporting needs for each organization.
