# Project GDExtension

This is an example Godot project that uses the C++ language.<br>

## Details

Follow the steps below to finish creating a Godot Project.<br>

1. Open Godot Engine and create a project in:
#ROOT#/#PROJECT#
2. Make sure there are no errors when importing the extension ("#GDEXTENSION#").
3. If necessary, recompile using Scons in:
#ROOT#
4. Make sure the extension is accessible by adding a new node or object ("#GDEXTENSION#").
5. Modify this README to document your project.

The "#GDEXTENSION#" extension in C++ needs to be implemented to perform actions.
Learn more at https://docs.godotengine.org/en/stable/tutorials/scripting/gdextension/index.html.

## Requeriments

- python
- scons
- gcc

## Run

1. Go to the "#ROOT#" directory.
2. Open the terminal and compile `SConstruct` by running the command `scons -Q`.
3. Recompile whenever you modify the C++ code in the `\src` directory.
4. Open the Godot project.

## Structure

<code>
#ROOT#/<br>
|<br>
|&nbsp;&nbsp;# Game project<br>
+--#PROJECT#/<br>				
|&nbsp;&nbsp;|<br>
|&nbsp;&nbsp;+--project.godot<br>
|&nbsp;&nbsp;|<br>
|&nbsp;&nbsp;# GDExtension<br>
|&nbsp;&nbsp;+--#GDEXTENSION#.gdextension<br>
|&nbsp;&nbsp;|<br>
|&nbsp;&nbsp;+--bin/<br>
|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|<br>
|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;+--libraries&nbsp;# Built with Scons<br>
|<br>
+--godot-cpp/&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# C++ bindings<br>
|<br>
+--src/&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# Extension source code<br>
|&nbsp;&nbsp;&nbsp;|<br>
|&nbsp;&nbsp;&nbsp;+--register_types.cpp<br>
|&nbsp;&nbsp;&nbsp;+--register_types.h<br>
|&nbsp;&nbsp;&nbsp;+--#GDEXTENSION#.cpp<br>
|&nbsp;&nbsp;&nbsp;+--#GDEXTENSION#.h<br>
|<br>
|&nbsp;Sconstruct&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# SCons script<br>
</code>

## References

[Godot Engine](https://godotengine.org/) : A free, all-in-one and cross-platform game engine to create 2D and 3D games.<br>
[GDExtension](https://docs.godotengine.org/en/stable/tutorials/scripting/gdextension/index.html) : Documentation.<br>
<br>
[Scons](https://scons.org/) : Open Source software construction tool.<br>
[Python](https://www.python.org/) : Official site.<br>