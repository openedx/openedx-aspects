"""
CSV Lake implementation.

This can be used to generate a gzipped csv of events that can be loaded into any system.
"""

import csv
import os
import uuid
from datetime import UTC, datetime

from smart_open import open as smart


class XAPILakeCSV:
    """
    CSV fake data lake implementation.
    """

    def __init__(self, config):
        self.output_destination = config["csv_output_destination"]

        self.xapi_csv_handle, self.xapi_csv_writer = self._get_csv_handle(
            "xapi", self.output_destination
        )

        self.row_count = 0

    def _get_csv_handle(self, file_type, output_destination):
        out_filepath = os.path.join(output_destination, f"{file_type}.csv.gz")
        os.makedirs(output_destination, exist_ok=True)
        file_handle = smart(out_filepath, "w", compression=".gz")
        return file_handle, csv.writer(file_handle)

    def print_db_time(self):
        """
        Print the database time, in our case it's just the local computer time.
        """
        print(datetime.now(), flush=True)

    def print_row_counts(self):
        """
        Print the number of rows written to CSV so far.
        """
        print("Currently written row count:")
        print(self.row_count)

    def create_db(self):
        """
        Create database, not needed here.
        """

    def drop_tables(self):
        """
        Drop tables, not needed here.
        """

    def create_tables(self):
        """
        Create tables, not needed here.
        """

    def batch_insert(self, events):
        """
        Write a batch of rows to the CSV.
        """
        for v in events:
            out = (v["event_id"], v["emission_time"], str(v["event"]))
            self.xapi_csv_writer.writerow(out)
        self.row_count += len(events)

    def insert_event_sink_course_data(self, courses):
        """
        Write the course overview data.
        """
        course_csv_handle, course_csv_writer = self._get_csv_handle(
            "courses", self.output_destination
        )

        for course in courses:
            c = course.serialize_course_data_for_event_sink()
            dump_id = str(uuid.uuid4())
            dump_time = datetime.now(UTC)
            course_csv_writer.writerow(
                (
                    c["org"],
                    c["course_key"],
                    c["display_name"],
                    c["course_start"],
                    c["course_end"],
                    c["enrollment_start"],
                    c["enrollment_end"],
                    c["self_paced"],
                    c["course_data_json"],
                    c["created"],
                    c["modified"],
                    dump_id,
                    dump_time,
                )
            )

        course_csv_handle.close()

    def insert_event_sink_block_data(self, courses):
        """
        Write out the block data file.
        """
        blocks_csv_handle, blocks_csv_writer = self._get_csv_handle(
            "blocks", self.output_destination
        )

        for course in courses:
            blocks, object_tags = course.serialize_block_data_for_event_sink()
            dump_id = str(uuid.uuid4())
            dump_time = datetime.now(UTC)
            for b in blocks:
                blocks_csv_writer.writerow(
                    (
                        b["org"],
                        b["course_key"],
                        b["location"],
                        b["display_name"],
                        b["xblock_data_json"],
                        b["order"],
                        b["edited_on"],
                        dump_id,
                        dump_time,
                    )
                )

            # Now insert all the "object tags" for these blocks
            self.insert_event_sink_object_tag_data(object_tags)

        blocks_csv_handle.close()

    def insert_event_sink_taxonomies(self, taxonomies):
        """
        Write out the taxonomies data file.
        """
        taxonomy_handle, taxonomy_csv_writer = self._get_csv_handle(
            "taxonomies", self.output_destination
        )
        dump_id = str(uuid.uuid4())
        dump_time = datetime.now(UTC)
        i = 1
        for taxonomy in taxonomies.keys():
            taxonomy_csv_writer.writerow((i, taxonomy, dump_id, dump_time))
            i += 1

        taxonomy_handle.close()

    def insert_event_sink_tag_data(self, tags):
        """
        Insert the tags into the event sink db.
        """
        tag_csv_handle, tag_csv_writer = self._get_csv_handle(
            "tags", self.output_destination
        )
        dump_id = str(uuid.uuid4())
        dump_time = datetime.now(UTC)

        for tag in tags:
            tag_csv_writer.writerow(
                (
                    tag["tag_id"],
                    tag["taxonomy_id"],
                    tag["parent_int_id"],
                    tag["value"],
                    tag["id"],
                    tag["hierarchy"],
                    dump_id,
                    dump_time,
                )
            )

        tag_csv_handle.close()

    def insert_event_sink_object_tag_data(self, object_tags):
        """
        Write the object_tag data.
        """
        object_tag_csv_handle, object_tag_csv_writer = self._get_csv_handle(
            "object_tags", self.output_destination
        )
        dump_id = str(uuid.uuid4())
        dump_time = datetime.now(UTC)

        row_id = 0

        for obj_tag in object_tags:
            row_id += 1
            object_tag_csv_writer.writerow(
                (
                    row_id,
                    obj_tag["object_id"],
                    obj_tag["taxonomy_id"],
                    obj_tag["tag_id"],
                    obj_tag["value"],
                    "fake export id",
                    obj_tag["hierarchy"],
                    dump_id,
                    dump_time,
                )
            )

        object_tag_csv_handle.close()

    def insert_event_sink_actor_data(self, actors):
        """
        Write out the user profile data and external id files.
        """
        profile_csv_handle, profile_csv_writer = self._get_csv_handle(
            "user_profiles", self.output_destination
        )
        external_id_csv_handle, external_id_csv_writer = self._get_csv_handle(
            "external_ids", self.output_destination
        )
        for actor in actors:
            dump_id = str(uuid.uuid4())
            dump_time = datetime.now(UTC)

            external_id_csv_writer.writerow(
                (
                    actor.id,
                    "xapi",
                    actor.username,
                    actor.user_id,
                    dump_id,
                    dump_time,
                )
            )

            profile_csv_writer.writerow(
                (
                    # This first column is usually the MySQL row pk, we just
                    # user this for now to have a unique id.
                    actor.user_id,
                    actor.user_id,
                    actor.name,
                    f"{actor.username}@aspects.invalid",
                    actor.meta,
                    actor.courseware,
                    actor.language,
                    actor.location,
                    actor.year_of_birth,
                    actor.gender,
                    actor.level_of_education,
                    actor.mailing_address,
                    actor.city,
                    actor.country,
                    actor.state,
                    actor.goals,
                    actor.bio,
                    actor.profile_image_uploaded_at,
                    actor.phone_number,
                    dump_id,
                    dump_time,
                )
            )

        profile_csv_handle.close()
        external_id_csv_handle.close()

    def finalize(self):
        """
        Close file handles so that they can be readable on import.
        """
        self.xapi_csv_handle.close()

    def do_queries(self, event_generator):
        """
        Execute queries, not needed here.
        """
