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


class MemberLimitTest(unittest.TestCase):
    def test_third_member_rejected(self):
        world = Shared(2, 1000)
        world.share("p1", "q1", 100, 0)
        self.assertTrue(world.contribute("p2", "q1", 1, 0, "r1"))
        self.assertFalse(world.contribute("p3", "q1", 1, 0, "r2"))

    def test_existing_member_not_blocked_by_limit(self):
        world = Shared(2, 1000)
        world.share("p1", "q1", 100, 0)
        world.contribute("p2", "q1", 1, 0, "r1")
        self.assertTrue(world.contribute("p2", "q1", 1, 0, "r2"))

    def test_rejected_contribution_adds_no_progress(self):
        world = Shared(2, 1000)
        world.share("p1", "q1", 100, 0)
        world.contribute("p2", "q1", 1, 0, "r1")
        world.contribute("p3", "q1", 5, 0, "r2")
        self.assertEqual(world.tasks["q1"]["count"], 1)


class IdempotencyTest(unittest.TestCase):
    def test_same_req_id_applies_once(self):
        world = Shared(4, 1000)
        world.share("p1", "q1", 10, 0)
        self.assertTrue(world.contribute("p2", "q1", 5, 0, "same"))
        self.assertFalse(world.contribute("p2", "q1", 5, 0, "same"))
        self.assertEqual(world.tasks["q1"]["count"], 5)

    def test_repeat_result_is_stable(self):
        world = Shared(4, 1000)
        world.share("p1", "q1", 10, 0)
        world.contribute("p2", "q1", 5, 0, "same")
        first = world.contribute("p2", "q1", 5, 0, "same")
        second = world.contribute("p2", "q1", 5, 0, "same")
        self.assertEqual(first, second)


class CapTest(unittest.TestCase):
    def test_progress_capped_at_target(self):
        world = Shared(4, 1000)
        world.share("p1", "q1", 10, 0)
        world.contribute("p2", "q1", 15, 0, "r1")
        self.assertEqual(world.tasks["q1"]["count"], 10)

    def test_progress_monotonic_and_done_consistent(self):
        world = Shared(4, 1000)
        world.share("p1", "q1", 10, 0)
        world.contribute("p2", "q1", 4, 0, "r1")
        self.assertFalse(world.done("q1", 0))
        world.contribute("p2", "q1", 6, 0, "r2")
        self.assertEqual(world.tasks["q1"]["count"], 10)
        self.assertTrue(world.done("q1", 0))
        world.contribute("p2", "q1", 3, 0, "r3")
        self.assertEqual(world.tasks["q1"]["count"], 10)


class ExpiryTest(unittest.TestCase):
    def test_expired_task_rejects_contribution(self):
        world = Shared(4, 1000)
        world.share("p1", "q1", 10, 0)
        self.assertFalse(world.contribute("p2", "q1", 5, 1000, "r1"))

    def test_expired_task_not_done(self):
        world = Shared(4, 1000)
        world.share("p1", "q1", 10, 0)
        world.contribute("p2", "q1", 10, 0, "r1")
        self.assertTrue(world.done("q1", 999))
        self.assertFalse(world.done("q1", 1000))

    def test_alive_task_still_works(self):
        world = Shared(4, 1000)
        world.share("p1", "q1", 10, 0)
        self.assertTrue(world.contribute("p2", "q1", 5, 999, "r1"))


class ScanCostTest(unittest.TestCase):
    def test_scanned_not_linear_in_task_count(self):
        world = Shared(100000, 100000)
        for index in range(3000):
            world.share("p1", "q-%d" % index, 100, 0)
        for _ in range(3000):
            world.done("q-2999", 0)
        self.assertLessEqual(world.scanned_count(), 6000)


if __name__ == "__main__":
    unittest.main()
