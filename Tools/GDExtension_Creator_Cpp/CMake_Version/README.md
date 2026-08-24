# GDExtension_Creator_Cpp

Modern replacement for the original `Tools/GDExtension_Creator_Cpp/SCons_Version`.

## What changed

- SCons was removed from the generated project; CMake consumes the official `godot-cpp/CMakeLists.txt`.
- The CLI interactively lists tags from the official `godotengine/godot-cpp` repository.
- `godot-cpp` is managed as a real Git submodule and pinned to the selected tag.
- Existing non-empty output directories are rejected instead of being overwritten.
- Generated C++/Godot/CMake files are assembled directly by Python. There is no `resources/` template directory.
- A deterministic CLI mode is available for CI and automation.

## Usage

Interactive:

```bash
python3 create.py
```

Deterministic:

```bash
python3 create.py \
  --output ./MyExtension \
  --project MyGame \
  --extension my_extension \
  --godot-cpp godot-4.5-stable
```

Build immediately:

```bash
python3 create.py \
  --output ./MyExtension \
  --project MyGame \
  --extension my_extension \
  --godot-cpp godot-4.5-stable \
  --build
```

Prerequisites: Python 3.13+, Git, CMake and a C++ compiler. Ninja is recommended.

For stable Godot projects, select the `godot-cpp` tag matching the Godot version you target.

## References

[Godot Engine](https://godotengine.org/) : A free, all-in-one and cross-platform game engine to create 2D and 3D games.<br>
[GDExtension](https://docs.godotengine.org/en/stable/tutorials/scripting/gdextension/index.html) : Documentation.<br>
<br>
[Python](https://www.python.org/) : Official site.<br>
