"""Generate and structurally check SQL with a project's sql/tools/convertor.py."""

import argparse
from collections import Counter
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import re
import subprocess
import sys


TARGETS = ("postgres", "oracle", "sqlserver", "dm8", "kingbase", "opengauss", "highgo")
ALIASES = {
    "postgresql": "postgres", "pg": "postgres", "甲骨文": "oracle",
    "mssql": "sqlserver", "sql server": "sqlserver", "sql-server": "sqlserver",
    "dm": "dm8", "达梦": "dm8", "达梦8": "dm8", "人大金仓": "kingbase",
    "金仓": "kingbase", "kingbasees": "kingbase", "open gauss": "opengauss",
    "华为opengauss": "opengauss", "瀚高": "highgo",
}
POSTGRES_TARGETS = {"postgres", "kingbase", "opengauss", "highgo"}
SEQUENCE_TARGETS = POSTGRES_TARGETS | {"oracle"}
DUAL_TARGETS = POSTGRES_TARGETS | {"sqlserver"}
KNOWN_CONVERTER = "985cbc60c37b5aa72955f51bfdc685782e9960a18f87a644597e155d7f7dd978"
CREATE = re.compile(r"\bCREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?`?([A-Za-z_][A-Za-z0-9_]*)`?\s*\(", re.I)
INSERT = re.compile(r"\bINSERT\s+INTO\s+`?([A-Za-z_][A-Za-z0-9_]*)`?", re.I)


def target_name(value):
    value = value.strip().casefold()
    return ALIASES.get(value, value)


def mask_sql(text, backslash_escapes=True):
    """Blank strings/comments while preserving identifiers, offsets and newlines."""
    masked = list(text)
    literals = []
    index = 0
    while index < len(text):
        start = index
        if text.startswith("/*", index):
            end = text.find("*/", index + 2)
            if end < 0:
                raise ValueError("Unterminated SQL comment")
            index = end + 2
        elif text[index] == "#" or (text.startswith("--", index)
                                    and (index + 2 == len(text) or text[index + 2].isspace())):
            end = text.find("\n", index)
            index = len(text) if end < 0 else end
        elif text[index] in "'\"":
            quote = text[index]
            index += 1
            while index < len(text):
                if text[index] == "\\" and backslash_escapes:
                    index += 2
                elif text[index] == quote:
                    if index + 1 < len(text) and text[index + 1] == quote:
                        index += 2
                    else:
                        index += 1
                        break
                else:
                    index += 1
            else:
                raise ValueError("Unterminated SQL string")
            literals.append((start, text[start:index]))
        elif text[index] == "`":
            end = text.find("`", index + 1)
            if end < 0:
                raise ValueError("Unterminated quoted identifier")
            index = end + 1
            continue
        else:
            index += 1
            continue
        masked[start:index] = ["\n" if char == "\n" else " " for char in text[start:index]]
    return "".join(masked), literals


