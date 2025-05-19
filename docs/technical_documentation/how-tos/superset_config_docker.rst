.. _superset-config-docker:

Superset Custom Production Config Settings
******************************************

To add or override production config settings in Superset, use the patch 
``superset-config-docker``. Changes take effect on LMS/CMS restart. 

To override *local* config settings, use ``superset-config`` patch instead.

Custom Color Schemes
--------------------

**Disable/Enable all custom schemes**

.. code-block::

    FEATURE_FLAGS = {
        "EXTRA_CATEGORICAL_COLOR_SCHEMES": True
    }


**Add a new custom color scheme**

1. Add color scheme to patch

.. code-block::
    
    EXTRA_CATEGORICAL_COLOR_SCHEMES.append(
        {
            "id": 'your_new_palette',
            "description": 'Custom color scheme for Company',
            "label": 'Custom Colors',
            "colors": ['#11406A', '#F4661F']
        },
    )

2. Restart and change color scheme in Dashboard settings

.. image:: /_static/superset_colors.png
