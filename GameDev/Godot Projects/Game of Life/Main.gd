extends Node2D


export(Color) var dead_color = Color(32)

const ZOOM_STEP = 0.1

var zoom = 1.0
var grids = [{}, {}]
var cells = {}
var alive_color: Color
var to_check = []



func _ready():
	$Cell.hide()
	$Canvas/Count.hide()
	alive_color = $Cell.modulate

func _process(delta):
	$Canvas/Count.text = "COUNT: " + str(sum(grids[0]))

func sum(d: Dictionary):
	var sum = 0
	for value in d.values():
		if value:
			sum += 1
	return sum

func _unhandled_input(event):
	if event is InputEventMouseButton:
		if event.button_index == BUTTON_LEFT and event.pressed:
			place_cell(event.position)
		if event.button_index == BUTTON_RIGHT and event.pressed:
			remove_cell(event.position)
		if event.button_index == BUTTON_WHEEL_DOWN and event.pressed:
			change_zoom(ZOOM_STEP)
		if event.button_index == BUTTON_WHEEL_UP and event.pressed:
			change_zoom(-ZOOM_STEP)
	if event is InputEventMouseMotion and event.button_mask == BUTTON_MASK_MIDDLE:
		move_camera(event.relative)
	
	if event.is_action_pressed("ui_cancel"):
		get_tree().quit()
	if event.is_action_pressed("ui_accept"):
		start_stop()
	if event.is_action_pressed("ui_reset"):
		reset()


func place_cell(pos: Vector2):
	pos = mouse_pos_to_cam_pos(pos)
	var grid_pos = get_grid_pos(pos)
	if not cells.has(grid_pos):
		add_new_cell(grid_pos)

func get_grid_pos(pos: Vector2) -> Vector2:
	var pixels = 32.0 / $Camera2D.zoom.x
	return pos.snapped(Vector2(pixels, pixels)) / pixels

func mouse_pos_to_cam_pos(pos: Vector2):
	return pos + $Camera2D.offset / $Camera2D.zoom - get_viewport_rect().size / 2

func remove_cell(pos: Vector2):
	var key = get_grid_pos(mouse_pos_to_cam_pos(pos))
	if cells.has(key):
		cells[key].queue_free()
		cells.erase(key)
		grids[1].erase(key)

func add_new_cell(grid_pos: Vector2):
	var pos = grid_pos * 32
	var cell = $Cell.duplicate()
	cell.position = pos
	add_child(cell)
	cell.show()
	cells[grid_pos] = cell
	grids[1][grid_pos] = true


func change_zoom(step: float):
	zoom = clamp(zoom + step, 0.1, 8.0)
	$Camera2D.zoom = Vector2(zoom, zoom)
	
func move_camera(dv: Vector2):
	$Camera2D.offset -= dv


func start_stop():
	if $Timer.is_stopped() and cells.size() > 0:
		$Timer.start()
		$Canvas/Stopped.hide()
		$Canvas/Running.show()
		$Canvas/Count.show()
	else:
		$Timer.stop()
		$Canvas/Stopped.show()
		$Canvas/Running.hide()

func reset():
	$Timer.stop()
	for key in cells.keys():
		cells[key].queue_free()
	grids[1].clear()
	cells.clear()


func regenerate():
	for key in cells.keys():
		var n = get_num_live_cells(key)
		if grids[0][key]:
			grids[1][key] = (n == 2 or n == 3)
		else:
			grids[1][key] = (n == 3)
		
func get_num_live_cells(pos: Vector2, first_pass = true):
	var num_live_cells = 0
	for y in [-1, 0, 1]:
		for x in [-1, 0, 1]:
			if x != 0 or y != 0:
				var new_pos = pos + Vector2(x, y)
				if grids[0].has(new_pos):
					if grids[0][new_pos]:
						num_live_cells += 1
				elif first_pass:
					to_check.append(new_pos)
	return num_live_cells

func update_cells():
	for key in cells.keys():
		cells[key].modulate = alive_color if grids[1][key] else dead_color

func add_new_cells():
	for pos in to_check:
		var n = get_num_live_cells(pos, false)
		if n == 3 and not grids[1].has(pos):
			add_new_cell(pos)
	to_check = []


func _on_Timer_timeout():
	grids.invert()
	grids[1].clear()
	regenerate()
	add_new_cells()
	update_cells()
