"""
Fake xAPI statements for various registration events.
"""
import json
from random import choice
from uuid import uuid4

from .xapi_common import XAPIBase


class BaseRegistration(XAPIBase):
    """
    Base xAPI class for registration events.
    """

    def get_data(self, course=None, enrolled_actor=None):
        """
        Generate and return the event dict, including xAPI statement as "event".
        """
        # We generate registration events for every course and actor as part
        # of startup, but also randomly through the events, so sometimes we will
        # have a course and actor, other times not.
        if not course:
            course = self.parent_load_generator.get_course()

        if not enrolled_actor:
            enrolled_actor = course.get_enrolled_actor()

        actor_id = enrolled_actor.actor.id
        event_id = str(uuid4())
        emission_time = course.get_random_emission_time(enrolled_actor)

        e = self.get_randomized_event(
            event_id, actor_id, course.course_url, emission_time
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

    def get_randomized_event(self, event_id, account, course_locator, create_time):
        """
        Given the inputs, return an xAPI statement.
        """
        enrollment_mode = choice(("audit", "honor", "verified"))
        event = {
            "id": event_id,
            "actor": {
                "objectType": "Agent",
                "account": {"homePage": "http://localhost:18000", "name": account},
            },
            "context": {
                "extensions": {
                    "https://w3id.org/xapi/openedx/extension/transformer-version": "event-routing-backends@7.0.1",
                    "https://w3id.org/xapi/openedx/extensions/session-id": "e4858858443cd99828206e294587dac5"
                }
            },
            "object": {
                "definition": {
                    "extensions": {
                        "https://w3id.org/xapi/acrossx/extensions/type": enrollment_mode
                    },
                    "name": {"en": "Demonstration Course"},
                    "type": "http://adlnet.gov/expapi/activities/course",
                },
                "id": course_locator,
                "objectType": "Activity",
            },
            "timestamp": create_time.isoformat(),
            "verb": {"display": {"en": self.verb_display}, "id": self.verb},
            "version": "1.0.3",
        }

        return json.dumps(event)


class Registered(BaseRegistration):
    verb = "http://adlnet.gov/expapi/verbs/registered"
    verb_display = "registered"


class Unregistered(BaseRegistration):
    verb = "http://id.tincanapi.com/verb/unregistered"
    verb_display = "unregistered"
