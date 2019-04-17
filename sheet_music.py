"""
Questions
- How to do key changes
- How to get signature and accidentals
- fuging tunes

Test cases
- Fermatad rest
-
"""
import ui
import midi
import inspect
import objc_util

screen_width, screen_height = ui.get_screen_size()
notes_drawn = 0
screen_padding = 1/6#of the screen
note_gap = 125
origin = screen_width / 2
note_pos = 0, 0
bars_to_draw = 0
player = None
rate = 1
play_back_location = 0
tracking_song = False
dragging = False
song = None

treble_lines = []
bass_lines = []
s_positions = []
a_positions = []
t_positions = []
b_positions = []
for i in range(0, 5):
	treble_lines.append(screen_height * (screen_padding*((i+7)/8)))
	bass_lines.append(screen_height - (screen_height * (screen_padding*((i+7)/8))))
step = (treble_lines[1] - treble_lines[0]) / 2
C0_treble_y = treble_lines[4] + step + ((step * 7) * 4)
C0_bass_y = (bass_lines[4] - (3 * step)) + ((step * 7) * 4) 
def create_index(note_name):
	note_name.split()
	index = ord(note_name[0]) - ord('C')
	if note_name[0] == 'R':
		return -1
	else:
		if index < 0:
			index += 7
		return index + (int(note_name[1]) * 7)
	
assert create_index('C0') == 0
assert create_index('G0') == 4
assert create_index('A0') == 5
assert create_index('B0') == 6
assert create_index('C1') == 7
assert create_index('C8') == 56
assert create_index('R') == -1

def write_midi(song):
	midi.Song(song).write_midi('output.midi', [
		int(get_subview('soprano_volume').value * 120),
		int(get_subview('alto_volume').value * 120),
		int(get_subview('tenor_volume').value * 120),
		int(get_subview('bass_volume').value * 120)])

def play():
	global rate
	if player:
		player.play()
		player.rate = rate

def stop():
	global rate
	if player:
		player.stop()
		rate = player.rate
		
def playing():
	return get_subview('play_button').title == 'Pause'
	
def get_subview(name):
	for subview in satb_page.subviews:
		if subview.name == name:
			return subview
	raise RuntimeError('nutn is namd ' + name)

def calculate_length(song):
	end = origin
	for measure in midi.Song(song).measures:
		voice_selected = measure[midi.Voice.Soprano]
		if isinstance(voice_selected, list):
			for note in voice_selected:
				if inspect.isclass(note):
					note_beats = note().beats
				else:
					note_beats = note.beats
				end += note_gap * note_beats
	return end

def play_pause(sender):
	#global song, player, rate, position
	if sender.playing:
		sender.image = ui.Image.named('iob:ios7_play_outline_256')
		sender.playing = False
	else:
		sender.image = ui.Image.named('iob:ios7_pause_outline_256')
		sender.playing = True
		#position = player.current_time
		#rate = player.rate
		#stop()
	#else:
		#sender.title = 'Pause'
		#write_midi(song)
		#player = sound.MIDIPlayer('output.midi')
		# obc_player = objc_util.ObjCClass('AVMIDIPlayer')
		# obc_player.init('output.midi', None)
		#adjust_time(get_subview('time_adjuster'))
		#play()
		#player.rate = get_subview('tempo_slider').value + 0.5
	
def track_time(slider):
	global player, dragging, last_position, rate, position
	if player and not dragging:
		if slider.value == last_position:
			slider.value = player.current_time / float(player.duration)
			if slider.value == 1 and get_subview('play_button').title == 'Pause':
				player.current_time = 0
				rate = player.rate
				play()
				slider.value = player.current_time / float(player.duration)
			last_position = slider.value
		else:
			dragging = True
			position = player.current_time
	if exiting:
		stop()
	else:
		ui.delay(lambda: track_time(slider), 0.05)
	
def settings(sender):
	satb_page = ui.load_view('midi_ui')
	satb_page.present('sheet')
	
