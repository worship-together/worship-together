import ui
import enum
import itertools
import struct
import os
import importlib
import array
import sound

import midi

player = None
song_button = []
soprano_volume = 60
alto_volume = 60
tenor_volume = 60
bass_volume = 60


def switched(sender):
	if sender.value == True:
		pass
	else:
		print(sender.name + ' off')


def change_tempo(sender):
	global player
	player.rate = 2 * sender.value
	print(player.rate)
	

def adjust_time(sender):
	global player
	player.current_time = sender.value * player.duration


def play_pause(sender):
	global song, player
	if sender.title == 'Pause':
		sender.title = 'Play'
		player.stop()
		print('Paused')
	else:
		sender.title = 'Pause'
		volumes = [soprano_volume, alto_volume, tenor_volume, bass_volume]
		print(volumes)
		song.write_midi('output.midi', volumes)
		player = sound.MIDIPlayer('output.midi')
		player.play()
		#player.rate
		print('Playing')
	
def adjust_volume(sender):
	global soprano_volume, alto_volume, tenor_volume, bass_volume
	if sender.name == "soprano_volume":
		soprano_volume = sender.value * 120
	elif sender.name == "alto_volume":
		alto_volume = sender.value * 120
	elif sender.name == "tenor_volume":
		tenor_volume = sender.value * 120
	else:
		bass_volume = sender.value * 120
satb_page = ui.load_view('midi_ui')
print(type(satb_page.subviews))
# find button
print(list(subview for subview in satb_page.subviews if type(subview) == ui.Button))
#table = ui.TableView()
#table.add_subview(satb_page)

def present_song(sender):
	global song, player
	song = sender.items[sender.selected_row]
	song.write_midi('output.midi', [soprano_volume, alto_volume, tenor_volume, bass_volume])
	if player:
		player.stop()
	player = sound.MIDIPlayer('output.midi')
	satb_page.name = str(song)
	satb_page.present('sheet')
	


start_screen = ui.View()
start_screen.background_color = 'white'

table = ui.TableView()
table.row_height = 40
song_list = ui.ListDataSource(midi.songs)
song_list.action = present_song
table.data_source = table.delegate = song_list
screen_width, screen_height = ui.get_screen_size()
table.frame = 0, 0, screen_width, screen_height
start_screen.add_subview(table)
start_screen.present('fullscreen')
switch_gap_width = 5
song_length = 10473
