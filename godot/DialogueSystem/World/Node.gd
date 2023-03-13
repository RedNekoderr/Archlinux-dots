extends Node

@onready var res = preload("res://Objects/Chest/dlg_chest.dialogue")
@onready var dlg_scene = load("res://UI/texbox.tscn")
@onready var dlg_window = dlg_scene.instantiate()

#func _process(_delta):
#	if Input.is_action_just_pressed("test2"):
#		res = preload("res://Objects/Chest/dlg_chest.dialogue")
#		dlg_scene = load("res://UI/texbox.tscn")
#		dlg_window = dlg_scene.instantiate()
#		add_child(dlg_window)
#		dlg_window.start_dialog(res, "Chest")
