"""
Tests for xapi-db-load.py.
"""
import gzip
import os
from contextlib import contextmanager
from unittest.mock import patch

import yaml
from click.testing import CliRunner

from aspects.xapi_db_load.main import load_db


@contextmanager
def override_config(config_path, tmpdir):
    """
    Override the config file with runtime variables (temp file paths, etc).

    Overrides for both the test code and the loading code.
    """
    with open(config_path, "r") as f:
        test_config = yaml.safe_load(f)

    test_config["log_dir"] = str(tmpdir)
    test_config["csv_output_destination"] = str(tmpdir)

    with patch('aspects.xapi_db_load.main.get_config') as mock_config:
        mock_config.return_value = test_config
        try:
            yield test_config
        finally:
            pass


def test_csv(tmpdir):
    test_path = "aspects/xapi_db_load/tests/fixtures/small_config.yaml"

    with override_config(test_path, tmpdir) as test_config:
        runner = CliRunner()
        result = runner.invoke(
            load_db,
            f"--config_file {test_path}",
            catch_exceptions=False
        )

        assert "Currently written row count" in result.output
        assert "Done" in result.output
        assert "Total run time" in result.output

        makeup = test_config["course_size_makeup"]["small"]

        expected_enrollments = test_config["num_course_sizes"]["small"] * makeup["actors"]
        expected_statements = test_config["num_batches"] * test_config["batch_size"] + expected_enrollments
        expected_actors = test_config["num_actors"]
        expected_courses = test_config["num_course_sizes"]["small"]

        # We want all the configured block types, which are currently everything in
        # the config except the actor and forum post count
        expected_course_blocks = sum(makeup.values()) - makeup["actors"] - makeup["forum_posts"]

        # Plus 1 for the course block
        expected_blocks = (expected_course_blocks + 1) * expected_courses

        for prefix, expected in (
            ("xapi", expected_statements),
            ("courses", expected_courses),
            ("blocks", expected_blocks),
            ("external_ids", expected_actors),
            ("user_profiles", expected_actors)
        ):
            with gzip.open(os.path.join(test_config["log_dir"], f"{prefix}.csv.gz"), "r") as csv:
                assert len(csv.readlines()) == expected, f"Bad row count in csv file {prefix}.csv.gz."


@patch("aspects.xapi_db_load.backends.clickhouse_lake.clickhouse_connect")
def test_clickhouse_lake(_, tmpdir):
    test_path = "aspects/xapi_db_load/tests/fixtures/small_clickhouse_config.yaml"

    with override_config(test_path, tmpdir):
        runner = CliRunner()
        result = runner.invoke(
            load_db,
            f"--config_file {test_path}",
            catch_exceptions=False,
        )

    assert "Done." in result.output
    assert "55 enrollment events inserted." in result.output
    assert "Done! Added 300 rows!" in result.output
    assert "Total run time" in result.output


@patch("aspects.xapi_db_load.backends.ralph_lrs.requests")
@patch("aspects.xapi_db_load.backends.clickhouse_lake.clickhouse_connect")
def test_ralph_clickhouse(mock_requests, _, tmpdir):
    test_path = "aspects/xapi_db_load/tests/fixtures/small_ralph_config.yaml"
    runner = CliRunner()

    with override_config(test_path, tmpdir):
        result = runner.invoke(
            load_db,
            f"--config_file {test_path}",
            catch_exceptions=False,
        )
    print(mock_requests.mock_calls)
    print(result.output)
    assert "Done." in result.output
    assert "60 enrollment events inserted." in result.output
    assert "Done! Added 300 rows!" in result.output
    assert "Total run time" in result.output
