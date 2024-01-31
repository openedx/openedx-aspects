.. _changing_actor_identifier:

Changing the xAPI actor identifier
##################################

The xAPI :ref:`actor <actor_concept>` identifier is a unique user identifier provided
in the xAPI statement generation process by the LMS. The default actor identifier
is the anonymous user ID, which is different for each user in each course. 
If you want to change this behavior, you can update the value of the `XAPI_AGENT_IFI_TYPE`
setting in the LMS to modify the identifier. The supported values are:

- `mbox`: The email is used as the identifier.
- `mbox_sha1sum`: The sha1sum of the email is used as the identifier.
- `external_id` (default): The anonymous user ID is used as the identifier.

If the `XAPI_AGENT_IFI_TYPE` is set to a value other than the ones mentioned above,
the anonymous user ID will be used.

Note that changing the xAPI actor identifier will not delete previous statements
in the data-lake, but it will cause new data to be associated with a different user ID.
To avoid confusion, we recommend deleting all previous data when changing the actor ID
(before replaying old events).

To reproduce the statements with the new identifier, you can use the `transform_tracking_logs`
command introduced in the linked `pull request <https://github.com/openedx/event-routing-backends/pull/301>`_.

Before starting to emit xAPI statements to the LRS, we strongly advise verifying which
identifier option is most suitable for your use case.

