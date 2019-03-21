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

screen_width, screen_height = ui.get_screen_size()
notes_drawn = 0
screen_padding = 1/6#of the screen
note_gap = 125
origin = screen_width / 2
note_tied = False
note_pos = 0, 0
bars_to_draw = 0

treble_lines = []
bass_lines = []
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
		#g_clef(self, 40)
		#f_clef(self, 40)
			
	def draw_notes(self, voice, measures, clef_C0, tail_direction):
		global origin, end, note_tied, note_pos, bars_to_draw
		position = origin
		for measure in measures:
			#measure bars
			position -= note_gap / 2
			measure_bar = ui.Path()
			measure_bar.move_to(position, treble_lines[0])
			measure_bar.line_to(position, bass_lines[0])
			measure_bar.stroke()
			position += note_gap / 2
			voice_selected = measure[voice]
			if isinstance(voice_selected, list):
				loop = 0
				run = []
				for note in voice_selected:
					
					#define variables
					prev_note_pos = note_pos
					prev_note_tied = note_tied
					if inspect.isclass(note):
						note_name = note.__name__
						note_beats = note().beats
						note_tied = note().tie
					else:
						note_name = type(note).__name__
						note_beats = note.beats
						note_tied = note.tie
					note_index = create_index(note_name)
					note_pos = position, clef_C0 - (note_index * step)
					prev_bars_to_draw = bars_to_draw
					bars_to_draw = int((1/note_beats) / 2)
					if loop + 1 < len(voice_selected):
						next_bars_to_draw = int((1/(voice_selected[loop + 1]().beats if inspect.isclass(voice_selected[loop + 1]) else voice_selected[loop + 1].beats)) / 2)
					else:
						next_bars_to_draw = None
						
					# draw note
					if not note_index == -1:
						note_dot = ui.Path.oval(position, clef_C0 - (note_index * step), 3 * step, 2 * step)
						ui.set_color('black')
						
						# hollow/solid notes
						if note_beats < 2:
							note_dot.fill()
							note_dot.stroke()
						else:
							#x, y = note_pos
							#note_dot.move_to(x, y)
							
							#rad = step * 2
							#x_offset = step
							#note_dot.add_arc(x + x_offset, y, rad, 0.1, 1)
							note_dot.stroke()
														
						# draw dots
						if note_beats % 1.5 == 0:
							note_dotted = ui.Path()
							note_dotted = ui.Path.oval(position + (4 * step), clef_C0 - ((note_index - 0.6) * step), 0.4 * step, 0.4 * step)
							note_dotted.stroke()
							ui.set_color('black')
							note_dotted.fill()
						
						# draw ties	
						#if prev_note_tied:
							#self.note_tie = ui.Path()
							#self.note_tie.move_to(prev_note_pos, clef_C0 - (note_index * step))
							#self.note_tie.add_quad_curve(position, clef_C0 - (note_index * step), 90, 90)
							#self.note_tie.stroke()
							
						# draw bars
						if bars_to_draw == next_bars_to_draw and bars_to_draw >= 1:
							run.append(note_pos)
						elif not run == []:
							
							#run bar
							for b in range(0, bars_to_draw):
								bar = ui.Path()
								offset = step * 2 * b * tail_direction
								line_thickness = step * tail_direction
								
								x, y = run[0]
								xcoord = x + (step * 1.5 * (1 + tail_direction))
								tail_length = y + (step * -6 * tail_direction)
								bar.move_to(xcoord, tail_length + step + offset)
								bar.line_to(xcoord, tail_length + (step - line_thickness) + offset)
								
								x, y = note_pos
								xcoord = x + (step * 1.5 * (1 + tail_direction))
								tail_length = y + (step * -6 * tail_direction)
								bar.line_to(xcoord, tail_length + (step - line_thickness) + offset)
								bar.line_to(xcoord, tail_length + step + offset)
								
								bar.close()
								bar.stroke()
								bar.fill()
							
							# tails in bar
							for run_note in run:
								note_tail = ui.Path()
								x, y = run_note
								fx, fy = run[0]
								cx, cy = note_pos
								abs_pos = x - fx
								run_length = cx - fx
								run_height = cy - fy
								note_side = ((tail_direction * 1.5) + 1.5) * step
								rel_pos = abs_pos / run_length
								grad_pos = (rel_pos * run_height) + fy
								tail_length = -7 * step * tail_direction
								note_tail.move_to(x + note_side, grad_pos + tail_length + step)
								note_tail.line_to(x + note_side, y + step)
									#((clef_C0 - (note_index * step)) + step) - (tail_direction * (7 * step)))
								note_tail.stroke()
								
							run = []
						else:
							
							# note flag
							for bar in range(0, bars_to_draw):
								x, y = note_pos
								flag = ui.Path()
								
								x_offset = step * 1.5 * (1 + tail_direction)
								tail_length = step * -5.5 * tail_direction
								y_offset = step * 2 * bar * tail_direction
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
								
						# tails
						if note_beats < 4 and run == []:
							note_tail = ui.Path()
							note_tail.move_to(
								position + (((tail_direction * 1.5) + 1.5) * step),
								(clef_C0 - (note_index * step)) + step)
							note_tail.line_to(
								position + (((tail_direction * 1.5) + 1.5) * step),
								((clef_C0 - (note_index * step)) + step) - (tail_direction * (7 * step)))
							note_tail.stroke()
					
					else:
						
						#draw rest
						rest = ui.Label()
						rest.center = position, 30
						rest.text = 'Rest'
						rest.font = 'Helvetica', 30
						self.add_subview(rest)
						
					#increment
					position += note_gap * note_beats
					loop += 1

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
		
		
	
class MyView(ui.View):
	def __init__(self, song):
		self.name = song
		w, h = ui.get_screen_size()
		self.sv = ui.ScrollView()
		self.sv.width = w
		self.sv.height = h
		length = calculate_length(song)
		self.sv.content_size = (length, h)
		self.sv.add_subview(MusicView(song, length, screen_height))
		self.sig = ui.View()
		self.sig.width = w * screen_padding * 0.8
		self.sig.height = h
		self.sig.add_subview(Signature(self.sig.width, self.sig.height))
		
		
		self.add_subview(self.sv)
		self.add_subview(self.sig)
