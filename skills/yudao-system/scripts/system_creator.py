"""CLI for read-only queries and explicitly applied missing master data."""

import argparse
import getpass
import json
import os
from pathlib import Path
import sys

from system_utils import ApplyError, RESOURCES, SystemAPIError, SystemClient, process_config


OUTPUT_FIELDS = {"id", "name", "code", "username", "nickname", "deptId", "postIds", "parentId",
                 "type", "status", "sort", "dictType", "label", "value", "permission", "path",
                 "component", "componentName", "icon", "visible", "keepAlive", "alwaysShow"}


def public_records(rows):
    return [{key: value for key, value in row.items() if key in OUTPUT_FIELDS} for row in rows]


def main(argv=None):
    parser = argparse.ArgumentParser(description="查询系统主数据；配置默认只预查，--apply 执行已授权创建。", allow_abbrev=False)
    parser.add_argument("--api-base", default=os.environ.get("YUDAO_API_BASE"), help="包含 admin-api 前缀的目标地址，或 YUDAO_API_BASE")
    tenant = parser.add_mutually_exclusive_group()
    tenant.add_argument("--tenant-id", help="任务指定租户，或 YUDAO_TENANT_ID")
    tenant.add_argument("--without-tenant", action="store_true", help="仅用于任务已核实关闭多租户的环境")
    parser.add_argument("--visit-tenant-id", default=os.environ.get("YUDAO_VISIT_TENANT_ID"))
    parser.add_argument("--prompt-token", action="store_true", help="通过受保护终端输入令牌；默认读取 YUDAO_TOKEN")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--action", choices=["query-" + key for key in RESOURCES])
    mode.add_argument("--config", type=Path, help="JSON 主数据配置，不含凭证")
    parser.add_argument("--keyword")
    parser.add_argument("--type", dest="dict_type", help="query-dict-data 的字典类型")
    parser.add_argument("--apply", action="store_true", help="执行当前任务已具体授权的创建操作")
    parser.add_argument("--output", type=Path, help="将结果另存为新 JSON 文件；拒绝覆盖")
    argv = list(sys.argv[1:] if argv is None else argv)
    if any(value.partition("=")[0] in ("--token", "--password") for value in argv):
        parser.error("Credential arguments are not accepted; use YUDAO_TOKEN or protected token input")
    args = parser.parse_args(argv)
    if args.apply and not args.config:
        parser.error("--apply requires --config")
    if args.action == "query-dict-data" and not args.dict_type:
        parser.error("query-dict-data requires --type")
    if not args.api_base:
        parser.error("Provide --api-base or YUDAO_API_BASE")
    tenant_id = args.tenant_id or os.environ.get("YUDAO_TENANT_ID")
    if args.without_tenant:
        if args.visit_tenant_id:
            parser.error("--without-tenant cannot be combined with visit-tenant-id")
        tenant_id = None
    elif tenant_id is None:
        parser.error("Provide tenant context or explicitly select --without-tenant")
    if args.output and (args.output.exists() or not args.output.parent.is_dir()):
        parser.error("--output must be a new file in an existing directory")
    try:
        if args.prompt_token and not sys.stdin.isatty():
            raise ValueError("Protected token entry requires an interactive terminal; use YUDAO_TOKEN otherwise")
        token = getpass.getpass("Bearer token: ") if args.prompt_token else os.environ.get("YUDAO_TOKEN", "")
        client = SystemClient(args.api_base, token, tenant_id=tenant_id, visit_tenant_id=args.visit_tenant_id)
        if args.config:
            config = json.loads(args.config.read_text(encoding="utf-8-sig"))
            result = process_config(client, config, apply=args.apply)
            result["lookups"] = {key: public_records(rows) for key, rows in result["lookups"].items()}
        else:
            result = public_records(client.query(args.action.removeprefix("query-"), keyword=args.keyword, dict_type=args.dict_type))
        output = json.dumps(result, ensure_ascii=False, indent=2)
        print(output)
        if args.output:
            with args.output.open("x", encoding="utf-8") as handle:
                handle.write(output + "\n")
        return 0
    except ApplyError as exc:
        print(json.dumps({"error": str(exc), "completed": exc.completed,
                          "uncertainOperation": exc.failed_operation}, ensure_ascii=False), file=sys.stderr)
    except (SystemAPIError, ValueError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
    except OSError:
        print('{"error": "Local file or protected input unavailable; inspect any result already printed before retrying"}', file=sys.stderr)
    return 1


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    raise SystemExit(main())
