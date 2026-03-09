.. _superset-extra-assets:

Superset extra assets
*********************

Developers can use the ``superset-extra-assets`` patch to add extra assets (charts, datasets, dashboards, databases) to Superset that will be imported at initialization.

The patch is expected to be a list of assets (with an extra attribute called ``_file_name`` to uniquely identify each asset). Each asset should be a valid yaml object with the attributes that Superset expects for each asset type. See 
`aspects assets <https://github.com/openedx/tutor-contrib-aspects/tree/main/tutoraspects/templates/aspects/build/aspects-superset/openedx-assets/assets>`_ for examples of asset yaml declarations.

Assets in a tutor inline plugin using the patch would look like:

.. code-block:: yaml

    name: custom-inline-plugin
    version: 0.1.0
    patches:
    superset-extra-assets: |
        - _file_name: my-dashboard.yaml
        dashboard_title: "..."
        ...
        - _file_name: my-chart.yaml
        slice_name: "..."
        ...
        - _file_name: my-database.yaml
        database_name: "..."
        ...
        - _file_name: my-dataset.yaml
        table_name: "..."
        ...      

|
In most cases, however, you will want to develop Superset dashboards, charts, datasets, and sometimes even databases in the Superset UI, and import them into a plugin that can be managed in source control. 

Creating a Tutor plugin
=======================

#. Use the `Tutor Plugin Cookiecutter <https://github.com/overhangio/cookiecutter-tutor-plugin/>`_ to create a skeleton plugin. We have created `tutor-contrib-aspects-sample <https://github.com/openedx/tutor-contrib-aspects-sample>`_ as an example.

#. Create a `patch file <https://github.com/openedx/tutor-contrib-aspects-sample/blob/main/tutoraspects_sample/patches/superset-extra-assets>`_ that will recursively include all of your Superset assets from ``templates/build/assets`` into Aspects when the plugin is enabled and ``tutor config save`` is run. 

   .. code-block:: 

        {% for file in "aspects-sample/build/assets"|walk_templates %}
        ---
        _file_name: {{ file.split('/')[-1] }}
        {% include file %}
        {% endfor %}

   .. attention::
        
        The directory containing ``assets`` must be included in `ENV_TEMPLATE_TARGETS <https://github.com/openedx/tutor-contrib-aspects-sample/blob/main/tutoraspects_sample/plugin.py>`_. Since this defaults to ``build`` and ``apps``, you can either add your asset files to one of these directories, or add an additional target to the plugin file. 

#. Create a `requirements.txt <https://github.com/openedx/tutor-contrib-aspects-sample/blob/main/requirements.txt>`_ with ``ruff`` for formatting.

Import assets into plugin
=========================

#. From the Superset UI, you can export your dashboard, which will download to your local computer as a ``.zip`` file.

#. As long as you are running Aspects 1.0.3 or newer, you can use this command to unzip the file to your plugin directory.

   .. code-block:: bash

    tutor aspects import_superset_zip <path to your dashboard>.zip --base_assets_path <path to your extension>/templates/build/assets/

   This command does several things to make import safer and easier including:

   * Check for some required security fields
   * Safely name files so that charts with duplicate names don't overwrite each other
   * Check that certain fields use Tutor settings instead of hard coded values
   * Add a special ``_file_name`` key that tells Aspects what name to use for the file when importing back to Superset

#. Before importing a dashboard back into Superset, you will need to manually add a `_roles <https://github.com/openedx/tutor-contrib-aspects-sample/blob/f52a649bb01640ce4fb6a4c38f9ea337c18afc8e/tutoraspects_sample/templates/aspects-sample/build/assets/dashboards/Sample_Aspects_Plugin.yaml#L2-L3>`_ key, which sets the permissions for who can view the dashboard. 

   .. code-block:: yaml

        _roles:
        - '{{ SUPERSET_ROLES_MAPPING.instructor }}'

   In addition to the default roles (student, instructor, operator, admin) you can also add custom roles in a ``superset_roles`` patch.

.. warning:: 

    When a Superset zip is exported it will contain any datasets and databases needed for all of the charts in that dashboard. This may include the default xapi and MySQL databases or Aspects datasets that you probably do not want to overwrite, and can include their passwords!

    Use caution when importing datasets or databases into your plugin - only ones you have created yourself should exist in your plugin. 
    
    If you truly mean to overwrite the default databases or datasets, make sure to remove any sensitive information such as passwords from the yaml files before importing.

    If you accidentally overwrite a default database, you can reset it by:

    #. Disabling your plugin (``tutor plugins disable <your plugin>``)
    #. Running ``tutor config save`` and ``tutor <local|dev|k8s> do import-assets`` to reset the assets
    #. Re-enabling your plugin

Update Superset assets
======================

Once you have your files imported to the plugin, make sure it is `installed and enabled <https://github.com/openedx/tutor-contrib-aspects?tab=readme-ov-file#installation>`_ in your Tutor environment, then use ``import-assets`` to update your Superset assets.

.. code-block:: bash

    pip install <your package>
    tutor plugins enable <your plugin>
    tutor config save
    tutor <local|dev|k8s> import-assets
