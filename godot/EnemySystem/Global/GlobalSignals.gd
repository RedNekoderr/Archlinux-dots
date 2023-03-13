extends Node

@onready var lamp_scene = load("res://Worlds/lamp.tscn")
@onready var lamps = lamp_scene.instantiate()

func lamp_action(action: String) -> void:
	lamps.do_action(action)

