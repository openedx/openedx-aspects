"""
ClickHouse data lake implementation.
"""
import os
import uuid
from datetime import UTC, datetime

import clickhouse_connect


class XAPILakeClickhouse:
    """
    Lake implementation for ClickHouse.
    """

    client = None

    def __init__(self, config):
        self.host = config.get("db_host", "localhost")
        self.port = config.get("db_port", "18123")
        self.username = config.get("db_username", "default")
        self.database = config.get("db_name", "xapi")
        self.event_sink_database = config.get("db_event_sink_name", "event_sink")
        self.db_password = config.get("db_password")
        self.s3_key = config.get("s3_key")
        self.s3_secret = config.get("s3_secret")

        self.event_raw_table_name = config.get(
            "event_raw_table_name", "xapi_events_all"
        )
        self.event_table_name = config.get("event_table_name", "xapi_events_all_parsed")
        self.set_client()

    def set_client(self):
        """
        Set up the ClickHouse client and connect.
        """
        client_options = {
            "date_time_input_format": "best_effort",  # Allows RFC dates
        }

        # For some reason get_client isn't automatically setting secure based on the port
        # so we have to do it ourselves. This is obviously limiting, but should be 90% correct
        # and keeps us from adding yet another command line option.
        secure = str(self.port).endswith("443") or str(self.port).endswith("440")

        self.client = clickhouse_connect.get_client(
            host=self.host,
            username=self.username,
            password=self.db_password,
            port=self.port,
            database=self.database,
            settings=client_options,
            secure=secure,
        )

    def print_db_time(self):
        """
        Print the current time according to the db.
        """
        res = self.client.query("SELECT timezone(), now()")
        # Always flush our output on these so we can follow the logs.
        print(res.result_set, flush=True)

    def print_row_counts(self):
        """
        Print the current row count.
        """
        print("Hard table row count:")
        res = self.client.query(f"SELECT count(*) FROM {self.event_table_name}")
        print(res.result_set)

    def batch_insert(self, events):
        """
        Insert a batch of events to ClickHouse.
        """
        out_data = []
        for v in events:
            try:
                out = f"('{v['event_id']}', '{v['emission_time']}', '{v['event']}')"
                out_data.append(out)
            except Exception:
                print(v)
                raise
        vals = ",".join(out_data)
        sql = f"""
                INSERT INTO {self.event_raw_table_name} (
                    event_id,
                    emission_time,
                    event
                )
                VALUES {vals}
            """

        self._insert_sql_with_retry(sql)

    def insert_event_sink_course_data(self, courses):
        """
        Insert the course overview data to ClickHouse.

        This allows us to test join performance to get course and block names.
        """
        out_data = []
        for course in courses:
            c = course.serialize_course_data_for_event_sink()
            dump_id = str(uuid.uuid4())
            dump_time = datetime.now(UTC)
            try:
                out = f"""(
                    '{c['org']}',
                    '{c['course_key']}',
                    '{c['display_name']}',
                    '{c['course_start']}',
                    '{c['course_end']}',
                    '{c['enrollment_start']}',
                    '{c['enrollment_end']}',
                    '{c['self_paced']}',
                    '{c['course_data_json']}',
                    '{c['created']}',
                    '{c['modified']}',
                    '{dump_id}',
                    '{dump_time}'
                )"""
                out_data.append(out)
            except Exception:
                print(c)
                raise

        self._insert_list_sql_retry(out_data, "course_overviews")

    def insert_event_sink_block_data(self, courses):
        """
        Insert the block data to ClickHouse.

        This allows us to test join performance to get course and block names.
        """
        for course in courses:
            out_data = []
            blocks, object_tags = course.serialize_block_data_for_event_sink()
            dump_id = str(uuid.uuid4())
            dump_time = datetime.now(UTC)
            for b in blocks:
                try:
                    out = f"""(
                        '{b['org']}',
                        '{b['course_key']}',
                        '{b['location']}',
                        '{b['display_name']}',
                        '{b['xblock_data_json']}',
                        '{b['order']}',
                        '{b['edited_on']}',
                        '{dump_id}',
                        '{dump_time}'
                    )"""
                    out_data.append(out)
                except Exception:
                    print(b)
                    raise

            self._insert_list_sql_retry(out_data, "course_blocks")

            # Now insert all the "object tags" for these blocks
            self.insert_event_sink_object_tag_data(object_tags)

    def insert_event_sink_actor_data(self, actors):
        """
        Insert the user_profile and external_id data to ClickHouse.

        This allows us to test PII reports.
        """
        out_external_id = []
        out_profile = []
        for actor in actors:
            dump_id = str(uuid.uuid4())
            dump_time = datetime.now(UTC)

            id_row = f"""(
                '{actor.id}',
                'xapi',
                '{actor.username}',
                '{actor.user_id}',
                '{dump_id}',
                '{dump_time}'
            )"""
            out_external_id.append(id_row)

            # This first column is usually the MySQL row pk, we just
            # user this for now to have a unique id.
            profile_row = f"""(
                '{actor.user_id}',
                '{actor.user_id}',
                '{actor.name}',
                '{actor.username}@aspects.invalid',
                '{actor.meta}',
                '{actor.courseware}',
                '{actor.language}',
                '{actor.location}',
                '{actor.year_of_birth}',
                '{actor.gender}',
                '{actor.level_of_education}',
                '{actor.mailing_address}',
                '{actor.city}',
                '{actor.country}',
                '{actor.state}',
                '{actor.goals}',
                '{actor.bio}',
                '{actor.profile_image_uploaded_at}',
                '{actor.phone_number}',
                '{dump_id}',
                '{dump_time}'
            )"""

            out_profile.append(profile_row)

        self._insert_list_sql_retry(out_external_id, "external_id")
        self._insert_list_sql_retry(out_profile, "user_profile")

    def insert_event_sink_taxonomies(self, taxonomies):
        """
        Insert the taxonomies into the event sink db.
        """
        dump_id = str(uuid.uuid4())
        dump_time = datetime.now(UTC)
        i = 1
        out_data = []
        for taxonomy in taxonomies.keys():
            out = f"""(
                {i},
                '{taxonomy}',
                '{dump_id}',
                '{dump_time}'
            )
            """
            out_data.append(out)
            i += 1

        self._insert_list_sql_retry(out_data, "taxonomy")

    def insert_event_sink_tag_data(self, tags):
        """
        Insert the tags into the event sink db.
        """
        dump_id = str(uuid.uuid4())
        dump_time = datetime.now(UTC)

        tag_out_data = []
        for tag in tags:
            out_tag = f"""(
                {tag["tag_id"]},
                {tag["taxonomy_id"]},
                {tag["parent_int_id"] or 0},
                '{tag["value"]}',
                '{tag["id"]}',
                '{tag["hierarchy"]}',
                '{dump_id}',
                '{dump_time}'
            )"""

            tag_out_data.append(out_tag)

        self._insert_list_sql_retry(tag_out_data, "tag")

    def insert_event_sink_object_tag_data(self, object_tags):
        """
        Insert the object_tag data to ClickHouse.

        Most of the work for this is done in insert_event_sink_block_data
        """
        dump_id = str(uuid.uuid4())
        dump_time = datetime.now(UTC)
        obj_tag_out_data = []

        row_id = 0
        for obj_tag in object_tags:
            row_id += 1

            out_tag = f"""(
            {row_id},
            '{obj_tag["object_id"]}',
            {obj_tag["taxonomy_id"]},
            {obj_tag["tag_id"]},
            '{obj_tag["value"]}',
            'fake export id',
            '{obj_tag["hierarchy"]}',
            '{dump_id}',
            '{dump_time}'
            )"""

            obj_tag_out_data.append(out_tag)

        self._insert_list_sql_retry(obj_tag_out_data, "object_tag")

    def _insert_list_sql_retry(self, data_list, table, database=None):
        """
        Wrap up inserts that join values to reduce some boilerplate.
        """
        if not database:
            database = self.event_sink_database

        sql = f"""
                INSERT INTO {database}.{table}
                VALUES {",".join(data_list)}
        """

        self._insert_sql_with_retry(sql)

    def _insert_sql_with_retry(self, sql):
        """
        Wrap insert commands with a single retry.
        """
        # Sometimes the connection randomly dies, this gives us a second shot in that case
        try:
            self.client.command(sql)
        except clickhouse_connect.driver.exceptions.OperationalError:
            print("ClickHouse OperationalError, trying to reconnect.")
            self.set_client()
            print("Retrying insert...")
            self.client.command(sql)
        except clickhouse_connect.driver.exceptions.DatabaseError:
            print("ClickHouse DatabaseError:")
            print(sql)
            raise

    def load_from_s3(self, s3_location):
        """
        Load generated csv.gz files from S3.

        This does a bulk file insert directly from S3 to ClickHouse, so files
        never get downloaded directly to the local process.
        """
        loads = (
            (
                f"{self.event_sink_database}.course_overviews",
                os.path.join(s3_location, "courses.csv.gz"),
            ),
            (
                f"{self.event_sink_database}.course_blocks",
                os.path.join(s3_location, "blocks.csv.gz"),
            ),
            (
                f"{self.event_sink_database}.external_id",
                os.path.join(s3_location, "external_ids.csv.gz"),
            ),
            (
                f"{self.event_sink_database}.user_profile",
                os.path.join(s3_location, "user_profiles.csv.gz"),
            ),

            (
                f"{self.event_sink_database}.taxonomy",
                os.path.join(s3_location, "taxonomies.csv.gz"),
            ),
            (
                f"{self.event_sink_database}.tag",
                os.path.join(s3_location, "tags.csv.gz"),
            ),
            (
                f"{self.event_sink_database}.object_tag",
                os.path.join(s3_location, "object_tags.csv.gz"),
            ),

            (
                f"{self.database}.{self.event_raw_table_name}",
                os.path.join(s3_location, "xapi.csv.gz"),
            ),
        )

        for table_name, file_path in loads:
            print(f"Inserting into {table_name}")

            sql = f"""
            INSERT INTO {table_name}
               SELECT *
               FROM s3('{file_path}', '{self.s3_key}', '{self.s3_secret}', 'CSV');
            """

            self.client.command(sql)
            self.print_db_time()

    def finalize(self):
        """
        Nothing to finalize here.
        """

    def _run_query_and_print(self, query_name, query):
        """
        Execute a ClickHouse query and print the elapsed client time.
        """
        print(query_name)
        start_time = datetime.now(UTC)
        result = self.client.query(query)
        end_time = datetime.now(UTC)
        print(result.summary)
        print(result.result_set[:10])
        print("Completed in: " + str((end_time - start_time).total_seconds()))
        print("=================================")

    def do_queries(self, event_generator):
        """
        Query data from the table and document how long the query runs (while the insert script is running).
        """
        # Get our randomly selected targets for this run
        course = event_generator.get_course()
        course_url = course.course_url
        org = event_generator.get_org()
        actor = course.get_enrolled_actor().actor.id

        self._run_query_and_print(
            "Count of enrollment events for course {course_url}",
            f"""
                select count(*)
                from {self.event_table_name}
                where course_id = '{course_url}'
                and verb_id = 'http://adlnet.gov/expapi/verbs/registered'
            """,
        )

        self._run_query_and_print(
            "Count of total enrollment events for org {org}",
            f"""
                select count(*)
                from {self.event_table_name}
                where org = '{org}'
                and verb_id = 'http://adlnet.gov/expapi/verbs/registered'
            """,
        )

        self._run_query_and_print(
            "Count of enrollments for this actor",
            f"""
                select count(*)
                from {self.event_table_name}
                where actor_id = '{actor}'
                and verb_id = 'http://adlnet.gov/expapi/verbs/registered'
            """,
        )

        self._run_query_and_print(
            "Count of enrollments for this course - count of unenrollments, last 30 days",
            f"""
                select a.cnt, b.cnt, a.cnt - b.cnt as total_registrations
                from (
                select count(*) cnt
                from {self.event_table_name}
                where course_id = '{course_url}'
                and verb_id = 'http://adlnet.gov/expapi/verbs/registered'
                and emission_time between date_sub(DAY, 30, now('UTC')) and now('UTC')) as a,
                (select count(*) cnt
                from {self.event_table_name}
                where course_id = '{course_url}'
                and verb_id = 'http://id.tincanapi.com/verb/unregistered'
                and emission_time between date_sub(DAY, 30, now('UTC')) and now('UTC')) as b
            """,
        )

        # Number of enrollments for this course - number of unenrollments, all time
        self._run_query_and_print(
            "Count of enrollments for this course - count of unenrollments, all time",
            f"""
                select a.cnt, b.cnt, a.cnt - b.cnt as total_registrations
                from (
                select count(*) cnt
                from {self.event_table_name}
                where course_id = '{course_url}'
                and verb_id = 'http://adlnet.gov/expapi/verbs/registered'
                ) as a,
                (select count(*) cnt
                from {self.event_table_name}
                where course_id = '{course.course_id}'
                and verb_id = 'http://id.tincanapi.com/verb/unregistered'
                ) as b
            """,
        )

        self._run_query_and_print(
            "Count of enrollments for all courses - count of unenrollments, last 5 minutes",
            f"""
                select a.cnt, b.cnt, a.cnt - b.cnt as total_registrations
                from (
                select count(*) cnt
                from {self.event_table_name}
                where verb_id = 'http://adlnet.gov/expapi/verbs/registered'
                and emission_time between date_sub(MINUTE, 5, now('UTC')) and now('UTC')) as a,
                (select count(*) cnt
                from {self.event_table_name}
                where verb_id = 'http://id.tincanapi.com/verb/unregistered'
                and emission_time between date_sub(MINUTE, 5, now('UTC')) and now('UTC')) as b
            """,
        )
