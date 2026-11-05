import argparse
import os
from pathlib import Path


DEFAULT_EXCLUDES = {
    ".git",
    "__pycache__",
    "node_modules",
    ".venv",
    "venv",
    "dist",
    "build"
}


def print_tree(path, depth, current_depth=0, show_files=True,
               excludes=None, prefix=""):
    if current_depth >= depth:
        return

    try:
        entries = sorted(
            (
                entry for entry in path.iterdir()
                if entry.name not in excludes
                and (show_files or entry.is_dir())
            ),
            key=lambda entry: (not entry.is_dir(), entry.name.lower())
        )
    except PermissionError:
        return

    for index, entry in enumerate(entries):
        is_last = index == len(entries) - 1

        connector = "└── " if is_last else "├── "
        next_prefix = prefix + ("    " if is_last else "│   ")

        print(prefix + connector + entry.name)

        if entry.is_dir():
            print_tree(
                entry,
                depth,
                current_depth + 1,
                show_files,
                excludes,
                next_prefix
            )


def main():
    parser = argparse.ArgumentParser(
        description="Display directory tree with configurable depth."
    )

    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Directory to inspect (default: current directory)"
    )

    parser.add_argument(
        "-d", "--depth",
        type=int,
        default=3,
        help="Maximum directory depth (default: 3)"
    )

    parser.add_argument(
        "-a", "--all",
        action="store_true",
        help="Include files"
    )

    parser.add_argument(
        "-x", "--exclude",
        nargs="*",
        default=[],
        help="Names of directories/files to exclude"
    )

    args = parser.parse_args()

    if args.depth < 0:
        parser.error("Depth cannot be negative.")

    root = Path(args.path).resolve()

    if not root.exists():
        parser.error(f"Path does not exist: {root}")

    if not root.is_dir():
        parser.error(f"Path is not a directory: {root}")

    excludes = DEFAULT_EXCLUDES | set(args.exclude)

    print(root.name or str(root))

    print_tree(
        root,
        depth=args.depth,
        show_files=args.all,
        excludes=excludes
    )


if __name__ == "__main__":
    main()
