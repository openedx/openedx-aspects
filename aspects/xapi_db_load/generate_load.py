"""
Generates batches of random xAPI events.
"""
import datetime
import json
import os
import pprint
import random
import uuid
from datetime import UTC
from random import choice, choices

from aspects.xapi_db_load.course_configs import Actor, RandomCourse
from aspects.xapi_db_load.fixtures.music_tags import MUSIC_TAGS
from aspects.xapi_db_load.utils import LogTimer, setup_timing
from aspects.xapi_db_load.xapi.xapi_forum import PostCreated
from aspects.xapi_db_load.xapi.xapi_grade import CourseGradeCalculated, FirstTimePassed
from aspects.xapi_db_load.xapi.xapi_hint_answer import ShowAnswer, ShowHint
from aspects.xapi_db_load.xapi.xapi_navigation import (
    LinkClicked,
    NextNavigation,
    PreviousNavigation,
    TabSelectedNavigation,
)
from aspects.xapi_db_load.xapi.xapi_problem import BrowserProblemCheck, ServerProblemCheck
from aspects.xapi_db_load.xapi.xapi_registration import Registered, Unregistered
from aspects.xapi_db_load.xapi.xapi_video import (
    CompletedVideo,
    LoadedVideo,
    PausedVideo,
    PlayedVideo,
    PositionChangedVideo,
    StoppedVideo,
    TranscriptDisabled,
    TranscriptEnabled,
)

# This is the list of event types to generate, and the proportion of total xapi
# events that should be generated for each. Should total roughly 100 to keep
# percentages simple.
EVENT_LOAD = (
    (Registered, 1.138),
    (Unregistered, 0.146),
    (CompletedVideo, 5.124),
    (LoadedVideo, 7.125),
    (PlayedVideo, 24.019),
    (PausedVideo, 14.912),
    (StoppedVideo, 3.671),
    (PositionChangedVideo, 12.105),
    (BrowserProblemCheck, 8.226),
    (ServerProblemCheck, 8.593),
    (NextNavigation, 6.05),
    (PreviousNavigation, 0.811),
    (TabSelectedNavigation, 0.001),
    (LinkClicked, 0.001),
    (FirstTimePassed, 0.031),
    (ShowHint, 0.076),
    (ShowAnswer, 1.373),
    (TranscriptEnabled, 0.05),
    (TranscriptDisabled, 0.05),
    (CourseGradeCalculated, 1.5),
    (PostCreated, 0.5),
)

EVENTS = [i[0] for i in EVENT_LOAD]
EVENT_WEIGHTS = [i[1] for i in EVENT_LOAD]
FILE_DIR = os.path.dirname(os.path.abspath(__file__))


def _get_uuid():
    return str(uuid.uuid4())


