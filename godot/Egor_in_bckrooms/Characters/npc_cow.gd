extends CharacterBody2D

enum COW_STATE { IDLE, WALK }

@export var move_speed : float = 20

@onready var animation_tree = $AnimationTree
@onready var state_machine = animation_tree.get("parameters/playback")
@onready var sprite = $Sprite2D
@onready var timer = $Timer

var move_direction : Vector2 = Vector2.ZERO
var current_state : COW_STATE = COW_STATE.IDLE

func _ready():
	animation_tree.active = true
#	pick_new_state()
	
func _physics_process(_delta):
		
		move_and_slide()
	
func select_new_direction():
	move_direction = Vector2(
		randi_range(-1, 1),
		randi_range(-1, 1)
	)
	
	if(move_direction.x < 0):
		sprite.flip_h = true
	elif(move_direction.x > 0):
		sprite.flip_h = false
	
#func pick_new_state():
#	match (current_state):
#		COW_STATE.IDLE:
#			state_machine.travel('Walk')
#			current_state = COW_STATE.WALK
#			select_new_direction()
#			timer.start(select_random_time(1, 4))
#		COW_STATE.WALK:
#			state_machine.travel('Idle')
#			current_state = COW_STATE.IDLE
#			timer.start(select_random_time(4, 8))

#func select_random_time(from : int, to : int) -> float:
#	return randi_range(from, to)

#func _on_timer_timeout():
#	pick_new_state()
