extends Area2D

const VELOCITY_MAX = 60
const X_MAX =  380
const X_MIN = -380
const Y_MAX =    0
const Y_MIN = -250

var index
var velocity
var energy
var speed
var counter
var timer
var posY

func _ready():
    posY = position.y
    velocity = 0
    speed = 0
    energy = 10
    counter = 0
    timer = 0
    
func _process(delta):

    var coordinate = Vector2()
    speed = velocity * 10
    
    if energy > 0:
        
        if velocity <= 0:
            index = 4
        if velocity > 0:
            timer += 1
            if timer > ((VELOCITY_MAX - velocity) / 10):
                index += 1
                timer = 0
                if index > 3:
                    index = 0
                        
        if Input.is_action_pressed("ui_left"):
            if (position.x > X_MIN):
                coordinate.x -= 1
            
        if Input.is_action_pressed("ui_right"):
            if (position.x < X_MAX):
                coordinate.x += 1
            
        if Input.is_action_pressed("ui_up"):
            velocity += 1
            if (velocity >= VELOCITY_MAX):
                velocity = VELOCITY_MAX
            if (position.y > Y_MIN):
                coordinate.y -= 1
            
        if Input.is_action_pressed("ui_down"):
            index = 5
            velocity -= 1
            if (velocity <= 0):
                velocity = 0
            if (position.y < Y_MAX):
                coordinate.y += 1
        
        position += coordinate.normalized() * speed * delta
        
    else:
        if Input.is_action_pressed("ui_accept"):
            velocity = 0
            speed = 0
            energy = 10
            counter = 0
            timer = 0
            
func Collision():
    position.y = posY
    velocity = 0
    energy -= 1
    
func Velocity():
    return velocity

func Speed():
    return speed

func Energy():
    return energy

func UpdateDistance():
    counter += 1

func Distance():
    return counter
