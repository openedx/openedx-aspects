.. _aspects-without-tutor:

Running Aspects Without Tutor
*****************************

In cases where Open edX is deployed outside of the Tutor environment, setting up Aspects is quite challenging. This guide aims to present the steps needed to stand up and configure an Aspects environment using Tutor and tutor-contrib-aspects to create the resources needed to configure an Aspects environment with an existing non-Tutor deployment.

.. warning::
    This is a complicated process with many moving pieces, and as Aspects evolves this piece of documentation is more likely than most to fall behind. Please help us keep it up to date by submitting changes back to openedx-aspects or opening issues there is you find it incorrect or incomplete. It is expected that this work is being done in a production-like test environment first as it will undoubtedly involve a lot of starting / stopping / re-configuring and downtime.

.. warning::
    Aspects through version 1.x has been tested with Open edX versions back to Nutmeg. It is likely that there will be bugs or other issues for earlier versions, and it is strongly recommended that Open edX be run on recent named releases that are still receiving security patches.

.. warning::
    This document assumes your final environment will be Docker based and offers instructions for Docker Compose and Kubernetes. Many of the instructions may be applicable to other deployment strategies with more work.

What tutor-contrib-aspects does
===============================

.. note::
    Almost all of the steps below are run as Tutor init steps, and the scripts that power them can be found here: https://github.com/openedx/tutor-contrib-aspects/tree/main/tutoraspects/templates/aspects/jobs/init

As an overview to the process, here are the high level steps that tutor-contrib-aspects takes to set up Aspects:

#. Builds custom images
    #. Dockerfiles are found here: https://github.com/openedx/tutor-contrib-aspects/tree/main/tutoraspects/templates/aspects/build
    #. aspects (to run various jobs and serve the dbt documentation)
    #. aspects-superset (to add our custom configuration, code, and assets to the default Superset image)
#. Configures and runs containers
    #. Superset (required due to our customizations)
    #. ClickHouse (optional)
    #. Ralph (optional)
    #. Vector(optional)
    #. Event bus consumer (optional)
    #. Aspects docs (optional)
#. Configures MySQL
    #. Adds Superset database
    #. Adds Superset database user
    #. Grants access to some Superset tables for operator dashboard reporting
#. Configures ClickHouse
    #. Creates databases for xapi, event_sink, vector, and reporting
    #. Creates users for ralph, vector, reporting, and event_sink (studio / lms)
        #. Makes sure those users' passwords are up to date, allowing rotating those passwords
    #. Grants appropriate permissions to those users
    #. Runs the Aspects Alembic schema migrations to create the base tables that Aspects writes to
    #. Runs the dbt migrations to create downstream reporting tables / views / dictionaries
#. Configures Ralph (optional)
    #. Creates a user for the LMS to use when sending xapi events
    #. Sets up authentication and configuration to write to ClickHouse
#. Configures Vector (optional)
    #. Sets up authentication and configuration to write to ClickHouse
    #. Creates source, transform, and sink configuration for xapi and/or tracking logs
#. Configures an event bus consumer (optional, experimental)
    #. If an event bus is being used in the deployment, consumer containers using the openedx image can be configured and run
#. Configures Superset
    #. Runs the Superset Alembic schema migrations to create the Superset database
    #. Creates a Superset UI admin user
    #. Creates an LMS UI admin user for embedded dashboards in the Instructor dashboard
    #. Sets up Superset roles and permissions
    #. Imports our databases, datasets, charts, and dashboards
        #. Each of these are created per-language due to limitations in Superset localization
#. Configures LMS / Studio
    #. Adds the event-routing-backends package for xapi event transformation and delivery
    #. Adds the platform-plugin-aspects package for event sinks and embedded dashboards
    #. Creates an LMS learner for Superset single-sign-on use
    #. Creates Superset single-sign-on Django OAuth Toolkit applications for dev and prod
    #. Creates a user in LMS for managing configuration (used in next steps)
    #. Creates a configuration for event-routing-backends to be able to write to Ralph if Ralph is being run
    #. Sets waffle flags to define which event sinks are enabled
    #. Many settings are added or changed based on Aspects configuration
        #. Event delivery settings for event-routing-backends
        #. Event sink settings for platform-plugin-aspects
        #. Embedded dashboard settings, including locales and dashboards to embed and the instructor dashboard filter
        #. Optional event bus configuration
