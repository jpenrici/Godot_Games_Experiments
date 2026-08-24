#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys

from dataclasses import dataclass
from pathlib import Path

GODOT_CPP_URL = "https://github.com/godotengine/godot-cpp.git"
DEFAULT_VERSION = "godot-4.5-stable"
MENU_TAG_LIMIT = 5
NAME_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
TAG_RE = re.compile(r"^(?:godot-)?\d+\.\d+(?:\.\d+)?(?:[-+._A-Za-z0-9]*)?$")


class GeneratorError(RuntimeError):
    pass


@dataclass(frozen=True, slots=True)
class ProjectConfig:
    """Fully resolved settings for generating one GDExtension project.

    Attributes:
        root: Output directory for the generated project.
        project_name: Godot project display name.
        extension_name: Snake_case name used for the C++ extension/class/files.
        godot_cpp_tag: Normalized git tag of godot-cpp to check out.
        godot_cpp_path: Path to the godot-cpp submodule (usually root/godot-cpp).
        init_git: Whether to initialize/use a Git repository at root.
        build_now: Whether to configure and build immediately after generation.
    """

    root: Path
    project_name: str
    extension_name: str
    godot_cpp_tag: str
    godot_cpp_path: Path
    init_git: bool
    build_now: bool


def main() -> int:
    """Entry point: resolve configuration, generate the project, and optionally build it.

    Runs either non-interactively (if any of --output/--project/--extension/
    --godot-cpp is given, all four must be given) or interactively otherwise.
    Writes project files, sets up the godot-cpp submodule at the requested
    tag, optionally stages everything with `git add`, and optionally runs
    a CMake/Ninja build. Returns a process exit code.

    Everything called here (require_tools, parse_args, interactive,
    write_files, ensure_godot_cpp, build, ...) is implemented further down
    in this file. That's fine in Python: a function body is only resolved
    when it *runs*, not when it's *defined*, so by the time main() actually
    executes (via the `if __name__ == "__main__":` guard at the bottom of
    the file) every name it references has already been defined.
    """
    if sys.version_info < (3, 13):
        print("Python 3.13+ is required.", file=sys.stderr)
        return 2

    try:
        require_tools()
        args = parse_args()
        values = (args.output, args.project, args.extension, args.godot_cpp)

        if any(v is not None for v in values):
            if not all(v is not None for v in values):
                raise GeneratorError(
                    "Non-interactive mode requires --output, --project, "
                    "--extension and --godot-cpp."
                )
            root = args.output.expanduser().resolve()
            ensure_safe_output(root)
            config = ProjectConfig(
                root,
                validate_name(args.project, "Project name"),
                validate_name(args.extension, "Extension name"),
                normalize_tag(args.godot_cpp),
                root / "godot-cpp",
                not args.no_git_init,
                args.build,
            )
        else:
            config = interactive()
            ensure_safe_output(config.root)

        write_files(config)

        if config.init_git and not git_repo_exists(config.root):
            run("git", "init", str(config.root))

        ensure_godot_cpp(config)

        if config.init_git:
            run("git", "add", ".", cwd=config.root)
            run("git", "status", "--short", cwd=config.root)

        if config.build_now:
            build(config)

        print(f"\nDone: {config.root}")
        return 0

    except KeyboardInterrupt:
        print("\nCancelled.")
        return 130
    except (GeneratorError, ValueError, subprocess.CalledProcessError) as exc:
        print(f"\nERROR: {exc}", file=sys.stderr)
        return 1


# ---------------------------------------------------------------------------
# Implementation of the helpers used by main() above.
# ---------------------------------------------------------------------------


def run(
    *args: str, cwd: Path | None = None, check: bool = True, capture: bool = False
) -> subprocess.CompletedProcess[str]:
    """Run an external command, echoing it first for visibility.

    Wraps subprocess.run with sensible defaults for this script: text mode,
    stderr merged into stdout, and optional output capture.
    """
    print("$", " ".join(args))
    return subprocess.run(
        args,
        cwd=cwd,
        check=check,
        text=True,
        stdout=subprocess.PIPE if capture else None,
        stderr=subprocess.STDOUT if capture else None,
    )


