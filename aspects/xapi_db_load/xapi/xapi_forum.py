"""
Fake xAPI statements for various forum events.
"""
import json
from uuid import uuid4

from .xapi_common import XAPIBase


class BaseForum(XAPIBase):
    """
    Base xAPI class for forum events.
    """

    def get_data(self):
        """
        Generate and return the event dict, including xAPI statement as "event".
        """
        # We generate registration events for every course and actor as part
        # of startup, but also randomly through the events.

        event_id = str(uuid4())
        course = self.parent_load_generator.get_course()
        enrolled_actor = course.get_enrolled_actor()
        actor_id = enrolled_actor.actor.id
        emission_time = course.get_random_emission_time(enrolled_actor)
        post_id = course.get_random_forum_post_id()

        e = self.get_randomized_event(
            event_id, actor_id, course, post_id, emission_time
        )

        return {
            "event_id": event_id,
            "verb": self.verb,
            "actor_id": actor_id,
            "org": course.org,
            "course_run_id": course.course_url,
            "emission_time": emission_time,
            "event": e,
        }

    def get_randomized_event(self, event_id, account, course, post_id, create_time):
        """
        Given the inputs, return an xAPI statement.

        Currently all forum events are treated the same, so we're just creating
        new posts.
        """
        event = {
            "id": event_id,
            "actor": {
                "objectType": "Agent",
                "account": {"homePage": "http://localhost:18000", "name": account},
            },
            "context": {
                "contextActivities": {
                    "parent": [
                        {
                            "id": course.course_url,
                            "objectType": "Activity",
                            "definition": {
                                "name": {"en-US": "Demonstration Course"},
                                "type": "http://adlnet.gov/expapi/activities/course",
                            },
                        }
                    ]
                },
                "extensions": {
                    "https://w3id.org/xapi/openedx/extension/transformer-version": "event-routing-backends@7.0.1",
                    "https://w3id.org/xapi/openedx/extensions/session-id": "054c9ddcb76d2096f862e66bda3bc308",
                    "https://w3id.org/xapi/acrossx/extensions/type": "discussion"
                }
            },
            "object": {
                "definition": {
                    "type": "http://id.tincanapi.com/activitytype/discussion"
                },
                "id": post_id,
                "objectType": "Activity"
            },
            "timestamp": create_time.isoformat(),
            "verb": {"display": {"en": self.verb_display}, "id": self.verb},
            "version": "1.0.3",
        }

        return json.dumps(event)


class PostCreated(BaseForum):
    verb = "https://w3id.org/xapi/acrossx/verbs/posted"
    verb_display = "posted"
