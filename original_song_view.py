import ui
import sound
import midi
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
	if playing():
		sender.title = 'Play'
		position = player.current_time
		rate = player.rate
		stop()
	else:
		sender.title = 'Pause'
		write_midi(song)
		player = sound.MIDIPlayer('output.midi')
		# obc_player = objc_util.ObjCClass('AVMIDIPlayer')
		# obc_player.init('output.midi', None)
		adjust_time(get_subview('time_adjuster'))
		play()
		player.rate = get_subview('tempo_slider').value + 0.5


def adjust_volume(sender):
	global player
	if player != None and playing():
		play_pause(get_subview('play_button'))
		play_pause(get_subview('play_button'))


def present_song(sender):
	global satb_page, song, player, tracking_song, position, dragging, last_position
	if not satb_page:
		satb_page = ui.load_view('original_midi_ui')
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