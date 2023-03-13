extends ColorRect

func _on_hurt_box_area_entered(area):
	print('blink')
	await get_tree().create_timer(1).timeout
	self.queue_free()
