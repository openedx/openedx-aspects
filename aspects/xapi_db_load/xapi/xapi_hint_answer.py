"""
Fake xAPI statements for various hint and answer events.
"""
import json
from uuid import uuid4

from .xapi_common import XAPIBase


class HintAnswerBase(XAPIBase):
    """
    Base xAPI class for hint and answer events.
    """

    verb_display = "asked"
    verb = "http://adlnet.gov/expapi/verbs/asked"

    # Whether this is a hint or an answer, "hint" or "answer" are valid values
    type = None

    def get_data(self):
        """
        Generate and return the event dict, including xAPI statement as "event".
        """
        event_id = str(uuid4())
        course = self.parent_load_generator.get_course()
        enrolled_actor = course.get_enrolled_actor()
        actor_id = enrolled_actor.actor.id
        emission_time = course.get_random_emission_time(enrolled_actor)
        problem_id = course.get_problem_id()

        e = self.get_randomized_event(
            event_id, actor_id, course, problem_id, emission_time
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

    def get_randomized_event(self, event_id, account, course, problem_id, create_time):
        """
        Given the inputs, return an xAPI statement.
        """
        hint_object = {
            "object": {
                "definition": {
                    "type": "https://w3id.org/xapi/acrossx/extensions/supplemental-info"
                },
                "id": f"{problem_id}/hint/1",
                "objectType": "Activity",
            }
        }

        answer_object = {
            "object": {
                "definition": {"type": "http://id.tincanapi.com/activitytype/solution"},
                "id": f"{problem_id}/answer",
                "objectType": "Activity",
            },
        }

        event = {
            "id": event_id,
            "actor": {
                "account": {"homePage": "http://localhost:18000", "name": account},
                "objectType": "Agent",
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
                    "https://w3id.org/xapi/openedx/extensions/session-id": "e4858858443cd99828206e294587dac5"
                }
            },
            "timestamp": create_time.isoformat(),
            "verb": {"display": {"en": self.verb_display}, "id": self.verb},
            "version": "1.0.3",
        }

        if self.type == "hint":
            event.update(hint_object)
        else:
            event.update(answer_object)

        return json.dumps(event)


class ShowHint(HintAnswerBase):
    type = "hint"


class ShowAnswer(HintAnswerBase):
    type = "answer"
