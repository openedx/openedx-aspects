.. _superset-extra-assets:

Superset extra assets
*********************

Developers user the `superset-extra-assets` patch to add extra assets to Superset and those
will be imported at initialization.

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


The patch is expected to be a list of assets with an extra attribute called **_file_name**,
which uniquely identifies the asset entry. Each asset is expected to be a valid yaml object
with the attributes that Superset expects for each asset type. See 
`assets <https://github.com/openedx/tutor-contrib-aspects/tree/main/tutoraspects/templates/aspects/build/aspects-superset/openedx-assets/assets>`_ 
for examples of asset yaml declarations.

In most cases, however, you will want to develop Superset dashboards, charts, datasets, and 
sometimes even databases in the Superset UI and import them into a plugin that can be managed
in source control. As of Aspects 1.0.3 use the same command to import assets into a Tutor 
plugin that we use to maintain Aspects itself.

You can use the `Tutor Plugin Cookiecutter <https://github.com/overhangio/cookiecutter-tutor-plugin/>`_ 
to create a skeleton plugin. Then you can create a patch file that will include all of your 
Superset assets into Aspects when the plugin is enabled. 

The file name is the patch name ``<your_extension>/patches/superset-extra-assets``:

.. code-block:: 

    {% for file in "<your_extension>/superset-assets/"|walk_templates %}
    ---
    _file_name: {{ file.split('/')[-1] }}
    {% include file %}
    {% endfor %}


This recursively includes each file in the superset-assets directory of your extension's 
tempates directory, when ``tutor config save is run``. For example 
``<your_extension>/templates/superset-assets/*``.

Now you can export your Superset dashboard, which it will download to your local computer
as a .zip file. As long as you are running Aspects 1.0.3 or newer you can use the following
command to unzip the file to your plugin directory:


.. code-block:: 

    tutor aspects import_superset_zip <path to>/<your dashboard>.zip --base_assets_path <path to>/<your extension>/templates/<your extension>/superset-assets/


This command does several things to make import safer and easier, including checking for some 
required security fields, safely naming files so that charts with duplicate names don't 
overwrite each other, and checking that certain fields use Tutor settings instead of hard
coded values. It also adds a special ``_file_name`` key that tells Aspects what name to use
for the file when importing back to Superset.

.. warning:: 

    When importing a dashboard you will need to manually add a ``_roles`` key, which 
    sets the permissions for who can view the dashboard. In addition to the default roles
    (student, instructor, operator, admin) you can also add custom roles <superset_roles>.


An example roles key looks like this:

.. code-block:: 
    
    _roles:
        - '{{ SUPERSET_ROLES_MAPPING.instructor }}'


.. warning:: 

    When a Superset zip is exported it will contain any datasets and databases needed for 
    all of the charts in that dashboard. This may include the default xapi and MySQL 
    databases or Aspects datasets that you probably do not want to overwrite, and can
    include their passwords!

    Use caution when importing datasets or databases your project and make sure that they
    are only ones you have created yourself unless you truly intend to overwrite defaults.


A simple example showing the final directory structure is available 
`here <https://github.com/bmtcril/tutor-contrib-aspects-extension>`_. 

Once you have your files imported to the plugin, make sure it is installed and enabled
in your Tutor environment, then you should just be able to do ``tutor config save`` and
``tutor <local|dev|k8s> import-assets`` to update your Superset assets.

