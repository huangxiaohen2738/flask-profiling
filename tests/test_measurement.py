# -*- coding: utf8 -*-
import time
import unittest
from flask_profiling.ext import backend
from .basetest import BasetTest, measure


def doWait(seconds, **kwargs):
    time.sleep(seconds)
    return seconds


class MeasurementTest(BasetTest):

    def setUp(self):
        app = self.create_app()
        self.app = app

    def test_01_returnValue(self):
        with self.app.app_context():
            wrapped = measure(doWait, "doWait", "call", context=None)
            waitSeconds = 1
            result = wrapped(waitSeconds)
            self.assertEqual(waitSeconds, result)

    def test_02_measurement(self):
        with self.app.app_context():
            wrapped = measure(doWait, "doWait", "call", context=None)
            waitSeconds = 2
            result = wrapped(waitSeconds)  # NOQA
            m = list(backend.filter())[0]
            self.assertEqual(m["name"], "doWait")
            self.assertEqual(float(m["elapsed"]) >= waitSeconds, True)

    def test_03_measurement_params(self):
        with self.app.app_context():
            context = {"token": "x"}
            name = "name_of_func"
            method = "invoke"
            wrapped = measure(doWait, name, method, context=context)

            waitSeconds = 1
            kwargs = {"k1": "kval1", "k2": "kval2"}
            result = wrapped(waitSeconds, **kwargs)  # NOQA
            m = list(backend.filter())[0]
            self.assertEqual(m["name"], name)
            self.assertEqual(m["method"], method)
            self.assertEqual(m["args"][0], waitSeconds)
            self.assertEqual(m["kwargs"], kwargs)
            self.assertEqual(m["context"], context)
            self.assertTrue(float(m["elapsed"]) >= waitSeconds)


if __name__ == '__main__':
    unittest.main()
