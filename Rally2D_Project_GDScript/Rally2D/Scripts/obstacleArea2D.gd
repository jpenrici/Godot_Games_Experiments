extends Area2D

var y_max
var x_max
var x_min
var posY

func _ready():
    posY = position.y   
    y_max = get_viewport().size.y + get_node("Obstacle").texture.get_height()
    x_max = get_parent().get_node("Player").X_MAX
    x_min = get_parent().get_node("Player").X_MIN
    
func _process(delta):
    var speed = get_parent().get_node("Player").Speed()
    position += Vector2(0, 1).normalized() * speed * delta
    if position.y > y_max:
        position.x = rand_range(x_min, x_max)
        position.y = posY
        get_node("Obstacle").change()

func _on_Obstacle_area_entered(area):
    if area.name == "Player":
        position.x = rand_range(x_min, x_max)
        position.y = posY
        get_node("Obstacle").change()       
        get_parent().get_node("Player").Collision()
