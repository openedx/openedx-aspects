"""
Configuration values for emulating courses of various sizes.
"""
import copy
import datetime
import json
import random
import uuid
from collections import namedtuple
from random import choice, randrange

EnrolledActor = namedtuple("Actor", ["actor", "enroll_datetime"])


class Actor:
    """
    Wrapper for actor PII data.

    These are a combination of fields from edx-platform UserProfile and
    ExternalId models. These fields are largely unpopulated in real life,
    especially after the introduction of the profile MFE, but operators have
    the capability to fill them in various ways.
    """

    def __init__(self, user_id):
        # Integer user id, just the counter from actor population
        self.user_id = user_id

        # "external_id" UUID
        self.id = str(uuid.uuid4())

        # LMS username
        self.username = f"actor_{self.user_id}"

        # These may or may not ever be populated in real life, potentially
        # useful values are populated here.
        self.name = f"Actor {user_id}"
        self.year_of_birth = random.randint(1900, 2010)
        self.gender = random.choice(["", "m", "f", "o"])
        self.level_of_education = random.choice(["", "p", "m", "b", "none", "other"])
        self.country = random.choice(["", "US", "CO", "AU", "IN", "PK"])
        self.goals = ""
        self.bio = ""

        # These will probably never be populated, and aren't expected to be used
        # but are part of the event sink and table
        self.meta = "{}"
        self.courseware = ""
        self.language = ""
        self.location = ""
        self.mailing_address = ""
        self.city = ""
        self.state = ""
        self.profile_image_uploaded_at = ""
        self.phone_number = ""


