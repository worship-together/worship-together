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
import traceback
import sys

from notes import *
import keys
import midi
import storage


def test_all_songs():
	try:
		verify_test_song()
		for song in os.listdir('./songs'):
			if midi.is_song(song):
				test_song(song)
	finally:
		delete_midi()


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
			assert size('soprano.midi') < size('full.midi') / 1.5
			assert size('soprano.midi') > size('full.midi') / 5.0
			assert size('soprano_bass.midi') < size('full.midi') * 3.0 / 4.0
			assert size('soprano_bass.midi') > size('full.midi') / 3.0
	except AssertionError as e:
		print(filename + ': AssertionError', file=sys.stderr)
		traceback.print_exc()
		print(file=sys.stderr)
	except Exception as e:
		print(filename + ': ' + str(e), file=sys.stderr)
		print(file=sys.stderr)



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

verse    'Tis    by      thy    strength  the   moun - tains stand,
verse    Thy     morn -  ing    light     and   ev -   'ning shade

verse    God     of     e -  ter - nal   power;
verse    Suc -   ces -  sive com - forts bring;

verse    O come,_ let us a - dore Him, Christ the Lord!


repeat	begin

s_verse  The  sea    grows calm   at    thy     com - mand,
s_verse  Thy  plen - teous fruits make  har -   vest  glad,

a_verse  _  _  _  The  sea    grows calm   at    thy     com - mand,
a_verse  _  _  _  Thy  plen - teous fruits make  har -   vest  glad,

t_verse  _  _  _  _  The  sea    grows calm   at    thy     com - mand,
t_verse  _  _  _  _  Thy  plen - teous fruits make  har -   vest  glad,

b_verse  _  _  _  _  _  The  sea    grows calm   at    thy     com - mand,
b_verse  _  _  _  _  _  Thy  plen - teous fruits make  har -   vest  glad,


s_verse  And tem -   pests cease  to   roar.    _  _  _  _

a_verse  And tem -   pests cease  to   roar.    _  _  _

t_verse  And tem -   pests cease  to   roar.    _  _

b_verse  And tem -   pests cease  to   roar.


verse    And tem -   pests cease  to   roar.
verse    Thy flowers a -   dorn   the  spring.

verse    And tem -   pests cease  to   roar.
verse    Thy flowers a -   dorn   the  spring.

verse    O come, let us a - dore Him, Christ the Lord!

repeat   end

"""


def verify_test_song():
	with open('songs/test', 'w') as song_file:
		song_file.write(new_file_format)
	test_song('test')
	song = midi.Song('test')
	verify_test_notes(song)
	# verify_test_lyrics(song)


def verify_test_notes(song):
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


def verify_test_lyrics(song):
	verses = song.verses
	assert len(verses) == 2
	verse_1 = verses[0]
	syllable = 0
	assert verse_1[syllable + 0] == ['', '', '', '', '\'Tis']
	assert verse_1[syllable + 1] == ['', '', '', '', 'by']
	assert verse_1[syllable + 5] == ['', '', '', '', 'moun-']
	syllable += 13
	assert verse_1[syllable + 0] == ['', '', '', '', 'power;']
	assert verse_1[syllable + 2] == ['', '', '', '', 'come,_']
	assert verse_1[syllable + 3] == ['', '', '', '', '']
	syllable += 11
	assert verse_1[syllable + 0] == ['', '', '', '', 'Lord!']
	assert verse_1[syllable + 1] == ['The', '', '', '', '']
	assert verse_1[syllable + 4] == ['calm', 'The', '', '', '']
	assert verse_1[syllable + 5] == ['at', 'sea', 'The', '', '']
	assert verse_1[syllable + 6] == ['thy', 'grows', 'sea', 'The', '']
	syllable += 14
	assert verse_1[syllable + 0] == ['roar.', 'to', 'cease', 'tem-', '']
	assert verse_1[syllable + 1] == ['', 'roar.', 'to', 'pests', '']
	assert verse_1[syllable + 2] == ['', '', 'roar.', 'cease', '']
	assert verse_1[syllable + 3] == ['', '', '', 'to', '']
	assert verse_1[syllable + 4] == ['', '', '', 'roar.', '']
	assert verse_1[syllable + 5] == ['', '', '', '', 'And']
	syllable += 16
	assert verse_1[syllable + 0] == ['', '', '', '', 'roar.']
	assert verse_1[syllable + 1] == ['', '', '', '', 'O']
	syllable += 9
	assert verse_1[syllable + 0] == ['', '', '', '', 'Lord!']
	assert verse_1[syllable + 1] == ['The', '', '', '', '']
	assert verse_1[syllable + 4] == ['calm', 'The', '', '', '']
	verse_2 = verses[0]
	syllable = 0
	assert verse_2[syllable + 0] == ['', '', '', '', 'Thy']
	assert verse_2[syllable + 1] == ['', '', '', '', 'morn-']
	assert verse_2[syllable + 5] == ['', '', '', '', 'ing']
	syllable += 13
	assert verse_2[syllable + 0] == ['', '', '', '', 'bring;']
	assert verse_2[syllable + 1] == ['', '', '', '', 'O']
	syllable += 19
	assert verse_2[syllable + 0] == ['glad,', 'make', 'fruits', 'teous', '']
	assert verse_2[syllable + 1] == ['And', 'har', 'make', 'fruits', '']


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
			storage.upload_file_to_remote('songs', os.path.basename(song), song)
	for tune in tunes:
		storage.upload_file_to_remote('tunes', os.path.basename(tune), tune)


def delete(songs):
	for song in songs:
		print('Deleting ' + song)
		storage.delete_remote_file('songs', os.path.basename(song))


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