def require_tools() -> None:
    """Ensure that git and cmake are available on PATH, raising if not."""
    missing = [x for x in ("git", "cmake") if shutil.which(x) is None]
    if missing:
        raise GeneratorError(f"Missing required tools: {', '.join(missing)}")


def validate_name(value: str, label: str) -> str:
    """Validate that value is a safe C/C++ identifier-style name.

    Strips surrounding whitespace and checks against NAME_RE. Raises
    ValueError with a message referencing `label` if the name is invalid.
    """
    value = value.strip()
    if not NAME_RE.fullmatch(value):
        raise ValueError(
            f"{label} must match {NAME_RE.pattern!r}; use letters, digits "
            "and '_' and do not start with a digit."
        )
    return value


def normalize_tag(value: str) -> str:
    """Normalize a user-supplied godot-cpp version string into a tag name.

    Strips a leading "refs/tags/" prefix, validates the result against
    TAG_RE, and ensures the returned tag starts with "godot-".
    """
    value = value.strip().removeprefix("refs/tags/")
    if not value or not TAG_RE.fullmatch(value):
        raise ValueError(f"Invalid godot-cpp tag: {value!r}")
    return value if value.startswith("godot-") else f"godot-{value}"


def available_tags(limit: int = 40) -> list[str]:
    """Fetch and return the most recent godot-cpp release tags.

    Queries the remote repository's tags via `git ls-remote`, filters to
    well-formed "godot-*" version tags, and returns up to `limit` of them
    sorted newest first by parsed (major, minor, patch) version.
    """
    result = run(
        "git",
        "ls-remote",
        "--tags",
        "--refs",
        GODOT_CPP_URL,
        capture=True,
    )
    tags: list[str] = []
    for line in result.stdout.splitlines():
        if "\t" not in line:
            continue
        tag = line.split("\t", 1)[1].removeprefix("refs/tags/")
        if tag.startswith("godot-") and TAG_RE.fullmatch(tag):
            tags.append(tag)

    def version_key(tag: str) -> tuple[int, ...]:
        return tuple(int(n) for n in re.findall(r"\d+", tag)[:3])

    return sorted(set(tags), key=version_key, reverse=True)[:limit]


def choose_tag(non_interactive: str | None = None) -> str:
    """Determine which godot-cpp tag to use.

    If `non_interactive` is given, it is normalized and returned directly.
    Otherwise, this fetches the available tags from the remote and prompts
    the user to pick one (by number, "c" for a custom tag, or "q" to
    cancel via KeyboardInterrupt). Falls back to a free-text prompt if the
    tag list could not be fetched.
    """
    if non_interactive:
        return normalize_tag(non_interactive)

    print("\nFetching available godot-cpp tags...")
    try:
        tags = available_tags()
    except subprocess.CalledProcessError:
        tags = []

    if not tags:
        return normalize_tag(input("Could not list tags. Enter godot-cpp tag: "))

    # Only show the most recent MENU_TAG_LIMIT tags to keep the CLI menu
    # readable; older releases remain reachable via the "custom tag" option.
    menu_tags = tags[:MENU_TAG_LIMIT]
    default_index = (
        menu_tags.index(DEFAULT_VERSION) if DEFAULT_VERSION in menu_tags else 0
    )
    for index, tag in enumerate(menu_tags, 1):
        marker = " [default]" if index - 1 == default_index else ""
        print(f"  {index:2d}) {tag}{marker}")
    print("   c) custom tag")
    print("   q) cancel")

    while True:
        answer = input(f"Select [{default_index + 1}]: ").strip().lower()
        if not answer:
            return menu_tags[default_index]
        if answer == "q":
            raise KeyboardInterrupt
        if answer == "c":
            return normalize_tag(input("Custom tag: "))
        if answer.isdigit() and 1 <= int(answer) <= len(menu_tags):
            return menu_tags[int(answer) - 1]
        print("Invalid selection.")


def ask(prompt: str, default: str) -> str:
    """Prompt the user for input, returning `default` if they enter nothing."""
    value = input(f"{prompt} [{default}]: ").strip()
    return value or default


