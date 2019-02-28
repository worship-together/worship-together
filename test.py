#!/usr/bin/env python3
"""
Test Song Parsing

Usage:
	test.py [--upload | --delete | --list] [<song> ...]

Options:
	--upload      Upload specified song(s) to remote
	--delete      Delete specified song(s) from remote
	--list        List all songs on remote
"""

import os
import glob
import docopt

from notes import *
import keys
import midi
import storage

def song_file(prefix):
	return os.path.basename(glob.glob('songs/' + prefix)[0])


def generate_midi(input):
	song = midi.Song(input)
	song.write_midi('full.midi', [60, 60, 60, 60])
	if not song.is_unison:
		song.write_midi('soprano.midi', [60, 0, 0, 0])
		song.write_midi('soprano_bass.midi', [30, 0, 0, 60])
	return song
	
	
def remove(filename):
	if os.path.exists(filename):
		os.remove(filename)
		
		
def delete_midi():
	remove('songs/test.py')
	remove('songs/test')
	for midi_file in glob.glob("*.midi"):
		remove(midi_file)

	
def size(filename):
	return os.stat(filename).st_size


def test_song(filename):
	try:
		song = generate_midi(filename)
		if not song.is_unison and size('full.midi') > 100:
			assert size('soprano.midi') < size('full.midi') / 2.0
			assert size('soprano.midi') > size('full.midi') / 5.0
			assert size('soprano_bass.midi') < size('full.midi') * 3.0 / 4.0
			assert size('soprano_bass.midi') > size('full.midi') / 3.0
	except Exception as e:
		print(filename + ': ' + str(e))



# ****************************************************************************
#
#  New File Format
#

new_file_format = """
title      Test Song
page       342
author     The Book of Psalms for Singing, 1973

tune       WESLEY (L.M.)
composer   Isaac B. Woodbury
key        C
rhythm     4:4
tempo      120

voice      soprano E4 to D5
voice      alto    A3 to G4
voice      tenor   E3 to D4
voice      bass    A2 to G3

soprano    e/2 e e | g/2. c+ | c+ a a f | e/2 d R | d#/1               | a
alto       c/2 c c | e/2. c  | f/2  f d | c/2 b R | bb. c/8 d/2        | b
tenor      g/2 g g | c/2. g  | a  c c a | g/2.  R | en-(3) f/2.        | c
bass       c/1 | c/1  | f/1 | g/1   | g#+/32.(1.2) f/64 a/16 c/8 d e f | d

verse      With all my heart my thanks I'll bring,
verse      For though a - bove Thy name a - dored
verse      All kings of earth shall thanks ac - cord 
"""


def test_all_songs():
	try:
		with open('songs/test', 'w') as song_file:
			song_file.write(new_file_format)
		test_song('test')
		song = midi.Song('test')
		assert type(song.measures[-2][midi.Voice.Soprano][0]) == D5s
		assert song.measures[-2][midi.Voice.Soprano][0].beats == 4
		assert type(song.measures[-2][midi.Voice.Alto][0]) == B3b
		assert song.measures[-2][midi.Voice.Alto][1].beats == 0.5
		assert song.measures[-2][midi.Voice.Alto][2].beats == 2.0
		assert type(song.measures[-2][midi.Voice.Tenor][0]) == E2n
		assert song.measures[-2][midi.Voice.Tenor][0].beats == 1.0
		assert song.measures[-2][midi.Voice.Tenor][0].fermata_beats == 3.0
		assert type(song.measures[-2][midi.Voice.Bass][0]) == G4s
		assert song.measures[-2][midi.Voice.Bass][0].beats == 0.1875
		assert song.measures[-2][midi.Voice.Bass][0].fermata_beats == 1.2
		for song in os.listdir('./songs'):
			if midi.is_song(song):
				test_song(song)
	finally:
		delete_midi()


def check_songs(songs):
	for song in arguments['<song>']:
		if not os.path.exists(song):
			exit('Song "' + song + '" does not exist.')


def test_and_delete_midi(song):
	try:
		print('Testing ' + song)
		test_song(os.path.basename(song))
	finally:
		delete_midi()


def upload(songs):
	tunes = []
	if not songs:
		songs = glob.glob('songs/*')
		tunes = glob.glob('tunes/*')
	for song in songs:
		if midi.is_song(os.path.basename(song)):
			test_and_delete_midi(song)
			print('Uploading ' + song)
			storage.sync_upload_file('songs', os.path.basename(song), song)
	for tune in tunes:
		storage.sync_upload_file('tunes', os.path.basename(tune), tune)


def delete(songs):
	for song in songs:
		print('Deleting ' + song)
		storage.sync_delete_remote_file('songs', os.path.basename(song))


def test(songs):
	for song in songs:
		test_and_delete_midi(song)


if __name__ == '__main__':
	arguments = docopt.docopt(__doc__)
	if arguments['<song>']:
		check_songs(arguments['<song>'])
	if arguments['--list']:
		storage.list_all_remote_files('songs')
	elif arguments['--upload']:
		upload(arguments['<song>'])
	elif arguments['--delete']:
		delete(arguments['<song>'])
	elif arguments['<song>']:
		test(arguments['<song>'])
	else:
		test_all_songs()
	print('success')