def source_inventory(text, target):
    _, original_literals = mask_sql(text)
    if any("\n" in literal or literal.startswith('"') for _, literal in original_literals):
        raise ValueError("Multiline or double-quoted SQL strings need explicit normalization before conversion")
    # This is the single wrapped INSERT line form the upstream loader supports.
    text = text.replace(")\nVALUES ", ") VALUES ")
    masked, literals = mask_sql(text)
    errors = []
    ignored = 0
    for statement in masked.split(";"):
        statement = statement.strip()
        if not statement:
            continue
        if not re.match(r"(?:CREATE\s+TABLE|INSERT\s+INTO|DROP\s+TABLE|SET|USE|BEGIN|COMMIT)\b", statement, re.I):
            errors.append("Unsupported statement; only table DDL, standard INSERT and dump session statements are accepted")
        elif re.match(r"(?:DROP|SET|USE|BEGIN|COMMIT)\b", statement, re.I):
            ignored += 1
    if re.search(r"\b(?:FOREIGN\s+KEY|REFERENCES|GENERATED\s+ALWAYS|PARTITION\s+BY|FULLTEXT|SPATIAL)\b|\bCHECK\s*\(", masked, re.I):
        errors.append("Foreign keys, CHECK, generated columns, partitions and special indexes need a separate conversion")
    for comment in re.finditer(r"/\*!([\s\S]*?)\*/", text):
        inside_literal = any(offset <= comment.start() < offset + len(literal) for offset, literal in literals)
        if not inside_literal and re.search(r"\b(?:CREATE|ALTER|INSERT|UPDATE|DELETE)\b", comment.group(1), re.I):
            errors.append("Executable MySQL comments contain objects/data not handled by this converter")
    for offset, literal in literals:
        if re.search(r"ENGINE| CHARACTER SET \w+| COLLATE \w+|UNIQUE INDEX| KEY `|`[^`]+`\(\d+\)|USING\s+BTREE\s+COMMENT", literal):
            errors.append("A string/comment intersects upstream global cleanup rules; normalize a reviewed copy first")
        if re.search(r"\bCOMMENT\s*(?:=\s*)?$", text[max(0, offset - 32):offset], re.I):
            if "\\'" in literal or "''" in literal[1:-1]:
                errors.append("Escaped quotes in comments need explicit target-dialect handling")
    tables = {}
    skipped = []
    creates = list(CREATE.finditer(masked))
    if len(creates) != len(re.findall(r"\bCREATE\s+TABLE\b", masked, re.I)):
        errors.append("A CREATE TABLE name/form is unsupported; use simple unqualified ASCII identifiers")
    for match in creates:
        name = match.group(1).lower()
        end = masked.find(";", match.end())
        if end < 0:
            errors.append(f"Missing CREATE TABLE terminator: {name}")
            continue
        if name.startswith("qrtz"):
            skipped.append(name)
            continue
        if name in tables:
            errors.append(f"Duplicate CREATE TABLE: {name}")
        if not text[match.start():].startswith("CREATE TABLE "):
            errors.append(f"Use the converter's uppercase CREATE TABLE format: {name}")
        body = masked[match.end():end]
        parts = []
        depth, start = 0, 0
        for position, character in enumerate(body):
            if character == "(":
                depth += 1
            elif character == ")":
                depth -= 1
                if depth < 0:
                    parts.append(body[start:position])
                    break
            elif character == "," and depth == 0:
                parts.append(body[start:position])
                start = position + 1
        columns = []
        for part in parts:
            column = re.match(r"\s*`([A-Za-z_][A-Za-z0-9_]*)`\s+([\s\S]+)", part)
            if column:
                columns.append(column.group(1).lower())
                if re.search(r"\b(?:UNIQUE|PRIMARY\s+KEY)\b", column.group(2), re.I):
                    errors.append(f"Inline column constraints need explicit table-level definitions: {name}")
                if re.search(r"\bAS\s*\(|\b(?:VIRTUAL|STORED)\b", column.group(2), re.I):
                    errors.append(f"Generated columns need a separate conversion: {name}")
            elif not re.match(r"\s*(?:PRIMARY\s+KEY|UNIQUE|KEY|INDEX|CONSTRAINT)\b", part, re.I):
                errors.append(f"Unsupported column/table definition: {name}")
        if not columns:
            errors.append(f"Backtick-quoted column definitions are required: {name}")
        primary = re.search(r"\bPRIMARY\s+KEY\s*\(([^)]*)\)", body, re.I)
        keys = [key.strip().strip('`').lower() for key in primary.group(1).split(',')] if primary else []
        if ("id" in columns and keys != ["id"]) or ("id" not in columns and keys):
            errors.append(f"Primary key is outside the converter's id-only convention: {name}")
        tables[name] = {"columns": columns, "max_id": 0, "inserts": 0}
    if not tables:
        errors.append("No supported business CREATE TABLE statements found")
    if "dual" in tables and target in DUAL_TARGETS:
        errors.append("Source dual conflicts with the converter's automatically generated dual table")
    for match in INSERT.finditer(masked):
        name = match.group(1).lower()
        if name in skipped:
            continue
        start = masked.rfind("\n", 0, match.start()) + 1
        end = masked.find("\n", match.start())
        end = len(text) if end < 0 else end
        line, masked_line = text[start:end], masked[start:end]
        row = re.fullmatch(r"INSERT INTO `([^`]+)`(?:\s*\(([^)]*)\))? VALUES \((.*)\);\s*", line)
        if not row or masked_line.count(";") != 1 or re.search(r"\)\s*,\s*\(", masked_line):
            errors.append(f"INSERT must be one complete uppercase, unindented, single-row statement per line: {name}")
            continue
        values = masked_line[row.start(3):row.end(3)]
        boundaries = [-1] + [index for index, character in enumerate(values) if character == ","] + [len(values)]
        tokens = [row.group(3)[left + 1:right].strip() for left, right in zip(boundaries, boundaries[1:])]
        literal = re.compile(r"(?:NULL|[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?|b'[01]'|'(?:[^'\\]|\\.|'')*')", re.S)
        if any(not literal.fullmatch(token) for token in tokens):
            errors.append(f"INSERT values must be literal data; functions, expressions and trailing clauses need a separate conversion: {name}")
            continue
        if name not in tables:
            errors.append(f"INSERT references a table without converted DDL: {name}")
            continue
        table = tables[name]
        table["inserts"] += 1
        columns = ([column.strip().strip('`').lower() for column in row.group(2).split(',')]
                   if row.group(2) else table["columns"])
        if len(tokens) != len(columns) or any(column not in table["columns"] for column in columns):
            errors.append(f"INSERT column/value count or column names differ from the table: {name}")
        if "id" in table["columns"]:
            number = re.match(r"\s*(-?\d+)\s*(?:,|$)", row.group(3))
            if not columns or columns[0] != "id" or not number:
                errors.append(f"Seed rows require a numeric id in the first value position: {name}")
            else:
                table["max_id"] = max(table["max_id"], int(number.group(1)))
        elif target in {"sqlserver", "dm8"}:
            errors.append(f"Seed rows on a table without id would emit invalid IDENTITY_INSERT: {name}")
    if errors:
        raise ValueError("; ".join(dict.fromkeys(errors)))
    return tables, skipped, ignored


