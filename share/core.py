"""任务共享：参与人数上限、贡献幂等、进度封顶与过期失效。"""


class Shared:
    def __init__(self, max_members, ttl_ms):
        self.max_members = max_members
        self.ttl_ms = ttl_ms
        self.tasks = {}
        self.scanned = 0

    def share(self, owner, quest, target, now_ms):
        self.tasks[quest] = {
            "target": target,
            "count": 0,
            "members": {owner},
            "seen": set(),
            "at": now_ms,
        }
        return True

    def _live(self, quest, now_ms):
        self.scanned += 1
        task = self.tasks.get(quest)
        if task is None:
            return None
        if now_ms - task["at"] >= self.ttl_ms:
            del self.tasks[quest]
            return None
        return task

    def contribute(self, member, quest, amount, now_ms, req_id):
        task = self._live(quest, now_ms)
        if task is None:
            return False
        if req_id in task["seen"]:
            return False
        if member not in task["members"] and len(task["members"]) >= self.max_members:
            return False
        task["seen"].add(req_id)
        task["members"].add(member)
        task["count"] = min(task["target"], task["count"] + amount)
        return True

    def done(self, quest, now_ms):
        task = self._live(quest, now_ms)
        return task is not None and task["count"] >= task["target"]

    def scanned_count(self):
        return self.scanned
