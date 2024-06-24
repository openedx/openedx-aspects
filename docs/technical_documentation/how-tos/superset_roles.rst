.. _superset-roles:

Superset extra roles
*********************

Create extra Superset roles, you can use the patch `superset-extra-roles`. This patch
expects validJSON objects with the following structure:

.. code-block:: yaml

    ## Add a comma before the new role
    superset-extra-roles: |
        ,
        {
            "name": "my_custom_role",
            "permissions": [
                {
                    "name": "can_read",
                    "view_menu": {
                        "name": "Superset",
                        "category": "Security",
                        "category_label": "Security",
                        "category_icon": "fa-bar-chart",
                    },
                }
            ],
        }

Once you have defined your custom roles, you probably want to assign them to users
automatically at login. You can do so by using the patch **superset-sso-assignment-rules**.
This patch expects valid python code and should return a list of roles:

.. code-block:: python

    if "edunext" in username:
        return ["admin"]
    else:
        return []

In the context of the code you can access to the following variables:

- **self**: OpenEdxSsoSecurityManager instance.
- **username**: username of the user.
- **decoded_access_token**: decoded JWT token of the user (can be used to perform API calls).
