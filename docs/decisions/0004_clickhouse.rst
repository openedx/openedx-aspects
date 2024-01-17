4. ClickHouse as Analytic Database
##################################

Status
******

Accepted

Context
*******

Historically the Open edX analytics project known as Insights used a variety of tools and technologies to
gather data from several sources (tracking log events, replicas of source MySQL databases, the results
of API calls, etc.) and transform it using many different data pipelines into a form that could be queried
quickly from a MySQL database and Elasticsearch storage at scale.

These steps were expensive, time
consuming, and required extensive domain specific knowledge of the tools involved to configure and run.
Additionally as MySQL is a transactional database it is not optimized for a large scale analytical
workload, creating issues at scale that meant more pre-processing (and therefore data delay).

Technology in the analytics space has evolved rapidly in the 10 years since Insights was designed,
unlocking new capabilities that were not possible at the time. In development of the Aspects system we
have an opportunity simplify and improve our collection and use of analytics data, as well as greatly
lower the skill and cost requirements of running such a system.

Decision
********

The Aspects Analytics system (Aspects) will use `ClickHouse`_ as its analytic database. This
decision is rooted in the desire to provide high performance results on inexpensive hardware, while
maintaining the ability to scale up to large data sets and removing as much complexity, domain specific
knowledge, and pre-processing of the data as possible.

We have prioritized tools that offer simplicity of deployment and use, modern features for scalability
and advanced use cases, security, and high performance on commodity hardware. ClickHouse has all of these
as well as:

- Being open-source (Apache 2 license)
- Being deployable and configurable to work with Aspects using Tutor
- Having row based access controls
- Able to store and query JSON documents, such as our xAPI statements
- Using a familiar SQL interface, no new or esoteric languages needed
- Requiring minimal new expertise for basic installation and configuration of a small instance
- Flexible configuration to scale up to very large datasets for large instances
- Compatible with other Aspects technology (Superset, xAPI, Python)
- Able to efficiently read and write from a single instance in most cases
- Offering a cloud service for providers who prefer that to running their own, or who need advanced
  scaling


.. _ClickHouse: https://clickhouse.com/


Consequences
************

ClickHouse will be integrated into Aspects via the Aspects Tutor plugin.
It will be configured with a simple schema that should be sufficient for most installs,
users for the LRS and Superset, and with networking and permissions configured appropriately
such that all of these pieces work together "out of the box".

A single ClickHouse instance should support a medium sized Open edX instance on commodity hardware,
including supporting our default reporting queries from Superset. More advanced deployments may be
required for large scale deployments, extremely intensive reports, or novel use cases outside the scope
of Aspects v1.

With proper configuration we expect there will be no need for schema management or additional data
pipelines for our default reports. Further ADRs will cover the specifics of these decisions.


Rejected Alternatives
*********************

Snowflake, Redshift, BigQuery, CockroachDB, etc.
------------------------------------------------
Providing a flexible solution to our diverse international community means avoiding vendor lock-in,
restrictive licensing, and expensive software-as-a-service. Most tools in the OLAP database space are
closed source, have licensing costs, or tie the operator to a particular cloud service provider.
ClickHouse has a cloud solution, but it is optional and support for other deployment mechanisms is
strong.

MongoDB
-------
The Open edX LMS has had MongoDB as a database requirement for years, and it was a strong contender for
this use. However the other uses for MongoDB are being deprecated and it's expected to be retired from
use in the ecosystem. Interviews with site operators cited Mongo as a pain point and difficult to
manage.

The Mongo query language is a barrier for people unfamiliar with it, and while Mongo can scale
quite well the types of aggregate queries used for analytics tend to be comparatively expensive in terms
of development time and server resources. In the end ClickHouse was a better fit in terms of cost to run,
difficulty of operation, and overall speed.

MySQL / PostgreSQL / Citus PostgreSQL
-------------------------------------
These transactional databases provide a different set of features and performance characteristics than
what is needed for a large scale analytical workload. Citus is a plugin for PostgreSQL that allows some
interesting analytic functionality such as a column store backend like ClickHouse. While any of them can
be made to scale in ways that would work for us, the investments in time, complexity, and additional
hardware costs ruled them out.
