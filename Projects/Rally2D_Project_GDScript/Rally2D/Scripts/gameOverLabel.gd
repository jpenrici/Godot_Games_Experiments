extends Label

var screen_size
var posY
var posX

func _ready():
	screen_size = get_viewport().size
	posY = rect_position.y
	posX = rect_position.x
	
func _process(_delta):
	var energy = get_parent().get_parent().get_node("Player").Energy()
	if (energy <= 0):
		rect_position = Vector2(screen_size.x / 2, posY)
	else:
		rect_position = Vector2(posX, posY)
