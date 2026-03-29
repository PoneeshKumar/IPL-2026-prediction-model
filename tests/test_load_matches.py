import unittest

from ipl_pred.load_matches import load_matches


class TestLoadMatches(unittest.TestCase):
    def test_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            load_matches("nonexistent.csv")
