11. Course and block data
#########################

Status
******

Accepted

Context
*******

Aspects needs a way to access up-to-date course and block metadata in order to display human-friendly labels and data to
instructors in a way that makes sense in the context of their course. 

The tracking event data that Aspects processes contains "object IDs", or string representations of UsageKeys that
identify the piece of content the event relates to. But these UsageKeys are not very legible to humans, and the metadata
for that content (display title of the block, title of the course it appears in, its position in the course, etc.) is
part of the context where these events occur, and is not stored in the events themselves.

Example:

*"As a course author, I need to know how many times the videos in my course have been viewed so I can see which videos are
the most helpful (or the most confusing)."*

Aspects receives tracking events every time someone watches a video, and so the videos watched can be counted purely
from these tracking events. However, videos which haven't been watched won't appear in the tracking events. To include
these unwatched videos in our chart, Aspects needs a way to query a course for all the video blocks it contains.

Open edX sends signals (which, confusingly, are also called "events", see OEP-41) when some actions are taken on the
platform, including publishing a course, or updating a course outline. These signals can be used to tell Aspects when
its course or block data needs to be updated.

Decision
********

Use Open edX's "course published" signal to trigger updating course outline and block relationship data stored in
Clickhouse. This approach is supported by `OEP-50 Hooks extension framework`_, and will be compatible with deployments
that use the Event Bus to manage signals sent between applications.

Consequences
************

#. Create an "event sink" which uses course and/or block signals from within the LMS/CMS to trigger course and block
   data synchronization to Clickhouse.
#. This "event sink" will run as a plugin on Open edX, and so has access to its models and data, which it can query and
   package up for insertion in Clickhouse.
#. Aspects will create custom views into this course and block data to ensure that the most relevant information is
   easily available to the datasets.

Rejected Alternatives
*********************

**Use course graph**

Previously Aspects used the `coursegraph`_ application in Open edX as the source of truth for course outline and block
relationships.

The synchronization script had to be run regularly in order to keep the data up-to-date.

However as the Aspects project has grown, course data isn't the only Open edX data that Aspects needs a copy of. So the
more general solution of "event sinks" was preferred.

References
**********

.. OEP-41 Asynchronous Server Event Message Format: https://open-edx-proposals.readthedocs.io/en/latest/architectural-decisions/oep-0041-arch-async-server-event-messaging.html
.. OEP-50 Hooks extension framework: https://open-edx-proposals.readthedocs.io/en/latest/architectural-decisions/oep-0050-hooks-extension-framework.html
.. OEP-52 Event Bus Architecture: https://open-edx-proposals.readthedocs.io/en/latest/architectural-decisions/oep-0052-arch-event-bus-architecture.html
