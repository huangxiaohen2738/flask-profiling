import json
import time
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Measurements, base


class Backend(object):

    def __init__(self):
        self.config = None
        self.db = None

    def init_app(self, app):
        db_config = app.config["FLASK_PROFILING"].get("db_url")
        assert db_config is not None, "db_url is None"
        self.db = create_engine(db_config)
        self.create_database()

    def create_database(self):
        base.metadata.create_all(self.db)

    @property
    def session(self):
        return sessionmaker(bind=self.db)()

    def to_filter(self, kwargs):
        kwargs = kwargs if kwargs is not None else {}
        return {
            "sort": kwargs.get("sort", "endedAt,desc").split(","),
            "endedAt": float(kwargs.get("endedAt", time.time() + 0.5)),
            "startedAt": float(kwargs.get(
                "startedAt", time.time() - 3600 * 24 * 7)),
            "elapsed": kwargs.get("elapsed", None),
            "method": kwargs.get("method", None),
            "name": kwargs.get("name", None),
            "args": json.dumps(list(kwargs.get("args", ()))),
            "kwargs": json.dumps(kwargs.get("kwargs", ())),
            "skip": int(kwargs.get("skip", 0)),
            "limit": int(kwargs.get("limit", 100))
        }

    def to_json(self, row):
        return {
            "id": row[0],
            "startedAt": row[1],
            "endedAt": row[2],
            "elapsed": row[3],
            "method": row[4],
            "args": tuple(json.loads(row[5])),
            "kwargs": json.loads(row[6]),
            "name": row[7],
            "context": json.loads(row[8]),
        }

    def to_datetime(self, timestamp, date_format):
        return datetime.fromtimestamp(timestamp).strftime(date_format)

    def get(self, id):
        m = Measurements.query.get(id)
        if m is None:
            return {}
        return m.to_dict()

    def insert(self, kwargs):
        elapsed = kwargs.get("elapsed", 0)
        kwargs["elapsed"] = elapsed
        kwargs["args"] = json.dumps(list(kwargs.get("args", ())))
        kwargs["kwargs"] = json.dumps(kwargs.get("kwargs", ()))
        kwargs["context"] = json.dumps(kwargs.get("context", {}))
        session = sessionmaker(bind=self.db)()
        session.add(Measurements(**kwargs))
        session.commit()

    def filter(self, kwargs=None):
        f = self.to_filter(kwargs)

        conditions = "WHERE 1=1 AND "
        if f["endedAt"]:
            conditions += "endedAt<={0} AND ".format(f["endedAt"])
        if f["startedAt"]:
            conditions += "startedAt>={0} AND ".format(f["startedAt"])
        if f["elapsed"]:
            conditions += "elapsed>={0} AND ".format(f["elapsed"])
        if f["method"]:
            conditions += "method='{0}' AND ".format(f["method"])
        if f["name"]:
            conditions += "name='{0}' AND ".format(f["name"])

        conditions = conditions.rstrip(" AND")

        sql = """SELECT * FROM flask_profiling_measurements {conditions}
        order by {sort_field} {sort_direction}
        limit {limit} OFFSET {skip} """.format(
            conditions=conditions,
            sort_field=f["sort"][0],
            sort_direction=f["sort"][1],
            limit=f["limit"],
            skip=f["skip"]
        )
        rows = self.session.execute(sql)
        return map(self.to_json, rows)

    def truncate(self):
        session = sessionmaker(bind=self.db)()
        try:
            session.query(Measurements).delete()
            session.commit()
            return True
        except BaseException:
            session.rollback()
            return False

    def delete(self, id):
        m = Measurements.query.get(id)
        if m is None:
            return False
        session = sessionmaker(bind=self.db)()
        session.delete(m)
        session.commit()
        return True

    def get_summary(self, kwargs=None):
        f = self.to_filter(kwargs)

        conditions = "WHERE 1=1 and "

        if f["startedAt"]:
            conditions += "startedAt>={0} AND ".format(
                f["startedAt"])
        if f["endedAt"]:
            conditions += "endedAt<={0} AND ".format(f["endedAt"])
        if f["elapsed"]:
            conditions += "elapsed>={0} AND".format(f["elapsed"])

        conditions = conditions.rstrip(" AND")

        sql = """SELECT
                method, name,
                count(id) as count,
                min(elapsed) as minElapsed,
                max(elapsed) as maxElapsed,
                avg(elapsed) as avgElapsed
            FROM flask_profiling_measurements {conditions}
            group by method, name
            order by {sort_field} {sort_direction}
            """.format(
                conditions=conditions,
                sort_field=f["sort"][0],
                sort_direction=f["sort"][1]
                )
        rows = self.session.execute(sql)
        return [
            {
                "method": r[0],
                "name": r[1],
                "count": r[2],
                "minElapsed": r[3],
                "maxElapsed": r[4],
                "avgElapsed": r[5]
            } for r in rows
        ]

    def get_timeseries(self, kwargs=None):
        f = self.to_filter(kwargs)

        if kwargs.get("interval") == "daily":
            interval, date_format = 3600 * 24, "%Y-%m-%d"
        else:
            interval, date_format = 3600, "%Y-%m-%d %H"

        end, start = f["endedAt"], f["startedAt"]
        conditions = "where endedAt<={0} AND startedAt>={1} ".format(
            end, start)

        sql = """SELECT
                startedAt, count(id) as count
            FROM flask_profiling_measurements {conditions}
            group by DATE_FORMAT(from_unixtime(startedAt), "{date_format}")
            order by startedAt asc
            """.format(
                date_format=date_format,
                conditions=conditions
                )
        rows = self.session.execute(sql)

        series = {}
        for i in range(int(start), int(end) + 1, interval):
            series[self.to_datetime(i, date_format)] = 0

        for row in rows:
            series[self.to_datetime(row[0], date_format)] = row[1]
        return series

    def get_method_distribution(self, kwargs=None):
        f = self.to_filter(kwargs)

        end, start = f["endedAt"], f["startedAt"]
        conditions = "where endedAt<={0} AND startedAt>={1} ".format(
            end, start)

        sql = """SELECT
                method, count(id) as count
            FROM flask_profiling_measurements {conditions}
            group by method
            """.format(conditions=conditions)

        rows = self.session.execute(sql)
        return {
            row[0]: row[1]
            for row in rows
        }
