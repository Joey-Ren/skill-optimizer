#!/usr/bin/env python3
"""Quick validation script for skills — zero external dependencies."""

import sys
import re
from pathlib import Path


def validate_skill(skill_path):
    skill_path = Path(skill_path)

    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return False, "SKILL.md not found"

    content = skill_md.read_text()
    if not content.startswith("---"):
        return False, "No YAML frontmatter found"

    match = re.match(r"^---\r?\n(.*?)\r?\n---", content, re.DOTALL)
    if not match:
        return False, "Invalid frontmatter format"

    frontmatter_text = match.group(1)

    ALLOWED_PROPERTIES = {
        "name",
        "description",
        "license",
        "allowed-tools",
        "metadata",
        "compatibility",
    }
    top_level_keys = set(
        re.findall(r"^([a-z][a-z0-9-]*):", frontmatter_text, re.MULTILINE)
    )

    unexpected_keys = top_level_keys - ALLOWED_PROPERTIES
    if unexpected_keys:
        return False, (
            f"Unexpected key(s) in SKILL.md frontmatter: {', '.join(sorted(unexpected_keys))}. "
            f"Allowed properties are: {', '.join(sorted(ALLOWED_PROPERTIES))}"
        )

    name_match = re.search(r"^name:\s*(.+)$", frontmatter_text, re.MULTILINE)
    if not name_match:
        return False, "Missing 'name' in frontmatter"
    name = name_match.group(1).strip().strip('"').strip("'")

    if name:
        if not re.match(r"^[a-z0-9-]+$", name):
            return (
                False,
                f"Name '{name}' should be kebab-case (lowercase letters, digits, and hyphens only)",
            )
        if name.startswith("-") or name.endswith("-") or "--" in name:
            return (
                False,
                f"Name '{name}' cannot start/end with hyphen or contain consecutive hyphens",
            )
        if len(name) > 64:
            return (
                False,
                f"Name is too long ({len(name)} characters). Maximum is 64 characters.",
            )

    desc_match = re.search(r"^description:", frontmatter_text, re.MULTILINE)
    if not desc_match:
        return False, "Missing 'description' in frontmatter"

    desc_line = re.search(r"^description:\s*(.*)$", frontmatter_text, re.MULTILINE)
    desc_value = desc_line.group(1).strip() if desc_line else ""

    if desc_value in (">", "|", ">-", "|-", ""):
        continuation = []
        lines = frontmatter_text.split("\n")
        found_desc = False
        for line in lines:
            if found_desc:
                if line.startswith("  ") or line.startswith("\t"):
                    continuation.append(line.strip())
                else:
                    break
            if line.startswith("description:"):
                found_desc = True
        description = " ".join(continuation)
    else:
        description = desc_value.strip('"').strip("'")

    if description:
        if "<" in description or ">" in description:
            return False, "Description cannot contain angle brackets (< or >)"
        if len(description) > 1024:
            return (
                False,
                f"Description is too long ({len(description)} characters). Maximum is 1024 characters.",
            )

    compatibility_match = re.search(
        r"^compatibility:\s*(.+)$", frontmatter_text, re.MULTILINE
    )
    if compatibility_match:
        compat = compatibility_match.group(1).strip().strip('"').strip("'")
        if len(compat) > 500:
            return (
                False,
                f"Compatibility is too long ({len(compat)} characters). Maximum is 500 characters.",
            )

    return True, "Skill is valid!"


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python quick_validate.py <skill_directory>")
        sys.exit(1)

    valid, message = validate_skill(sys.argv[1])
    print(message)
    sys.exit(0 if valid else 1)
