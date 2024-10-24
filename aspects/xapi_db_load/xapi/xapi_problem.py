"""
Fake xAPI statements for various problem_check events.
"""
import json
import random
from uuid import uuid4

from .xapi_common import XAPIBase


# TODO: There are various other problem samples we should probably include eventually:
# https://github.com/openedx/event-routing-backends/tree/master/event_routing_backends/processors/xapi/tests/fixtures/expected
class BaseProblemCheck(XAPIBase):
    """
    Base xAPI class for problem check events.
    """

    problem_type = None  # "browser" or "server"

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
            event_id, actor_id, course.course_url, problem_id, emission_time
        )

        return {
            "event_id": event_id,
            "verb": self.verb,
            "actor_id": actor_id,
            "org": course.org,
            "problem_id": problem_id,
            "course_run_id": course.course_url,
            "emission_time": emission_time,
            "event": e,
        }

    def get_randomized_event(
        self, event_id, account, course_locator, problem_id, create_time
    ):
        """
        Given the inputs, return an xAPI statement.
        """
        browser_object = {
            "object": {
                "definition": {
                    "type": "http://adlnet.gov/expapi/activities/cmi.interaction"
                },
                "id": problem_id,
                "objectType": "Activity",
            }
        }

        response_options = [
            ("A correct answer", True),
            ("An incorrect answer", False),
            # FIXME: These aren't serializing correctly
            # ('["A correct answer 1", "A correct answer 2"]', True),
            # ('["A correct answer 1", "An incorrect answer 2"]', False),
        ]

        response, success = random.choice(response_options)
        attempts = random.randrange(1, 10)

        max_score = random.randint(1, 100)
        raw_score = random.randint(0, max_score)
        scaled_score = raw_score / max_score
        score_obj = {
            "scaled": scaled_score,
            "raw": raw_score,
            "min": 0.0,
            "max": max_score
        }

        server_object = {
            "object": {
                "definition": {
                    "extensions": {"http://id.tincanapi.com/extension/attempt-id": attempts},
                    "description": {
                        "en-US": "Add the question text, or prompt, here. This text is required."
                    },
                    "interactionType": "other",
                    "type": "http://adlnet.gov/expapi/activities/cmi.interaction",
                },
                "id": problem_id,
                "objectType": "Activity",
            },
            "result": {
                "response": response,
                "score": score_obj,
                "success": success,
            },
        }

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
                            "id": course_locator,
                            "objectType": "Activity",
                            "definition": {
                                "name": {"en-US": "Demonstration Course"},
                                "type": "http://adlnet.gov/expapi/activities/course",
                            },
                        }
                    ]
                },
                "extensions": {
                    "https://github.com/openedx/event-routing-backends/blob/master/docs/xapi-extensions/eventVersion.rst": "1.0"  # pylint: disable=line-too-long
                },
            },
            "timestamp": create_time.isoformat(),
            "verb": {"display": {"en": self.verb_display}, "id": self.verb},
            "version": "1.0.3",
        }

        if self.problem_type == "browser":
            event.update(browser_object)
        else:
            event.update(server_object)

        return json.dumps(event)


class BrowserProblemCheck(BaseProblemCheck):
    verb = "http://adlnet.gov/expapi/verbs/attempted"
    verb_display = "attempted"
    problem_type = "browser"


class ServerProblemCheck(BaseProblemCheck):
    verb = "https://w3id.org/xapi/acrossx/verbs/evaluated"
    verb_display = "evaluated"
    problem_type = "server"
