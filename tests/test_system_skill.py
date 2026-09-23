"""System master-data import regression tests; all HTTP traffic is mocked."""

import contextlib
import http.client
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import urllib.error
import urllib.parse
import urllib.request


sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills/yudao-system/scripts"
spec = importlib.util.spec_from_file_location("system_utils", SCRIPTS / "system_utils.py")
utils = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = utils
spec.loader.exec_module(utils)
spec_cli = importlib.util.spec_from_file_location("system_creator", SCRIPTS / "system_creator.py")
cli = importlib.util.module_from_spec(spec_cli)
spec_cli.loader.exec_module(cli)


class Response(io.BytesIO):
    def __init__(self, data):
        super().__init__(json.dumps(data).encode("utf-8"))


class MockOpener:
    def __init__(self, *responses):
        self.responses = list(responses)
        self.requests = []

    def open(self, request, timeout):
        self.requests.append(request)
        response = self.responses.pop(0)
        if isinstance(response, Exception):
            raise response
        return Response(response)


def success(data):
    return {"code": 0, "data": data}


def page(rows, total=None):
    return success({"list": rows, "total": len(rows) if total is None else total})


def client(opener, **kwargs):
    return utils.SystemClient("https://example.invalid/admin-api", "test-token-only", tenant_id="7",
                              visit_tenant_id="9", opener=opener, **kwargs)


ROLE = {"name": "审核员", "code": "reviewer", "status": 1}


class SystemClientTests(unittest.TestCase):
    def test_fetches_all_pages_past_one_hundred_and_preserves_tenants(self):
        rows = [{"id": number, "name": f"Role {number}", "code": f"r{number}"} for number in range(1, 104)]
        opener = MockOpener(page(rows[:100], 103), page(rows[100:], 103))
        result = client(opener).query("roles", keyword="r103")
        self.assertEqual(result, [rows[-1]])
        self.assertEqual([urllib.parse.parse_qs(urllib.parse.urlsplit(req.full_url).query)["pageNo"] for req in opener.requests], [["1"], ["2"]])
        for request in opener.requests:
            self.assertEqual(request.get_header("Tenant-id"), "7")
            self.assertEqual(request.get_header("Visit-tenant-id"), "9")
            self.assertEqual(request.get_header("Authorization"), "Bearer test-token-only")

    def test_server_page_size_cap_does_not_stop_on_short_page(self):
        opener = MockOpener(page([{"id": 1}], 3), page([{"id": 2}], 3), page([{"id": 3}], 3))
        self.assertEqual(len(client(opener).query("users")), 3)

    def test_query_failures_never_create(self):
        failures = [
            {"code": 401, "msg": "secret test-token-only", "data": None},
            urllib.error.URLError("secret test-token-only"),
            urllib.error.HTTPError("https://example.invalid", 403, "test-token-only", {}, None),
            {"code": 0, "data": None},
            {"code": False, "data": {"list": [], "total": 0}},
        ]
        for failure in failures:
            opener = MockOpener(failure)
            with self.subTest(failure=type(failure).__name__), self.assertRaises(utils.SystemAPIError) as caught:
                utils.process_config(client(opener), {"roles": [ROLE]}, apply=True)
            self.assertNotIn("test-token-only", str(caught.exception))
            self.assertEqual([req.method for req in opener.requests], ["GET"])

    def test_page_two_failure_prevents_creating_absent_record(self):
        opener = MockOpener(page([{"id": 1}], 2), {"code": 503, "data": None})
        with self.assertRaises(utils.SystemAPIError):
            utils.process_config(client(opener), {"roles": [ROLE]}, apply=True)
        self.assertTrue(all(req.method == "GET" for req in opener.requests))

    def test_rejects_incomplete_and_changing_pages(self):
        cases = [
            [page([{"id": 1}], 2), page([], 2)],
            [page([{"id": 1}], 2), page([{"id": 1}], 2)],
            [page([{"id": 1}], 2), page([{"id": 2}], 3)],
            [page([{"id": 1}, {"id": 1}], 2)],
            [success({"list": [], "total": "0"})],
            [page([{"name": "Missing ID"}])],
        ]
        for responses in cases:
            with self.subTest(responses=responses), self.assertRaises(utils.SystemAPIError):
                client(MockOpener(*responses)).query("roles")

    def test_dict_query_includes_disabled_items_and_escapes_type(self):
        item = {"id": 8, "dictType": "order status&", "value": "pending", "label": "待处理", "status": 1}
        opener = MockOpener(page([item]))
        self.assertEqual(client(opener).query("dict-data", dict_type=item["dictType"]), [item])
        query = urllib.parse.parse_qs(urllib.parse.urlsplit(opener.requests[0].full_url).query)
        self.assertEqual(query["dictType"], [item["dictType"]])
        self.assertNotIn("status", query)
        self.assertIn("/dict-data/page", opener.requests[0].full_url)

    def test_wrong_dictionary_response_stops_instead_of_becoming_empty(self):
        opener = MockOpener(page([{"id": 1, "dictType": "different"}]))
        with self.assertRaises(utils.SystemAPIError):
            client(opener).query("dict-data", dict_type="requested")

    def test_invalid_url_or_tenant_rejected(self):
        for url in ("https://user:password@example.invalid", "https://example.invalid?token=value",
                    "https://example.invalid#fragment", "file:///tmp/data"):
            with self.subTest(url=url), self.assertRaises(ValueError):
                utils.SystemClient(url, "test", tenant_id="1")
        with self.assertRaises(ValueError):
            utils.SystemClient("https://example.invalid", "test", tenant_id="1\nextra")

    def test_redirects_rejected_and_default_tls_handler_kept(self):
        actual = utils.SystemClient("https://example.invalid", "test", tenant_id=None)
        handlers = actual._opener.handlers
        self.assertTrue(any(isinstance(handler, urllib.request.HTTPSHandler) for handler in handlers))
        redirect = next(handler for handler in handlers if isinstance(handler, utils._NoRedirect))
        request = urllib.request.Request("https://example.invalid", headers={"Authorization": "Bearer test"})
        self.assertIsNone(redirect.redirect_request(request, None, 302, "moved", {}, "https://other.invalid"))

    def test_large_long_string_ids_are_normalized_without_precision_loss(self):
        large_id = 9007199254740992
        opener = MockOpener(page([dict(ROLE, id=str(large_id))]))
        result = utils.process_config(client(opener), {"roles": [ROLE]}, apply=True)
        self.assertEqual(result["operations"][0]["id"], large_id)
        opener = MockOpener(page([]), success(str(large_id)))
        result = utils.process_config(client(opener), {"roles": [ROLE]}, apply=True)
        self.assertEqual(result["operations"][0]["id"], large_id)

    def test_large_parent_id_in_config_and_response_resolves_existing_menu(self):
        large_id = 9007199254740992
        menu = {"name": "订单", "type": 1, "parentId": str(large_id), "path": "order", "status": 0}
        rows = [{"id": str(large_id), "parentId": "0", "name": "业务", "type": 1},
                dict(menu, id=str(large_id + 1))]
        opener = MockOpener(success(rows))
        result = utils.process_config(client(opener), {"menus": [menu]}, apply=True)
        self.assertEqual(result["operations"][0]["action"], "existing")
        self.assertEqual(result["operations"][0]["data"]["parentId"], large_id)

    def test_invalid_boolean_fractional_and_negative_ids_are_rejected(self):
        for record_id in (True, 1.5, -1, "1.5", "-1", "NaN", "9223372036854775808"):
            with self.subTest(record_id=record_id), self.assertRaises(utils.SystemAPIError):
                client(MockOpener(page([{"id": record_id}]))).query("roles")


