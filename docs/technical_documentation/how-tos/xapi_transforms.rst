.. _xapi_transforms:

xAPI Transforms
###############

Aspects converts raw Open edX tracking event JSON into :ref:`xapi-concepts` for storage and analysis. This conversion process is called "transformation".

This document covers two ways to customize Aspect's xAPI transforms:

#. :ref:`transform_new_event`
#. :ref:`mod_existing_transform`

.. _transform_new_event:

Transforming a new event
************************

Events emitted by ``openedx`` packages are transformed by `event-routing-backends`_ (ERB), a Django plugin which Aspects installs on Open edX.

Transformers for events emitted by non-openedx packages should be stored close to the code that produces the events, and registered using decorators provided by `event-routing-backends`_. We
will use OpenCraft's `completion aggregator`_ as the example for this tutorial, building on events emitted by `pr#173`_.

xAPI Schema
===========

To decide on an event's xAPI schema, consider any similar events already being transformed, and what event data will be useful for analysis or visualization in Aspects.

The schema for a new event must uniquely describe that event. However, it's also important to be as consistent as possible with existing event schemas so that the event can be processed and
used in Aspects in a similar way to other events.

As a reminder, an xAPI statement can be expressed as:

  **Actor** **Verbed** an **Object** (within **Context**).

Actor
~~~~~

For most events, the default Actor transform is enough:

.. code-block:: json

   {
      "objectType": "Agent",
      "account": {
        "homePage": "https://lms.url",
        "name": "32e08e30-f8ae-4ce2-94a8-c2bfe38a70cb"
      }
   }


Here, the actor's `external ID`_ (of type=xapi) is used as the ``name`` field. This external ID can be matched against PII data to access the actor's name, email, and other profile details.

Verb
~~~~

The verb is the primary differentiator between different xAPI events in Open edX. Select a verb that describes the event as concisely and accurately as possible, so that future, similar
events can still be discerned.

Where possible:

* use verbs from one of the registered `xAPI profiles`_.
* avoid re-using verbs that are already in use in Aspects (see `ERB's verb list`_).

For example, the completion aggregator will emit events when progress has been made on a
unit/section/subsection/course, so we could use the verb `progressed`_.

.. code-block:: json

  {
    "id": "http://adlnet.gov/expapi/verbs/progressed",
    "display": {
      "en": "progressed"
    }
  }

Object
~~~~~~

Most events in Open edX are Activities, which look like this:

.. code-block:: json

  {
    "id": "https://lms.url/block/block-v1:edX+DemoX+Demo_Course+type@video+block@0b9e39477cf34507a7a48f74be381fdd",
    "description": {
      "type": "block",
      "name": {
        "en": "Welcome!"
      },
    }
  }

* ``id`` should uniquely identify the activity
* ``type`` should describe the type of activity, e.g. "unit" or "course"
* ``name`` should provide human-friendly display name(s) for the activity
* ``extensions`` can be added to provide any extra data important to the activity

Context
~~~~~~~

Most events in Open edX happen on an element within a course, like a block or a discussion forum, and so the "context activity" for the event is the course.

Aspects also uses "extensions" to record extra information, like the transformer code version and the actor's session ID (if found in the event). These "extensions" can be used to
communicate any high-level information that is important for the event record.

For example:

.. code-block:: json

  {
    "contextActivities": {
      "parent": [
        {
          "id": "https://lms.url/course/course-v1:edX+DemoX+Demo_Course",
          "object_type": "Activity",
          "definition": {
            "type": "course",
            "name": {
              "en-US": "Demonstration Course"
            }
          }
        }
      ]
    },
    "extensions": {
      "https://w3id.org/xapi/openedx/extension/transformer-version": "7.2.0",
      "https://w3id.org/xapi/openedx/extensions/session-id": "993110e9c27848a545da74a74114158d"
     }
  }


Result
~~~~~~

Some Open edX events use a "result" stanza that communicates information about the effect that this event had. For example, "problem check" events record whether the problem was answered
correctly, and what score the actor received.

For these completion "progressed" events, we would want to store:

.. code-block:: json

  {
    "completion": false,
    "score": {
      "scaled": ".45"
    }
  }


Implementation
==============

Once the xAPI event schema is settled, the implementation should be pretty straightforward using
`event-routing-backends`_ and `TinCan`_.

#. Create a new transformer class that extends `XApiTransformer`_.
#. Implement the ``get_verb`` method, returning your chosen verb URI and its short name.
#. Implement any other custom components by overriding their ``get`` method.

   For example, to customize the context activities for your event, override ``get_context_activities``.

   Use the built-in transformer method ``get_data`` to parse and return data from the original tracking event.
#. Register your transformer class using the registry decorator.

   Use the raw tracking event's ``type`` as the parameter to ensure this class is used to transform those type of events.


.. warning::
   There can only be one registered xAPI transformer class per tracking event ``type``.
   While it is technically possible to overwrite a registered transformer class with another, this is not recommended
   and may have unintended side effects.

Example code
~~~~~~~~~~~~

