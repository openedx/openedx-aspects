.. _superset-extra-assets:

Superset extra assets
*********************

Developers can use the `superset-extra-assets` patch to add extra assets to Superset and those will be imported at initialization.

An example a tutor inline plugin using the patch is the following:

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


The patch is expected to be a list of assets with an extra attribute called ``_file_name``, which uniquely identifies the asset entry. Each asset is expected to be a valid yaml object with the attributes that Superset expects for each asset type. See 
`assets <https://github.com/openedx/tutor-contrib-aspects/tree/main/tutoraspects/templates/aspects/build/aspects-superset/openedx-assets/assets>`_ for examples of asset yaml declarations.

In most cases, however, you will want to develop Superset dashboards, charts, datasets, and sometimes even databases in the Superset UI and import them into a plugin that can be managed in source control. As of Aspects 1.0.3, use the same command to import assets into a Tutor plugin that we use to maintain Aspects itself.

Creating a Tutor plugin
=======================

#. Use the `Tutor Plugin Cookiecutter <https://github.com/overhangio/cookiecutter-tutor-plugin/>`_ to create a skeleton plugin. See `tutor-contrib-aspects-sample <https://github.com/openedx/tutor-contrib-aspects-sample>`_ for an example.

#. Create a `patch file <https://github.com/openedx/tutor-contrib-aspects-sample/blob/main/tutoraspects_sample/patches/superset-extra-assets>`_ that will recursively include all of your Superset assets from ``<your_extension>/templates/build/assets`` into Aspects when the plugin is enabled and ``tutor config save`` is run. 

   * The directory containing ``assets`` must be included in `ENV_TEMPLATE_TARGETS <https://github.com/openedx/tutor-contrib-aspects-sample/blob/main/tutoraspects_sample/plugin.py#L136>`_. Since this defaults to ``build`` and ``apps``, you can either add your asset files to one of these directories, or add an additional target to the plugin file. 

#. Create a `requirements.txt <https://github.com/openedx/tutor-contrib-aspects-sample/blob/main/requirements.txt>`_ with ``ruff`` for formatting.

Import assets into plugin
=========================

#. From the Superset UI, you can export your dashboard, which will download to your local computer as a .zip file. 
   
#. As long as you are running Aspects 1.0.3 or newer you can use this command to unzip the file to your plugin directory.

   ``tutor aspects import_superset_zip <path to your dashboard>.zip --base_assets_path <path to your extension>/templates/build/assets/``

   * This command does several things to make import safer and easier, including checking for some required security fields, safely naming files so that charts with duplicate names don't overwrite each other, and checking that certain fields use Tutor settings instead of hard coded values. It also adds a special ``_file_name`` key that tells Aspects what name to use for the file when importing back to Superset.

#. Before importing a dashboard back into Superset, you will need to manually add a `_roles <https://github.com/openedx/tutor-contrib-aspects-sample/blob/main/tutoraspects_sample/templates/aspects-sample/build/assets/dashboards/Sample_Aspects_Plugin.yaml#L2-L3>`_ key, which sets the permissions for who can view the dashboard. 

   * In addition to the default roles (student, instructor, operator, admin) you can also add custom roles in a ``superset_roles`` patch.

.. warning:: 

    When a Superset zip is exported it will contain any datasets and databases needed for all of the charts in that dashboard. This may include the default xapi and MySQL databases or Aspects datasets that you probably do not want to overwrite, and can include their passwords!

    Use caution when importing datasets or databases in your project and make sure that they are only ones you have created yourself unless you truly intend to overwrite defaults.

Update Superset assets
======================

Once you have your files imported to the plugin, make sure it is installed and enabled in your Tutor environment, then run ``tutor config save`` and ``tutor <local|dev|k8s> import-assets`` to update your Superset assets.