def git_repo_exists(path: Path) -> bool:
    """Return True if `path` is (or is inside) an existing Git working tree."""
    if (path / ".git").exists():
        return True
    return (
        run(
            "git",
            "-C",
            str(path),
            "rev-parse",
            "--is-inside-work-tree",
            check=False,
            capture=True,
        ).returncode
        == 0
    )


def ensure_safe_output(path: Path) -> None:
    """Guard against generating into a non-empty or non-directory path.

    Raises GeneratorError if `path` already exists and is either not a
    directory or is a non-empty directory, so existing files are never
    silently overwritten.
    """
    if path.exists() and (not path.is_dir() or any(path.iterdir())):
        raise GeneratorError(
            f"Output directory is not empty: {path}. "
            "No existing files will be overwritten."
        )


def ensure_godot_cpp(config: ProjectConfig) -> None:
    """Ensure the godot-cpp checkout exists and is set to the right tag.

    If godot-cpp is missing, it is fetched one of two ways depending on
    `config.init_git`:
      - True: added as a proper Git submodule of `config.root` (a Git
        repository is initialized at `config.root` first if needed, so
        the pin is tracked in .gitmodules).
      - False: fetched as a plain, standalone `git clone` into
        `config.godot_cpp_path`, with no repository required or created
        at `config.root` and no submodule tracking. This is what lets
        "don't touch Git for my project" actually work, since
        `git submodule add` always requires a parent repository.
    If godot-cpp already exists but isn't a Git checkout, that's an
    error. Either way, the checkout is then fetched and switched
    (detached HEAD) to `config.godot_cpp_tag`.
    """
    cpp = config.godot_cpp_path

    if not cpp.exists():
        if config.init_git:
            if not git_repo_exists(config.root):
                run("git", "init", str(config.root))
            run("git", "submodule", "add", GODOT_CPP_URL, "godot-cpp", cwd=config.root)
        else:
            run("git", "clone", GODOT_CPP_URL, str(cpp))
            print(
                "Note: Git initialization is disabled, so godot-cpp was "
                "fetched as a standalone clone (not a submodule). Its "
                "version pin is not tracked by any repository of yours."
            )
    elif not (cpp / ".git").exists():
        raise GeneratorError(f"{cpp} exists but is not a Git checkout.")

    run(
        "git",
        "fetch",
        "--tags",
        "--depth",
        "1",
        "origin",
        config.godot_cpp_tag,
        cwd=cpp,
    )
    run("git", "checkout", "--detach", config.godot_cpp_tag, cwd=cpp)


def class_name(extension: str) -> str:
    """Derive a PascalCase C++ class name from a snake_case extension name.

    Unlike str.capitalize(), this only uppercases the first character of
    each underscore-separated part and leaves the rest untouched, so
    "myCoolExt" stays "MyCoolExt" instead of becoming "Mycoolext".
    """
    return "".join(part[:1].upper() + part[1:] for part in extension.split("_") if part)


