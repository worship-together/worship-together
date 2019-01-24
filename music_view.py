import ui
import photos
import console
import midi
import inspect


screen_width, screen_height = ui.get_screen_size()
notes_drawn = 0
screen_padding = 1/4#of the screen
note_gap = 100
origin = 50
treble_lines = []
bass_lines = []
for i in range(0, 5):
	treble_lines.append(screen_height * (screen_padding*((i+7)/8)))
	bass_lines.append(screen_height - (screen_height * (screen_padding*((i+7)/8))))
step = (treble_lines[1] - treble_lines[0]) / 2.0
C0_treble_y = treble_lines[4] + step + ((step * 7) * 4)


def create_index(note_name):
	note_name.split()
	index = ord(note_name[0]) - ord('C')
	if index < 0:
		index += 7
	return index + (int(note_name[1]) * 7)


class MusicView(ui.View):
	def __init__(self, width=1024, height=1024):
		self.frame = (0, 0, width, height)
		self.bg_color = 'white'
		
	def draw(self):
		global origin
		self.staff = ui.Path()
		for i in range(0, 5):
			self.staff.move_to(0, treble_lines[i])
			self.staff.line_to(screen_width, treble_lines[i])
			self.staff.move_to(0, bass_lines[i])
			self.staff.line_to(screen_width, bass_lines[i])
			
		song = [song for song in midi.songs if '334' in str(song)][0]
		print(song)
		for measure in song.measures:
			soprano = measure[midi.Voice.Soprano]
			for note in soprano:
				if inspect.isclass(note):
					note_name = note.__name__
				else:
					note_name = type(note).__name__
				print(note_name)
				note_index = create_index(note_name)
				print(note_index)
				
				self.note = ui.Path.oval(origin, C0_treble_y - (note_index * step), 3 * step, 2 * step)
				print(C0_treble_y - (note_index * step))
				self.note.fill()
				ui.set_color('black')
				origin += note_gap
			
			self.staff.stroke()
			self.note.stroke()
			

music_view = MusicView(screen_width * 2, screen_height)
music_view.name = 'Sketch'
music_view.present('fullscreen')
