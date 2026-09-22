"""Run the real project converter against all seven target dialects; no database connections."""

import argparse
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
TARGETS = ("postgres", "oracle", "sqlserver", "dm8", "kingbase", "opengauss", "highgo")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True, help="A new directory for test artifacts")
    parser.add_argument("--with-project-source", action="store_true", help="Also convert the project's MySQL initialization file locally")
    args = parser.parse_args()
    project = args.project_root.resolve()
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=False)
    cases = [("sample", ROOT / "tests/fixtures/mysql_conversion.sql")]
    if args.with_project_source:
        cases.append(("project", project / "sql/mysql/ruoyi-vue-pro.sql"))
    results = []
    for case, source in cases:
        for target in TARGETS:
            output = output_dir / f"{case}.{target}.sql"
            process = subprocess.run([
                sys.executable, str(ROOT / "scripts/convert_sql.py"),
                "--project-root", str(project), "--target", target,
                "--source", str(source), "--output", str(output),
            ], capture_output=True)
            report_path = output.with_suffix(".sql.report.json")
            report = json.loads(report_path.read_text(encoding="utf-8")) if report_path.exists() else {"status": "failed", "errors": ["No conversion report"]}
            passed = process.returncode == 0 and report["status"] == "generated_only"
            if case == "sample" and passed:
                passed = (report["tables"] == ["sample_record"] and report["source_insert_statements"] == 2
                          and report["quartz_tables_skipped"] == ["qrtz_demo"]
                          and "中文样例" in output.read_text(encoding="utf-8"))
                if target not in {"sqlserver", "dm8"}:
                    passed = passed and report["sequence_adjustments"] == [{"table": "sample_record", "from": 3, "to": 21}]
            result = {"case": case, "target": target, "passed": passed, "status": report["status"],
                      "tables": len(report.get("tables", [])), "inserts": report.get("source_insert_statements"),
                      "errors": report.get("errors", []), "database_validation": "not_run"}
            results.append(result)
            print(json.dumps(result, ensure_ascii=False), flush=True)
    (output_dir / "acceptance.json").write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0 if all(row["passed"] for row in results) else 1


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    sys.exit(main())