def source_files(config: ProjectConfig) -> dict[str, str]:
    """Build the C++ source/header file contents for the extension.

    Returns a mapping of relative file path -> file content covering the
    extension's Sprite2D-derived class (header + implementation) and the
    GDExtension registration entry point (register_types.h/.cpp).
    """
    ext = config.extension_name
    cls = class_name(ext)
    return {
        f"src/{ext}.h": f"""#ifndef {ext.upper()}_H
#define {ext.upper()}_H

#include <godot_cpp/classes/sprite2d.hpp>

namespace godot {{

class {cls} : public Sprite2D {{
    GDCLASS({cls}, Sprite2D)

private:
    int variable;

protected:
    static void _bind_methods();

public:
    {cls}();
    ~{cls}();

    void _ready();
    void _process(double delta);
}};

}} // namespace godot

#endif // {ext.upper()}_H
""",
        f"src/{ext}.cpp": f"""#include "{ext}.h"

#include <godot_cpp/core/class_db.hpp>

using namespace godot;

void {cls}::_bind_methods()
{{
    // Pass
}}

{cls}::{cls}() {{
    // Initialize any variables here.
    variable = 1;
}}

{cls}::~{cls}() {{
    // Add your cleanup here.
}}

void {cls}::_ready()
{{
    // Pass
}}

void {cls}::_process(double delta)
{{
    // Pass
}}
""",
        "src/register_types.h": f"""#ifndef {ext.upper()}_REGISTER_TYPES_H
#define {ext.upper()}_REGISTER_TYPES_H

#include <godot_cpp/core/class_db.hpp>

using namespace godot;

void initialize_{ext}_module(ModuleInitializationLevel p_level);
void uninitialize_{ext}_module(ModuleInitializationLevel p_level);

#endif // {ext.upper()}_REGISTER_TYPES_H
""",
        "src/register_types.cpp": f"""#include "register_types.h"

#include "{ext}.h"

#include <gdextension_interface.h>
#include <godot_cpp/core/defs.hpp>
#include <godot_cpp/core/class_db.hpp>
#include <godot_cpp/godot.hpp>

using namespace godot;

void initialize_{ext}_module(ModuleInitializationLevel p_level) {{

    if (p_level != MODULE_INITIALIZATION_LEVEL_SCENE) {{
        return;
    }}

    ClassDB::register_class<{cls}>();
}}

void uninitialize_{ext}_module(ModuleInitializationLevel p_level) {{
    if (p_level != MODULE_INITIALIZATION_LEVEL_SCENE) {{
        return;
    }}
}}

extern "C" {{
    // Initialization.
    GDExtensionBool GDE_EXPORT {ext}_library_init(GDExtensionInterfaceGetProcAddress p_get_proc_address, const GDExtensionClassLibraryPtr p_library, GDExtensionInitialization *r_initialization)
    {{
        godot::GDExtensionBinding::InitObject init_obj(p_get_proc_address, p_library, r_initialization);

        init_obj.register_initializer(initialize_{ext}_module);
        init_obj.register_terminator(uninitialize_{ext}_module);
        init_obj.set_minimum_library_initialization_level(MODULE_INITIALIZATION_LEVEL_SCENE);

        return init_obj.init();
    }}
}} // extern "C"
""",
    }


def project_files(config: ProjectConfig) -> dict[str, str]:
    """Build the non-C++ project file contents for the generated project.

    Returns a mapping of relative file path -> file content covering
    CMakeLists.txt, project.godot, the .gdextension descriptor,
    .gitignore, and README.md.
    """
    ext = config.extension_name
    return {
        "CMakeLists.txt": f"""cmake_minimum_required(VERSION 3.24)
project({config.project_name} LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

add_subdirectory(godot-cpp)

add_library({ext} SHARED
    src/{ext}.cpp
    src/register_types.cpp
)

target_include_directories({ext} PRIVATE "${{CMAKE_CURRENT_SOURCE_DIR}}/src")
target_link_libraries({ext} PRIVATE godot-cpp)

if(WIN32)
    set(GDEXT_PLATFORM "windows")
elseif(APPLE)
    set(GDEXT_PLATFORM "macos")
else()
    set(GDEXT_PLATFORM "linux")
endif()

if(CMAKE_SYSTEM_PROCESSOR MATCHES "^(arm64|aarch64)$")
    set(GDEXT_ARCH "arm64")
else()
    set(GDEXT_ARCH "x86_64")
endif()

set_target_properties({ext} PROPERTIES
    PREFIX ""
    OUTPUT_NAME "{ext}.${{GDEXT_PLATFORM}}.${{GDEXT_ARCH}}"
    RUNTIME_OUTPUT_DIRECTORY "${{CMAKE_CURRENT_SOURCE_DIR}}/bin"
    LIBRARY_OUTPUT_DIRECTORY "${{CMAKE_CURRENT_SOURCE_DIR}}/bin"
    ARCHIVE_OUTPUT_DIRECTORY "${{CMAKE_CURRENT_SOURCE_DIR}}/bin"
)

if(WIN32)
    set_target_properties({ext} PROPERTIES SUFFIX ".dll")
elseif(APPLE)
    set_target_properties({ext} PROPERTIES SUFFIX ".dylib")
else()
    set_target_properties({ext} PROPERTIES SUFFIX ".so")
endif()
""",
        "project.godot": f"""config_version=5

[application]

config/name="{config.project_name}"

[rendering]

renderer/rendering_method="gl_compatibility"
renderer/rendering_method.mobile="gl_compatibility"
""",
        f"{ext}.gdextension": f"""[configuration]

entry_symbol = "{ext}_library_init"
compatibility_minimum = "4.3"

[libraries]

linux.x86_64 = "res://bin/{ext}.linux.x86_64.so"
windows.x86_64 = "res://bin/{ext}.windows.x86_64.dll"
macos.arm64 = "res://bin/{ext}.macos.arm64.dylib"
macos.x86_64 = "res://bin/{ext}.macos.x86_64.dylib"
""",
        ".gitignore": """build/
cmake-build*/
compile_commands.json
.vscode/
.idea/
*.user
*.user.*
""",
        "README.md": f"""# {config.project_name}

Generated C++ GDExtension.

- Build system: CMake
- Python generator: 3.13+
- godot-cpp: `{config.godot_cpp_tag}`
- `godot-cpp` is pinned as a Git submodule.

## Build

```bash
cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=Debug
cmake --build build
```

The extension is emitted into `bin/`.

To change the binding version:

```bash
git -C godot-cpp fetch --tags
git -C godot-cpp checkout --detach <godot-cpp-tag>
git add godot-cpp
git commit -m "Update godot-cpp"
```
""",
    }


