extends Sprite

var list = []

func _ready():
	list = Util.loadImage("Arrow", "arrow_")
	
func _process(_delta):
	if !list.empty():
		texture = list[0]
		if Input.is_action_pressed("ui_up"):
			texture = list[1]
		if Input.is_action_pressed("ui_down"):
			texture = list[2]
		if Input.is_action_pressed("ui_left"):
			texture = list[3]
		if Input.is_action_pressed("ui_right"):
			texture = list[4]
