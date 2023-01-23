1. Open Analytics
##################################

Status
******

**Draft** (-> Accepted)

Context
*******

Analytics for Open edX has been neglected since Insights and the related repositories stopped being
actively supported around 2018. The goal at the time was to eventually replace Insights, but
that project was never picked up. While the community has done some recent work circa 2022 to update
Insights, it was never a widely adopted solution for the wider community. Interviews with the community
have revealed a few reasons why:

- It is complicated, comprising 6 Github repositories, many pieces of infrastructure, and requiring
  knowledge of several domain specific technologies to configure (Pandas, Hive, Sqoop, Hadoop,
  Luigi, etc.)
- It is expensive to run, and is in many ways specific to Amazon Web Services technologies
- Turnaround time for data refreshes are on the order of a day or more in most cases
- Documentation is out of date, further complicating any new adoption or alternative deployments
- Discrepancies between Insights data calculations and data displayed in Studio have caused confusion

Architectural decisions made post-Insights and new technologies have changed the analytics
landscape, unlocking the ability to deliver analytical and operational data and display it in
near-real time on commodity hardware with much simpler configuration and deployment. Additionally
we have a wide variety of use cases in the Open edX community with differing requirements for
privacy, scalability, budget, and expertise.

Decision
********

We will create the Open Analytics Reference System (OARS) that combines existing open source projects
into a preconfigured bundle that can be easily deployed using Tutor.

This system will:

- Transform existing Open edX tracking log events into an open standard format
- Store them using a standards-compliant learning record store
- Present a user interface of data visualizations secured via single-sign-on against the LMS
- Allow download of report data for those with permissions to view it
- Provide a secure API for integrations with other tools or data viewing methods

The guiding principals for technology selection are:

- Based on open standards and open source
- Hosting service agnostic
- Inexpensive to run
- Able to support near-real-time data where possible
- Require little specialized knowledge to set up and maintain
- Be extensible for a variety of common use cases not covered by the default configuration

Consequences
************

- Small and medium Open edX installs will have easy access to timely and relevant reports
  about the usage of their site, the performance of their classes, and the status of their
  students.
- Use cases for advanced learner interventions and data-guided learning pathways will be
  unblocked by access to near-real-time data provided in an industry standard format.
- This reference implementation will replace Insights as the recommended analytics platform
  for Open edX.

Rejected Alternatives
*********************

Resurrect support of Insights
-----------------------------
Given the low adoption rate of Insights and its extremely high development, deployment, and
maintenance costs, the value of this work seemed low.

Rewrite Insights
----------------
A complete rewrite of the Insights project could have met many of our goals here, however
our focus is on education. The cost and maintenance burden of creating a bespoke analytics
pipeline and visualization solution is an unnecessary distraction when excellent open source
tools exist that are much more feature rich, configurable, and better maintained than we could
manage given our competing priorities.

Use an existing community system
--------------------------------
In the absense of an officially supported analytics system, several organizations have created
their own solutions. At the time of investigation none supported all of the features we are hoping
to make available through this system.


References
**********

- `OEP-26: Real Time Events <https://docs.openedx.org/projects/openedx-proposals/en/latest/architectural-decisions/oep-0026-arch-realtime-events.html/>`_
- `OEP-30: PII Markup and Auditing <https://docs.openedx.org/projects/openedx-proposals/en/latest/architectural-decisions/oep-0030-arch-pii-markup-and-auditing.html/>`_
- `OEP-52: Event Bus Architecture <https://docs.openedx.org/projects/openedx-proposals/en/latest/architectural-decisions/oep-0052-arch-event-bus-architecture.html/>`_
- `External User IDs ADR-0001 <https://github.com/openedx/edx-platform/blob/master/openedx/core/djangoapps/external_user_ids/docs/decisions/0001-externalid.rst/>`_
