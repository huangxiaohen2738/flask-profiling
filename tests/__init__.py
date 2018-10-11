import unittest

import logging

import sys

from .test_measurement import MeasurementTest

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(MeasurementTest))
    return suite
