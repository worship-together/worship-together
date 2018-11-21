import ui
import midi

screen_width, screen_height = ui.get_screen_size()
notes_drawn = 0
screen_padding = 1/6#of the screen
note_gap = 100
origin = 50
end = origin
soprano_position = origin
alto_position = origin
tenor_position = origin
bass_position = origin
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


def draw_notes(self, voice, measures, clef):
	global origin, end
	position = origin
	for measure in measures:
		voice_selected = measure[voice]
		for note in voice_selected:
			if type(note) is type:
				note_name = note.__name__
			else:
				note_name = type(note).__name__
			note_index = create_index(note_name)
			if clef == 'treble':
				self.note = ui.Path.oval(position, C0_treble_y - (note_index * step), 3 * step, 2 * step)
			else:
				self.note = ui.Path.oval(position, C0_bass_y - (note_index * step), 3 * step, 2 * step)
			self.note.fill()
			ui.set_color('black')
			position += note_gap

def calculate_length():
	global origin
	song = [song for song in midi.songs if '362' in str(song)][0]
	end = origin
	for measure in song.measures:
		voice_selected = measure[midi.Voice.Soprano]
		for note in voice_selected:
			end += note_gap
	return end
			

class MusicView(ui.View):
	def __init__(self, width=1024, height=1024):
		self.frame = (0, 0, width, height)
		self.bg_color = 'white'
		
	def draw(self):
		global origin
			
		song = [song for song in midi.songs if '362' in str(song)][0]
		draw_notes(self, midi.Voice.Soprano, song.measures, 'treble')
		draw_notes(self, midi.Voice.Alto, song.measures, 'treble')
		draw_notes(self, midi.Voice.Tenor, song.measures, 'bass')
		draw_notes(self, midi.Voice.Bass, song.measures, 'bass')
				
		self.staff = ui.Path()
		for i in range(0, 5):
			self.staff.move_to(0, treble_lines[i])
			self.staff.line_to(calculate_length(), treble_lines[i])
			self.staff.move_to(0, bass_lines[i])
			self.staff.line_to(calculate_length(), bass_lines[i])
			
		self.staff.stroke()
		self.note.stroke()
			
			
music_view = MusicView(calculate_length(), screen_height)


class MyView(ui.View):
	def __init__(self):
		w, h = ui.get_screen_size()
		self.sv = ui.ScrollView()
		self.sv.width = w
		self.sv.height = h
		self.sv.content_size = (calculate_length(), h)
		self.sv.add_subview(music_view)
		self.add_subview(self.sv)
view = MyView()
view.present('fullscreen')

