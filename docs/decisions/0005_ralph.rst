5. Ralph as Learning Record Store
#################################

Status
******

Accepted

Context
*******

The xAPI specification adopted in :doc:`0002_xapi` uses a learning record store (LRS) as a
storage destination for xAPI statements. More information about LRSs can be found at `xapi.com`_.
There are many xAPI compatible LRSs, each with their own pluses and minuses, and supporting different
data storage backends. In discussions with the community while developing the OARS architecture
no community preference for an LRS was forthcoming.

.. _xapi.com: https://xapi.com/learning-record-store/

Decision
********

The Open Analytics Reference System (OARS) will use `Ralph`_ as its LRS. This decision was made for
several reasons:

- It is a toolkit already rooted in the Open edX ecosystem, and developed by a long-term Open edX partner (OpenFUN)
- It allows us to use `ClickHouse`_ as a database backend as decided in :doc:`0004_clickhouse`
- It uses technologies that are familiar in the community, increasing the likelihood of adoption and contribution
- It is open source (MIT License)
- It is deployable on commodity hardware with minimal configuration, using Tutor plugins


.. _ClickHouse: https://clickhouse.com/
.. _Ralph: https://openfun.github.io/ralph/


Consequences
************

Ralph will be integrated into OARS via a Tutor plugin. It will be configured to write xAPI statements to a
single table, and other OARS components will manage the downstream reporting schema separately.

A single Ralph instance should support a medium sized Open edX instance on commodity hardware,
including writing to ClickHouse while it is under normal reporting load for a small to medium Open edX install.
Large scale deployments, extremely intensive reports, or novel use cases are outside the scope of OARS v1.

Ralph does not currently support the entire xAPI LRS specification, only the `statements` endpoint, which is
all that we require for OARS v1. OpenFUN has been happy to receive pull requests and would welcome new contributions if further endpoints need
to be developed.

As Ralph's `statements` endpoint is xAPI compliant, other LRSs can be used for xAPI storage, however doing so
would likely mean losing the other OARS functionality (Superset reporting) if it does not support ClickHouse
for storage.


Rejected Alternatives
*********************

Off the shelf LRSs
------------------
No other xAPI LRS had the technology choices we were looking for, or had performance or licensing
restrictions that did not meet our desired levels for OARS. For instance, Learning Locker has an open
source version of their LRS, however it does not seem to be supported in any way. The xAPI reference
implementation is in Django, which is a familiar technology but is written as a transactional system
against MySQL and would not scale in the ways that we want. Other systems were cloud offerings or
otherwise licensed in ways that might restrict community adoption.

Writing our own
---------------
While the parts of the xAPI specification that we wish to use for OARS v1 are relatively simple, writing
and maintaining our own project was additional work that seemed to have little benefit over working with
an existing partner's existing project to mutual benefit.
