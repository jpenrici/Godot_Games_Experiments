# -*- Mode: Python3; coding: utf-8; indent-tabs-mpythoode: nil; tab-width: 4 -*-

import os
import sys
import datetime
import pkg_resources

# PATH
FULL_PATH = os.path.realpath(__file__)
PATH, FILENAME = os.path.split(FULL_PATH)
NOW = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
RESOURCES = "{}/resources".format(PATH)


def load(path):
    text = ""
    try:
        file = open(path)
        text = "".join([i for i in file])
        file.close()
        _, filename = os.path.split(path)
        print("Loaded: {}".format(filename))
    except Exception:
        print("Error: couldn't open file.\nFile: {}".format(path))
    return text


def save(path, text):
    try:
        f = open(path, "w")
        f.write(text)
        f.close()
        _, filename = os.path.split(path)
        print("Saved: {}".format(filename))
    except Exception:
        print("Error: couldn't save file.\nFile: {}".format(path))
        return False
    return True


def create(directoryName, projectName, gdextensionName):

	# Godot 
	gdversion = "4.1"

	# Names
	directoryName = "CustomGDExtension" if directoryName == "" else directoryName.strip()
	projectName = "NewProject" if projectName == "" else projectName.strip()
	gdextensionName = "customGDExtension" if gdextensionName == "" else gdextensionName.strip().replace(' ', '')
	print("Script: {}\nDate: {}\nDirectory: {}\nProject: {}\nGDExtension: {}".format(FILENAME, NOW, directoryName, projectName, gdextensionName))

	# Packages
	print("Check packages ...")
	requeriments = ['scons']
	installed_pkgs_list = sorted([i.key for i in pkg_resources.working_set])
	for pkg in requeriments:
		installed = pkg in installed_pkgs_list
		print("{}: {}".format(pkg, "ok!" if installed else "installation required!"))
		if not installed:
			print("Recommended to install packages before continuing!")
			exit(0)

	# Directories
	root = "{}/{}".format(PATH, directoryName)
	project = "{}/{}".format(root, projectName)
	godotCpp = "{}/godot-cpp".format(root)
	repository = "https://github.com/godotengine/godot-cpp"
	source = "{}/src".format(root)
	if not os.path.isdir(RESOURCES):
		print("Resources directory missing!")
		exit(0)
	if not os.path.isdir(root):
		print("Create: {}".format(root))
		os.mkdir(root)
	if not os.path.isdir(project):
		print("Create: {}".format(project))
		os.mkdir(project)
	if not os.path.isdir(source):
		print("Create: {}".format(source))
		os.mkdir(source)
	if not os.path.isdir(godotCpp):
		try:
			print("Download: {}".format(repository))
			os.system("git clone -b {} {} {}".format(gdversion, repository, godotCpp))
		except Exception as e:
			print("Something went wrong when cloning the godot-cpp repository!")
			raise e

	# Files
	actions = [
		[RESOURCES, "gdexample.h", source, gdextensionName + ".h"],
		[RESOURCES, "gdexample.cpp", source, gdextensionName + ".cpp"],
		[RESOURCES, "register_types.h", source, "register_types.h"],
		[RESOURCES, "register_types.cpp", source, "register_types.cpp"],
		[RESOURCES, "SConstruct", root, "SConstruct"],
		[RESOURCES, "message.md", root, "README.md"]
	]
	for pathIn, fileIn, pathOut, fileOut in actions:
		text = load("{}/{}".format(pathIn, fileIn))
		text = text.replace("#GDEXTENSION#", gdextensionName)
		text = text.replace("#GDEXTENSIONH#", gdextensionName.upper())
		text = text.replace("#GDEXTENSIONCLASS#", gdextensionName.title())
		text = text.replace("#PROJECT#", projectName)
		text = text.replace("#ROOT#", root)
		if not save("{}/{}".format(pathOut, fileOut), text):
			exit(0)

	# Scons
	try:
		result = input("Do you want to run Scons? Process can take some time! Yes or No [Y/N]?")
		if result.upper() == 'Y':
			os.system("scons -j4 --directory={}".format(root))
		else:
			print("Skip Scons ...")
	except Exception as e:
		print("Something went wrong when running Scons!")	


	# Exit
	print("\n\nRead the \"README\" file in {}".format(root))


if __name__ == '__main__':
	# Test
	create("GDExtension_Example", "Demo", "example")
	