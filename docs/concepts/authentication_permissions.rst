.. _authentication-permissions:

Authentication and Permissions
######################################

Users access Aspects data and reports by signing into Superset, which will confirm their identity and permissions with the LMS.
with the following roles:

- Alpha
- Gamma
- granter
- Public
- sql_lab

Superset Authentication
-----------------------

Superset authentication is performed against the LMS using SSO. In this process the LMS provides
an JWT token that's later used to perform API calls to find out the user's roles and permissions.

Additional Aspects Roles
-----------------------

We use the following roles:

- Admin: Full access to all aspects
- Operator: Access to the instructor dashboard and data about the state of the installation.
- Instructor: Access to the instructor dashboard and course specific data.

Roles can be extended and assigned using a combination of extensions described in
:ref:`extensions` docs.

Superset Permissions
-----------------------

Permissions are assigned to roles and are used to control access to specific resources
such as dashboards, tables, menus, etc.

Additionally, dashboards are assigned to specific roles. This means that a dashboard
can only be accessed by users with the role assigned to it.


Superset Row Level Security Filters
-----------------------------------

Row level security filters (RLSF) are used to control access to specific data. For example,
an instructor should only be able to see data for the courses they are teaching.

The following RLSF are implemented by default:

- **can_view_courses**: Return courses a user has access to.

RLSF can be extended and assigned using a combination of extensions described in
:ref:`extensions` docs.

