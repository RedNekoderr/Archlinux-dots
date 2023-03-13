extends CharacterBody2D

@onready var input_direction : Vector2 = Vector2(0, 1)
@onready var current_state : DIRECTION_STATES = define_direction(input_direction)
@onready var prev_state: DIRECTION_STATES

enum DIRECTION_STATES { WALK_UP, WALK_LEFT, WALK_DOWN, WALK_RIGHT, IDLE }

var move_speed : float = 100

func _physics_process(_delta):
	input_direction = Vector2(
		Input.get_action_strength("right") - Input.get_action_strength("left"),
		Input.get_action_strength("down") - Input.get_action_strength("up")
		)
	
	current_state = define_direction(input_direction)
	update_animation()
	
	velocity = input_direction.normalized() * move_speed
	
	move_and_slide()

func define_direction(local_direction : Vector2) -> DIRECTION_STATES:
	prev_state = current_state
	match local_direction:
		Vector2(-1, 0), Vector2(-1, -1), Vector2(-1, 1):
			return DIRECTION_STATES.WALK_LEFT
		Vector2(0, -1):
			return DIRECTION_STATES.WALK_UP
		Vector2(0, 1):
			return DIRECTION_STATES.WALK_DOWN
		Vector2(1, 0), Vector2(1, -1), Vector2(1, 1):
			return DIRECTION_STATES.WALK_RIGHT
	return DIRECTION_STATES.IDLE

func update_animation() -> void:
	if prev_state != current_state:
		pass
	pass
