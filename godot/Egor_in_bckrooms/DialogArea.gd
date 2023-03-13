extends Area2D

@export var dialog_key = ""
var area_active = false

func _init(event):
	if area_active and Input.is_action_pressed("accept"):
		SignalBus.emit_signal("display_dialog", dialog_key)

func _on_area_entered(area):
	area_active = true

func _on_area_exited(area):
	area_active = false
