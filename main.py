"""Deprecated entry: prefer `pytest testcases/ --platform=oh`."""
import sys
import pytest


def main():
    args = ["testcases", "-v"]
    if "--platform" not in sys.argv:
        args.extend(["--platform", "oh"])
    args.extend(sys.argv[1:])
    raise SystemExit(pytest.main(args))


if __name__ == "__main__":
    main()
