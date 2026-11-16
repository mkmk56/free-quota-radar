#!/usr/bin/env python3
"""拉取能机器拉取的三个源，存到 sources/（该目录已进 .gitignore，不入库）。

- 懒猫：https://lanmao.ai/zh/offers.md
- 赛博鸡蛋：https://jidan.si/c/credit
- 白嫖计：https://baipiaoji.com/limits.json

AIHot（https://aihot.news/free-tokens）会屏蔽非浏览器访问，
不要用 curl 硬拉——那份数据经浏览器读取、人工复核后才进 data.json。
本脚本不伪装全自动，拉不到的源会直接报错退出，不写空文件。
"""
import sys
import urllib.request
from pathlib import Path

SOURCES = {
    "lanmao-offers.md": "https://lanmao.ai/zh/offers.md",
    "jidan-credit.html": "https://jidan.si/c/credit",
    "baipiaoji-limits.json": "https://baipiaoji.com/limits.json",
}


def main() -> int:
    out_dir = Path(__file__).resolve().parent.parent / "sources"
    out_dir.mkdir(exist_ok=True)
    for name, url in SOURCES.items():
        req = urllib.request.Request(url, headers={"User-Agent": "free-quota-radar/1.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read()
        if len(body) < 100:
            print(f"内容过短，拒绝写入：{name}（{len(body)} 字节）", file=sys.stderr)
            return 1
        (out_dir / name).write_bytes(body)
        print(f"{name}: {len(body)} 字节 <- {url}")
    print("注意：AIHot 需经浏览器读取，本脚本不拉取，见 README。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