class SystemPlanTests(unittest.TestCase):
    def test_default_is_get_only_plan_with_server_role_defaults(self):
        opener = MockOpener(page([]))
        result = utils.process_config(client(opener), {"roles": [ROLE]})
        self.assertFalse(result["applied"])
        operation = result["operations"][0]
        self.assertEqual(operation["action"], "create")
        self.assertEqual(operation["serverDefaults"]["dataScope"], "ALL")
        self.assertEqual(operation["data"], dict(ROLE, sort=0))
        self.assertEqual([req.method for req in opener.requests], ["GET"])

    def test_apply_creates_only_role_with_no_grant_or_binding(self):
        opener = MockOpener(page([]), success(21))
        result = utils.process_config(client(opener), {"roles": [ROLE]}, apply=True)
        self.assertEqual(result["operations"][0]["id"], 21)
        self.assertEqual([req.method for req in opener.requests], ["GET", "POST"])
        request = opener.requests[1]
        self.assertTrue(request.full_url.endswith("/system/role/create"))
        self.assertEqual(json.loads(request.data), dict(ROLE, sort=0))
        self.assertEqual(request.get_header("Tenant-id"), "7")

    def test_existing_record_on_later_page_reused(self):
        opener = MockOpener(page([{"id": 1, "name": "other", "code": "other"}], 2), page([dict(ROLE, id=2)], 2))
        result = utils.process_config(client(opener), {"roles": [ROLE]}, apply=True)
        self.assertEqual(result["operations"][0]["action"], "existing")
        self.assertEqual(result["operations"][0]["id"], 2)
        self.assertTrue(all(req.method == "GET" for req in opener.requests))

    def test_fuzzy_name_is_not_reused_and_conflicting_identity_is_rejected(self):
        opener = MockOpener(page([{"id": 1, "name": "高级审核员", "code": "senior", "status": 1}]))
        self.assertEqual(utils.process_config(client(opener), {"roles": [ROLE]})["operations"][0]["action"], "create")
        for row in (dict(ROLE, id=1, code="another"), dict(ROLE, id=1, name="different")):
            opener = MockOpener(page([row]))
            with self.assertRaises(utils.DataConflict):
                utils.process_config(client(opener), {"roles": [ROLE]}, apply=True)
            self.assertEqual(len(opener.requests), 1)

    def test_validation_and_late_preflight_failure_happen_before_all_writes(self):
        opener = MockOpener()
        with self.assertRaises(ValueError):
            utils.process_config(client(opener), {"roles": [ROLE], "dicts": [{"type": "bad"}]}, apply=True)
        self.assertEqual(opener.requests, [])
        opener = MockOpener(page([]), {"code": 403, "data": None})
        with self.assertRaises(utils.SystemAPIError):
            utils.process_config(client(opener), {"roles": [ROLE], "users": [{"keyword": "operator"}]}, apply=True)
        self.assertTrue(all(req.method == "GET" for req in opener.requests))

    def test_empty_existing_dict_and_disabled_item_are_reused(self):
        dictionary = {"name": "订单状态", "type": "order_status", "status": 0}
        item = {"label": "待处理", "value": "pending", "status": 1}
        opener = MockOpener(page([dict(dictionary, id=10)]), page([dict(item, id=11, dictType="order_status")]))
        result = utils.process_config(client(opener), {"dicts": [dict(dictionary, items=[item])]}, apply=True)
        self.assertEqual([op["action"] for op in result["operations"]], ["existing", "existing"])
        opener = MockOpener(page([dict(dictionary, id=10)]), page([]), success(12))
        result = utils.process_config(client(opener), {"dicts": [dict(dictionary, items=[item])]}, apply=True)
        self.assertEqual([op["action"] for op in result["operations"]], ["existing", "created"])
        self.assertEqual(json.loads(opener.requests[-1].data)["dictType"], "order_status")

    def test_dictionary_conflict_and_duplicate_input_stop(self):
        dictionary = {"name": "状态", "type": "state", "status": 0}
        item = {"label": "待处理", "value": "pending", "status": 0}
        opener = MockOpener(page([dict(dictionary, id=10)]), page([dict(item, id=11, label="不同", dictType="state")]))
        with self.assertRaises(utils.DataConflict):
            utils.process_config(client(opener), {"dicts": [dict(dictionary, items=[item])]}, apply=True)
        self.assertTrue(all(req.method == "GET" for req in opener.requests))
        with self.assertRaises(utils.DataConflict):
            utils.validate_config({"dicts": [dict(dictionary, items=[item, item])]})

    def test_menu_parent_must_exist_and_button_payload_is_supported(self):
        menu = {"name": "订单查询", "type": 3, "parentId": 20, "permission": "order:item:query", "status": 0}
        opener = MockOpener(success([]))
        with self.assertRaises(utils.DataConflict):
            utils.process_config(client(opener), {"menus": [menu]}, apply=True)
        opener = MockOpener(success([{"id": 20, "name": "订单", "type": 2}]), success(22))
        result = utils.process_config(client(opener), {"menus": [menu]}, apply=True)
        self.assertEqual(result["operations"][0]["id"], 22)
        self.assertTrue(opener.requests[-1].full_url.endswith("/system/menu/create"))
        self.assertNotIn("component", json.loads(opener.requests[-1].data))

    def test_partial_failure_reports_completed_and_never_retries(self):
        opener = MockOpener(page([]), success(21), urllib.error.URLError("timeout"))
        another = dict(ROLE, name="审核主管", code="review_manager")
        with self.assertRaises(utils.ApplyError) as caught:
            utils.process_config(client(opener), {"roles": [ROLE, another]}, apply=True)
        self.assertEqual(caught.exception.completed[0]["id"], 21)
        self.assertEqual(caught.exception.failed_operation["data"]["code"], "review_manager")
        self.assertEqual(len(opener.requests), 3)

    def test_truncated_http_body_preserves_partial_write_report(self):
        opener = MockOpener(page([]), success(21), http.client.IncompleteRead(b"secret response", 20))
        another = dict(ROLE, name="审核主管", code="review_manager")
        with self.assertRaises(utils.ApplyError) as caught:
            utils.process_config(client(opener), {"roles": [ROLE, another]}, apply=True)
        self.assertEqual(caught.exception.completed[0]["id"], 21)
        self.assertEqual(caught.exception.failed_operation["data"]["code"], "review_manager")
        self.assertNotIn("secret response", str(caught.exception))
        self.assertEqual(len(opener.requests), 3)

    def test_disabled_dictionary_type_cannot_receive_new_items(self):
        dictionary = {"name": "已停用状态", "type": "old_state", "status": 1}
        item = {"label": "待处理", "value": "pending", "status": 1}
        for existing in ([], [dict(dictionary, id=10)]):
            opener = MockOpener(page(existing), page([]))
            with self.subTest(existing=existing), self.assertRaises(utils.DataConflict):
                utils.process_config(client(opener), {"dicts": [dict(dictionary, items=[item])]}, apply=True)
            self.assertTrue(all(req.method == "GET" for req in opener.requests))
        opener = MockOpener(page([dict(dictionary, id=10)]), page([dict(item, id=11, dictType="old_state")]))
        result = utils.process_config(client(opener), {"dicts": [dict(dictionary, items=[item])]}, apply=True)
        self.assertEqual([op["action"] for op in result["operations"]], ["existing", "existing"])

    def test_every_write_requires_boolean_apply_and_unknown_fields_rejected(self):
        opener = MockOpener()
        actual = client(opener)
        for flag in (False, None, "true", 1):
            with self.subTest(flag=flag), self.assertRaises(ValueError):
                actual._request("/system/role/create", payload=ROLE, apply=flag)
        with self.assertRaises(ValueError):
            utils.process_config(actual, {"roles": [ROLE]}, apply="true")
        with self.assertRaises(ValueError):
            utils.process_config(actual, {"roles": [dict(ROLE, add_admin=True)]}, apply=True)
        self.assertEqual(opener.requests, [])


