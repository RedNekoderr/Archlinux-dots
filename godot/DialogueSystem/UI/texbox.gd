extends CanvasLayer


@export var DRAW_SPEED : int = 20

@onready var text : RichTextLabel = $Background/MarginContainer/VBoxContainer/Label
@onready var speaker : RichTextLabel = $Background/MarginContainer/VBoxContainer/Speaker
@onready var options_container_parent : NinePatchRect = $OptionsContainer
@onready var options_container : VBoxContainer = $OptionsContainer/MarginContainer/VBoxContainer/Options
@onready var indicator : Sprite2D = $Background/MarginContainer/Indicator
@onready var button : Button = $Button

var dialog_file : DialogueResource
var dialog_line : DialogueLine
var total_characters : float = 0
var drawn_characters : float = 0
var prev_drawn_characters : int = 0
var speed_key : int = 0
var is_typing_dialogue : bool = false
var is_awaiting_selection : bool = false


func _ready():
	DialogueManager.dialogue_finished.connect(end_dialogue)


func _process(delta):
	actions_pressed()
	update_visible(delta)
	update_speed()


func actions_pressed() -> void:
	if Input.is_action_just_pressed("accept"):
		if not is_typing_dialogue:
			if not is_awaiting_selection:
				get_next_dialogue(dialog_line.next_id)
				DRAW_SPEED = 40
				speed_key = 0
			else:
				var first_option = dialog_line.responses[0].next_id
				get_next_dialogue(first_option)
		else:
			drawn_characters = total_characters - 0.1
	return


func update_visible(delta) -> void:
	if drawn_characters < total_characters:
		drawn_characters += DRAW_SPEED * delta
		text.visible_characters = int(drawn_characters)
	else:
		indicator.frame = 0
		is_typing_dialogue = false
	return


func update_speed() -> void:
	if dialog_line is DialogueLine:
		if dialog_line.speeds != {} and speed_key != dialog_line.speeds.keys().size() and text.visible_characters == dialog_line.speeds.keys()[speed_key] and text.visible_characters != prev_drawn_characters:
			DRAW_SPEED = dialog_line.speeds.values()[speed_key] * 10
			speed_key += 1
	prev_drawn_characters = text.visible_characters
	return


func start_dialog(dialog : DialogueResource, start_point : String) -> void:
	dialog_file = dialog
	dialog_line = await DialogueManager.get_next_dialogue_line(dialog_file, start_point)
	update_dialog_window()
	return


func get_next_dialogue(next_id : String) -> void:
	dialog_line = await DialogueManager.get_next_dialogue_line(dialog_file, next_id)
	update_dialog_window()
	return


func update_dialog_window() -> void:
	if dialog_line is DialogueLine:
		speaker.text = dialog_line.character
		text.text = dialog_line.text
	else:
		end_dialogue()
		return
	clear_options()
	set_options()
	hide_text()
	return


func set_options() -> void:
	var options
	if dialog_line.responses.size() > 0:
		is_awaiting_selection = true
		options = dialog_line.responses
	else:
		is_awaiting_selection = false
		options_container_parent.hide()
	if is_awaiting_selection:
		options_container_parent.show()
		for i in options.size():
			var option_button = button.duplicate()
			options_container.add_child(option_button)
			option_button.show()
			option_button.text = options[i].text
			set_response_action(option_button, options[i].next_id)
	return


func set_response_action(local_option_button : Button, next_id : String) -> void:
	local_option_button.pressed.connect(get_next_dialogue.bind(next_id))
	return


func clear_options() -> void:
	for child in options_container.get_children():
		child.queue_free()
	return


func hide_text() -> void:
	total_characters = text.get_total_character_count()
	text.visible_characters = 0
	drawn_characters = 0
	indicator.frame = 1
	is_typing_dialogue = true
	return


func end_dialogue() -> void:
	self.queue_free()
	return
