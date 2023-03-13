extends CharacterBody2D

enum SMILER_STATES { SPAWN, SCOUR, FOLLOW, HIT }

@onready var animation_tree : AnimationTree = $AnimationTree
@onready var state_machine : AnimationNodeStateMachinePlayback = animation_tree.get("parameters/playback")
@onready var shader : ColorRect = $ColorRect
@onready var sprite : Sprite2D = $SmilerSprite
@onready var timer : Timer = $Timer

var move_direction : Vector2 = Vector2.ZERO
var current_state : SMILER_STATES = SMILER_STATES.SPAWN
var target : PlayerCat
var move_speed : float = 30

func _ready() -> void:
	animation_tree.active = true
	state_player()

func _physics_process(_delta) -> void:
	match current_state:
		SMILER_STATES.SCOUR:


func state_player() -> void:
	match current_state:
		SMILER_STATES.SPAWN:
			state_machine.travel("Spawn")
			await get_tree().create_timer(1).timeout
			current_state = SMILER_STATES.SCOUR
			timer.start(2)
			state_player()
		SMILER_STATES.SCOUR:
			state_machine.travel("Scour")
			shader.show()

func choose_direction() -> void:
	move_direction = Vector2(randi_range(-1,1), randi_range(-1,1))

func _on_timer_timeout() -> void:
	choose_direction()