class SystemCLITests(unittest.TestCase):
    def test_query_outputs_minimal_identity_fields(self):
        opener = MockOpener(page([{"id": 1, "username": "operator", "nickname": "操作员",
                                  "mobile": "private", "email": "private", "accessToken": "private"}]))
        output = io.StringIO()
        env = {"YUDAO_API_BASE": "https://example.invalid/admin-api", "YUDAO_TOKEN": "test-token-only", "YUDAO_TENANT_ID": "7"}
        with patch.dict(os.environ, env, clear=True), patch.object(utils.urllib.request, "build_opener", return_value=opener), contextlib.redirect_stdout(output):
            self.assertEqual(cli.main(["--action", "query-users"]), 0)
        self.assertEqual(json.loads(output.getvalue()), [{"id": 1, "username": "operator", "nickname": "操作员"}])

    def test_cli_refuses_unsupported_actions_and_secret_argv(self):
        for args in (["--action", "query-approval-roles"], ["--action", "query-roles", "--token", "test-only"]):
            with self.subTest(args=args), contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                cli.main(args)

    def test_rejected_credential_arguments_are_not_echoed(self):
        for argument in ("--token", "--password"):
            output = io.StringIO()
            with self.subTest(argument=argument), contextlib.redirect_stderr(output), self.assertRaises(SystemExit):
                cli.main(["--action", "query-roles", argument, "do-not-echo-this-test-value"])
            self.assertNotIn("do-not-echo-this-test-value", output.getvalue())

    def test_cli_does_not_overwrite_output_or_prompt_in_noninteractive_shell(self):
        env = {"YUDAO_API_BASE": "https://example.invalid", "YUDAO_TOKEN": "test-only", "YUDAO_TENANT_ID": "7"}
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "result.json"
            output.write_text("keep", encoding="utf-8")
            with patch.dict(os.environ, env, clear=True), contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                cli.main(["--action", "query-roles", "--output", str(output)])
            self.assertEqual(output.read_text(encoding="utf-8"), "keep")
        with patch.dict(os.environ, env, clear=True), patch.object(sys.stdin, "isatty", return_value=False), patch.object(cli.getpass, "getpass") as prompt, contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(cli.main(["--action", "query-roles", "--prompt-token"]), 1)
            prompt.assert_not_called()

    def test_subprocess_help_is_utf8_without_x_utf8(self):
        env = dict(os.environ, PYTHONIOENCODING="gbk", PYTHONUTF8="0", PYTHONDONTWRITEBYTECODE="1")
        result = subprocess.run([sys.executable, str(SCRIPTS / "system_creator.py"), "--help"],
                                capture_output=True, check=True, env=env)
        self.assertIn("查询系统主数据", result.stdout.decode("utf-8"))


if __name__ == "__main__":
    unittest.main()