Here is the full code for the new transformer described in this tutorial.

.. code-block:: python

  from tincan import LanguageMap, Result, Verb
  from event_routing_backends.processors.xapi.registry import XApiTransformersRegistry
  from event_routing_backends.processors.xapi.transformer import XApiTransformer

  class ProgressTransformerBase(XApiTransformer):
      """
      Transformer for completion-aggregated "progress" events.

      Uses the default implementations for `get_actor` and `get_context`.

      Expects at these fields to be present in the original tracking event:

      {
        "data": {
          "block_id": "block-v1:...",  # block usage key
          "percent":  "0.123", # percent completed, > 0, < 1.0
        }
      }
      """
      object_type = None
      additional_fields = ('result', )

      def get_verb(self) -> Verb:
          return Verb(
              id="http://adlnet.gov/expapi/verbs/progressed",
              display=LanguageMap({"en": "progressed"}),
          )

      def get_object(self) -> Activity:
          return Activity(
              id=self.get_object_iri("xblock", self.get_data("data.block_id")),
              definition=ActivityDefinition(
                type=self.object_type,
              )
          )

      def get_result(self) -> Result:
          return Result(
              completion=self.get_data("data.percent") == 1.0,
              score={
                "scaled": self.get_data("data.percent") or 0,
              },
          )

  # Register subclasses for each individual event type

  @XApiTransformersRegistry.register("edx.completion_aggregator.progress.chapter")
  @XApiTransformersRegistry.register("edx.completion_aggregator.progress.sequential")
  @XApiTransformersRegistry.register("edx.completion_aggregator.progress.vertical")
  class ModuleProgressTransformer
      object_type = "http://adlnet.gov/expapi/activities/module"

  @XApiTransformersRegistry.register("edx.completion_aggregator.progress.course")
  class CourseProgressTransformer
      object_type = "http://adlnet.gov/expapi/activities/course"


.. _mod_existing_transform:

Modifying an existing transform
*******************************

ERB supports modifying some of its transforms using `openedx-filters`_. See `ERB's xAPI filters`_ for a list of available filters.

.. warning:: Use xAPI filters with care.

  Aspects visualizations depend heavily on ERB's transforms, so removing or modifying data may cause unexpected issues.

  Adding new fields is low risk.


Example code
============

The example below shows how to add extra data to an event's Activity object.

See these `xapi filters`_ for more examples.

.. code-block:: python

  from openedx_filters import PipelineStep

  class XApiContextExtensionsFilter(PipelineStep):
      """This filter adds tags to the object.definition.extensions list for "course graded" events.

      How to set:
          OPEN_EDX_FILTERS_CONFIG = {
              "event_routing_backends.processors.xapi.grading_events.course_graded.get_object": {
                  "pipeline": ["this_module.this_file.XApiContextExtensionsFilter"],
                  "fail_silently": False,
              },
          }
      """

      def run_filter(self, transformer, result):
          """Appends the list of block tags to the object's extensions list.

          Arguments:
              transformer <XApiTransformer>: Transformer instance.
              result <Activity>: Target activity for the event.

          Returns:
              Activity: Modified activity object.
          """
          block_id = result.id
          tags = get_tags(block_id)

          if not result.definition.extensions:
            result.definition.extensions = {}

          result.definition.extensions["http://id.tincanapi.com/extension/tags"] = [
              f"{tag.name}={tag.value}",
              for tag in tags
          ]
          return resultevent_routing_backends.processors.xapi.grading_events.course_graded.get_object


References
**********

* `event-routing-backends`_: Django plugin that receives tracking events and transforms them into xAPI
* `completion aggregator`_: OpenCraft's plugin which accumulates block completion up to the enclosing unit/section/subsection/course.
* `xAPI profiles`_: registry of xAPI schemas
* `openedx-filters`_: Open edX filters library

.. _completion aggregator: https://github.com/open-craft/openedx-completion-aggregator
.. _xapi filters: https://github.com/eduNEXT/eox-nelp/blob/master/eox_nelp/openedx_filters/xapi/filters.py
.. _event-routing-backends: https://github.com/openedx/event-routing-backends
.. _ERB's verb list: https://github.com/openedx/event-routing-backends/blob/master/event_routing_backends/processors/xapi/constants.py
.. _ERB's xAPI filters: https://event-routing-backends.readthedocs.io/en/latest/getting_started.html#openedx-filters
.. _external ID: https://github.com/openedx/edx-platform/blob/master/openedx/core/djangoapps/external_user_ids/docs/decisions/0001-externalid.rst
.. _openedx-filters: https://github.com/openedx/openedx-filters
.. _pr#173: https://github.com/open-craft/openedx-completion-aggregator/pull/173
.. _progressed: http://adlnet.gov/expapi/verbs/progressed
.. _TinCan: https://github.com/RusticiSoftware/TinCanPython
.. _xAPI profiles: https://profiles.adlnet.gov/
.. _XApiTransformer: https://github.com/nelc/event-routing-backends/blob/master/event_routing_backends/processors/xapi/transformer.py#L27
