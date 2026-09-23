"""Query system master data and prepare/apply missing records, using stdlib only."""

import http.client
import json
import urllib.error
import urllib.parse
import urllib.request


class SystemAPIError(RuntimeError):
    """A request failed; this must never be interpreted as an empty result."""


class DataConflict(ValueError):
    """Existing or requested identities conflict; no automatic update is allowed."""


class ApplyError(SystemAPIError):
    def __init__(self, completed, failed_operation):
        super().__init__("Apply stopped; the last write may have succeeded. Requery before retrying.")
        self.completed = completed
        self.failed_operation = failed_operation


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        # An API redirect must not forward a bearer token to another endpoint.
        return None


RESOURCES = {
    "roles": ("/system/role/page", True, ("name", "code")),
    "users": ("/system/user/page", True, ("username", "nickname")),
    "depts": ("/system/dept/list", False, ("name",)),
    "posts": ("/system/post/page", True, ("name", "code")),
    "dicts": ("/system/dict-type/page", True, ("name", "type")),
    "dict-data": ("/system/dict-data/page", True, ("label", "value")),
    "menus": ("/system/menu/list", False, ("name", "permission")),
    "tenants": ("/system/tenant/page", True, ("name",)),
}
CREATE_PATHS = {
    "roles": "/system/role/create",
    "dicts": "/system/dict-type/create",
    "dict-data": "/system/dict-data/create",
    "menus": "/system/menu/create",
}


def _numeric_id(value, *, allow_zero=False):
    # The project's NumberSerializer emits large Long IDs as decimal strings.
    if isinstance(value, str) and value.isascii() and value.isdecimal():
        value = int(value)
    if type(value) is not int or not (0 if allow_zero else 1) <= value <= 2 ** 63 - 1:
        raise ValueError("Expected a valid numeric record ID")
    return value


class SystemClient:
    def __init__(self, api_base, token, *, tenant_id, visit_tenant_id=None,
                 page_size=100, timeout=20, opener=None):
        parsed = urllib.parse.urlsplit(api_base)
        if (parsed.scheme not in ("https", "http") or not parsed.hostname
                or parsed.username or parsed.password or parsed.query or parsed.fragment):
            raise ValueError("api_base must be an HTTP(S) API base without credentials, query or fragment")
        if not isinstance(token, str) or not token.strip() or any(c.isspace() for c in token):
            raise ValueError("Provide a raw bearer token through a protected input or environment variable")
        if type(page_size) is not int or not 1 <= page_size <= 100:
            raise ValueError("page_size must be an integer from 1 to 100")
        if not isinstance(timeout, (int, float)) or timeout <= 0:
            raise ValueError("timeout must be positive")
        self.api_base = api_base.rstrip("/")
        self._token = token
        self.headers = {"Content-Type": "application/json; charset=utf-8"}
        for key, value in (("tenant-id", tenant_id), ("visit-tenant-id", visit_tenant_id)):
            if value is not None:
                if not str(value).isascii() or not str(value).isdigit():
                    raise ValueError("Tenant headers must be nonnegative numeric IDs")
                self.headers[key] = str(value)
        self.page_size = page_size
        self.timeout = timeout
        self._opener = opener or urllib.request.build_opener(_NoRedirect())

    def _request(self, path, *, params=None, payload=None, apply=False):
        method = "POST" if payload is not None else "GET"
        if method == "POST" and (apply is not True or path not in CREATE_PATHS.values()):
            raise ValueError("Creating records requires apply=True and a supported create endpoint")
        query = "?" + urllib.parse.urlencode(params) if params else ""
        headers = dict(self.headers, Authorization="Bearer " + self._token)
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8") if payload is not None else None
        request = urllib.request.Request(self.api_base + path + query, body, headers, method=method)
        try:
            with self._opener.open(request, timeout=self.timeout) as response:
                result = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            raise SystemAPIError(f"{method} {path}: HTTP {exc.code}; response body suppressed") from None
        except (urllib.error.URLError, OSError, ValueError, http.client.HTTPException):
            raise SystemAPIError(f"{method} {path}: transport or JSON response failure") from None
        if not isinstance(result, dict) or type(result.get("code")) is not int:
            raise SystemAPIError(f"{method} {path}: invalid CommonResult envelope")
        if result["code"] != 0:
            raise SystemAPIError(f"{method} {path}: API code {result['code']}; response message suppressed")
        if "data" not in result:
            raise SystemAPIError(f"{method} {path}: missing response data")
        return result["data"]

    @staticmethod
    def _rows(data):
        if not isinstance(data, list) or any(not isinstance(row, dict) for row in data):
            raise SystemAPIError("Expected a list of records")
        rows = []
        try:
            for row in data:
                row = dict(row, id=_numeric_id(row.get("id")))
                if row.get("parentId") is not None:
                    row["parentId"] = _numeric_id(row["parentId"], allow_zero=True)
                rows.append(row)
        except ValueError:
            raise SystemAPIError("Expected numeric record IDs and parent IDs") from None
        return rows

    def _pages(self, path, params):
        rows, seen, total, page_no = [], set(), None, 1
        while True:
            data = self._request(path, params=dict(params, pageNo=page_no, pageSize=self.page_size))
            if not isinstance(data, dict) or type(data.get("total")) is not int or data["total"] < 0:
                raise SystemAPIError("Invalid PageResult total")
            if total is not None and total != data["total"]:
                raise SystemAPIError("Pagination total changed; requery before deciding whether data exists")
            total = data["total"]
            batch = self._rows(data.get("list"))
            ids = [row["id"] for row in batch]
            if len(set(ids)) != len(ids) or seen.intersection(ids):
                raise SystemAPIError("Repeated records across pages; query is incomplete")
            seen.update(ids)
            rows.extend(batch)
            if len(rows) > total:
                raise SystemAPIError("PageResult contains more records than total")
            if len(rows) == total:
                return rows
            if not batch:
                raise SystemAPIError("Empty page before total was reached; query is incomplete")
            page_no += 1

    def query(self, resource, *, keyword=None, dict_type=None):
        if resource not in RESOURCES:
            raise ValueError("Unsupported resource")
        if resource == "dict-data" and (not isinstance(dict_type, str) or not dict_type.strip()):
            raise ValueError("dict-data requires a nonempty dict_type")
        path, paginated, fields = RESOURCES[resource]
        params = {"dictType": dict_type} if resource == "dict-data" else {}
        rows = self._pages(path, params) if paginated else self._rows(self._request(path))
        if resource == "dict-data":
            if any(row.get("dictType") != dict_type for row in rows):
                raise SystemAPIError("Dictionary page returned records from an unexpected type")
        if keyword:
            needle = keyword.casefold()
            rows = [row for row in rows if any(needle in str(row.get(field, "")).casefold() for field in fields)]
        return rows


