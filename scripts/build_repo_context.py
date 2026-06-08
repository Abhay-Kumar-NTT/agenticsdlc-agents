"""
build_repo_context.py

Walks a cloned repository and produces a single Markdown context file
suitable for passing to an LLM agent as --input.

Usage:
    python scripts/build_repo_context.py --repo-path <dir> --output <file>
"""

import argparse
import os
import pathlib
import sys

# File extensions treated as text/source code
TEXT_EXTENSIONS = {
    ".py", ".js", ".ts", ".tsx", ".jsx", ".java", ".go", ".rb", ".php",
    ".cs", ".cpp", ".c", ".h", ".hpp", ".rs", ".swift", ".kt", ".scala",
    ".sh", ".bash", ".zsh", ".fish", ".ps1",
    ".html", ".css", ".scss", ".less", ".vue", ".svelte",
    ".json", ".yaml", ".yml", ".toml", ".ini", ".cfg", ".conf", ".env.example",
    ".xml", ".graphql", ".proto",
    ".md", ".mdx", ".rst", ".txt",
    ".sql", ".prisma",
    ".dockerfile", ".tf", ".hcl",
    ".gradle", ".maven",
    "Makefile", "Dockerfile", "Jenkinsfile", "Procfile",
}

# Directories to always skip
SKIP_DIRS = {
    ".git", "node_modules", ".venv", "venv", "__pycache__", ".pytest_cache",
    "dist", "build", ".next", ".nuxt", "target", "vendor", "bin", "obj",
    ".idea", ".vscode", "coverage", ".nyc_output", "logs", "tmp", ".cache",
}

MAX_FILE_BYTES = 100_000   # skip individual files larger than 100 KB
MAX_TOTAL_CHARS = 800_000  # stop adding files once context exceeds ~800K chars


def is_text_file(path: pathlib.Path) -> bool:
    suffix = path.suffix.lower()
    if suffix in TEXT_EXTENSIONS or path.name in TEXT_EXTENSIONS:
        return True
    # No extension — try reading a small chunk to detect binary
    if not suffix:
        try:
            with open(path, "rb") as f:
                chunk = f.read(512)
            return b"\x00" not in chunk
        except OSError:
            return False
    return False


def walk_repo(repo_path: pathlib.Path):
    """Yield (relative_path_str, content_str) for every readable text file."""
    for root, dirs, files in os.walk(repo_path):
        # Prune skip dirs in-place so os.walk doesn't descend into them
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
        for fname in sorted(files):
            fpath = pathlib.Path(root) / fname
            rel = fpath.relative_to(repo_path)
            if not is_text_file(fpath):
                continue
            if fpath.stat().st_size > MAX_FILE_BYTES:
                yield str(rel), f"[skipped — file too large ({fpath.stat().st_size} bytes)]"
                continue
            try:
                content = fpath.read_text(encoding="utf-8", errors="replace")
                yield str(rel), content
            except OSError as e:
                yield str(rel), f"[error reading file: {e}]"


def build_context(repo_path: pathlib.Path, repo_label: str) -> str:
    lines = [
        f"# Repository: {repo_label}",
        "",
        "The following is the complete source code and configuration of the repository.",
        "Files are listed in directory order. Binary files, build artefacts, and",
        f"dependency directories ({', '.join(sorted(SKIP_DIRS))}) are excluded.",
        "",
    ]

    # Directory tree overview first
    lines.append("## Directory Structure")
    lines.append("")
    lines.append("```")
    for root, dirs, files in os.walk(repo_path):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
        depth = len(pathlib.Path(root).relative_to(repo_path).parts)
        indent = "  " * depth
        folder_name = pathlib.Path(root).name if depth > 0 else repo_label
        lines.append(f"{indent}{folder_name}/")
        sub_indent = "  " * (depth + 1)
        for f in sorted(files):
            lines.append(f"{sub_indent}{f}")
    lines.append("```")
    lines.append("")

    # File contents
    lines.append("## File Contents")
    lines.append("")

    total_chars = sum(len(l) for l in lines)
    truncated = False

    for rel_path, content in walk_repo(repo_path):
        section = (
            f"### `{rel_path}`\n"
            f"\n"
            f"```{pathlib.Path(rel_path).suffix.lstrip('.')}\n"
            f"{content}\n"
            f"```\n"
            f"\n"
        )
        if total_chars + len(section) > MAX_TOTAL_CHARS:
            lines.append(
                f"_[Context limit reached — remaining files omitted. "
                f"Analyse based on the structure and files shown above.]_\n"
            )
            truncated = True
            break
        lines.append(section)
        total_chars += len(section)

    if not truncated:
        lines.append("_[End of repository]_\n")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Build LLM context from a cloned repo")
    parser.add_argument("--repo-path", required=True, help="Path to the cloned repository")
    parser.add_argument("--output", required=True, help="Output context file path")
    parser.add_argument("--label", default="", help="Human-readable repo label (e.g. owner/repo)")
    args = parser.parse_args()

    repo_path = pathlib.Path(args.repo_path).resolve()
    if not repo_path.is_dir():
        print(f"Error: repo path does not exist or is not a directory: {repo_path}", file=sys.stderr)
        sys.exit(1)

    label = args.label or repo_path.name
    print(f"Building context for: {label} ({repo_path})")

    context = build_context(repo_path, label)

    out = pathlib.Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(context, encoding="utf-8")

    char_count = len(context)
    print(f"Context written to: {out} ({char_count:,} chars)")


if __name__ == "__main__":
    main()
