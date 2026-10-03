# quest-share

任务共享：参与人数上限、贡献幂等、进度封顶与过期失效，只用 Python 标准库。

```
python3 -m share.cli --sample idem
python3 -m share.cli --sample cap
python3 -m share.cli --sample limit
python3 -m share.cli --sample scan
python3 -m unittest discover -s tests -v
```

## 口径（README 为准）

- **参与上限**：同一共享任务的参与者不超过 `max_members`，超出时 `contribute` 返回 false。
- **贡献幂等**：同一个 `req_id` 只生效一次，重复调用返回 false 且不加进度。
- **进度封顶**：进度最多等于目标值，超出部分丢弃。
- **过期**：共享任务存在时间达到 `ttl_ms` 后失效，既不能贡献也不再算完成。
- **不变量**：进度单调不减且不超过目标值；`done` 与进度一致；重复执行结果相同。
- **代价**：`done` 不许扫描全部共享任务，`scanned_count` 不随任务数线性增长。
- **规模**：10 万个共享任务、每秒 10 万次查询，单次摊还 O(1)。

## 输出契约（不改格式）

```
second=..
count=..
third=..
scanned=..
```

## 目录

```
share/core.py   上限、幂等、封顶与过期
share/cli.py    命令行入口
tests/          unittest 用例
```
