.. _superset-dockerfile-patch:

Modifying the Superset Dockerfile
*********************************

To modify the Superset Dockerfile, use the `superset-dockerfile` patch. This patch takes effect when the `aspects-superset` image is built.

.. code-block:: yaml

    name: custom-inline-plugin
    version: 0.1.0
    patches:
      superset-dockerfile: |
        # Add custom Dockerfile instructions here
        RUN pip install additional-package
        # Example: Overriding default CMD or ENTRYPOINT
        # CMD ["superset", "run", "-p", "8088", "--with-threads"]

This patch appends your instructions to the final layer of the Dockerfile—making it ideal for installing dependencies or overriding the `CMD` or `ENTRYPOINT`.
