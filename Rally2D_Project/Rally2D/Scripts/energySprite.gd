extends Sprite

var list = []

func _ready():
    list = Util.loadImage("Energy", "energy_")

func _process(_delta):
    if !list.empty():
        var index = get_parent().get_parent().get_node("Player").Energy()
        if index < 0:
            index = 0
        if index > (list.size() - 1):
            index = list[-1]
        texture = list[index]
