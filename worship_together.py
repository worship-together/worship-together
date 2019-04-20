import ui
import sound
import midi
import sheet_music
import storage
import objc_util
import ctypes
import os
import sound

exiting = False
player = None
rate = 1
position = 0
tracking_song = False
dragging = False
last_position = 0.0000000
satb_page = None
song = None

settings = ui.load_view('midi_ui')

def bring_up_sheet_music(sender):
	button_width = 50
	music = sheet_music.MyView(song)
	music.present('fullscreen', hide_title_bar=True)
	exit_btn = ui.Button(image=ui.Image.named('iob:ios7_arrow_left_256'))
	exit_btn.frame = (0, 10, button_width, button_width + 10)
	exit_btn.action = lambda sender: music.close()
	music.add_subview(exit_btn)


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
	return get_play_button().title == 'Pause'


def get_subview(name):
	global settings
	for subview in settings.subviews:
		if subview.name == name:
			return subview
	raise RuntimeError('nutn is namd ' + name)

def get_play_button():
	for subview in satb_page.subviews:
		if subview.name == 'play_button':
			return subview
	raise RuntimeError('fruvit nub it')

def track_time(slider):
	global player, dragging, last_position, rate, position
	if player and not dragging:
		if slider.value == last_position:
			slider.value = player.current_time / float(player.duration)
			if slider.value == 1 and get_play_button().playing:
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


def change_tempo(sender):
	player.rate = sender.value + 0.5
	print(player.rate)


def adjust_time(slider):
	global player, position, last_position, dragging
	if player:
		player.current_time = slider.value * player.duration
		position = player.current_time
		last_position = slider.value
		dragging = False


def play_pause(sender):
	global song, player, rate, position
	if sender.playing:
		sender.image = ui.Image.named('iob:ios7_play_outline_256')
		sender.playing = False
		position = player.current_time
		rate = player.rate
		stop()
	else:
		sender.image = ui.Image.named('iob:ios7_pause_outline_256')
		sender.playing = True
		write_midi(song)
		player = sound.MIDIPlayer('output.midi')
		# obc_player = objc_util.ObjCClass('AVMIDIPlayer')
		# obc_player.init('output.midi', None)
		adjust_time(satb_page.sv)
		play()
		player.rate = get_subview('tempo_slider').value + 0.5


def adjust_volume(sender):
	global player
	if player != None and playing():
		play_pause(get_play_button())
		play_pause(get_play_button())

def present_settings(sender):
	global settings
	settings.present('sheet')

def present_song(sender):
	global satb_page, song, player, tracking_song, position, dragging, last_position
	song = sender.items[sender.selected_row]
	if not satb_page:
		satb_page = sheet_music.MyView(song)
		w, h = ui.get_screen_size()
		exit_btn = ui.Button(image=ui.Image.named('iob:ios7_arrow_left_256'))
		button_width = 50
		exit_btn.frame = (0, 10, button_width, button_width + 10)
		exit_btn.action = lambda sender: satb_page.close()
		satb_page.add_subview(exit_btn)
		play_btn = ui.Button(image=ui.Image.named('iob:ios7_play_outline_256'))
		play_btn.frame = ((h/2) - button_width, h - button_width, h/2, button_width)
		play_btn.action = play_pause
		play_btn.playing = False
		play_btn.name = 'play_button'
		
		settings_btn = ui.Button(image=ui.Image.named('iob:ios7_gear_outline_256'))
		settings_btn.frame = (h/2, h - button_width, button_width, button_width)
		settings_btn.action = present_settings
		
		
		satb_page.add_subview(play_btn)
		satb_page.add_subview(settings_btn)
	play_button = get_play_button()
	if play_button.playing:
		play_pause(play_button)
	if player:
		player.current_time = 0
	satb_page.present('fullscreen', hide_title_bar=True)
	position = 0
	satb_page.sv.value = 0
	slider = satb_page.sv
	dragging = False
	last_position = slider.value
	if not tracking_song:
		tracking_song = True
		track_time(slider)


class StartScreen(ui.View):
	def will_close(self):
		global exiting
		exiting = True


def sync_songs_and_tunes():
	storage.iPad('songs', 'songs').synchronize()
	storage.iPad('songs', 'songs').synchronize()


def create_sync_button():
	btn_container = ui.View(frame=(0, 0, 32, 44))
	btn = ui.Button(image=ui.Image.named('iob:loop_256'))
	btn.frame = (64, 0, 32, 44)
	btn.action = lambda sender: sync_songs_and_tunes()
	btn_container.add_subview(btn)
	btn_item = ui.ButtonItem()
	btn_item_objc = objc_util.ObjCInstance(btn_item)
	btn_item_objc.customView = objc_util.ObjCInstance(btn_container)
	return btn_item


def create_song_list():
	table = ui.TableView()
	song_files = [file for file in os.listdir('./songs')
				  if midi.is_song(file)]
	song_list = ui.ListDataSource(sorted(song_files))
	song_list.action = present_song
	table.data_source = table.delegate = song_list
	screen_width, screen_height = ui.get_screen_size()
	table.row_height = 40
	table.frame = 0, 0, screen_width, screen_height - 64
	return table


start_screen = StartScreen()
start_screen.background_color = 'white'
start_screen.add_subview(create_song_list())
start_screen.right_button_items = [create_sync_button()]
start_screen.present('fullscreen')
