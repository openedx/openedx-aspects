6. Areas of Responsibility
###############################

Status
******

Superseded by `ADR 8 Project structure`_.

Context
*******

The Aspects Analytics system (Aspects) consists of several pieces of technology working together via
some configuration and scripting. Decisions around where to store data and configuration need to be made
so that developers understand where to make changes and look for the causes of issues. These decisions
can have wide ranging impact on things such as extensibility and configurability of the system as a whole.

The number of plugins and systems in play can make it difficult to know where to look for configuration
or add new features. This ADR hopes to address this by offering the following guiding principles:

- Each service-based Tutor plugin should be able to be run the service separately from Aspects, and in different
  configurations
- Opinionated configuration and non-LMS service associations belong in the tutor-contrib-aspects plugin


Decisions
*********

The service-based Tutor plugins (``tutor-contrib-clickhouse``, ``tutor-contrib-ralph``, ``tutor-contrib-superset``)
will each be able to be run outside the Aspects context, such that if members of the community want to use
them in a modified way, or override Aspects defaults, that will be possible. It is still assumed that the
plugins will be used in an Open edX context and they will integrate themselves with the platform where
necessary.

Specifically:

#. ``tutor-contrib-clickhouse`` will:
    #. Create a ClickHouse admin user
    #. NOT create any databases or tables
#. ``tutor-contrib-ralph`` will:
    #. Create an Ralph admin user
    #. Create a Ralph user for an LMS to use to insert statements
    #. NOT create any ClickHouse databases, users, or tables
    #. Note: Ralph will fail to start if the configured ClickHouse database and table
       for xAPI statements has not yet been created
#. ``tutor-contrib-superset`` will:
    #. Create an admin user
    #. Create the Superset-specific MySQL database and permissions for the admin user (Note:
       By default this uses the LMS MySQL instance to save on system resources)
    #. Create a user in LMS for SSO
    #. Register itself as an SSO target with the LMS
    #. Disable local user management to force SSO login from LMS
    #. Create a set of default roles and permissions based on LMS permissions for each user
       (course staff, global staff, superuser, etc)
    #. Create row-based filters for queries to enforce course-level permissions (Note:
       since there are no datasets yet there is nothing to connect them to, but
       they are created here as they would likely be useful for a non-Aspects use case)
    #. NOT create any ClickHouse databases, users, or tables

The process of tying these plugins together is managed by the ``tutor-contrib-aspects`` plugin, which
does not provide a running service, but rather the opinionated configuration of the above services
and commands to manage them:

#. In ClickHouse:
    #. Create any necessary databases (currently xAPI and course data)
    #. Create and manage the schemas (currently this is a very basic proof-of-concept, but will
       soon be managed via dbt)
    #. Create users and permissions for Ralph, Superset, and CMS (for inserting course structure data)
#. In Ralph:
    #. Configure the ClickHouse user
    #. Configure the ClickHouse database and xAPI statements table to write to
    #. Optionally create test data in ClickHouse via Ralph
#. In Superset:
    #. Configure the ClickHouse user
    #. Configure default dashboards, datasets, and reports
    #. Attach the row level course filter to the appropriate datasets
#. In LMS:
    #. Add event-routing-backends as a Python requirement
    #. Create an Aspects user, necessary for the next step...
    #. Configure event-routing-backends to use xAPI and send statements to Ralph
       using the LMS user created in ``tutor-contrib-ralph``)

The Aspects plugin will also be the conduit for running dbt via Tutor "do" commands. The
dbt integration will be covered in a separate ADR.

Consequences
************

* The service-related plugins (ClickHouse, Ralph, Superset) can be run together or separately
  with configurations different from the Aspects defaults
* A separate set of plugins could be created to replaces pieces of the stack with different
  technologies (ex. replace Superset with Tableau, or ClickHouse with other supported Ralph
  backend)
* Extensions can be made at any level via additional Tutor plugins or other configuration
* Configuration of the same services takes place in different plugins, which can be confusing.
  The hope is that this ADR clarifies where to look and add new functionality.

Rejected Alternatives
*********************

**Placing all of each service's configuration into its plugin**

This was considered and briefly implemented, but required tight coupling between the plugins
and created a different level of confusion about whether a ClickHouse user for Ralph belonged
in the ClickHouse plugin or Ralph's. It was similarly confusing for shared resources like the
ClickHouse schema which Ralph writes to part of, but the rest is managed elsewhere.

This would also leak Aspects implementation details into all of the plugins, reducing their
flexibility for other use cases.


.. _ADR 8 Project structure: 0008_project_structure.rst