def write_files(config: ProjectConfig) -> None:
    """Create the output directory and write all generated project files to disk."""
    config.root.mkdir(parents=True, exist_ok=True)
    for relative, content in {**project_files(config), **source_files(config)}.items():
        path = config.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        print("created", path.relative_to(config.root))


def build(config: ProjectConfig) -> None:
    """Configure the project with CMake/Ninja and build it in Debug mode."""
    build_dir = config.root / "build"
    run(
        "cmake",
        "-S",
        ".",
        "-B",
        str(build_dir),
        "-G",
        "Ninja",
        "-DCMAKE_BUILD_TYPE=Debug",
        cwd=config.root,
    )
    run("cmake", "--build", str(build_dir), "--parallel", cwd=config.root)


def interactive() -> ProjectConfig:
    """Prompt the user interactively for all project settings.

    Collects the output directory, project name, extension name,
    godot-cpp tag, and the git-init/build-now flags, shows a summary, and
    asks for final confirmation before returning a ProjectConfig. Raises
    KeyboardInterrupt if the user cancels.
    """
    print("=" * 64)
    print(" Godot C++ GDExtension Creator — CMake / Python 3.13+")
    print("=" * 64)

    root = (
        Path(ask("Output directory", str(Path.cwd() / "GDExtension_Example")))
        .expanduser()
        .resolve()
    )

    project = validate_name(ask("Godot project name", "Demo"), "Project name")
    extension = validate_name(
        ask("C++ extension/class name", "example"), "Extension name"
    )
    tag = choose_tag()

    init_git = ask("Initialize Git repository if needed? Y/N", "Y").lower() in {
        "y",
        "yes",
    }
    build_now = ask("Configure and build after generation? Y/N", "N").lower() in {
        "y",
        "yes",
    }

    print(f"\nOutput:    {root}")
    print(f"Project:   {project}")
    print(f"Extension: {extension}")
    print(f"godot-cpp: {tag}")

    if input("\nCreate project? [Y/n] ").strip().lower() in {"n", "no"}:
        raise KeyboardInterrupt

    return ProjectConfig(
        root, project, extension, tag, root / "godot-cpp", init_git, build_now
    )


def parse_args() -> argparse.Namespace:
    """Define and parse the script's command-line arguments for non-interactive mode."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument("--project")
    parser.add_argument("--extension")
    parser.add_argument("--godot-cpp", dest="godot_cpp")
    parser.add_argument("--no-git-init", action="store_true")
    parser.add_argument("--build", action="store_true")
    return parser.parse_args()


if __name__ == "__main__":
    raise SystemExit(main())
