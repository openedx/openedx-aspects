.. _superset-config-docker:

Superset Custom Production Config Settings
******************************************

To add or override production config settings in Superset, you can use the patch 
`superset-config-docker`. For example, to disable any custom color schemes:

.. code-block::

    FEATURE_FLAGS = {
        "EXTRA_CATEGORICAL_COLOR_SCHEMES": False
    }

Or to add a new custom color scheme:

.. code-block::
    
    EXTRA_CATEGORICAL_COLOR_SCHEMES.append(
        {
            "id": 'your_new_palette',
            "description": 'Custom color scheme for Company',
            "label": 'Custom Colors',
            "colors": ['#11406A', '#F4661F']
        },
    )

These changes will take effect on restart. To override *local* config settings, use `superset-config` patch instead.