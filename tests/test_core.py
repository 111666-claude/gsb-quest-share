import unittest

from share.core import Shared


class BasicTest(unittest.TestCase):
    def test_unknown_quest_contribution(self):
        self.assertFalse(Shared(4, 1000).contribute("p1", "ghost", 1, 0, "r1"))

    def test_share_then_done_false(self):
        world = Shared(4, 1000)
        world.share("p1", "q1", 10, 0)
        self.assertFalse(world.done("q1", 0))

    def test_unknown_quest_not_done(self):
        self.assertFalse(Shared(4, 1000).done("ghost", 0))

    def test_scanned_starts_at_zero(self):
        self.assertEqual(Shared(4, 1000).scanned_count(), 0)


if __name__ == "__main__":
    unittest.main()
