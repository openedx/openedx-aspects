Permissions
###########

The permissions work by consulting the LMS APIs, the permission used is “course_staff.” Once granted, users are able to enter the LMS and assume the role of instructor, with which they can visit the assigned dashboard to its language code.

Please refer to the `Superset official documentation <https://superset.apache.org/docs/security/>`_ for more information. 

Manage Roles
************
New roles and assignment rules can be created for them, and their permissions must also be configured. Those can be added programmatically, allowing you better control over their deployment and synchronization, or manually. This is not recommended, as the state of the installation can not be readily determined from the source code and can cause weird behavior.

To learn more about this topic, review the `technical documentation <superset_roles>`_.