#. Adds Docker Compose (dev and local) and Kuberenetes configurations

Using Tutor to template configuration
=====================================

As you can see, the plugin does many things to simplify and automate some very complicated service connections and configuration. Because so many things need to be kept in step across services (ex: database passwords need to set in ClickHouse and used in LMS) we recommend using Tutor to generate rendered scripts, settings files, Dockerfiles, Superset assets, and other configuration that you can either use directly in your own deployments or add to your existing files.

This way settings for things which may impact multiple services (ex: using Ralph) can be handled in the way that Aspects is expecting, hopefully leading to a lot less confusion and frustration for you in the end. You never even need to start your Tutor environment up or install Docker, we will just be using the rendered template files that are generated by `tutor config save`.

The rest of this guide assumes you are using Tutor locally to create the files you can use to power your own deployments.

Step 0: Make configuration choices
==================================

When running outside of Tutor the cycle of making changes and testing them is likely to be substantially more difficult and time consuming. It's worth it to take some time and understand the Aspects options ahead of time so you can make informed choices from the start. We suggest you review :ref:`Production Configuration <production_configuration>` before continuing, and especially make choices on:

- Event delivery
    - Ralph vs Vector
    - If Ralph is chosen, Celery vs Event bus
- How & Where ClickHouse is going to be run
    - If running in Kubernetes or hosted at Altinity you will need cluster settings
    - If running a single server or in ClickHouse Cloud you will not
    - ClickHouse has a very unstable API, make sure that if you are not running the same images as Aspects that it is at least the same minor version (ex: 24.3) to prevent errors and issues
- How will services connect to each other?
    - Will you run a Kubernetes environment, a Docker Compose environment, or something else?
    - Once secured, how will the following communications take place, and will you need intermediate addresses to facilitate those communications like proxies, bastion hosts, or load balancers
        - LMS / Studio worker -> Ralph or Vector
        - LMS / Studio -> ClickHouse (event sink)
        - Ralph / Vector -> ClickHouse (xapi / tracking logs)
        - Superset -> ClickHouse
        - Superset -> MySQL (will it have its own database server?)

By default the Aspects plugin will create random passwords for any new credentials that it needs. If you have special requirements for credential generation or credentials provided by a service provider (such as ClickHouse Cloud) you can apply them in the next step, but it's good to gather them now.

Step 1: Set up Tutor
====================

#. Follow the instructions here: https://docs.tutor.edly.io/gettingstarted.html to set up a local Tutor environment
    #. It should use the version of Tutor that works with the closest Open edX named release to what you are running in production.
#. (suggested) Set up a git repository to store the rendered files so that you can maintain history and view your changes over time. NOTE: This will contain MANY sensitive passwords used in your Open edX data! Make sure it is appropriately secured!
    #. When you run ``tutor config save`` it will output the path to your ``config.yml`` and ``env`` directories. These are the things you will want to save, and what we will be working with here.
#. Install the tutor-contrib-aspects plugin and enable it: https://github.com/openedx/tutor-contrib-aspects
#. Update settings to match your environment. At a minimum you will need to add or change these settings in your ``config.yml`` to point to the correct values for your environment:
    #. General environment settings
        #. LMS_HOST should be the name of your base LMS URL (ex: school.edu). Tutor will attempt to use subdomains off of this URL for services, such as "ralph.school.edu" and "superset.school.edu".
        #. ENABLE_HTTPS should be ``true`` if your subdomains are behind a TLS certificate. When true all links between public interfaces (ex: LMS -> Superset) will be prepended with ``https`` instead of ``http``.
    #. By default Aspects configures Superset to use the same MySQL and redis servers that LMS / Studio use, which will be incorrect for your environment:
        #. SUPERSET_DB_HOST
        #. SUPERSET_DB_PORT
        #. SUPERSET_DB_NAME
        #. SUPERSET_DB_PASSWORD
        #. SUPERSET_DB_USERNAME
        #. REDIS_HOST
        #. REDIS_PORT
        #. REDIS_PASSWORD
    #. If you are running Vector you will likely need to make a number of adjustments to the generated configuration in order to get it to work.

