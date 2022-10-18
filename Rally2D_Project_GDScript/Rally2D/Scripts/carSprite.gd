extends Sprite

var list = []

func _ready():
    list = Util.loadImage("Car", "car_")

func _process(_delta):
    var index = get_parent().index
    if !list.empty():
        if index >= 0 && index < list.size():
            texture = list[index]
