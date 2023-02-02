3. Superset as Data Visualizer
##############################

Status
******

Accepted

Context
*******

As we found in development of Insights, creating web-based visualization of data is a complicated
problem requiring a fair amount of resources and technical knowledge of both data and UI design. The
complexity and expense of adding new visualizations contributed to the stagnation of the Insights
project, in spite of it having a tremendous quantity of data to draw from.

Creating our new analytics system gives us an opportunity to bring in tools that are more flexible
and able to support our needs without introducing a lot of new technology for small site operators
to manage.

Decision
********

The Open Analytics Reference System (OARS) will use `Apache Superset`_ as its primary data visualization
and exploration tool. When developing a plan to support analytics in Open edX installs we have looked
for a solution that offered at least the level of functionality we were able to get from the Insights
user interface, as well as the following:

- Open source
- Deployable and configurable to work with OARS using Tutor
- Able to use the LMS as an authentication and authorization provider
- Capable of handling large quantities of data
- Minimal new technology / expertise needed beyond the usual Open edX stack
- Well supported
- Comes with a large set of visualizations to choose from
- Presents an API that allows authorized users to further access their data (for example via
  download or Javascript extensions to the LMS)
- Allows extension and customization for novel use cases
- Allows operators to create and share queries / visualizations with each other
- Allows site operators to choose from a wide variety of analytic database backends if necessary

Superset simple meets all of our needs without ballooning our tech stack or introducing vendor lock-in
or expensive paid solutions.

.. _Apache Superset: https://superset.apache.org/


Consequences
************

Superset will be integrated into OARS via a Tutor plugin that:

- Allows it to share the existing Tutor redis and MySQL services
- Integrates it with our chosen analytic database (detailed in a future ADR)
- Creates our default suite of visualizations
- Creates OAUTH integration with the LMS, with default permissions allowing different permissions for
  site operators, course instructors, and analytics users
- Any custom UI components that are needed to support our use cases (ex: a template showing all of an
  instructor's courses)

Rejected Alternatives
*********************

Rewrite the Insights Dashboard / New Custom UI
----------------------------------------------
As stated in Context, this is a complicated problem and would be an expensive distraction from our
core mission of education. Superset provides all that we could hope to create and much more with
a tool that is available today. Several Javascript libraries exist that simplify the visualization
aspect, but still require a great deal of work to create and maintain a site framework to drive
them.

Grafana
-------
While `Grafana`_ can be used for a variety of data visualization purposes, it is primarily for supporting
live services and lacks a lot of the visualizations that Superset has.

.. _Grafana: https://grafana.com/


Redash
------
`Redash`_ is similar in many ways to Superset, but seems poorly supported and possibly defunct. There
have been few commits and no responses to Github Issues in the last 3 months. It would also seem
to require operators to run Postgres in addition to the service itself, which isn't ideal.

.. _Redash: https://redash.io/

Several other options
----------------------
Most other packages in this space are either Javascript front-end components, make assumptions
about data sharing that are incompatible with our desired permissions, lack features we need, or do
not provide things we need in the open source versions of their products.
