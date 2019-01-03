import ui
import sound
import midi
import sheet_music
import storage
from objc_util import *

exiting = False
player = None
rate = 1
position = 0
tracking_song = False
dragging = False
last_position = 0.0000000
satb_page = None
song = None

def bring_up_sheet_music(sender):
	music = sheet_music.MyView(song)
	music.present('fullscreen')

def write_midi(song):
	song.write_midi('output.midi', [
		int(get_subview('soprano_volume').value * 120), 
		int(get_subview('alto_volume').value * 120), 
		int(get_subview('tenor_volume').value * 120), 
		int(get_subview('bass_volume').value * 120)])


def play():
	if player:
		player.play()
	
	
def stop():
	if player:
		player.stop()


def playing():
	return get_subview('play_button').title == 'Pause'
	
	
def get_subview(name):
	for subview in satb_page.subviews:
		if subview.name == name:
			return subview
	raise RuntimeError(f'nutn is namd {name}')

def track_time(slider):
	global player, dragging, last_position, rate, position
	if player and not dragging:
		if slider.value == last_position:
			slider.value = player.current_time / player.duration
			if slider.value == 1:
				player.current_time = 0
				player.rate = rate
				play()
				slider.value = player.current_time / player.duration
			last_position = slider.value
		else:
			dragging = True
			position = player.current_time
	if exiting:
		stop()
	else:
		ui.delay(lambda: track_time(slider), 0.05)
	

def change_tempo(sender):
	player.rate = sender.value + 0.5


def adjust_time(slider):
	global player, position, last_position, dragging
	if player:
		player.current_time = slider.value * player.duration
		position = player.current_time
		last_position = slider.value
		dragging = False
		

def play_pause(sender):
	global song, player, rate, position
	if playing():
		sender.title = 'Play'
		position = player.current_time
		rate = player.rate
		stop()
	else:
		sender.title = 'Pause'
		write_midi(song)
		player = sound.MIDIPlayer('output.midi')
		adjust_time(get_subview('time_adjuster'))
		play()
		player.rate = get_subview('tempo_slider').value + 0.5
		
		
def adjust_volume(sender):
	global player
	if player != None and playing():
		play_pause(get_subview('play_button'))
		play_pause(get_subview('play_button'))



def present_song(sender):
	global song, player, tracking_song, position, dragging, last_position
	song = sender.items[sender.selected_row]
	# write_midi(song)
	play_button = get_subview('play_button')
	if play_button.title == 'Pause':
		play_pause(play_button)
	if player:
		player.current_time = 0
	satb_page.name = str(song)
	satb_page.present('sheet')
	position = 0
	get_subview('time_adjuster').value = 0
	slider = get_subview("time_adjuster")
	dragging = False
	last_position = slider.value
	if not tracking_song:
		tracking_song = True
		track_time(slider)


class StartScreen(ui.View):
	def will_close(self):
		global exiting
		exiting = True


satb_page = ui.load_view('midi_ui')
start_screen = StartScreen()
start_screen.background_color = 'white'

table = ui.TableView()
btn_images = [ui.Image.named(n) for n in ['iob:beaker_32', 'iob:beer_32', 'iob:coffee_32']]
btn_container = ui.View(frame=(0, 0, len(btn_images)*32, 44))
btn = ui.Button(image=ui.Image.named('iob:loop_256'))
btn.frame = (64, 0, 32, 44)
btn.action = lambda sender: storage.synchronize('songs', 'songs')
btn_container.add_subview(btn)

btn_item = ui.ButtonItem()
btn_item_objc = ObjCInstance(btn_item)
btn_item_objc.customView = ObjCInstance(btn_container)
song_list = ui.ListDataSource(midi.songs)
song_list.action = present_song
table.data_source = table.delegate = song_list
screen_width, screen_height = ui.get_screen_size()
table.row_height = 40
table.frame = 0, 0, screen_width, screen_height - 64
start_screen.add_subview(table)
start_screen.right_button_items = [btn_item]
start_screen.present('fullscreen')
