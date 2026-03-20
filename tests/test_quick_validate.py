#!/usr/bin/env python3
"""Tests for quick_validate.py"""

import tempfile
import shutil
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from quick_validate import validate_skill


def make_skill(tmp, content):
    d = Path(tmp) / "test-skill"
    d.mkdir(exist_ok=True)
    (d / "SKILL.md").write_text(content)
    return d


def test_valid_skill():
    with tempfile.TemporaryDirectory() as tmp:
        d = make_skill(
            tmp, "---\nname: my-skill\ndescription: A valid skill.\n---\n# My Skill\n"
        )
        ok, msg = validate_skill(d)
        assert ok, f"Expected valid, got: {msg}"


def test_missing_skill_md():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp) / "empty"
        d.mkdir()
        ok, msg = validate_skill(d)
        assert not ok
        assert "SKILL.md not found" in msg


def test_no_frontmatter():
    with tempfile.TemporaryDirectory() as tmp:
        d = make_skill(tmp, "# No frontmatter\n")
        ok, msg = validate_skill(d)
        assert not ok
        assert "frontmatter" in msg.lower()


def test_missing_name():
    with tempfile.TemporaryDirectory() as tmp:
        d = make_skill(tmp, "---\ndescription: Has desc but no name.\n---\n")
        ok, msg = validate_skill(d)
        assert not ok
        assert "name" in msg.lower()


def test_missing_description():
    with tempfile.TemporaryDirectory() as tmp:
        d = make_skill(tmp, "---\nname: my-skill\n---\n")
        ok, msg = validate_skill(d)
        assert not ok
        assert "description" in msg.lower()


def test_name_not_kebab_case():
    with tempfile.TemporaryDirectory() as tmp:
        d = make_skill(tmp, "---\nname: MySkill\ndescription: Bad name.\n---\n")
        ok, msg = validate_skill(d)
        assert not ok
        assert "kebab-case" in msg


def test_name_consecutive_hyphens():
    with tempfile.TemporaryDirectory() as tmp:
        d = make_skill(tmp, "---\nname: my--skill\ndescription: Bad hyphens.\n---\n")
        ok, msg = validate_skill(d)
        assert not ok
        assert "consecutive" in msg or "hyphen" in msg


def test_name_too_long():
    with tempfile.TemporaryDirectory() as tmp:
        long_name = "a" * 65
        d = make_skill(
            tmp, f"---\nname: {long_name}\ndescription: Too long name.\n---\n"
        )
        ok, msg = validate_skill(d)
        assert not ok
        assert "too long" in msg.lower()


def test_description_angle_brackets():
    with tempfile.TemporaryDirectory() as tmp:
        d = make_skill(
            tmp, "---\nname: my-skill\ndescription: Has <html> brackets.\n---\n"
        )
        ok, msg = validate_skill(d)
        assert not ok
        assert "angle brackets" in msg.lower()


def test_description_too_long():
    with tempfile.TemporaryDirectory() as tmp:
        long_desc = "x" * 1025
        d = make_skill(tmp, f"---\nname: my-skill\ndescription: {long_desc}\n---\n")
        ok, msg = validate_skill(d)
        assert not ok
        assert "too long" in msg.lower()


def test_multiline_description():
    content = "---\nname: my-skill\ndescription: >\n  This is a multiline\n  description that spans lines.\n---\n"
    with tempfile.TemporaryDirectory() as tmp:
        d = make_skill(tmp, content)
        ok, msg = validate_skill(d)
        assert ok, f"Expected valid, got: {msg}"


def test_unexpected_keys():
    with tempfile.TemporaryDirectory() as tmp:
        d = make_skill(
            tmp, "---\nname: my-skill\ndescription: Valid.\nauthor: someone\n---\n"
        )
        ok, msg = validate_skill(d)
        assert not ok
        assert "unexpected" in msg.lower() or "author" in msg.lower()


def test_allowed_optional_keys():
    content = "---\nname: my-skill\ndescription: Valid.\nlicense: MIT\ncompatibility: Works everywhere.\n---\n"
    with tempfile.TemporaryDirectory() as tmp:
        d = make_skill(tmp, content)
        ok, msg = validate_skill(d)
        assert ok, f"Expected valid, got: {msg}"


def test_validates_own_skill():
    skill_dir = Path(__file__).parent.parent
    ok, msg = validate_skill(skill_dir)
    assert ok, f"skill-optimizer itself should be valid, got: {msg}"


def test_crlf_line_endings():
    with tempfile.TemporaryDirectory() as tmp:
        d = make_skill(
            tmp,
            "---\r\nname: my-skill\r\ndescription: A CRLF skill.\r\n---\r\n# My Skill\r\n",
        )
        ok, msg = validate_skill(d)
        assert ok, f"CRLF should be accepted, got: {msg}"


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    passed = 0
    failed = 0
    for t in tests:
        try:
            t()
            passed += 1
            print(f"  PASS  {t.__name__}")
        except AssertionError as e:
            failed += 1
            print(f"  FAIL  {t.__name__}: {e}")
        except Exception as e:
            failed += 1
            print(f"  ERROR {t.__name__}: {type(e).__name__}: {e}")
    print(f"\n{passed} passed, {failed} failed out of {passed + failed}")
    sys.exit(1 if failed else 0)