def close(sender, self):
	self.close()
	
def sharp(self, size, x, y):
	ui.set_color("black")
	self.left = ui.Path()
	self.left.move_to(x + (size * (3/8)), y + (size / 6))
	self.left.line_to(x + (size * (3/8)), y + size)
	self.left.stroke()
	
	self.right = ui.Path()
	self.right.move_to(x + (size * (5/8)), y)
	self.right.line_to(x + (size * (5/8)), y + (size * (5/6)))
	self.right.stroke()
	
	self.upper = ui.Path()
	self.upper.move_to(x + (size / 6), y + (size / 1.8))
	self.upper.line_to(x + (size * (5/6)), y + (size / 8))
	self.upper.stroke()
	
	self.lower = ui.Path()
	self.lower.move_to(x + (size / 6), y + (size / 1.8) + (size / 3))
	self.lower.line_to(x + (size * (5/6)), y + (size / 8) + (size / 3))
	self.lower.stroke()
	
def g_clef(self, x):
	self.gclef = ui.Path()
	self.gclef.move_to(x - step, treble_lines[4] - step)
	self.gclef.add_arc(x, treble_lines[3], step * 1.5, 40, 0)
	self.gclef.add_arc(x - (step * 0.5), treble_lines[3], step * 2, 0, 3.8)
	self.gclef.add_arc(x - (step * 1.5), treble_lines[0] + (step / 3), step * 2, 0.75, 5.5, False)
	self.gclef.add_arc(x - (step / 4), treble_lines[0] - (step * 0.6), step / 2, 5, 4, False)
	self.gclef.add_arc(x + (step * 0.6), treble_lines[0] + (step / 1.5), step * 2, 4, 2.7, False)
	self.gclef.add_arc(x, treble_lines[4] + (step * 2), step, 6, 3.8)
	self.gclef.add_arc(x, treble_lines[4] + (step * 2), step, 3.8, 6, False)
	self.gclef.add_arc(x + (step * 0.6), treble_lines[0] + (step / 1.5), step * 2, 2.7, 2.7)
	self.gclef.add_arc(x + (step * 1), treble_lines[0] + (step / 1), step * 2.3, 3, 3.5)
	self.gclef.add_arc(x - (step / 6), treble_lines[0] - (step * 0.2), step / 2, 4, 6)
	self.gclef.add_arc(x - (step * 1.7), treble_lines[0] - (step / 3), step * 2, 0, 0.75)
	self.gclef.add_arc(x - (step * 0.1), treble_lines[3] - (step / 2), step * 2.5, 3.8, 3, False)
	self.gclef.add_arc(x - (step * 0.5), treble_lines[3], step * 2, 3, 1, False)
	self.gclef.add_arc(x, treble_lines[3] + (step / 2), step * 1.2, 1, 3, False)
	self.gclef.close()
	self.gclef_end = ui.Path.oval(x - (step / 1.1), treble_lines[4] + (step * 1.1), step, step)
	self.gclef_end.fill()
	ui.set_color("black")
	self.gclef.stroke()
	self.gclef.fill()
	
def f_clef(self, x):
	self.fclef = ui.Path()
	self.fclef.move_to(x - (step * 3), bass_lines[1] + step)
	self.fclef.add_arc(x - (step * 4), bass_lines[3], step * 5, 1, 0, False)
	self.fclef.add_arc(x - step, bass_lines[3], step * 2, 0, 3, False)
	self.fclef.add_arc(x - step, bass_lines[3], step * 2, 3, 4.7)
	self.fclef.add_arc(x - (step * 1.2), bass_lines[3] - (step / 1.7), step * 1.4, 5, 6)
	self.fclef.add_arc(x - (step * 5), bass_lines[3], step * 5.2, 6.3, 1)
	self.fclef.close()
	self.fclef_end = ui.Path.oval(x - (step * 3.05), bass_lines[3] - (step * 0.3), step, step)
	self.fclef_end.fill()
	self.ud = ui.Path.oval(x + (step * 2), bass_lines[3] - step, step / 2, step / 2)
	self.ud.fill()
	self.ld = ui.Path.oval(x + (step * 2), bass_lines[3] + step, step / 2, step / 2)
	self.ld.fill()
	ui.set_color("black")
	self.fclef.stroke()
	self.fclef.fill()
	
