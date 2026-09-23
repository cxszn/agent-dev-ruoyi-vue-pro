"""执行七方言和 PostgreSQL 版本矩阵的文件验收，不连接数据库。"""

import argparse
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
TARGETS = ("postgres", "oracle", "sqlserver", "dm8", "kingbase", "opengauss", "highgo")
PG_VERSIONS = ("9.4", "9.5", "9.6") + tuple(str(version) for version in range(10, 19))


def main():
    """在新目录生成版本矩阵，按需使用 PostgreSQL 16 解析器检查对应产物。"""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True, help="A new directory for test artifacts")
    parser.add_argument("--with-project-source", action="store_true", help="Also convert the project's MySQL initialization file locally")
    parser.add_argument("--pg-versions", nargs="+", choices=PG_VERSIONS, default=PG_VERSIONS)
    parser.add_argument("--pg16-syntax-check", action="store_true", help="Require a pglast parser based on PostgreSQL 16")
    args = parser.parse_args()
    pg_parser = None
    if args.pg16_syntax_check:
        import pglast
        if pglast.get_postgresql_version()[0] != 16:
            parser.error("PG16 syntax checks require the PostgreSQL 16 parser, e.g. pglast==6.16")
        pg_parser = pglast
    project = args.project_root.resolve()
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=False)
    cases = [("sample", ROOT / "tests/fixtures/mysql_conversion.sql")]
    if args.with_project_source:
        cases.append(("project", project / "sql/mysql/ruoyi-vue-pro.sql"))
    results = []
    targets = [(target, None, None) for target in TARGETS if target != "postgres"]
    targets += [("postgres", version, "auto") for version in args.pg_versions]
    if "16" in args.pg_versions:
        targets.append(("postgres", "16", "sequence"))
    for case, source in cases:
        for target, version, strategy in targets:
            suffix = f"postgres{version}.{strategy}" if version else target
            output = output_dir / f"{case}.{suffix}.sql"
            command = [
                sys.executable, str(ROOT / "scripts/convert_sql.py"),
                "--project-root", str(project), "--target", target,
                "--source", str(source), "--output", str(output),
            ]
            if version:
                command += ["--target-version", version, "--pg-id-strategy", strategy]
            process = subprocess.run(command, capture_output=True)
            report_path = output.with_suffix(".sql.report.json")
            report = json.loads(report_path.read_text(encoding="utf-8")) if report_path.exists() else {"status": "failed", "errors": ["No conversion report"]}
            passed = process.returncode == 0 and report["status"] == "generated_only"
            sql = output.read_text(encoding="utf-8") if passed else ""
            if case == "sample" and passed:
                passed = (report["tables"] == ["sample_record"] and report["source_insert_statements"] == 2
                          and report["quartz_tables_skipped"] == ["qrtz_demo"]
                          and "中文样例" in sql)
                if target not in {"sqlserver", "dm8"}:
                    passed = passed and report["sequence_adjustments"] == [{"table": "sample_record", "from": 3, "to": 21}]
            if version and passed:
                expected_strategy = "sequence" if strategy == "sequence" or version.startswith("9.") else "identity"
                bindings = report["postgres_adaptations"]["id_bindings"]
                passed = (report["target_version"] == version
                          and report["postgres_id_strategy"] == expected_strategy
                          and all(binding["strategy"] == expected_strategy for binding in bindings))
                if case == "sample":
                    passed = passed and len(bindings) == 1 and bindings[0]["start"] == 21
            syntax = "not_run"
            syntax_error = None
            if pg_parser and version == "16" and passed:
                try:
                    parsed = pg_parser.parse_sql(sql)
                    passed = bool(parsed)
                    syntax = "postgres16_parser_passed" if passed else "failed"
                except pg_parser.Error as error:
                    passed, syntax, syntax_error = False, "failed", str(error)
            result = {"case": case, "target": target, "target_version": version, "id_strategy": strategy,
                      "passed": passed, "status": report["status"],
                      "tables": len(report.get("tables", [])), "inserts": report.get("source_insert_statements"),
                      "errors": report.get("errors", []) + ([syntax_error] if syntax_error else []),
                      "syntax_validation": syntax, "database_validation": "not_run"}
            results.append(result)
            print(json.dumps(result, ensure_ascii=False), flush=True)
    (output_dir / "acceptance.json").write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0 if all(row["passed"] for row in results) else 1


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    sys.exit(main())
