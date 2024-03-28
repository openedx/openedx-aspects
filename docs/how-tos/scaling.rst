.. _scaling:

Scaling your deployment
***********************

By default, the `Aspects Tutor plugin`_ deploys single nodes for these services:

* :ref:`quick-start-ralph` or :ref:`quick-start-vector`
* Clickhouse: ephemeral single node cluster
* Superset: shares Open edX's MySQL and Redis instances

Most deployments will benefit greatly from scaling horizontally and/or vertically, especially when running Aspects. Aspects is fed by Open edX event data, which is triggered by user actions on the site, and Open edX can generate a lot of event data. The initial processing of this event data occurs in platform plugins, so scaling your LMS workers speeds this processing time. And the faster events can be processed, the quicker you will see them appear in Aspects' dashboards and charts.

And all production deployments will need a `persistent Clickhouse cluster`_.

Preparing the LMS workers
=========================

Before deploying Aspects, we recommend :ref:`event_bus`.

Or, if you'd rather use celery, we recommend boosting the number of LMS workers to prepare the celery queue for the high-volume of Aspects tasks.

These plugins can be used to configure and enable autoscaling for the LMS and CMS. See their READMEs for details:

* `tutor-contrib-pod-autoscaling`_ : for single instance deployments
* `tutor-contrib-grove`_ : for multiple instance deployments

We also recommend configuring the LMS to use the high-priority celery queue for Aspects tasks (`platform-plugin-aspects event sinks`_, `event-routing-backends xAPI tasks`_). This leaves the low-priority queue clear for other LMS tasks.

.. code-block:: yaml

  TBD -- implement configurable queue for Aspects tasks

Scaling Ralph
=============

Without scaling, Ralph can be a bottleneck in the Aspects data pipeline. If you do not need an LRS at all, you can disable Ralph and use :ref:`quick-start-vector` instead.

But if you will ever need an LRS, it's better to start with Ralph enabled and autoscaled.

Ralph runs CPU-intensive operations, so we recommend scaling mainly on CPU:

.. code-block:: yaml

  TBD -- implement RALPH autoscaling

.. _scaling-clickhouse:

Scaling Clickhouse
==================

We recommend using a Clickhouse service provider to manage your production cluster.

Aspects `avoids using experimental Clickhouse features`_, and so is suitable for use with cloud providers. Cloud hosting also provides support, automated backups, and autoscaling. See :ref:`clickhouse-cluster` for details.

However, if you decide to run your own Clickhouse instance, you will need to take into account:

* horizontal and vertical scaling
* replication and quorum
* data storage requirements over time

References:

* `Clickhouse Operator`_: Helm charts, docs and examples from Altinity
* `Clickhouse Keeper`_: recommended replication setup

Small deployments can start with the following set up, and scale later:

* 1 Clickhouse Keeper node, see `04-replication-zookeeper-01-minimal.yaml`_
* 1 Clickhouse node, see `03-persistent-volume-01-default-volume.yaml`_

For large deployments, we recommend:

* 3 Clickhouse Keeper nodes to form the quorum: see `02-extended-3-nodes.yaml`_
* N Clickhouse nodes to perform the replication.

  If your k8s provider supports resizable volumes, see `03-persistent-volume-05-resizeable-volume-2.yaml`_
  Otherwise, see `03-persistent-volume-02-pod-template.yaml`_

Scaling Superset
================

By default, Aspects configures Superset to share these resources with Open edX:

* mysql
* redis

However, if it becomes too resource intensive, these services can be replaced with separate standalone services.

.. code-block:: yaml

  TBD -- needs fixing


Superset should also be configured to autoscale based on CPU and RAM. Use a similar configuration as your CMS:

.. code-block:: yaml

  TBD -- implement Superset autoscaling


Superset also supports these scaling features, which may be supported by future versions of Aspects.

* `asynchronous queries`_: configure the database assets to enable "Asynchronous query execution mode", which moves query execution to the celery workers. 
  This is useful for queries thtat run beyond a typical web request's timeout (30-60 seconds).
* cache warming: schedule tasks to use the `Superset API`_ to pre-fetch data into the caches.
  This is useful for frequently-accessed datasets or charts.

References:

* https://www.restack.io/docs/superset-on-kubernetes
* https://medium.com/airbnb-engineering/supercharging-apache-superset-b1a2393278bd
* https://preset.io/blog/2020-08-11-nielsen-superset/
* https://flask.palletsprojects.com/en/1.1.x/becomingbig/


.. _Aspects Tutor plugin: https://github.com/openedx/tutor-contrib-aspects
.. _tutor-contrib-pod-autoscaling: https://github.com/eduNEXT/tutor-contrib-pod-autoscaling
.. _tutor-contrib-grove: https://gitlab.com/opencraft/dev/tutor-contrib-grove
.. _platform-plugin-aspects event sinks: https://github.com/openedx/platform-plugin-aspects/blob/main/platform_plugin_aspects/tasks.py
.. _event-routing-backends xAPI tasks: https://github.com/openedx/event-routing-backends/blob/master/event_routing_backends/tasks.py
.. _persistent Clickhouse cluster: #scaling-clickhouse
.. _Clickhouse cloud: https://clickhouse.com/cloud
.. _avoids using experimental Clickhouse features: ../decisions/0013_clickhouse_experimental.html
.. _Clickhouse Operator: https://github.com/Altinity/clickhouse-operator
.. _Clickhouse Keeper: https://github.com/Altinity/clickhouse-operator/blob/master/docs/zookeeper_setup.md
.. _04-replication-zookeeper-01-minimal.yaml: https://github.com/Altinity/clickhouse-operator/blob/master/docs/chi-examples/04-replication-zookeeper-01-minimal.yaml
.. _03-persistent-volume-01-default-volume.yaml: https://github.com/Altinity/clickhouse-operator/blob/master/docs/chi-examples/03-persistent-volume-01-default-volume.yaml
.. _02-extended-3-nodes.yaml: https://github.com/Altinity/clickhouse-operator/blob/master/docs/chk-examples/02-extended-3-nodes.yaml
.. _03-persistent-volume-05-resizeable-volume-2.yaml: https://github.com/Altinity/clickhouse-operator/blob/master/docs/chi-examples/03-persistent-volume-05-resizeable-volume-2.yaml
.. _03-persistent-volume-02-pod-template.yaml: https://github.com/Altinity/clickhouse-operator/blob/master/docs/chi-examples/03-persistent-volume-02-pod-template.yaml
.. _asynchronous queries: https://superset.apache.org/docs/installation/async-queries-celery/
.. _Superset API: https://superset.apache.org/docs/api/