class MusicView(ui.View):
	def __init__(self, song, width=1024, height=1024):
		self.song = song
		self.width = width
		self.frame = (0, 0, width, height)
		self.bg_color = 'white'
		
	
			
	def draw(self):
		measures = midi.Song(self.song).measures
		self.draw_notes(midi.Voice.Soprano, measures, C0_treble_y, 1)
		self.draw_notes(midi.Voice.Alto, measures, C0_treble_y, -1)
		self.draw_notes(midi.Voice.Tenor, measures, C0_bass_y, 1)
		self.draw_notes(midi.Voice.Bass, measures, C0_bass_y, -1)
				
		self.staff = ui.Path()
		for i in range(0, 5):
			self.staff.move_to(0, treble_lines[i])
			self.staff.line_to(self.width, treble_lines[i])
			self.staff.move_to(0, bass_lines[i])
			self.staff.line_to(self.width, bass_lines[i])
			
		self.staff.stroke()
		
	def draw_notes(self, voice, measures, clef_C0, tail_direction):
		global origin, end, note_tied, note_pos, bars_to_draw
		position = origin
		note_width = 1.15
		note_tied = False
		for measure in measures:
			self.measure_bars(position)
			voice_selected = measure[voice]
			if isinstance(voice_selected, list):
				loop = 0
				run = []
				slur = []
				note_tied = False
				prev_note_pos = origin
				for note in voice_selected:
					prev_note_tied = note_tied
					if inspect.isclass(note):
						note_name = note.__name__
						note_beats = note().beats
						note_tied = note().tie
						note_slurred = note().slur
					else:
						note_name = type(note).__name__
						note_beats = note.beats
						note_tied = note.tie
						note_slurred = note.slur
					note_index = create_index(note_name)
					note_pos = position, clef_C0 - (note_index * step)
					prev_bars_to_draw = bars_to_draw
					bars_to_draw = int((1/note_beats) / 2)
					if loop + 1 < len(voice_selected):
						next_bars_to_draw = int((1/(voice_selected[loop + 1]().beats if inspect.isclass(voice_selected[loop + 1]) else voice_selected[loop + 1].beats)) / 2)
					else:
						next_bars_to_draw = None

					self.draw_note(note_index, note_beats, clef_C0, note_slurred, slur, prev_note_tied, prev_note_pos, tail_direction, run, bars_to_draw, next_bars_to_draw, position, note_width)
									
					#increment
					prev_note_pos = position
					position += note_gap * note_beats
					loop += 1
					
	def measure_bars(self, position):
		position += note_gap / 2
		measure_bar = ui.Path()
		measure_bar.move_to(position, treble_lines[0])
		measure_bar.line_to(position, treble_lines[4])
		measure_bar.move_to(position, bass_lines[0])
		measure_bar.line_to(position, bass_lines[4])
		measure_bar.stroke()
		position -= note_gap / 2
		
	def draw_note(self, index, beats, C0, slurred, slur, prev_note_tied, prev_note_pos, tail_direction, run, bars_to_draw, next_bars_to_draw, position, width):
		if not index == -1:
			oval = self.draw_dot(C0, index, position)
			self.fill_note(C0, index, oval, beats, position)
			self.dots(index, beats, C0, position)
			self.slur(slurred, slur, index, C0, tail_direction, position)
			self.tie(index, C0, prev_note_tied, prev_note_pos, tail_direction, position, width)		
			if bars_to_draw == next_bars_to_draw and bars_to_draw >= 1:
				run.append(note_pos)
			elif not run == []:
				self.run_bar(bars_to_draw, tail_direction, run, position, width)
				self.tails(tail_direction, run, position)
				run = []
			else:
				self.flag(note_pos, tail_direction, position)
				self.tail(beats, index, C0, tail_direction, run, position, width)
				
		else:
				self.rest(beats, position, C0)
				
	def draw_dot(self, C0, index, position):
		ui.set_color('black')
		note_dot = ui.Path()
		rel_x = position - (step * 0.53)
		note_y = C0 - (index * step)
		note_dot.move_to(rel_x + step, (step * 2) + note_y)
		note_dot.add_arc(rel_x + (step * 1.1), (step * 0.3) + note_y, step * 1.7, 1.7, 0.25, False)
		note_dot.add_arc(rel_x + (step * 2.2), (step * 0.6) + note_y, step * 0.6, 6.9, 5, False)
		note_dot.add_arc(rel_x + (step * 2.2), (step * 1.7) + note_y, step * 1.7, 4.8, 3.5, False)
		note_dot.add_arc(rel_x + (step * 1.1), (step * 1.4) + note_y, step * 0.6, 3.5, 2, False)	
		return note_dot
		
	def fill_note(self, C0, index, note, beats, position):
		if beats < 2:
			note.fill()
			note.stroke()
		else:
			rel_x = position - (step * 0.53)
			note_y = C0 - (index * step)
			note.add_arc(rel_x + (step * 1.12), (step * 1.38) + note_y, step * 0.6, 2, 2.8)
			note.add_arc(rel_x + (step * 2.8), (step * 2.3) + note_y, step * 2.3, 3.5, 4.5)
			note.add_arc(rel_x + (step * 2.15), (step * 0.65) + note_y, step * 0.6, 5.1, 0)
			note.add_arc(rel_x + (step * 0.35), (step * -0.6) + note_y, step * 2.6, 0.5, 1.35)
			note.stroke()
			note.close()
			note.fill()
			note.stroke()
			
	def dots(self, index, beats, C0, position):
		if beats % 1.5 == 0:
			dot = ui.Path()
			dot = ui.Path.oval(position + (4 * step), C0 - ((index - 0.6) * step), 0.4 * step, 0.4 * step)
			dot.stroke()
			ui.set_color('black')
			dot.fill()
			
	def slur(self, slurred, slurs, index, C0, tail_direction, position):
		if slurred:
			slurs.append((position, C0 - (index * step)))
		elif not slurs == []:
			f_x, f_y = slurs[0]
			thickness = 3
			tail_end = -(((3.5 * tail_direction) - 3.5) * step)
			f_y += tail_end
			y_pos = (C0 - (index * step)) + tail_end
			t_b = step * (1 - tail_direction)
			curve_y = (step * tail_direction * -2) + t_b
			prev_note_side = f_x + (note_width * step * 2)
			middle_x = prev_note_side + ((position - prev_note_side) / 2)
			middle_y = f_y + ((y_pos - f_y) / 2)
			center_s = 3 * ((middle_x - prev_note_side) / 200)
			
			slur = ui.Path()
			slur.move_to(position, y_pos + t_b)
			slur.add_quad_curve(middle_x, middle_y + curve_y, position - (step * center_s), y_pos + curve_y)
			slur.add_quad_curve(prev_note_side, f_y + t_b, prev_note_side + (step * center_s), f_y + curve_y)
			slur.add_quad_curve(middle_x, middle_y + curve_y + ((step * tail_direction) / thickness), prev_note_side + (step * center_s), f_y + curve_y)
			slur.add_quad_curve(position, y_pos + t_b, position - (step * center_s), y_pos + curve_y)
			slur.fill()
			slur.stroke()
			slurs = []
			
	def tie(self, index, C0, prev_note_tied, prev_note_pos, tail_direction, position, width):
		if prev_note_tied:
			thickness = 3
			y_pos = C0 - (index * step)
			t_b = step * (1 - tail_direction)
			curve_y = (step * tail_direction * -2) + t_b
			prev_note_side = prev_note_pos + (width * step * 2)
			middle = prev_note_side + ((position - prev_note_side) / 2)
			center_s = 3 * ((middle - prev_note_side) / 200)
			
			tie = ui.Path()
			tie.move_to(position, y_pos + t_b)
			tie.add_quad_curve(middle, y_pos + curve_y, position - (step * center_s), y_pos + curve_y)
			tie.add_quad_curve(prev_note_side, y_pos + t_b, prev_note_side + (step * center_s), y_pos + curve_y)
			tie.add_quad_curve(middle, y_pos + curve_y + ((step * tail_direction) / thickness), prev_note_side + (step * center_s), y_pos + curve_y)
			tie.add_quad_curve(position, y_pos + t_b, position - (step * center_s), y_pos + curve_y)
			tie.fill()
			tie.stroke()
	
	def run_bar(self, bars, tail_direction, run, position, width):
		for b in range(0, bars):
			bar = ui.Path()
			offset = step * 2 * b * tail_direction
			line_thickness = step * tail_direction
			
			x, y = run[0]
			xcoord = x + (step * width * (1 + tail_direction))
			tail_length = y + (step * -6 * tail_direction)
			bar.move_to(xcoord, tail_length + step + offset)
			bar.line_to(xcoord, tail_length + (step - line_thickness) + offset)
			
			x, y = note_pos
			xcoord = x + (step * width * (1 + tail_direction))
			tail_length = y + (step * -6 * tail_direction)
			bar.line_to(xcoord, tail_length + (step - line_thickness) + offset)
			bar.line_to(xcoord, tail_length + step + offset)
			
			bar.close()
			bar.stroke()
			bar.fill()
			
	def tails(self, tail_direction, run, position):
		for run_note in run:
			note_tail = ui.Path()
			x, y = run_note
			fx, fy = run[0]
			cx, cy = note_pos
			abs_pos = x - fx
			run_length = cx - fx
			run_height = cy - fy
			note_side = ((tail_direction * note_width) + note_width) * step
			rel_pos = abs_pos / run_length
			grad_pos = (rel_pos * run_height) + fy
			tail_length = -7 * step * tail_direction
			note_tail.move_to(x + note_side, grad_pos + tail_length + step)
			note_tail.line_to(x + note_side, y + step)
			note_tail.stroke()
			
	def flag(self, pos, tail_direction, position):
		for bar in range(0, bars_to_draw):
			x, y = pos
			flag = ui.Path()
			
			x_offset = step * note_width * (1 + tail_direction)
			tail_length = step * -5.5 * tail_direction
			y_offset = step * 1.5 * bar * tail_direction
			y_dis = step - (tail_direction * step)
			
			y_pos = y + tail_length + y_dis + y_offset
			rad = step / 2
			flag.move_to(x + x_offset, y_pos)
			flag.add_arc(x + rad + x_offset, y_pos, rad, 3 * tail_direction, 2 * tail_direction, tail_direction < 0)
								
			rad = step * 2.5
			tail_length = step * -2.5 * tail_direction
			y_pos = y + tail_length + y_dis + y_offset
			flag.add_arc(x + x_offset, y_pos, rad, 5 * tail_direction, tail_direction, tail_direction > 0)
								
			rad = step * 2
			tail_length = step * -2 * tail_direction
			y_pos = y + tail_length + y_dis + y_offset
			flag.add_arc(x + x_offset, y_pos, rad, tail_direction,  4.8 * tail_direction, tail_direction < 0)
								
			tail_length = step * -4 * tail_direction
			y_pos = y + tail_length + y_dis + y_offset
			flag.line_to(x + x_offset, y_pos)
								
			ui.set_color("black")
			flag.close()
			flag.stroke()
			flag.fill()
			run = []
			
	def tail(self, beats, index, C0, direction, run, position, width):
		if beats < 4 and run == []:
			note_tail = ui.Path()
			note_tail.move_to(position + (((direction * width) + width) * step),(C0 - (index * step)) + step)
			note_tail.line_to(position + (((direction * width) + width) * step),((C0 - (index * step)) + step) - (direction * (7 * step)))
			note_tail.stroke()
	
	def rest(self, beats, position, C0):
		rests = []
		rest_beats = beats
		rest_div = 4
		for i in range(0, 16):
			while rest_beats - rest_div >= 0:
				rest_beats -= rest_div
				rests.append(rest_div)
			rest_div /= 2
		for rest_type in rests:
			if C0 == C0_treble_y:
				bottom = treble_lines[4]
			else:
				bottom = bass_lines[0]
			if rest_type == 4:
				rest = ui.Path.rect(position + (note_gap * 1.5), bottom - (step * 4), step * 3, step)
				rest.fill()
			elif rest_type == 2:
				rest = ui.Path.rect(position + (note_gap / 2), bottom - (step * 5), step * 3, step)
				rest.fill()
			elif rest_type == 1:
				rest = ui.Path()
				rest.move_to(position - (step / 3), bottom - (step * 7.1))
				rest.add_arc(position + (step * 2.5), bottom - (step * 4), step * 2, 4, 2.3, False)
				rest.add_quad_curve(position, bottom - step, position - (step * 0.7), bottom - (step * 2.9))
				rest.add_quad_curve(position + step, bottom - (step * 2.6), position - (step * 1.7), bottom - (step * 3.9))
				rest.add_arc(position - (step * 2), bottom - (step * 6), step * 2, 1, 5.7, False)
				rest.close()
				rest.stroke()
				rest.fill()

