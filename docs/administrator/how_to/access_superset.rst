How to Access Aspects Superset
##############################

Apache Superset is an open-source platform that is the primary data visualization and exploration tool for Aspects. You can access the different dashboards from this platform, edit them, or create new ones. You can also modify the charts and `data sets <https://docs.openedx.org/projects/openedx-aspects/en/latest/administrator/how_to/database_connections.html>`_, control the SQL connection, and `add or edit users <https://docs.openedx.org/projects/openedx-aspects/en/latest/administrator/how_to/create_new_role.html>`_ accessing the analytics system.

.. image:: /_static/superset_access_overview.png

There are two ways to access Superset. The first one is the Superset Aspects URL of your platform. The second one is through the link in the Instructor dashboard of the LMS. Let’s learn more about these two forms.

Superset Aspects URL:
*********************
As an `administrator or site operator <https://docs.openedx.org/projects/openedx-aspects/en/latest/administrator/concepts/role_description.html>`_, you can access Superset using the URL given/created during installation.

The process is quite simple.

1. In the browser of your choice, type the URL of your Aspects platform and press **Enter**. The URL usually follows a format like “superset.axim.atlas.edunext.link.”

2. Click the **Sign In with OPENEDXSSO** button. The system will use your Open edX platform credentials to access Aspects’ Superset platform. Make sure you are signed in to your Open edX platform with credentials that have permission to access Superset.

.. image:: /_static/superset_access_1.png

Aspects’ Superset LMS Link:
***************************
The other method to access Superset is through the link in the LMS. This is useful for users with different roles, like the `Course Delivery Team <https://docs.openedx.org/projects/openedx-aspects/en/latest/course_team/index.html>`_. Follow these steps to access the platform.

.. note:: The site operator of the Aspects platform must enable this link to appear on the LMS Open edX instance. 

1. From a course page in the LMS, go to the **Instructor dashboard**.

2. In the Instructor dashboard, select the **Reports tab**.

.. image:: /_static/superset_access_3.png

3. Click on **View dashboard in Superset**.

.. image:: /_static/superset_access_4.png

4. If it is your first time accessing Superset with that account's credentials, an authorization for the Superset-SSO box will appear. Click on **Allow**.

.. image:: /_static/superset_access_5.png

5. Click the **Sign in with OpenedXSSO button** to finally access Superset.

.. image:: /_static/superset_access_1.png
