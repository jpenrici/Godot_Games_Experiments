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
GDVERSION = "4.1"


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

    # Names
    projectName = "Demo" if projectName == "" else projectName.strip()
    directoryName = "GDExtension_Example" if directoryName == "" else directoryName.strip()
    gdextensionName = "example" if gdextensionName == "" else gdextensionName.strip().replace(' ', '')
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
            result = input("The godot-cpp library was not found!\nWant to download the repository from GitHub. Yes or No [Y/N]?")
            if result.upper() == 'Y':
                print("Download: {}".format(repository))
                os.system("git clone -b {} {} {}".format(GDVERSION, repository, godotCpp))
            else:
                print("\nCopy or enter a path from the godot-cpp library!")
                print("Change the SConstruct file in the root directory before compiling using SCons!")
                print("Consult the official documentation of the SCons package!")
                result = input("Press Enter to continue.")
        except Exception as e:
            print("Something went wrong when cloning the godot-cpp repository!")
            raise e

    # Files
    paths = [
        [RESOURCES, "gdexample.h", source, gdextensionName + ".h"],
        [RESOURCES, "gdexample.cpp", source, gdextensionName + ".cpp"],
        [RESOURCES, "register_types.h", source, "register_types.h"],
        [RESOURCES, "register_types.cpp", source, "register_types.cpp"],
        [RESOURCES, "SConstruct", root, "SConstruct"],
        [RESOURCES, "message.md", root, "README.md"]
    ]
    for pathIn, fileIn, pathOut, fileOut in paths:
        text = load("{}/{}".format(pathIn, fileIn))
        text = text.replace("#GDEXTENSION#", gdextensionName)
        text = text.replace("#GDEXTENSIONH#", gdextensionName.upper())
        text = text.replace("#GDEXTENSIONCLASS#", gdextensionName.title())
        text = text.replace("#PROJECT#", projectName)
        text = text.replace("#ROOT#", root)
        if not save("{}/{}".format(pathOut, fileOut), text):
            exit(0)

    # Scons
    if not os.path.isdir(godotCpp):
        print("You will need the godot-cpp library in the root directory to finish!")
        exit(0)
    try:
        result = input("Do you want to run Scons? Process can take some time! Yes or No [Y/N]?")
        if result.upper() == 'Y':
            os.system("scons -j4 -Q --directory={}".format(root))
        else:
            print("Skip Scons ...")
    except Exception as e:
        print("Something went wrong when running Scons!")   

    # Exit
    print("\n\nRead the \"README\" file in {}\n".format(root))


if __name__ == '__main__':
    # Test
    print("Enter the names without special characters and numbers at the beginning!")
    print("If empty, the default will be used!\n")
    directoryName = input("Enter the name of the root directory: ")
    projectName = input("Enter the name of the project Godot: ")
    gdextensionName = input("Enter the name of the Godot extension in C++: ")
    create(directoryName, projectName, gdextensionName)
