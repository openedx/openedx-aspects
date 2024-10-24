"""
Lake implementation for the Ralph LRS.

Currently only supports the ClickHouse Ralph backend, but older versions of this file supported Mongo.
"""
import datetime
import json

import requests

from aspects.xapi_db_load.backends.clickhouse_lake import XAPILakeClickhouse


class DateTimeEncoder(json.JSONEncoder):
    """
    Makes our generated datetime object format compliant with what Ralph expects.
    """

    def default(self, o):
        """
        Override the default method add our formatting.
        """
        if isinstance(o, (datetime.date, datetime.datetime)):
            return o.isoformat()
        raise TypeError("Not a valid date or datetime instance!")


class XAPILRSRalphClickhouse(XAPILakeClickhouse):
    """
    Wraps the XAPILakeClickhouse backend so that queries can be run against it while using Ralph to do the insertion.
    """

    def __init__(self, config):
        super().__init__(config)
        self.lrs_url = config["lrs_url"]
        self.lrs_username = config["lrs_username"]
        self.lrs_password = config["lrs_password"]

    def batch_insert(self, events):
        """
        POST a batch of rows to Ralph.

        Ralph wants one json object per line, not an array of objects.
        """
        out_data = [json.loads(x["event"]) for x in events]
        resp = requests.post(  # pylint: disable=missing-timeout
            self.lrs_url,
            auth=(self.lrs_username, self.lrs_password),
            json=out_data,
            headers={"Content-Type": "application/json"},
        )
        try:
            resp.raise_for_status()
        except requests.HTTPError:
            print(json.dumps(out_data))
            raise