Once you execute a ``tutor config save`` you will have many files created in your Tutor ``env`` directory with the new settings. Every time you change ``config.yml`` you MUST re-run ``tutor config save`` to update the generated files.

.. note:: If you need to override the automatically generated passwords with other credentials you can do that now, in the ``config.yml`` file. After saving those changes, you will need to re-run ``tutor config save`` to apply them.

Step 2: Service environment
===========================

In the next steps you'll combine the new services created by Tutor with your existing environment. For each of these you should only need the information for the subset of services that are specific to Aspects. Specifically:

- superset / superset-worker / superset-beat
- clickhouse (if enabled)
- ralph (if enabled)
- vector (if enabled)
- aspects-docs (if enabled)

Step 2a: Docker Compose
#######################

If you are working in a Docker Compose environment you will find files that you can modify for your needs in ``env/local``. The mounted volumes in those files include files needed by Aspects and will need to updated and have their local contents copied if you move the Compose files to a different location.

Step 2b: Kubernetes
###################

If you are working in a Kubernetes environment the resources are located in ``env/k8s``.

Step 3: Build custom images
===========================

The Dockerfiles for the ``aspects`` and ``aspects-superset`` images will be in ``env/plugins/aspects/build``. The files in those directories are necessary for the images to build. You should be able to just ``docker build`` them as usual, or take the custom parts of the images for your own build process. Custom configuration for LMS / Studio is added via a Tutor patch. You will need a version of these settings for things to work properly. The section of configuration you need to add is here:

https://github.com/openedx/tutor-contrib-aspects/blob/main/tutoraspects/patches/openedx-common-settings


Step 4: Initialize
=============================

This step emulates the running of Tutor init tasks. It must be completed in this order. It's possible that this list will fall out of date, you can see the current version of this list of tasks here: https://github.com/openedx/tutor-contrib-aspects/blob/main/tutoraspects/plugin.py#L469

.. warning::
    Right now Tutor doesn't save the Jinja-rendered initialization scripts to disk, it just renders them at runtime and sends them the Docker commands. As such you can either run the tutor `do init` command for you deployment type (local/k8s), find a way to render the Jinja files referenced in the above list of tasks using your set of variables, or painstaking copy those files and replace the variables by hand.

    If people are doing this often it would be useful to write a Tutor plugin to just render the files to a given location to ease this part of the process. The templates we use are included below:

The paths to the template files can be found in the plugin.py linked above. So to find the template:

``("mysql", ("aspects", "jobs", "init", "mysql", "init-mysql.sh"), 92),``

you would look here: https://github.com/openedx/tutor-contrib-aspects/blob/main/tutoraspects/templates/aspects/jobs/init/mysql/init-mysql.sh


Testing
=======

If you've made it this far, congratulations! There are likely to be a number of issues you'll need to troubleshoot since there are a lot of assumptions being made about how things are run in the Tutor environment. To test your environment you can do the following:

- Create or publish a course, this should result in rows being written to the ClickHouse `event_sink` schema. If those rows are not populating, check that `platform-plugin-aspects` is installed in your Studio/LMS (and Celery) images and your configuration is updated as indicated in Step 3. You can also check your Celery logs to see if there are errors present.

- Register for the course you published and interact with content by navigating, watching videos, and attempting problems. This should populate xAPI events in the ClickHouse `xapi` schema tables, starting with `xapi_events_all`. If those are not appearing, you should view your Celery logs, Vector logs, or event bus consumer logs (depending on your chosen configuration), and if those are showing nothing then the LMS logs may have more information. The tracking event configuration is often a difficulty here.

- Try to access Superset and see if you can log in using your LMS credentials and view populated dashboards or go to the embedded dashboards in the Instructor dashboard of the LMS (if enabled) and see if the Superset dashboards appear and are populated. If not, there is likely configuration missing in your LMS settings, difficulties with the single sign-on configuration in the LMS admin Django OAuth Toolkit "Applications" section, or Superset setup. Browser and LMS logs will help here.

Finish
======

Due to the number of possible issues and complexity of debugging, the Aspects team can't fully assist in setting up these configurations. We can try to help you find the right places to look for errors if you find us in the #aspects Open edX Slack channel, however.

Please remember to review your security settings to make sure every service is only available from the expected places, and by the correct people!
