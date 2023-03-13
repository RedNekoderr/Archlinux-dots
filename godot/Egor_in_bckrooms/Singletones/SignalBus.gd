extends Node

const TEXTBOX = preload("res://Objects/texbox.tscn")

func imit_dialog(speaker : String, dialog : String):
	var local_texbox = TEXTBOX.instantiate()
	local_texbox.get_node("Background/MarginContainer/VBoxContainer/Speaker").text = speaker
	local_texbox.get_node("Background/MarginContainer/VBoxContainer/LabelText").text = dialog
	add_child(local_texbox)
	await get_tree().create_timer(2).timeout
	local_texbox.queue_free()