def validate_output(sql, tables, target):
    masked, _ = mask_sql(sql, backslash_escapes=target not in POSTGRES_TARGETS)
    expected_tables = Counter({name: 1 for name in tables})
    expected_inserts = Counter({name: data["inserts"] for name, data in tables.items() if data["inserts"]})
    if target in DUAL_TARGETS:
        expected_tables["dual"] += 1
        expected_inserts["dual"] += 1
    if Counter(m.group(1).lower() for m in CREATE.finditer(masked)) != expected_tables:
        raise ValueError("Generated table inventory differs from source (excluding Quartz and accounting for dual)")
    if Counter(m.group(1).lower() for m in INSERT.finditer(masked)) != expected_inserts:
        raise ValueError("Generated INSERT inventory differs from source")
    if re.search(r"\bNone\b", masked):
        raise ValueError("Converter emitted an unsupported type/precision placeholder: None")
    adjustments = []
    if target in SEQUENCE_TARGETS:
        for name, data in tables.items():
            if "id" not in data["columns"]:
                continue
            pattern = re.compile(rf"^([ \t]*CREATE SEQUENCE {re.escape(name)}_seq\s+START(?: WITH)?\s+)(\d+)", re.I | re.M)
            matches = list(pattern.finditer(sql))
            if len(matches) != 1:
                raise ValueError(f"Expected one sequence for table: {name}")
            old = int(matches[0].group(2))
            start = data["max_id"] + 1
            if old != start:
                sql = pattern.sub(lambda m: m.group(1) + str(start), sql)
                adjustments.append({"table": name, "from": old, "to": start})
    return sql, adjustments


