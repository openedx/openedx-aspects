Superset
#############

Apache Superset is a modern, enterprise-ready business intelligence web application.
It is fast, lightweight, intuitive, and loaded with options that make it easy for users
of all skill sets to explore and visualize their data, from simple pie charts to highly
detailed deck.gl geospatial charts.

Superset is used as the reporting and visualization tool of the Aspects project. Authentication
is performed agains the LMS using SSO. You can find more information in
:ref:`authentication-permissions`.

Superset Concepts
-----------------

Superset is composed of several main concepts:

- **Databases**: Superset can connect to a wide variety of databases. Once connected,
  Superset allows you to explore your data, build dashboards, and create charts.
- **Datasets**: A dataset is a reference to a table in a database. Superset uses
  datasets to refer to the raw data that will be visualized in a chart. Datasets
  can also be virtual (SQL queries).
- **Slices**: A slice is a configuration object that tells Superset how to visualize
  a dataset. Slices are composed of a set of fields, a visualization type (such as
  line chart or world map), and a variety of other parameters that determine how the
  data is displayed.
- **Dashboards**: Dashboards are collections of slices that can be arranged in a
  single screen to provide a high-level overview of data. Dashboards can be shared
  with other users, and can be scheduled to refresh periodically.
- **Assets**: Assets are any or the components described above.

For instance, in Aspects when we want to display enrollments in a course Superset will:

Display an Enrollment Dashboard, with several Slices (pie charts, line charts) that pull
data from the Enrollments Dataset which are stored in the ClickHouse databases. Aspects
stores the definitions for all of these things (and any custom ones a site operator adds)
in a set of Assets that are imported when the tutor init command is run.

You can find more information about Superset concepts in the `Superset Documentation <https://superset.apache.org/docs/intro>`_.