class EventGenerator:
    """
    Generates a batch of random xAPI events based on the EVENT_WEIGHTS proportions.
    """

    actors = []
    courses = []
    orgs = []
    taxonomies = {}
    tags = []

    def __init__(self, config):
        self.config = config
        self.start_date = config["start_date"]
        self.end_date = config["end_date"]
        self._validate_config()
        self.setup_orgs()
        self.setup_taxonomies_tags()
        self.setup_actors()
        self.setup_courses()

    def _validate_config(self):
        """
        Make sure the given values make sense.
        """
        if self.start_date >= self.end_date:
            raise ValueError("Start date must be before end date.")

        if (self.end_date - self.start_date).days < self.config["course_length_days"]:
            raise ValueError("The time between start and end dates must be longer than course_length_days.")

        for s in self.config["num_course_sizes"]:
            if self.config["course_size_makeup"][s]["actors"] > self.config["num_actors"]:
                raise ValueError(f"Course size {s} wants more actors than are configured in num_actors.")

    def setup_orgs(self):
        """
        Create some random organizations based on the config.
        """
        for i in range(self.config["num_organizations"]):
            self.orgs.append(f"Org{i}")

    def setup_courses(self):
        """
        Pre-create a number of courses based on the config.
        """
        for course_config_name, num_courses in self.config["num_course_sizes"].items():
            print(f"Setting up {num_courses} {course_config_name} courses")

            curr_num = 0
            while curr_num < num_courses:
                course_config_makeup = self.config["course_size_makeup"][course_config_name]
                org = choice(self.orgs)
                actors = choices(self.actors, k=course_config_makeup["actors"])
                runs = random.randrange(1, 5)
                course_id = str(uuid.uuid4())[:6]

                # Create 1-5 of the same course size / makeup / name
                # but different course runs.
                for run_id in range(runs):
                    course = RandomCourse(
                        org,
                        course_id,
                        run_id,
                        self.start_date,
                        self.end_date,
                        self.config["course_length_days"],
                        actors,
                        course_config_name,
                        course_config_makeup,
                        self.tags
                    )

                    self.courses.append(course)

                    curr_num += 1

                    # Don't let our number of runs overrun the total number
                    # of this type of course
                    if curr_num == num_courses:
                        break

    def setup_actors(self):
        """
        Create all known actors.

        Random samplings of these will be passed into courses.
        """
        self.actors = [Actor(i) for i in range(self.config["num_actors"])]

    @staticmethod
    def _get_hierarchy(tag_hierarchy, start_parent_id):
        """
        Return a list of all the parent values of the given parent_id.

        tag_hierarchy is a tuple of ("Tag name", "parent_id")
        """
        if not start_parent_id or start_parent_id not in tag_hierarchy:
            return []

        hierarchy = []
        parent_id = start_parent_id
        while parent_id:
            hierarchy.append(tag_hierarchy[parent_id][0])
            parent_id = tag_hierarchy[parent_id][1]

        # Reverse the list to get the highest parent first, which is how Studio
        # sends it
        hierarchy.reverse()
        return hierarchy

    def setup_taxonomies_tags(self):
        """
        Load a sample set of tags and format them for use.
        """
        self.taxonomies["Music"] = list(MUSIC_TAGS)

        # tag_hierarchy holds all of the known tags and their parents. This
        # works because the incoming CSV is sorted in a parent-first way. So
        # it should be guaranteed that all parents already exist when we get to
        # the child.
        tag_hierarchy = {}
        taxonomy_id = 0
        for taxonomy in self.taxonomies:  # pylint: disable=consider-using-dict-items
            taxonomy_id += 1
            tag_id = 0
            for tag in self.taxonomies[taxonomy]:
                tag_id += 1
                tag["tag_id"] = tag_id
                tag["taxonomy_id"] = taxonomy_id
                tag["parent_int_id"] = tag_hierarchy[tag["parent_id"]][2] if tag["parent_id"] in tag_hierarchy else None
                tag["hierarchy"] = json.dumps(self._get_hierarchy(
                    tag_hierarchy,
                    tag["parent_id"]
                ))

                tag_hierarchy[tag["id"]] = (tag["value"], tag["parent_id"], tag["tag_id"])
                self.tags.append(tag)

    def get_batch_events(self):
        """
        Create a batch size list of random events.

        Events are from our EVENTS list, based on the EVENT_WEIGHTS proportions.
        """
        events = choices(EVENTS, EVENT_WEIGHTS, k=self.config["batch_size"])
        return [e(self).get_data() for e in events]

    def get_enrollment_events(self):
        """
        Generate enrollment events for all actors.
        """
        enrollments = []
        for course in self.courses:
            for actor in course.actors:
                enrollments.append(Registered(self).get_data(course, actor))
        return enrollments

    def get_course(self):
        """
        Return a random course from our pre-built list.
        """
        return choice(self.courses)

    def get_org(self):
        """
        Return a random org from our pre-built list.
        """
        return choice(self.orgs)

    def dump_courses(self):
        """
        Prettyprint all known courses.
        """
        for c in self.courses:
            pprint.pprint(c)


def generate_events(config, backend):
    """
    Generate the actual events in the backend, using the given config.
    """
    setup_timing(config["log_dir"])

    print("Checking table existence and current row count in backend...")
    backend.print_row_counts()
    start = datetime.datetime.now(UTC)

    with LogTimer("setup", "full_setup"):
        with LogTimer("setup", "event_generator"):
            event_generator = EventGenerator(config)
            event_generator.dump_courses()

    print("Inserting course metadata...")
    with LogTimer("insert_metadata", "course"):
        backend.insert_event_sink_course_data(event_generator.courses)

    print("Inserting block metadata...")
    with LogTimer("insert_metadata", "blocks"):
        backend.insert_event_sink_block_data(event_generator.courses)

    print("Inserting user data...")
    with LogTimer("insert_metadata", "user_data"):
        backend.insert_event_sink_actor_data(event_generator.actors)

    print("Inserting taxonomy data...")
    with LogTimer("insert_metadata", "taxonomy"):
        backend.insert_event_sink_taxonomies(event_generator.taxonomies)

    print("Inserting tag data...")
    with LogTimer("insert_metadata", "tag"):
        backend.insert_event_sink_tag_data(event_generator.tags)

    insert_registrations(event_generator, backend)
    insert_batches(event_generator, config["num_batches"], backend)

    with LogTimer("batches", "total"):
        print(f"Done! Added {config['num_batches'] * config['batch_size']:,} rows!")

    end = datetime.datetime.now(UTC)
    print("Batch insert time: " + str(end - start))

    backend.finalize()
    backend.print_db_time()
    backend.print_row_counts()

    end = datetime.datetime.now(UTC)
    print("Total run time: " + str(end - start))


def insert_registrations(event_generator, lake):
    """
    Insert all of the registration events.
    """
    with LogTimer("enrollment", "get_enrollment_events"):
        events = event_generator.get_enrollment_events()

    with LogTimer("enrollment", "insert_events"):
        lake.batch_insert(events)

    print(f"{len(events)} enrollment events inserted.")


def insert_batches(event_generator, num_batches, lake):
    """
    Generate and insert num_batches of events.
    """
    for x in range(num_batches):
        if x % 100 == 0:
            print(f"{x} of {num_batches}")
            lake.print_db_time()

        with LogTimer("batch", "get_events"):
            events = event_generator.get_batch_events()

        with LogTimer("batch", "insert_events"):
            lake.batch_insert(events)

        if x % 1000 == 0:
            with LogTimer("batch", "all_queries"):
                lake.do_queries(event_generator)
            lake.print_db_time()
            lake.print_row_counts()
