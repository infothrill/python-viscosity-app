import unittest

import viscosity_app


class TestViscosityApp(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test(self):
        self.assertTrue(isinstance(viscosity_app.get_active_connection_names(), list))
        self.assertTrue(isinstance(viscosity_app.get_all_connection_names(), list))
        print(viscosity_app.get_all_connection_names())
