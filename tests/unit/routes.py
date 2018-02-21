import opencrossfitapi
import unittest

class RouteTestCase(unittest.TestCase):
    def setUp(self):
        opencrossfitapi.app.testing = True
        self.app = opencrossfitapi.app.test_client()

    def test_affiliates_route(self):
        rv = self.app.get('/affiliates/Brazil/Bahia')
        assert b'affiliates in' in rv.data

if __name__ == '__main__':
    unittest.main()
