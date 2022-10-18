extends Sprite

var screen_size
var posY
var posX

func _ready():
    screen_size = get_viewport().size
    posY = position.y
    posX = position.x
    
func _process(_delta):
    var energy = get_parent().get_parent().get_node("Player").Energy()
    if energy <= 0:
        position = Vector2(screen_size.x / 2, screen_size.y / 2)
    else:
        position = Vector2(posX, posY)
