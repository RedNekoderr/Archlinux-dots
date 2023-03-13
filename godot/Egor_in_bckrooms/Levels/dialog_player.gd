extends CanvasLayer

@export var scene_text_file : FileDialog

@onready var background = $Background
@onready var speaker_name = $Background/MarginContainer/VBoxContainer/SpeakerName
@onready var text_label = $Background/MarginContainer/VBoxContainer/TextLabel

var scene_text = {}
var selected_text = []
var in_progress = false

func _ready():
	background.visible = false
	scene_text = load_scene_text()

	
	
