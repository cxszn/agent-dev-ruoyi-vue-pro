"""Focused regression tests for safeguards around the project converter."""

import argparse
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch


sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("convert_sql", ROOT / "scripts/convert_sql.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
DDL = "CREATE TABLE `t` (\n  `id` bigint NOT NULL,\n  `name` varchar(100),\n  PRIMARY KEY (`id`)\n);\n"


class ConversionSafetyTests(unittest.TestCase):
    def test_rejects_truncated_and_unsupported_data(self):
        rows = [
            "INSERT INTO `t` VALUES (1, 'a'),\n(2, 'b');\n",
            " INSERT INTO `t` VALUES (1, 'a');\n",
            "insert into `t` values (1, 'a');\n",
            "INSERT INTO t VALUES (1, 'a');\n",
            "INSERT INTO `t` VALUES (1, 'a'); INSERT INTO `t` VALUES (2, 'b');\n",
            "INSERT INTO `t` VALUES (1, 'x CHARACTER SET utf8mb4 y');\n",
            "INSERT INTO `t` VALUES (1, 'ENGINE blue;');\n",
            "INSERT INTO `t` VALUES (1, 'line)\nVALUES rest');\n",
            'INSERT INTO `t` VALUES (1, "b\'0\'");\n',
            "INSERT INTO `t` VALUES (1, 'a') ON DUPLICATE KEY UPDATE name=VALUES(name);\n",
            "INSERT INTO `t` VALUES (1, IFNULL(NULL, 'a'));\n",
            "INSERT INTO `t` VALUES (1, 1+2);\n",
            "INSERT INTO `t` VALUES (1);\n",
        ]
        for row in rows:
            with self.subTest(row=row), self.assertRaises(ValueError):
                MODULE.source_inventory(DDL + row, "postgres")

    def test_rejects_objects_and_keys_the_converter_drops(self):
        cases = [DDL + "CREATE VIEW v AS SELECT * FROM t;",
                 DDL.replace("PRIMARY KEY (`id`)", "PRIMARY KEY (`id`, `name`)"),
                 DDL.replace("PRIMARY KEY (`id`)", "PRIMARY KEY (`id`), CHECK ( id > 0)"),
                 DDL.replace("`name` varchar(100)", "`name` varchar(100) UNIQUE"),
                 DDL.replace("`name` varchar(100)", "`name` varchar(100) REFERENCES p(id)"),
                 DDL + DDL.replace("`t`", "`bad-name`"),
                 DDL.replace("`name` varchar(100)", "`name` varchar(100) AS (CONCAT(id,id)) STORED"),
                 DDL.lower()]
        for source in cases:
            with self.subTest(source=source), self.assertRaises(ValueError):
                MODULE.source_inventory(source, "postgres")

    def test_inventory_ignores_sql_words_inside_data(self):
        source = DDL + "INSERT INTO `t` VALUES (20, 'CREATE TABLE ghost (id int); INSERT INTO hidden');\n"
        tables, skipped, _ = MODULE.source_inventory(source, "postgres")
        self.assertEqual(list(tables), ["t"])
        self.assertEqual(tables["t"]["inserts"], 1)
        self.assertEqual(skipped, [])

    def test_mysql_dump_session_comments_do_not_hide_normal_tables(self):
        source = "/*!40101 SET NAMES utf8mb4 */;\n" + DDL + "/*!40101 SET FOREIGN_KEY_CHECKS=1 */;\n"
        tables, _, _ = MODULE.source_inventory(source, "postgres")
        self.assertEqual(list(tables), ["t"])
        with self.assertRaises(ValueError):
            MODULE.source_inventory(DDL + "/*!50001 CREATE VIEW v AS SELECT 1 */;", "postgres")

    def test_sequence_uses_max_seed_id_even_when_rows_are_unsorted(self):
        source = DDL + "INSERT INTO `t` VALUES (20, 'a');\nINSERT INTO `t` VALUES (2, 'b');\n"
        tables, _, _ = MODULE.source_inventory(source, "oracle")
        sql = source + "CREATE SEQUENCE t_seq START WITH 3;\n"
        fixed, changes = MODULE.validate_output(sql, tables, "oracle")
        self.assertIn("START WITH 21", fixed)
        self.assertEqual(changes, [{"table": "t", "from": 3, "to": 21}])

    def test_postgres_backslash_is_literal_after_mysql_escape_conversion(self):
        source = DDL + "INSERT INTO `t` VALUES (1, 'path');\n"
        tables, _, _ = MODULE.source_inventory(source, "postgres")
        output = (DDL + "INSERT INTO t VALUES (1, 'path\\');\n"
                  "CREATE TABLE dual (id int);\nINSERT INTO dual VALUES (1);\n"
                  "CREATE SEQUENCE t_seq START 2;\n")
        sql, changes = MODULE.validate_output(output, tables, "postgres")
        self.assertIn("START 2", sql)
        self.assertEqual(changes, [])

    def test_incomplete_tables_and_unknown_types_cannot_pass(self):
        tables, _, _ = MODULE.source_inventory(DDL, "oracle")
        for sql in ["", DDL.replace("varchar(100)", "None")]:
            with self.subTest(sql=sql), self.assertRaises(ValueError):
                MODULE.validate_output(sql, tables, "oracle")

    def test_exit_zero_with_stderr_does_not_publish_sql(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            (project / "sql/tools").mkdir(parents=True)
            (project / "sql/mysql").mkdir()
            (project / "sql/mysql/ruoyi-vue-pro.sql").write_text(DDL, encoding="utf-8")
            (project / "sql/tools/convertor.py").write_text(
                "import sys\nprint('partial SQL')\nprint('parse failed', file=sys.stderr)\n", encoding="utf-8")
            args = argparse.Namespace(project_root=project, target="postgres", target_version="16",
                                      source=None, output=None, timeout=30)
            with patch.object(MODULE.importlib.metadata, "version", return_value="test"):
                report, path = MODULE.convert(args)
            self.assertEqual(report["status"], "failed")
            self.assertEqual(report["converter_exit_code"], 0)
            self.assertTrue(path.is_file())
            self.assertFalse((project / "sql/converted/ruoyi-vue-pro.postgres16.sql").exists())
            self.assertEqual(json.loads(path.read_text(encoding="utf-8"))["status"], "failed")

    def test_existing_input_and_output_are_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            (project / "sql/tools").mkdir(parents=True)
            source = project / "input.sql"
            source.write_text(DDL, encoding="utf-8")
            (project / "sql/tools/convertor.py").write_text("", encoding="utf-8")
            for destination in (source, project / "existing.sql"):
                destination.write_text(DDL, encoding="utf-8")
                args = argparse.Namespace(project_root=project, target="postgres", target_version="16", source=source,
                                          output=destination, timeout=30)
                with self.assertRaises(ValueError):
                    MODULE.convert(args)
                self.assertEqual(destination.read_text(encoding="utf-8"), DDL)


if __name__ == "__main__":
    unittest.main()
