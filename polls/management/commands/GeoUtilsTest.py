from django.test import TestCase
from GeoUtils import GeoUtils

class TestGeoUtils(TestCase):

    def test1(self):
        polygon1 = [(0, 0), (10, 0), (10, 10), (0, 10)]
        p = (20, 20)
        self.assertFalse(GeoUtils().isInside(polygon1, p))

        p = (5, 5)
        self.assertTrue(GeoUtils().isInside(polygon1, p))


    def test2(self):
        polygon2 = [(0, 0), (5, 5), (5, 0)]
        p = (3, 3)
        self.assertTrue(GeoUtils().isInside(polygon2, p))

        p = (5, 1)
        self.assertTrue(GeoUtils().isInside(polygon2, p))

        p = (8, 1)
        self.assertFalse(GeoUtils().isInside(polygon2, p))


    def test3(self):
        polygon3 = [(0, 0), (10, 0), (10, 10), (0, 10)]
        p = (-1,10);
        self.assertFalse(GeoUtils().isInside(polygon3, p))


    # Test with real lat lons
    def test4(self):
        polygon4 = [(-121.7, 28.5), (-121.5, 28.2), (-121.5, 28.7), (-121.2, 28.5)]
        p = (-121.4, 28.6)
        self.assertTrue(GeoUtils().isInside(polygon4, p))

        p = (-121.2, 28.2)
        self.assertFalse(GeoUtils().isInside(polygon4, p))

    def testDistance1(self):
        # Expected value using http://boulter.com/gps/distance/
        polygon = [(0.0,0.0), (0.0,4.0), (4.0,0.0), (4.0,4.0)]
        p1 = GeoUtils().getCentroid(polygon)
        p2 = (2.0, 10.0)
        self.assertAlmostEqual(GeoUtils().distance(p1, p2), 890, delta=1.0)

        polygon = [(-121.7, 28.5), (-121.5, 28.2), (-121.5, 28.7), (-121.2, 28.5)]
        p1 = GeoUtils().getCentroid(polygon)
        p2 = (-121.4, 28.6)
        self.assertAlmostEqual(GeoUtils().distance(p1, p2), 11, delta=1.0)

        p2 = (-121.2, 28.2)
        self.assertAlmostEqual(GeoUtils().distance(p1, p2), 34, delta=1.0)


if __name__ == '__main__':
    unittest.main()