# 免费额度雷达 | Free Quota Radar

每天复核一次的 AI 免费额度清单。只收录核实过的、不需要绑信用卡的额度，过期就下架。

- 当前数据：`data/data.json`，62 条（核实日期 2026-11-16）
- 在线看：打开 `web/index.html`，或把 `web/` + `data/` 部署到任意静态托管（Cloudflare Pages / Vercel / GitHub Pages 都行）
- 今日可领总额（AIHot 口径，2026-11-16）：¥2427

## 数据长什么样

每条一个对象，12 项字段，缺了就标「待确认」，不猜：

| 字段 | 说明 |
| --- | --- |
| `id` | 唯一标识，如 `zcode-weekend-500m` |
| `title` / `desc` / `quota` | 名称、描述、额度 |
| `category` | `api` / `app` / `cloud` / `dev` / `compute` |
| `is_new` / `expiring` | 是否新上 / 是否在 16 天内到期 |
| `source` / `source_url` | 来源站及来源链接 |
| `verified` / `expires` | 最后核实日期 / 到期时间 |
| `claim_url` / `cost` / `risk` | 领取链接 / 成本说明 / 风险提示 |
| `scores` / `avg` | 7 项评分（每项 0–10）与平均分 |
| `region` / `valid_from` / `claim_steps` / `value` / `type` | 适用地区 / 起止时间 / 领取步骤 / 实际价值 / 类型 |

评分 7 项：额度大小、平台可信度、领取难度、实用性、适用面、稀缺性与紧迫性、风险提示。综合评分 = 7 项平均分，保留 1 位小数。

## 数据来源

只认这四个站 + 厂商官方页：

1. 懒猫 AI 全量清单 — https://lanmao.ai/zh/offers.md
2. AIHot Token 羊毛站 — https://aihot.news/free-tokens
3. 赛博鸡蛋福利列表 — https://jidan.si/c/credit
4. 白嫖计 — https://baipiaoji.com/limits.json

## 每天怎么刷新

1. 拉四个源的最新版，对照上一天的数据逐条核对。
2. 新增的写进去，下架过期的，限时项的倒计时减一天。
3. 跑 `python3 scripts/validate.py`，校验通过才提交。
4. AIHot 那个站会屏蔽非浏览器访问，所以它的数据要经浏览器读取，不能只靠 curl。`scripts/fetch_sources.py` 只拉能机器拉的三个源，AIHot 那部分是人工复核，不伪装成全自动。

历史快照在 `data/history/`，按日期存。

## 校验

```bash
python3 scripts/validate.py
# 输出：条数、分类统计、新上 / 即将过期条数、最高分条目
```

GitHub Actions 也会在每次 push / PR 时跑同一份校验（`.github/workflows/validate.yml`）。

## 收录规则

- 免费 = 不需要绑信用卡。需要绑卡、需要手机号验证的，单独标注，不混进免费档。
- 只收录能追溯到官方来源的条目，来源不明的不收。
- 额度、到期时间以官方页为准，四个源互相印证。
- 领之前以官网为准，额度变动很快。

## 许可

MIT，见 `LICENSE`。
