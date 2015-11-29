import unittest

import snotel_tools

class TestSnotel(unittest.TestCase):
    def setUp(self):
        pass

    def test_scrape(self):
        results = snotel_tools.scrape_snotel_sites()
        self.assertEquals("1267:AK:SNTL", snotel_tools.build_id(results[0]))

    def tearDown(self):
        pass