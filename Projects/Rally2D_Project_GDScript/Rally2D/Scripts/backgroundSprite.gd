extends Sprite

var posY

func _ready():
	posY = position.y

func _process(delta):
	var speed = get_parent().get_parent().get_node("Player").Speed()
	position += Vector2(0, 1).normalized() * speed * delta
	if position.y > get_viewport().size.y:
		position.y = posY
		get_parent().get_parent().get_node("Player").UpdateDistance()
