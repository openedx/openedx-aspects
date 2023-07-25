.. _superset-extra-assets:

Superset extra assets
#####################

Developers the patch `superset-extra-assets` to add extra assets to Superset and those
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
`assets.yaml <https://github.com/openedx/tutor-contrib-aspects/blob/main/tutoraspects/templates/aspects/apps/superset/pythonpath/assets.yaml>`_ 
for examples of asset yaml declarations.

Additionally to the default fields for each asset type, the following fields are supported:

- Dashboard: **_roles** a list of roles names to be associated with a dashboard.

Override Superset Default Assets
================================

Aspects allows to override the default Superset assets by creating an Superset extra asset
as explained above using the same UUID as the default asset. The UUID of the default assets
can be found in the `assets.yaml`
