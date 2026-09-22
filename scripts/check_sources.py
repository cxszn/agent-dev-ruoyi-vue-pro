"""Read-only check of a supplied Yudao project against the recorded baseline."""

import argparse
import hashlib
import json
from pathlib import Path
import sys
import xml.etree.ElementTree as ET


MANIFEST = Path(__file__).resolve().parent.parent / "references" / "source-manifest.json"
NS = {"m": "http://maven.apache.org/POM/4.0.0"}
IGNORED_DIRS = {"target", "node_modules", "dist", ".git", ".idea"}


def pom_value(path: Path, key: str) -> str | None:
    tree = ET.parse(path)
    node = tree.find(f"./m:properties/m:{key}", NS)
    return node.text.strip() if node is not None and node.text else None


def active_modules(path: Path) -> list[str]:
    tree = ET.parse(path)
    return [node.text.strip() for node in tree.findall("./m:modules/m:module", NS) if node.text]


def tree_fingerprint(root: Path, directory: Path) -> tuple[int, str]:
    files = sorted(
        (path for path in directory.rglob("*")
         if path.is_file() and not path.is_symlink()
         and not IGNORED_DIRS.intersection(path.relative_to(root).parts)),
        key=lambda path: path.relative_to(root).as_posix(),
    )
    digest = hashlib.sha256()
    for path in files:
        relative = path.relative_to(root).as_posix().encode("utf-8")
        digest.update(relative + b"\0" + hashlib.sha256(path.read_bytes()).digest())
    return len(files), digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True, help="Source tree to compare with the recorded baseline")
    args = parser.parse_args()
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    root = args.root.resolve()
    changes = []
    if not root.is_dir():
        print(f"MISSING SOURCE ROOT: {root}")
        return 1

    for relative, expected in manifest["files"].items():
        path = root / relative
        if not path.is_file():
            changes.append(f"MISSING {relative}")
            continue
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != expected:
            changes.append(f"CHANGED {relative} sha256={actual}")

    tracked = manifest["trees"]
    current = {path.name for path in root.iterdir()
               if path.is_dir() and (path.name.startswith("yudao-") or path.name == "sql")}
    for name in sorted(current - tracked.keys()):
        changes.append(f"NEW TREE {name}")
    for name, expected in tracked.items():
        directory = root / name
        if not directory.is_dir():
            changes.append(f"MISSING TREE {name}")
            continue
        count, sha256 = tree_fingerprint(root, directory)
        if count != expected["count"] or sha256 != expected["sha256"]:
            changes.append(f"CHANGED TREE {name} files={count} sha256={sha256}")

    baseline = manifest["baseline"]
    pom = root / "pom.xml"
    bom = root / "yudao-dependencies" / "pom.xml"
    if pom.is_file() and bom.is_file():
        checks = {
            "revision": pom_value(pom, "revision"),
            "java_version": pom_value(pom, "java.version"),
            "spring_boot_root": pom_value(pom, "spring.boot.version"),
            "spring_boot_bom": pom_value(bom, "spring.boot.version"),
            "modules": active_modules(pom),
            "vue3_package_json_present": (root / "yudao-ui/yudao-ui-admin-vue3/package.json").is_file(),
        }
        for key, actual in checks.items():
            if actual != baseline[key]:
                changes.append(f"BASELINE {key}: expected={baseline[key]!r} actual={actual!r}")

    print(f"Source: {root}")
    print(f"Baseline verified at: {manifest['verified_at']}")
    if changes:
        print("Differences:")
        for change in changes:
            print(f"  {change}")
        return 1
    print(f"MATCH: {len(manifest['files'])} key files, {len(tracked)} trees, and version/module baseline")
    return 0


if __name__ == "__main__":
    sys.exit(main())
