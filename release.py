#!/usr/bin/env python3
import argparse
import subprocess
import re
from pathlib import Path
import sys


def fail(msg):
    """Print an error and exit."""
    print(f"Error: {msg}", file=sys.stderr)
    sys.exit(1)


def check_clean_git():
    """Fail if there are uncommitted changes to tracked files."""
    result = subprocess.run(
        ["git", "status", "--porcelain"], stdout=subprocess.PIPE, text=True
    )
    dirty = [
        line
        for line in result.stdout.strip().split("\n")
        if line and not line.startswith("??")
    ]
    if dirty:
        fail("Uncommitted changes present in tracked files.")


def get_current_version(file_path):
    """Return match object and full file text for galaxy.yml version line."""
    text = file_path.read_text()
    match = re.search(r"^(\s*version\s*:\s*)(\d+\.\d+\.\d+)(\s*)$", text, re.MULTILINE)
    if not match:
        fail("No valid version line found in galaxy.yml.")
    return match, text


def bump_version(old_version, mode):
    """Return new version string after bumping or replacing."""
    major, minor, patch = map(int, old_version.split("."))
    if mode == "major":
        return f"{major + 1}.0.0"
    elif mode == "minor":
        return f"{major}.{minor + 1}.0"
    elif mode == "patch":
        return f"{major}.{minor}.{patch + 1}"
    elif re.fullmatch(r"\d+\.\d+\.\d+", mode):
        return mode
    else:
        fail("Invalid version specifier. Use major, minor, patch, or explicit x.y.z")


def main():
    """Parse arguments, update version, commit and tag."""
    parser = argparse.ArgumentParser(
        description="Bump version in galaxy.yml and create git tag."
    )
    parser.add_argument("version", help="major, minor, patch, or x.y.z")
    args = parser.parse_args()

    check_clean_git()

    galaxy_file = Path("galaxy.yml")
    if not galaxy_file.exists():
        fail("galaxy.yml not found.")

    match, content = get_current_version(galaxy_file)
    old_version = match.group(2)
    new_version = bump_version(old_version, args.version)

    new_line = f"{match.group(1)}{new_version}{match.group(3)}"
    new_content = content[: match.start()] + new_line + content[match.end() :]
    galaxy_file.write_text(new_content)

    subprocess.run(["git", "add", "galaxy.yml"], check=True)
    subprocess.run(
        ["git", "commit", "-m", f"Release version v{new_version}"], check=True
    )
    subprocess.run(["git", "tag", f"v{new_version}"], check=True)

    print(f"Bumped version: {old_version} → {new_version}")
    print(f"Committed and tagged as v{new_version}.")
    print("You can now push the changes and tag with:")
    print(f"  git push origin master --tags")


if __name__ == "__main__":
    main()