FIELDS = {
    "roles": {"name", "code", "sort", "status", "remark"},
    "dicts": {"name", "type", "status", "remark", "items"},
    "dict-data": {"label", "value", "sort", "status", "colorType", "cssClass", "remark"},
    "menus": {"name", "parentId", "type", "sort", "status", "permission", "path", "icon",
              "component", "componentName", "visible", "keepAlive", "alwaysShow"},
}
REQUIRED = {
    "roles": ("name", "code", "status"),
    "dicts": ("name", "type", "status"),
    "dict-data": ("label", "value", "status"),
    "menus": ("name", "parentId", "type", "status"),
}


def _validate_record(resource, row):
    if not isinstance(row, dict) or set(row) - FIELDS[resource]:
        raise ValueError(f"Unsupported fields in {resource} record")
    if any(key not in row for key in REQUIRED[resource]):
        raise ValueError(f"Missing required fields in {resource}: {', '.join(REQUIRED[resource])}")
    row = dict(row)
    if resource == "menus":
        row["parentId"] = _numeric_id(row["parentId"], allow_zero=True)
    for key, value in row.items():
        if key == "items":
            continue
        if key in ("sort", "status", "parentId") or (resource == "menus" and key == "type"):
            if type(value) is not int:
                raise ValueError(f"{resource}.{key} must be an integer")
        elif key in ("visible", "keepAlive", "alwaysShow"):
            if type(value) is not bool:
                raise ValueError(f"{resource}.{key} must be a boolean")
        elif not isinstance(value, str):
            raise ValueError(f"{resource}.{key} must be a string")
    if row["status"] not in (0, 1):
        raise ValueError("status must be 0 or 1")
    for key in REQUIRED[resource]:
        if isinstance(row[key], str) and not row[key].strip():
            raise ValueError(f"{resource}.{key} cannot be blank")
    if resource == "menus":
        if row["type"] not in (1, 2, 3) or row["parentId"] < 0:
            raise ValueError("Menu type must be 1/2/3 and parentId must be nonnegative")
        required = ("permission",) if row["type"] == 3 else ("path",)
        if row["type"] == 2:
            required += ("component", "componentName")
        if any(not row.get(key, "").strip() for key in required):
            raise ValueError("Menu is missing its route, component or button permission")
        if row["type"] == 3 and any(row.get(key) for key in ("path", "icon", "component", "componentName")):
            raise ValueError("Buttons must not carry route or component fields")
    return dict(row)


