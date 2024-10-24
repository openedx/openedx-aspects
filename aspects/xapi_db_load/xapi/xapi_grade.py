"""
Fake xAPI statements for various grading events.
"""
import json
import random
from uuid import uuid4

from .xapi_common import XAPIBase


class FirstTimePassed(XAPIBase):
    """
    Base xAPI class for grading events.
    """

    verb = "http://adlnet.gov/expapi/verbs/passed"
    verb_display = "passed"

    def get_data(self):
        """
        Generate and return the event dict, including xAPI statement as "event".
        """
        event_id = str(uuid4())
        course = self.parent_load_generator.get_course()
        enrolled_actor = course.get_enrolled_actor()
        actor_id = enrolled_actor.actor.id
        emission_time = course.get_random_emission_time(enrolled_actor)

        e = self.get_randomized_event(event_id, actor_id, course, emission_time)

        return {
            "event_id": event_id,
            "verb": self.verb,
            "actor_id": actor_id,
            "org": course.org,
            "course_run_id": course.course_url,
            "emission_time": emission_time,
            "event": e,
        }

    def get_randomized_event(self, event_id, account, course, create_time):
        """
        Given the inputs, return an xAPI statement.
        """
        event = {
            "id": event_id,
            "actor": {
                "account": {"homePage": "http://localhost:18000", "name": account},
                "objectType": "Agent",
            },
            "context": {
                "extensions": {
                    "https://w3id.org/xapi/openedx/extension/transformer-version": "event-routing-backends@7.0.1",
                    "https://w3id.org/xapi/openedx/extensions/session-id": "e4858858443cd99828206e294587dac5"
                }
            },
            "object": {
                "definition": {
                    "extensions": {},
                    "name": {"en": "Demonstration Course"},
                    "type": "http://adlnet.gov/expapi/activities/course",
                },
                "id": course.course_url,
                "objectType": "Activity",
            },
            "timestamp": create_time.isoformat(),
            "verb": {"display": {"en": self.verb_display}, "id": self.verb},
            "version": "1.0.3",
        }

        return json.dumps(event)


class GradeCalculated(XAPIBase):
    """
    Base xAPI event for grade_calculated events.
    """

    verb = "http://id.tincanapi.com/verb/earned"
    verb_display = "earned"
    object_type = None

    def get_data(self):
        """
        Generate and return the event dict, including xAPI statement as "event".
        """
        event_id = str(uuid4())
        course = self.parent_load_generator.get_course()
        enrolled_actor = course.get_enrolled_actor()
        actor_id = enrolled_actor.actor.id
        emission_time = course.get_random_emission_time(enrolled_actor)

        e = self.get_randomized_event(event_id, actor_id, course, emission_time)
        return {
            "event_id": event_id,
            "verb": self.verb,
            "actor_id": actor_id,
            "org": course.org,
            "course_run_id": course.course_url,
            "emission_time": emission_time,
            "event": e,
        }

    def get_randomized_event(self, event_id, actor_id, course, emission_time):
        """
        Given the inputs, return an xAPI statement for a grade_calculated event.
        """
        max_score = random.randint(1, 100)
        raw_score = random.randint(0, max_score)
        scaled_score = raw_score / max_score
        score_obj = {
            "scaled": scaled_score,
            "raw": raw_score,
            "min": 0.0,
            "max": max_score
        }

        event = {
            "actor": {
                "account": {
                    "homePage": "http://localhost:18000",
                    "name": actor_id
                },
                "objectType": "Agent"
            },
            "id": event_id,
            "verb": {
                "id": self.verb,
                "display": {
                    "en": self.verb_display
                }
            },
            "context": {
                "contextActivities": {
                    "parent": [
                        {
                            "id": course.course_url,
                            "objectType": "Activity",
                            "definition": {
                                "name": {
                                    "en-US": "Demonstration Course"
                                },
                                "type": "http://adlnet.gov/expapi/activities/course"
                            },
                        }
                    ]
                },
                "extensions": {
                    "https://w3id.org/xapi/openedx/extension/transformer-version": "event-routing-backends@5.6.0"
                },
            },
            "version": "1.0.3",
            "timestamp": emission_time.isoformat(),
        }

        if self.object_type == "course":
            grade_classification = "Pass" if scaled_score > 0.65 else "Fail"
            course_fields = {
                "object": {
                    "id": course.course_url,
                    "definition": {
                        "name": {"en": "Demonstration Course"},
                        "type": "http://adlnet.gov/expapi/activities/course",
                    },
                    "objectType": "Activity",
                },
                "result": {
                    "score": score_obj,
                    "extensions": {
                        "http://www.tincanapi.co.uk/activitytypes/grade_classification": grade_classification
                    }
                }
            }
            event.update(course_fields)
        elif self.object_type == "subsection":
            subsection_fields = {
                "object": {
                    "id": course.get_random_sequential_id(),
                    "definition": {
                        "type": "http://id.tincanapi.com/activitytype/resource"
                    },
                    "objectType": "Activity"
                },
                "result": {
                    "score": score_obj,
                    "success": random.choice([True, False]),
                }
            }
            event.update(subsection_fields)

        return json.dumps(event)


class CourseGradeCalculated(GradeCalculated):
    object_type = "course"


class SubsectionGradeCalculated(GradeCalculated):
    object_type = "subsection"