def convert(args):
    project = args.project_root.resolve()
    source = (project / (args.source or "sql/mysql/ruoyi-vue-pro.sql")).resolve()
    converter = project / "sql/tools/convertor.py"
    output = (project / (args.output or f"sql/converted/{source.stem}.{args.target}.sql")).resolve()
    report_path = output.with_suffix(output.suffix + ".report.json")
    diagnostic_path = output.with_suffix(output.suffix + ".stderr.log")
    if not source.is_file() or not converter.is_file():
        raise ValueError("Project must contain the input SQL and sql/tools/convertor.py")
    if output in {source, converter.resolve()} or any(path.exists() or path.is_symlink() for path in (output, report_path, diagnostic_path)):
        raise ValueError("Choose a new output path; source, converter and existing artifacts cannot be overwritten")
    source_bytes = source.read_bytes()
    report = {
        "status": "failed", "target": args.target, "source_name": source.name,
        "source_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "converter_sha256": hashlib.sha256(converter.read_bytes()).hexdigest(),
        "database_validation": "not_run", "errors": [], "warnings": [],
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    try:
        tables, skipped, ignored = source_inventory(source_bytes.decode("utf-8-sig"), args.target)
        report.update({"tables": list(tables), "source_insert_statements": sum(t["inserts"] for t in tables.values()),
                       "quartz_tables_skipped": skipped, "source_session_or_drop_statements_ignored": ignored})
        try:
            report["simple_ddl_parser_version"] = importlib.metadata.version("simple-ddl-parser")
        except importlib.metadata.PackageNotFoundError:
            raise ValueError("Missing simple-ddl-parser; run this wrapper in the documented isolated uv environment") from None
        # PLY's first parser build can emit megabytes of INFO grammar logs.
        # Keep warnings/errors and the converter's direct stderr diagnostics.
        bootstrap = "import logging,runpy,sys; logging.disable(logging.INFO); p=sys.argv.pop(1); sys.argv[0]=p; runpy.run_path(p,run_name='__main__')"
        process = subprocess.run(
            [sys.executable, "-X", "utf8", "-c", bootstrap, str(converter), args.target, str(source)],
            cwd=converter.parent, capture_output=True, timeout=args.timeout,
            env={**os.environ, "PYTHONIOENCODING": "utf-8"},
        )
        report["converter_exit_code"] = process.returncode
        if process.stderr.strip():
            with diagnostic_path.open("xb") as stream:
                stream.write(process.stderr)
            report["diagnostic_file"] = diagnostic_path.name
            raise ValueError("Converter emitted diagnostics; inspect the local stderr log before publishing SQL")
        if process.returncode:
            raise ValueError(f"Converter failed with exit code {process.returncode}")
        sql, adjustments = validate_output(process.stdout.decode("utf-8"), tables, args.target)
        report["sequence_adjustments"] = adjustments
        report["warnings"].append("generated_only: target database import, type ranges, defaults, comments, indexes and data semantics require validation")
        if skipped:
            report["warnings"].append("Quartz tables are excluded; use the target database's separate Quartz script")
        if report["converter_sha256"] != KNOWN_CONVERTER:
            report["warnings"].append("Project converter differs from the inspected source version; review its changes")
        report["destructive_statements"] = len(re.findall(r"\bDROP\s+(?:TABLE|SEQUENCE)\b", mask_sql(sql, backslash_escapes=args.target not in POSTGRES_TARGETS)[0], re.I))
        encoded = sql.encode("utf-8")
        with output.open("xb") as stream:
            stream.write(encoded)
        report.update({"status": "generated_only", "output_sha256": hashlib.sha256(encoded).hexdigest(), "output_file": output.name})
    except (ValueError, UnicodeError, OSError, subprocess.TimeoutExpired) as error:
        report["errors"].append(str(error))
    with report_path.open("x", encoding="utf-8") as stream:
        json.dump(report, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    return report, report_path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, required=True)
    parser.add_argument("--target", type=target_name, choices=TARGETS, required=True)
    parser.add_argument("--source", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--timeout", type=int, default=300)
    args = parser.parse_args()
    try:
        report, path = convert(args)
        print(json.dumps({"status": report["status"], "target": args.target,
                          "report": str(path), "errors": report["errors"]}, ensure_ascii=False))
        return 0 if report["status"] == "generated_only" else 1
    except (ValueError, OSError) as error:
        print(json.dumps({"status": "failed", "errors": [str(error)]}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    sys.exit(main())
