#!/usr/bin/env python3
"""
Agrivision AI+ — Translation Coverage Audit Script
Checks that all translation keys exist across all supported languages.
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, Set, List, Tuple

LOCALES_DIR = Path(__file__).parent.parent / "mobile" / "src" / "i18n" / "locales"
SUPPORTED_LANGUAGES = ["en", "mr", "hi"]
BASE_LANGUAGE = "en"


def load_json(filepath: Path) -> dict:
    """Load a JSON file safely."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"  ⚠ Error loading {filepath}: {e}")
        return {}


def get_all_keys(data: dict, prefix: str = "") -> Set[str]:
    """Recursively extract all keys from a nested dict."""
    keys = set()
    for key, value in data.items():
        full_key = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict):
            keys.update(get_all_keys(value, full_key))
        else:
            keys.add(full_key)
    return keys


def audit_namespace(namespace: str) -> Tuple[bool, List[str]]:
    """Audit a single namespace across all languages."""
    issues = []
    base_file = LOCALES_DIR / BASE_LANGUAGE / f"{namespace}.json"

    if not base_file.exists():
        issues.append(f"  ❌ Base file missing: {base_file}")
        return False, issues

    base_data = load_json(base_file)
    base_keys = get_all_keys(base_data)

    if not base_keys:
        issues.append(f"  ⚠ No keys found in {base_file}")
        return False, issues

    all_ok = True
    for lang in SUPPORTED_LANGUAGES:
        if lang == BASE_LANGUAGE:
            continue

        lang_file = LOCALES_DIR / lang / f"{namespace}.json"
        if not lang_file.exists():
            issues.append(f"  ❌ [{lang}] File missing: {lang_file}")
            all_ok = False
            continue

        lang_data = load_json(lang_file)
        lang_keys = get_all_keys(lang_data)

        missing = base_keys - lang_keys
        extra = lang_keys - base_keys

        if missing:
            all_ok = False
            issues.append(f"  ❌ [{lang}] Missing {len(missing)} keys:")
            for key in sorted(missing)[:10]:
                issues.append(f"       - {key}")
            if len(missing) > 10:
                issues.append(f"       ... and {len(missing) - 10} more")

        if extra:
            issues.append(f"  ⚠ [{lang}] {len(extra)} extra keys (not in {BASE_LANGUAGE})")

    return all_ok, issues


def main():
    """Run translation coverage audit."""
    print("=" * 60)
    print("🌍 Agrivision AI+ Translation Coverage Audit")
    print("=" * 60)

    if not LOCALES_DIR.exists():
        print(f"\n❌ Locales directory not found: {LOCALES_DIR}")
        sys.exit(1)

    # Find all namespaces from base language
    namespaces = []
    base_dir = LOCALES_DIR / BASE_LANGUAGE
    if base_dir.exists():
        namespaces = [f.stem for f in base_dir.glob("*.json")]

    if not namespaces:
        print(f"\n❌ No translation files found in {base_dir}")
        sys.exit(1)

    print(f"\nLanguages: {', '.join(SUPPORTED_LANGUAGES)}")
    print(f"Base language: {BASE_LANGUAGE}")
    print(f"Namespaces: {len(namespaces)}")
    print()

    total_ok = 0
    total_issues = 0

    for namespace in sorted(namespaces):
        ok, issues = audit_namespace(namespace)
        status = "✅" if ok else "❌"
        print(f"{status} {namespace}")
        for issue in issues:
            print(issue)

        if ok:
            total_ok += 1
        else:
            total_issues += 1

    print()
    print("=" * 60)
    print(f"Results: {total_ok} OK, {total_issues} with issues")
    print(f"Coverage: {total_ok}/{total_ok + total_issues} namespaces fully translated")
    print("=" * 60)

    if total_issues > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()

