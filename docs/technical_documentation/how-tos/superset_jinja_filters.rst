.. _superset-jinja-filters:

Superset extra jinja filters
*****************************


To create extra jinja filters, you can use the patch `superset-jinja-filters`
which you can use to define new filters like the **can_view_courses** clause defined in
:ref:`superset-row-level-security`. 

This patch expects valid python code, and the function should return an SQL 
fragment as a string, e.g:

.. code-block:: yaml

    superset-jinja-filters: |
        ALL_COURSES = "1 = 1"
        NO_COURSES = "1 = 0"
        def can_view_courses(username, field_name="course_id"):
            """
            Returns SQL WHERE clause which restricts access to the courses the current user has staff access to.
            """
            from superset.extensions import security_manager
            user = security_manager.get_user_by_username(username)
            if user:
                user_roles = security_manager.get_user_roles(user)
            else:
                user_roles = []

            # Users with no roles don't get to see any courses
            if not user_roles:
                return NO_COURSES

            # Superusers and global staff have access to all courses
            for role in user_roles:
                if str(role) == "Admin" or str(role) == "Alpha":
                    return ALL_COURSES

            # Everyone else only has access if they're staff on a course.
            courses = security_manager.get_courses(username)

            # TODO: what happens when the list of courses grows beyond what the query will handle?
            if courses:
                course_id_list = ", ".join(f"'{course_id}'" for course_id in courses)
                return f"{field_name} in ({course_id_list})"
            else:
                # If you're not course staff on any courses, you don't get to see any.
                return NO_COURSES

Once the custom jinja filter is defined, it is necessary to register it using 
**SUPERSET_EXTRA_JINJA_FILTERS** in the config.yaml file. It's a dictionary
that expects a key for the name of the filter and the name of underlying function:

.. code-block:: yaml

    SUPERSET_EXTRA_JINJA_FILTERS:
        can_view_courses: can_view_courses
