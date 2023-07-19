# Project

1. Open Godot Engine and create a project in:
#ROOT#/#PROJECT#
2. Make sure there are no errors when importing the extension ("#GDEXTENSION#").
3. If necessary, recompile using Scons in:
#ROOT#
4. Make sure the extension is accessible from the component panel.

## Details

The "#GDEXTENSION#" extension in C++ needs to be implemented to perform actions.
Learn more at https://docs.godotengine.org/en/stable/tutorials/scripting/gdextension/index.html

## Structure

#ROOT#/
|
|  # game to test the extension
+--#PROJECT#/						
|   |
|   +--project.godot
|   |
|	# GDExtension
|   +--#GDEXTENSION#.gdextension
|   |
|   +--bin/
|       |
|       +--libraries	# Built with Scons
|
+--godot-cpp/			# C++ bindings
|
+--src/         		# Extension source code
|   |
|   +--register_types.cpp
|   +--register_types.h
|   +--#GDEXTENSION#.cpp
|   +--#GDEXTENSION#.h
|
| Sconstruct		  	# SCons script