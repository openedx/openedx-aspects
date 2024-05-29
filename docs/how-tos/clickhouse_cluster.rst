.. _clickhouse-cluster:

How To Run Aspects With ClickHouse Cluster
******************************************

ClickHouse clusters are an advanced way of running ClickHouse, but offer many benefits for large scale installations. Deciding whether to run in a clustered environment is a big decision with many cost and administrative impacts and should be carefully considered before launching a production environment. In most cases we expect Aspects to perform well without cluster scaling.

.. warning::
    Please fully understand the nuances of ClickHouse replication before choosing this route! While we have done some testing to ensure basic functionality of Aspects in a clustered environment, it may be expected to fail in novel and spectacular ways until we have a fully tested release running under load.


It is strongly suggested that if you are considering clustering you use a service provider to manage the cluster for you. `ClickHouse Cloud <https://clickhouse.com/cloud>`_ and `Altinity <https://altinity.com/cloud-database/>`_ both offer ClickHouse as a service. Altinity also offers `management services <https://altinity.com/cloud-database/#anywhere>`_ for running ClickHouse in your own Kubernetes environment.

Configuring Aspects to run in clustered mode is simple:

- Follow the directions in :ref:`remote-clickhouse` to set up your ClickHouse connection
- Set the ``CLICKHOUSE_CLUSTER_NAME`` Tutor configuration variables as appropriate for your installation
- Save your Tutor configuration: ``tutor config save``

When you initialize your environment the following changes will happen from a single server install:

- All users, databases, tables, views, functions, etc. will be created with ``ON CLUSTER 'your-cluster-name'``, including dbt managed views.
- All tables will be created with the Replicated versions of their table engines (ex: ``ReplicatedReplacingMergeTree``)
- ClickHouse traffic will be split among your nodes, as described in `their documentation <https://clickhouse.com/docs/en/architecture/cluster-deployment>`_ .
