extends Node2D

var temp_child : CharacterBody2D

func _process(_delta):
	if Input.is_action_just_pressed("test"):
		var enm_smiler = preload("res://Enemies/character_body_2d.tscn").instantiate()
		temp_child = enm_smiler
		add_child(temp_child)
