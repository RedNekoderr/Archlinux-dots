extends CharacterBody2D

class_name PlayerCharacter

@onready var animation_tree : AnimationTree = $AnimationTree
@onready var state_machine : AnimationNodeStateMachinePlayback = animation_tree.get("parameters/playback")
@onready var input_direction : Vector2 = Vector2(0, 1)
@onready var current_state : DIRECTION_STATES = define_direction(input_direction)
@onready var prev_state: DIRECTION_STATES

enum DIRECTION_STATES { WALK_UP, WALK_LEFT, WALK_DOWN, WALK_RIGHT, IDLE }

var move_speed : float = 120

func _physics_process(_delta):
	input_direction = Vector2(
		Input.get_action_strength("right") - Input.get_action_strength("left"),
		Input.get_action_strength("down") - Input.get_action_strength("up")
		)
	
	current_state = define_direction(input_direction)
	if current_state != prev_state:
		update_animation(input_direction)
	
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

func update_animation(blend_direction: Vector2) -> void:
	if blend_direction != Vector2.ZERO:
		animation_tree.set("parameters/Walk/blend_position", blend_direction)
		animation_tree.set("parameters/Idle/blend_position", blend_direction)
		state_machine.travel('Walk')
	else:
		state_machine.travel('Idle')
