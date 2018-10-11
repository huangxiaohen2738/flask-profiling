# -*- coding: utf8 -*-
import unittest
from flask import Flask
from flask_profiling import Profile
from flask_profiling.decorators import measure  # NOQA


class BasetTest(unittest.TestCase):

    def create_app(self):
        app = Flask(__name__)
        app.config["flask_profiling"] = {
            "db_url": "mysql+pymysql://root:root@192.168.3.172/testd?charset=utf8mb4"
        }
        profile = Profile()

        @app.route("/api/people/<firstname>")
        def sayHello(firstname):
            return firstname

        @app.route("/static/photo/")
        def getStaticPhoto():
            return "your static photo"

        @app.route("/static/")
        def getStatic():
            return "your static"

        @app.route("/api/static/")
        def getApiStatic():
            return "your api static"

        @app.route("/api/settings/system/secret/")
        def getSystemSettingsSecret():
            return "your system settings secret"

        @app.route("/api/settings/personal/secret/")
        def getPersonalSettingsSecret():
            return "your personal settings secret"

        @app.route("/api/settings/personal/name/")
        def getPersonalSettingsName():
            return "your personal settings name"

        profile.init_app(app)

        @app.route("/api/without/profiler")
        def withoutProfiler():
            return "without profiler"
        return app
