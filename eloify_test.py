import unittest
import eloify

class TestGetExpectedScore(unittest.TestCase):
  
  def test_zero(self):
    self.assertEqual(eloify.get_expected_score(0), 0.5)

  def test_max(self):
    self.assertAlmostEqual(eloify.get_expected_score(10000), 0)

  def test_min(self):
    self.assertAlmostEqual(eloify.get_expected_score(-10000), 1)

  def test_symmetry(self):
    self.assertAlmostEqual(eloify.get_expected_score(100), 0.35993500)
    self.assertAlmostEqual(eloify.get_expected_score(-100), 1-0.35993500)
    for i in range(100):
      self.assertAlmostEqual(eloify.get_expected_score(i), 1-eloify.get_expected_score(-i))

class TestGetRatingUpdate(unittest.TestCase):
  
  def test_zero(self):
    self.assertEqual(eloify.get_rating_update(0, 1), 10)
    self.assertEqual(eloify.get_rating_update(0, 0.5), 0)
    self.assertEqual(eloify.get_rating_update(0, 0), -10)

  def test_max(self):
    self.assertAlmostEqual(eloify.get_rating_update(10000, 1), 20)
    self.assertAlmostEqual(eloify.get_rating_update(10000, 0.5), 10)
    self.assertAlmostEqual(eloify.get_rating_update(10000, 0), 0)

  def test_min(self):
    self.assertAlmostEqual(eloify.get_rating_update(-10000, 1), 0)
    self.assertAlmostEqual(eloify.get_rating_update(-10000, 0.5), -10)
    self.assertAlmostEqual(eloify.get_rating_update(-10000, 0), -20)

  def test_symmetry(self):
    self.assertAlmostEqual(eloify.get_rating_update(100, 1), 12.801299996057702)
    self.assertAlmostEqual(eloify.get_rating_update(-100, 0), -12.801299996057702)
    self.assertAlmostEqual(eloify.get_rating_update(-100, 1), 20-12.801299996057702)
    for i in range(-100, 100):
      self.assertAlmostEqual(eloify.get_rating_update(i, 1), 20-eloify.get_rating_update(-i, 1))
      self.assertAlmostEqual(eloify.get_rating_update(i, 1), -eloify.get_rating_update(-i, 0))

class TestParseCsv(unittest.TestCase):

  def test_singles(self):
    self.assertEqual(next(eloify.parse_csv(['1,a,b,2-2'])), ('a', 'b', 0.5))
    self.assertEqual(next(eloify.parse_csv(['2020-10-30, team1, team 2, 3-1'])), ('team1', 'team 2', 1))
    self.assertEqual(next(eloify.parse_csv(['11564, Magnus Carlsen, Roger Federer, 0-5'])), ('Magnus Carlsen', 'Roger Federer', 0))

  def test_multi(self):
    inp = ['1,a,b,2-2', '2020-10-30, team1, team 2, 3-1', '11564, Magnus Carlsen, Roger Federer, 0-5']
    want = [ ('a', 'b', 0.5), ('team1', 'team 2', 1), ('Magnus Carlsen', 'Roger Federer', 0)]
    self.assertEqual(list(eloify.parse_csv(inp)), want)

  def test_file(self):
    want = [
      ('team 1', 'team 2', 0),
      ('team 1', 'team 3', 0),
      ('team 2', 'team 3', 0.5),
      ('team 3', 'team 1', 0.5),
      ('team 2', 'team 1', 1),
    ]
    self.assertEqual(list(eloify.parse_csv(open('testdata/matches.csv'))), want)

class TestParseCsv(unittest.TestCase):

  def setUp(self):
    eloify.args.input_csv = 'testdata/matches.csv'

  def test_singles(self):
    ratings = eloify.main()
    self.assertEqual(ratings, None)

if __name__ == '__main__':
    unittest.main()