extends Object

class_name Util

const IMAGE_PATH = "res://Textures/"

static func loadImage(var directory, var filename):
	var list = []
	var texture = ImageTexture.new()
	for i in range(500):
		var path = IMAGE_PATH + directory + "/" + filename + String(i) + ".png"
		var fileExists = File.new().file_exists(path)
		if fileExists:
			texture = load(path)
			list += [texture]
	print(directory + " ok ...")
	return list