class Signature(ui.View):
	def __init__(self, width, height):
		self.width = width
		self.frame = (0, 0, width, height)
		self.bg_color = 'white'		
		
	def draw(self):
		self.lines = ui.Path()
		for i in range(0, 5):
			self.lines.move_to(0, treble_lines[i])
			self.lines.line_to(self.width, treble_lines[i])
			self.lines.move_to(0, bass_lines[i])
			self.lines.line_to(self.width, bass_lines[i])
			
		self.lines.stroke()
		#sharp(self, step * 3, step, 10)
		g_clef(self, step * 4)
		f_clef(self, step * 4)
		
		
class Controls(ui.View):
	def __init__(self, width, height, button_width):
		self.width = width
		self.frame = (0, 0, width, height)
		play_btn = ui.Button(image=ui.Image.named('iob:ios7_play_outline_256'))
		play_btn.frame = (0, 0, button_width, button_width)
		play_btn.action = play_pause
		play_btn.playing = False
		play_btn.name = 'play_button'
		
		settings_btn = ui.Button(image=ui.Image.named('iob:ios7_gear_outline_256'))
		settings_btn.frame = (button_width, 0, button_width * 2, button_width)
		settings_btn.action = settings
		
		
		self.add_subview(play_btn)
		self.add_subview(settings_btn)
		

class MyView(ui.View):
	def __init__(self, song):
		self.name = song
		w, h = ui.get_screen_size()
		self.sv = ui.ScrollView()
		self.sv.width = w
		self.sv.height = h
		heading_thickness = 20
		self.sv.frame = (0, -heading_thickness, w, h)
		length = calculate_length(song)
		self.sv.content_size = (length, h - heading_thickness)
		self.sv.add_subview(MusicView(song, length, screen_height))
		self.sv.shows_horizontal_scroll_indicator = False
		self.sv.shows_vertical_scroll_indicator = False
		self.sig = ui.View()
		self.sig.width = w * screen_padding * 0.8
		self.sig.height = h
		self.sig.add_subview(Signature(self.sig.width, self.sig.height))
		button_width = 50
		self.controls = ui.View()
		self.controls.width = button_width * 2
		self.controls.height = button_width
		print(h)
		self.controls.frame = ((w / 2) - button_width, 718, (w/2) + button_width, 768)
		self.controls.add_subview(Controls(self.controls.width, self.controls.height, button_width))
		self.add_subview(self.sv)
		self.add_subview(self.sig)
		self.add_subview(self.controls)