def validate_config(config):
    """Validate the whole input before any API request or write."""
    if not isinstance(config, dict) or set(config) - {"roles", "dicts", "menus", "users", "depts", "posts"}:
        raise ValueError("Unsupported config sections")
    clean = {}
    for resource, rows in config.items():
        if not isinstance(rows, list):
            raise ValueError("Each config section must be a list")
        clean[resource] = []
        identities = set()
        for row in rows:
            if resource in ("users", "depts", "posts"):
                if (not isinstance(row, dict) or set(row) != {"keyword"}
                        or not isinstance(row["keyword"], str) or not row["keyword"].strip()):
                    raise ValueError("Read-only references require one nonempty keyword")
                clean[resource].append(dict(row))
                continue
            value = _validate_record(resource, row)
            key = (value["parentId"], value["name"]) if resource == "menus" else value["code" if resource == "roles" else "type"]
            if key in identities:
                raise DataConflict("Duplicate requested identity")
            identities.add(key)
            if resource == "dicts":
                items = value.pop("items", [])
                if not isinstance(items, list):
                    raise ValueError("Dictionary items must be a list")
                value["items"] = [_validate_record("dict-data", item) for item in items]
                for field in ("value", "label"):
                    if len({item[field] for item in items}) != len(items):
                        raise DataConflict("Duplicate requested dictionary value or label")
            clean[resource].append(value)
    return clean


def _operation(resource, desired, existing, identity_fields, *, unique_fields=()):
    matches = [row for row in existing if all(row.get(key) == desired[key] for key in identity_fields)]
    if len(matches) > 1:
        raise DataConflict(f"Ambiguous existing identity in {resource}")
    if matches:
        found = matches[0]
        if any(found.get(key) != value for key, value in desired.items()):
            raise DataConflict(f"Existing {resource} differs from requested fields; review an explicit update separately")
        return {"resource": resource, "action": "existing", "id": found["id"], "data": desired}
    if any(any(row.get(field) == desired.get(field) for field in unique_fields if desired.get(field)) for row in existing):
        raise DataConflict(f"Existing {resource} has the same name, label or component with another identity")
    payload = dict(desired)
    if resource != "dicts":
        payload.setdefault("sort", 0)
    if resource == "menus":
        for field, default in (("visible", True), ("keepAlive", False), ("alwaysShow", False)):
            payload.setdefault(field, default)
    operation = {"resource": resource, "action": "create", "data": payload}
    if resource == "roles":
        operation["serverDefaults"] = {"type": "CUSTOM", "dataScope": "ALL"}
    return operation


def process_config(client, config, *, apply=False):
    """Preflight every query, then create missing records only when apply is True.

    No authorization is inferred from this flag: the calling agent must already
    have task-specific permission for the target environment and concrete data.
    """
    if type(apply) is not bool:
        raise ValueError("apply must be a boolean")
    clean = validate_config(config)
    operations, lookups = [], {}
    for resource in ("roles", "dicts", "menus"):
        if not clean.get(resource):
            continue
        existing = client.query(resource)
        for row in clean[resource]:
            desired = {key: value for key, value in row.items() if key != "items"}
            if resource == "menus":
                if desired["parentId"] and not any(item["id"] == desired["parentId"] and item.get("type") in (1, 2) for item in existing):
                    raise DataConflict("Menu parent must be an existing directory or menu; create and requery parent first")
                op = _operation(resource, desired, existing, ("parentId", "name"), unique_fields=("componentName",))
            else:
                op = _operation(resource, desired, existing, ("code" if resource == "roles" else "type",), unique_fields=("name",))
            operations.append(op)
            # Include pending rows to reject conflicts between records in this batch.
            existing.append(dict(desired, id=op.get("id", -len(operations))))
            if resource == "dicts" and row["items"]:
                items = client.query("dict-data", dict_type=desired["type"])
                for item in row["items"]:
                    item = dict(item, dictType=desired["type"])
                    item_operation = _operation("dict-data", item, items, ("value",), unique_fields=("label",))
                    if desired["status"] != 0 and item_operation["action"] == "create":
                        raise DataConflict("Cannot create dictionary items under a disabled dictionary type")
                    operations.append(item_operation)
    for resource in ("users", "depts", "posts"):
        if clean.get(resource):
            rows = client.query(resource)
            fields = RESOURCES[resource][2]
            lookups[resource] = []
            for item in clean[resource]:
                found = [row for row in rows if any(row.get(field) == item["keyword"] for field in fields)]
                if len(found) != 1:
                    raise DataConflict(f"Read-only {resource} lookup must resolve exactly one record")
                lookups[resource].append(found[0])
    if not apply:
        return {"applied": False, "operations": operations, "lookups": lookups}
    completed = []
    for operation in operations:
        if operation["action"] == "existing":
            completed.append(operation)
            continue
        try:
            record_id = client._request(CREATE_PATHS[operation["resource"]], payload=operation["data"], apply=True)
            try:
                record_id = _numeric_id(record_id)
            except ValueError:
                raise SystemAPIError("Create returned an invalid record ID")
        except SystemAPIError:
            raise ApplyError(completed, operation) from None
        completed.append(dict(operation, action="created", id=record_id))
    return {"applied": True, "operations": completed, "lookups": lookups}
