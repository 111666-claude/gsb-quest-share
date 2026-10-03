"""任务共享：参与人数上限、贡献幂等、进度封顶与过期失效。"""


class Shared:
    def __init__(self, max_members, ttl_ms):
        self.max_members = max_members
        self.ttl_ms = ttl_ms
        self.tasks = {}
        self.memo = set()
        self.scanned = 0

    def share(self, owner, quest, target, now_ms):
        self.tasks[quest] = {"target": target, "count": 0, "members": {owner}, "at": now_ms}
        return True

    def _expired(self, task, now_ms):
        return now_ms - task["at"] >= self.ttl_ms

    def contribute(self, member, quest, amount, now_ms, req_id):
        self.scanned += 1
        if req_id in self.memo:
            return False
        task = self.tasks.get(quest)
        if task is None:
            return False
        if self._expired(task, now_ms):
            return False
        if member not in task["members"] and len(task["members"]) >= self.max_members:
            return False
        self.memo.add(req_id)
        task["members"].add(member)
        task["count"] = min(task["target"], task["count"] + amount)
        return True

    def done(self, quest, now_ms):
        self.scanned += 1
        task = self.tasks.get(quest)
        if task is None or self._expired(task, now_ms):
            return False
        return task["count"] >= task["target"]

    def scanned_count(self):
        return self.scanned
