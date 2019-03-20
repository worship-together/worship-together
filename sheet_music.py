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
		for measure in measures:
			position -= note_gap / 2
			measure_bar = ui.Path()
			measure_bar.move_to(position, treble_lines[0])
			measure_bar.line_to(position, bass_lines[0])
			measure_bar.stroke()
			position += note_gap / 2
			voice_selected = measure[voice]
			if isinstance(voice_selected, list):
				for note in voice_selected:
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
					
					# draw note
					if not note_index == -1:
						self.note_dot = ui.Path.oval(position, clef_C0 - (note_index * step), 3 * step, 2 * step)
						self.note_dot.stroke()
						ui.set_color('black')
						
						# draw tails, hollow/solid notes
						if note_beats < 2:
							self.note_dot.fill()
						if note_beats < 4:
							self.note_tail = ui.Path()
							self.note_tail.move_to(
								position + (((tail_direction * 1.5) + 1.5) * step),
								(clef_C0 - (note_index * step)) + step)
							self.note_tail.line_to(
								position + (((tail_direction * 1.5) + 1.5) * step),
								((clef_C0 - (note_index * step)) + step) - (tail_direction * (7 * step)))
							self.note_tail.stroke()
							
						# draw dots
						if not note_beats == 3 and note_beats % 1.5 == 0:
							self.note_dotted = ui.Path()
							self.note_dotted = ui.Path.oval(position + (4 * step), clef_C0 - ((note_index - 0.6) * step), 0.4 * step, 0.4 * step)
							self.note_dotted.stroke()
							ui.set_color('black')
							self.note_dotted.fill()
						
						# draw ties	
						#if prev_note_tied:
							#self.note_tie = ui.Path()
							#self.note_tie.move_to(prev_note_pos, clef_C0 - (note_index * step))
							#self.note_tie.add_quad_curve(position, clef_C0 - (note_index * step), 90, 90)
							#self.note_tie.stroke()
							
						# draw bars
						if bars_to_draw == prev_bars_to_draw:
							for bar in range(0, bars_to_draw):
								self.bar = ui.Path()
								x, y = prev_note_pos
								self.bar.move_to(x + (step * 1.5 * (1 + tail_direction)), (y + (step * -6 * tail_direction)) + (step - (tail_direction * step)))
								x, y = note_pos
								self.bar.line_to(x + (step * 1.5 * (1 + tail_direction)), (y + (step * -6 * tail_direction)) + (step - (tail_direction * step)))
								self.bar.stroke()
						
					else:
						rest = ui.Label()
						rest.center = position, 30
						rest.text = 'Rest'
						rest.font = 'Helvetica', 30
						self.add_subview(rest)
					position += note_gap * note_beats


class MyView(ui.View):
	def __init__(self, song):
		w, h = ui.get_screen_size()
		self.sv = ui.ScrollView()
		self.sv.width = w
		self.sv.height = h
		length = calculate_length(song)
		self.sv.content_size = (length, h)
		self.sv.add_subview(MusicView(song, length, screen_height))
		self.add_subview(self.sv)
