"""命令行入口：跑任务共享样例。"""

import argparse

from .core import Shared


def main(argv=None):
    parser = argparse.ArgumentParser(prog="quest-share", description="任务共享")
    parser.add_argument("--sample", default="idem", help="idem / cap / limit / scan")
    args = parser.parse_args(argv)
    if args.sample == "idem":
        world = Shared(max_members=4, ttl_ms=100000)
        world.share("p1", "q1", 10, 0)
        world.contribute("p2", "q1", 5, 0, "same")
        print("second=%s" % str(world.contribute("p2", "q1", 5, 0, "same")).lower())
    elif args.sample == "cap":
        world = Shared(max_members=4, ttl_ms=100000)
        world.share("p1", "q1", 10, 0)
        world.contribute("p2", "q1", 15, 0, "r1")
        print("count=%d" % world.tasks["q1"]["count"])
    elif args.sample == "limit":
        world = Shared(max_members=2, ttl_ms=100000)
        world.share("p1", "q1", 100, 0)
        world.contribute("p2", "q1", 1, 0, "r1")
        print("third=%s" % str(world.contribute("p3", "q1", 1, 0, "r2")).lower())
    elif args.sample == "scan":
        world = Shared(max_members=100000, ttl_ms=100000)
        for index in range(3000):
            world.share("p1", "q-%d" % index, 100, 0)
        for index in range(3000):
            world.done("q-2999", 0)
        print("scanned=%d" % world.scanned_count())
    else:
        raise SystemExit("需要 --sample idem|cap|limit|scan")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
