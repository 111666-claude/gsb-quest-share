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

    def test_member_limit_rejects_extra_contributor(self):
        world = Shared(2, 1000)
        world.share("p1", "q1", 100, 0)
        self.assertTrue(world.contribute("p2", "q1", 1, 0, "r1"))
        self.assertFalse(world.contribute("p3", "q1", 1, 0, "r2"))
        self.assertEqual(world.tasks["q1"]["count"], 1)

    def test_existing_member_can_contribute_again_at_limit(self):
        world = Shared(1, 1000)
        world.share("p1", "q1", 100, 0)
        self.assertTrue(world.contribute("p1", "q1", 1, 0, "r1"))
        self.assertTrue(world.contribute("p1", "q1", 1, 5, "r2"))
        self.assertFalse(world.contribute("p2", "q1", 1, 5, "r3"))

    def test_duplicate_req_id_is_idempotent(self):
        world = Shared(4, 1000)
        world.share("p1", "q1", 10, 0)
        self.assertTrue(world.contribute("p2", "q1", 5, 0, "same"))
        self.assertFalse(world.contribute("p2", "q1", 5, 1, "same"))
        self.assertEqual(world.tasks["q1"]["count"], 5)
        self.assertEqual(len(world.tasks["q1"]["members"]), 2)

    def test_progress_capped_at_target(self):
        world = Shared(4, 1000)
        world.share("p1", "q1", 10, 0)
        self.assertTrue(world.contribute("p2", "q1", 15, 0, "r1"))
        self.assertEqual(world.tasks["q1"]["count"], 10)
        self.assertTrue(world.done("q1", 0))
        self.assertTrue(world.contribute("p2", "q1", 5, 1, "r2"))
        self.assertEqual(world.tasks["q1"]["count"], 10)

    def test_expired_task_rejects_contribution_and_done(self):
        world = Shared(4, 100)
        world.share("p1", "q1", 10, 0)
        world.contribute("p2", "q1", 10, 0, "r1")
        self.assertTrue(world.done("q1", 99))
        self.assertFalse(world.done("q1", 100))
        self.assertFalse(world.contribute("p2", "q1", 1, 100, "r2"))
        self.assertNotIn("q1", world.tasks)

    def test_done_scan_cost_is_constant_per_query(self):
        world = Shared(100000, 100000)
        for index in range(3000):
            world.share("p1", "q-%d" % index, 100, 0)
        for index in range(3000):
            world.done("q-2999", 0)
        self.assertLessEqual(world.scanned_count(), 6000)


if __name__ == "__main__":
    unittest.main()
