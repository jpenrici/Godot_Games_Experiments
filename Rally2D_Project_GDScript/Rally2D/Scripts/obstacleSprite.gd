extends Sprite

var list = []

func _ready():
    list = Util.loadImage("Obstacle", "obstacle_")

func change():
    if !list.empty():
        var index = int(rand_range(0, list.size() - 1))
        texture = list[index]
