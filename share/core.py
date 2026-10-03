"""任务共享：参与人数上限、贡献幂等、进度封顶与过期失效。

缺陷：参与人数上限不生效、同一请求重复贡献、进度不封顶、
过期任务继续生效、每次查询扫描全部共享任务。
"""


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

    def contribute(self, member, quest, amount, now_ms, req_id):
        self.scanned += len(self.tasks)
        task = self.tasks.get(quest)
        if task is None:
            return False
        self.memo.add(req_id)
        task["members"].add(member)
        task["count"] += amount
        return True

    def done(self, quest, now_ms):
        self.scanned += len(self.tasks)
        task = self.tasks.get(quest)
        return task is not None and task["count"] >= task["target"]

    def scanned_count(self):
        return self.scanned
