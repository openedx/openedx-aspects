.. _authentication-permissions:

Authentication and Permissions
######################################

Users access Aspects data and reports by signing into Superset, which will confirm their identity
and permissions with the LMS. This is done using Single Sign On (SSO) and JSON Web Tokens (JWT).

By default Superset provides the following roles:

- Alpha
- Gamma
- granter
- Public
- sql_lab

You can find more information about these roles in the 
`Superset documentation <https://superset.apache.org/docs/security/#roles>`_.

We do not use any of the provided roles, instead we have created custom roles for our specific
uses cases:

- **Admin**: Full access to all Superset data, dashboards, and reports.
- **Operator**: Access to the operator dashboard and data about the state of the installation.
- **Instructor**: Access to the instructor dashboard and course specific data.

Roles can be extended and assigned using a combination of extensions described in
:ref:`extensions` docs.

Superset Authentication
-----------------------

Superset authentication is performed against the LMS using SSO. In this process, the LMS provides
a JWT token that's later used to perform API calls to find out the user's roles and permissions.

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