class RandomCourse:
    """
    Holds "known objects" and configuration values for a fake course.
    """

    items_in_course = 0
    chapter_ids = []
    sequential_ids = []
    vertical_ids = []
    problem_ids = []
    video_ids = []
    forum_post_ids = []
    actors = []
    all_tags = []
    start_date = None
    end_date = None

    def __init__(
        self,
        org,
        course_uuid,
        course_run,
        overall_start_date,
        overall_end_date,
        course_length,
        actors,
        course_config_name,
        course_size_makeup,
        tags
    ):
        self.course_uuid = course_uuid
        self.course_run = course_run
        # It's important that the course name stay the same between runs
        # as Superset limitations have us filtering by course name and we want
        # to be able to catch all course runs in those queries.
        self.course_name = f"{self.course_uuid} ({course_config_name})"
        self.org = org
        self.course_id = f"course-v1:{org}+{self.course_uuid}+{self.course_run}"
        self.course_url = f"http://localhost:18000/course/{self.course_id}"

        delta = datetime.timedelta(days=course_length)
        self.start_date = self._random_datetime(overall_start_date, overall_end_date - delta)
        self.end_date = self.start_date + delta

        self.actors = [
            EnrolledActor(a, self._random_datetime(self.start_date, self.end_date))
            for a in actors
        ]

        self.course_config_name = course_config_name
        self.course_config = course_size_makeup
        self.all_tags = tags
        self.configure()

    def __repr__(self):
        return f"""{self.course_name}:
        {self.start_date} - {self.end_date}
        {self.course_config}
        """

    def configure(self):
        """
        Set up the fake course configuration such as course length, start and end dates, and size.
        """
        self.chapter_ids = [
            self._generate_random_block_type_id("chapter")
            for _ in range(self.course_config["chapters"])
        ]

        self.sequential_ids = [
            self._generate_random_block_type_id("sequential")
            for _ in range(self.course_config["sequences"])
        ]

        self.vertical_ids = [
            self._generate_random_block_type_id("vertical")
            for _ in range(self.course_config["verticals"])
        ]

        self.problem_ids = [
            self._generate_random_block_type_id("problem")
            for _ in range(self.course_config["problems"])
        ]

        self.video_ids = [
            self._generate_random_block_type_id("video")
            for _ in range(self.course_config["videos"])
        ]

        self.forum_post_ids = [
            self._generate_random_forum_post_id()
            for _ in range(self.course_config["forum_posts"])
        ]

        for config in ("videos", "problems", "verticals", "sequences", "chapters", "forum_posts"):
            self.items_in_course += self.course_config[config]

    def get_random_emission_time(self, actor=None):
        """
        Randomizes an emission time for events that falls within the course start and end dates.
        """
        if actor:
            start = actor.enroll_datetime
        else:
            start = self.start_date

        # Make sure we're passing in a datetime, not a date
        start = datetime.datetime.combine(start, datetime.time())

        # time() is midnight, so make sure we get that last day in there
        end = datetime.datetime.combine(self.end_date, datetime.time()) + datetime.timedelta(days=1)

        return self._random_datetime(
            start_datetime=start, end_datetime=end
        )

    @staticmethod
    def _random_datetime(start_datetime=None, end_datetime=None):
        """
        Create a random datetime within the given boundaries.

        If no start date is given, we start 5 years ago.
        If no end date is given, we end now.
        """
        if not end_datetime:
            end_datetime = datetime.datetime.now(datetime.UTC)
        if not start_datetime:
            start_datetime = end_datetime - datetime.timedelta(days=365 * 5)

        delta = end_datetime - start_datetime
        int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
        random_second = randrange(int_delta)
        return start_datetime + datetime.timedelta(seconds=random_second)

    def get_enrolled_actor(self):
        """
        Return an actor from those known in this course.
        """
        return choice(self.actors)

    def get_video_id(self):
        """
        Return a video id from our list of known video ids.
        """
        return choice(self.video_ids)

    def _generate_random_block_type_id(self, block_type):
        block_uuid = str(uuid.uuid4())[:8]
        return f"http://localhost:18000/xblock/block-v1:{self.course_id}+type@{block_type}+block@{block_uuid}"

    def get_problem_id(self):
        """
        Return a problem id from our list of known problem ids.
        """
        return choice(self.problem_ids)

    def get_random_sequential_id(self):
        """
        Return a sequential id from our list of known sequential ids.
        """
        return choice(self.sequential_ids)

    def get_random_forum_post_id(self):
        """
        Return a sequential id from our list of known sequential ids.
        """
        return choice(self.forum_post_ids)

    def _generate_random_forum_post_id(self):
        thread_id = str(uuid.uuid4())[:8]
        return f"http://localhost:18000/api/discussion/v1/threads/{thread_id}"

    def get_random_nav_location(self):
        """
        Return a navigation location from our list of known ids.
        """
        return str(randrange(1, self.items_in_course))

    def serialize_course_data_for_event_sink(self):
        """
        Return a dict representing the course data from event-sink-clickhouse.
        """
        return {
            "org": self.org,
            "course_key": self.course_id,
            "display_name": self.course_name,
            "course_start": self.start_date,
            "course_end": self.end_date,
            "enrollment_start": self.start_date,
            "enrollment_end": self.end_date,
            "self_paced": choice([True, False]),
            # This is a catchall field, we don't currently use it
            "course_data_json": "{}",
            "created": self.start_date,
            "modified": self.end_date
        }

    def _serialize_block(self, block_type, block_id, cnt):
        return {
            "org": self.org,
            "course_key": self.course_id,
            "location": block_id.split("/xblock/")[-1],
            "display_name": f"{block_type.title()} {cnt}",
            # This gets appended with location data below
            "xblock_data_json": {"block_type": block_type},
            "order": cnt,
            "edited_on": self.end_date
        }

    def _serialize_course_block(self):
        location_course_id = self.course_id.replace("course-v1:", "")
        return {
            "org": self.org,
            "course_key": self.course_id,
            "location": f"block-v1:{location_course_id}+type@course+block@course",
            "display_name": f"Course {self.course_uuid[:5]}",
            # This gets appended with location data below
            "xblock_data_json": {"block_type": "course"},
            "order": 1,
            "edited_on": self.end_date
        }

    def serialize_block_data_for_event_sink(self):
        """
        Return lists of dicts representing block and block tag data.

        The data formats mirror what is created by event-sink-clickhouse.
        """
        blocks = []
        object_tags = []
        cnt = 1

        # Get all of our blocks in order
        for v in self.video_ids:
            blocks.append(self._serialize_block("video", v, cnt))
            cnt += 1
        for p in self.problem_ids:
            blocks.append(self._serialize_block("problem", p, cnt))
            cnt += 1

        course_structure = [self._serialize_course_block()]

        for c in self.chapter_ids:
            course_structure.append(self._serialize_block("chapter", c, cnt))
            cnt += 1

        for s in self.sequential_ids:
            # Randomly insert some sequentials under the chapters
            course_structure.insert(
                # Start at 2 here to make sure it's after the course and first
                # chapter block
                random.randint(2, len(course_structure)),
                self._serialize_block("sequential", s, cnt)
            )
            cnt += 1

        for v in self.vertical_ids:
            # Randomly insert some verticals under the sequentials
            course_structure.insert(
                # Start at 3 here to make sure it's after the course and first
                # chapter block and first sequential block
                random.randint(2, len(course_structure)),
                self._serialize_block("vertical", v, cnt)
            )
            cnt += 1

        # Now add in the blocks wherever, as long as they're after the
        # course, first chapter, first sequential, and first vertical. After
        # that they'll all be mixed together, but this will do for now.
        for b in blocks:
            course_structure.insert(
                random.randint(4, len(course_structure)),
                b
            )

        # Now actually set up the locations. These are important and used to
        # generate block display names in the database
        section_idx = 0
        subsection_idx = 0
        unit_idx = 0

        for block in course_structure:
            if block["display_name"].startswith("Chapter"):
                section_idx += 1
                subsection_idx = 0
                unit_idx = 0
            elif block["display_name"].startswith("Sequential"):
                subsection_idx += 1
                unit_idx = 0
            elif block["display_name"].startswith("Vertical"):
                unit_idx += 1

            block["xblock_data_json"].update({
                "section": section_idx,
                "subsection": subsection_idx,
                "unit": unit_idx,
            })

            block["xblock_data_json"] = json.dumps(block["xblock_data_json"])

            num_tags = randrange(0, 3)

            for _ in range(num_tags):
                tag = random.choice(self.all_tags)
                object_tag = copy.deepcopy(tag)
                object_tag["object_id"] = block["location"]
                object_tags.append(object_tag)

        return course_structure, object_tags
