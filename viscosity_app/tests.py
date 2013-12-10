import unittest

from . import vpn


class ViscosityTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test(self):
        self.assertTrue(isinstance(vpn.get_active_connection_names(), list))
        self.assertTrue(isinstance(vpn.get_all_connection_names(), list))
        print(vpn.get_all_connection_names())
