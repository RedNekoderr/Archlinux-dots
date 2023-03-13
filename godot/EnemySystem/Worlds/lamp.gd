extends Node

func start_flickering() -> void:
	print('Blink')

func turn_off() -> void:
	print('Lights off')

func turn_on() -> void:
	print('Lights on')

func do_action(action: String):
	match action:
		'blink': start_flickering()
		'off': turn_off()
		'on': turn_on()
