import ui
import photos
import console

screen_width, screen_height = ui.get_screen_size()
origin = 0
notes_drawn = 0
screen_padding = 1/6#of the screen
note_gap = 100

treble_lines = []
bass_lines = []
for i in range(0, 5):
	treble_lines.append(screen_height * (screen_padding*((i+7)/8)))
	bass_lines.append(screen_height - (screen_height * (screen_padding*((i+7)/8))))

#middle_treble_line = screen_height * 
# The main SketchView contains a PathView for the current
# line and an ImageView for rendering completed strokes.
# It also manages the 'Clear' and 'Save' ButtonItems that
# are shown in the title bar.

class MusicView(ui.View):
	def __init__(self, width=1024, height=1024):
		self.bg_color = 'white'
	
	def draw(self):
		self.staff = ui.Path()
		for i in range(0, 5):
			self.staff.move_to(0, treble_lines[i])
			self.staff.line_to(screen_width, treble_lines[i])
			self.staff.move_to(0, bass_lines[i])
			self.staff.line_to(screen_width, bass_lines[i])
		self.note1 = ui.Path.oval(50,50,25,15)
		self.note2 = ui.Path.oval(100,57,25,15)
		self.note1.fill()
		self.note2.fill()
		#ui.set_color('black')
			
		self.staff.stroke()
		self.note1.stroke()
		self.note2.stroke()
		
		#play_pause = ui.

	
# We use a square canvas, so that the same image
# can be used in portrait and landscape orientation.
canvas_size = max(screen_width, screen_height)

sv = MusicView(canvas_size, canvas_size)
sv.name = 'Sketch'
sv.present('fullscreen')
