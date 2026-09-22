"""Search, validate and render the recorded Yudao documentation index; no network access."""

import argparse
import json
from pathlib import Path
import sys
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "references/docs-index.json"
STATUS = {
    "read-prior-turn": "正文已读（此前核验）",
    "restricted-prior-turn": "此前访问受限",
    "not-read": "正文未读",
}


def pages(data):
    for group in data["groups"]:
        for page in group["pages"]:
            yield {"group": group["title"], **page}


def check(data, source_root):
    errors = []
    seen = set()
    for page in pages(data):
        if page["id"] in seen:
            errors.append(f"Duplicate page id: {page['id']}")
        seen.add(page["id"])
        if not (ROOT / "skills" / page["skill"] / "SKILL.md").is_file():
            errors.append(f"Missing skill: {page['skill']}")
        if page["url"] and (urlsplit(page["url"]).hostname != "doc.iocoder.cn"
                            or urlsplit(page["url"]).scheme != "https"):
            errors.append(f"Unexpected URL: {page['id']}")
        if page["body_status"] not in STATUS:
            errors.append(f"Unknown status: {page['id']}")
        if page["body_status"] != "not-read" and not page["url"]:
            errors.append(f"Read status without URL: {page['id']}")
    for row in [*pages(data), *data.get("additional_source_links", [])]:
        for ref in row["source_refs"]:
            relative = Path(ref["path"])
            if relative.is_absolute() or ".." in relative.parts or ":" in ref["path"]:
                errors.append(f"Source path must be relative: {ref['path']}")
            elif source_root:
                path = source_root / relative
                if not path.is_file():
                    errors.append(f"Missing source: {ref['path']}")
                elif ref["line"] < 1 or ref["line"] > len(path.read_text(encoding="utf-8").splitlines()):
                    errors.append(f"Invalid source line: {ref['path']}:{ref['line']}")
    return errors


def render(data):
    rows = list(pages(data))
    known = sum(bool(row["url"]) for row in rows)
    body_read = sum(row["body_status"] == "read-prior-turn" for row in rows)
    restricted = sum(row["body_status"] == "restricted-prior-turn" for row in rows)
    lines = ["# 芋道文档导航索引", "",
             "由 `scripts/docs_index.py render` 根据 [docs-index.json](docs-index.json) 生成。", "",
             f"收录 {len(data['groups'])} 个分组、{len(rows)} 个目录项：{known} 项有已知 URL，"
             f"{len(rows) - known} 项的具体 URL 待定位；{body_read} 页正文此前已读，{restricted} 页此前访问受限。", "",
             f"导航来源：{data['navigation_source']}。观察日期：{data['navigation_observed_at']}。", "",
             f"本轮刷新状态：{data['current_browser_refresh']['status']}。{data['current_browser_refresh']['note']}", "",
             "标题收录不等于正文已读；源码提供的链接也不等于网页可访问。根据任务先读对应技能，再通过允许的浏览器核对需要的页面。", "",
             "快速查找：`python scripts/docs_index.py search 租户 --json`；"
             "按技能筛选：`python scripts/docs_index.py search --skill yudao-codegen`。", "",
             "## 分组概览", "", "| 分组 | 项数 | 已知 URL |", "| --- | ---: | ---: |"]
    for group in data["groups"]:
        lines.append(f"| {group['title']} | {len(group['pages'])} | {sum(bool(p['url']) for p in group['pages'])} |")
    for group in data["groups"]:
        lines.extend(["", f"## {group['title']}", "", "| 文档 | 任务技能 | 阅读状态 |", "| --- | --- | --- |"])
        for page in group["pages"]:
            title = f"[{page['title']}]({page['url']})" if page["url"] else f"{page['title']}（URL 待定位）"
            skill = f"[{page['skill']}](../skills/{page['skill']}/SKILL.md)"
            lines.append(f"| {title} | {skill} | {STATUS[page['body_status']]} |")
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    search = sub.add_parser("search", help="Search titles, categories and URLs")
    search.add_argument("query", nargs="?", default="")
    search.add_argument("--skill")
    search.add_argument("--limit", type=int, default=20)
    search.add_argument("--json", action="store_true")
    validate = sub.add_parser("check", help="Check structure, skill targets and optional source paths")
    validate.add_argument("--source-root", type=Path)
    sub.add_parser("render", help="Regenerate references/docs-index.md")
    args = parser.parse_args()
    data = json.loads(INDEX.read_text(encoding="utf-8"))
    if args.command == "check":
        errors = check(data, args.source_root)
        print(json.dumps({"pages": len(list(pages(data))), "errors": errors}, ensure_ascii=False, indent=2))
        return int(bool(errors))
    if args.command == "render":
        output = ROOT / "references/docs-index.md"
        output.write_text(render(data), encoding="utf-8")
        print("Rendered references/docs-index.md")
        return 0
    query = args.query.casefold().split()
    found = [p for p in pages(data)
             if (not args.skill or p["skill"] == args.skill)
             and all(term in (p["title"] + " " + p["group"] + " " + (p["url"] or "")).casefold() for term in query)]
    if args.json:
        print(json.dumps({"total": len(found), "results": found[:max(args.limit, 0)]}, ensure_ascii=False, indent=2))
    else:
        print(f"Matches: {len(found)}")
        for row in found[:max(args.limit, 0)]:
            print(f"{row['group']} / {row['title']} -> {row['skill']} | {row['url'] or 'URL unresolved'} | {STATUS[row['body_status']]}")
    return 0


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    sys.exit(main())
