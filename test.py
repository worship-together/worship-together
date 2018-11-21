import midi
import os
import shutil
import glob

from notes import *
import keys

midi.Song('cc_008').write_midi('cc_008.midi', [60, 60, 60, 60])
midi.Song('cc_345').write_midi('cc_345.midi', [60, 60, 60, 60])
midi.Song('cc_150.py').write_midi('cc_150.midi', [60, 60, 60, 60])
midi.Song('cc_182.py').write_midi('cc_182.midi', [60, 60, 60, 60])
midi.Song('cc_192.py').write_midi('cc_192.midi', [60, 60, 60, 60])
midi.Song('cc_334.py').write_midi('cc_334.midi', [60, 60, 60, 60])
midi.Song('cc_368.py').write_midi('cc_368.midi', [60, 60, 60, 60])
midi.Song('cc_074.py').write_midi('cc_074.midi', [60, 60, 60, 60])


def generate_midi(input):
	midi.Song(input).write_midi('full.midi', [60, 60, 60, 60])
	midi.Song(input).write_midi('soprano.midi', [60, 0, 0, 0])
	midi.Song(input).write_midi('soprano_bass.midi', [60, 0, 0, 60])
	
	
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
	generate_midi(filename)
	assert size('soprano.midi') < size('full.midi') / 2
	assert size('soprano.midi') > size('full.midi') / 4
	assert size('soprano_bass.midi') < size('full.midi') * 3 / 4
	assert size('soprano_bass.midi') > size('full.midi') / 2


# ****************************************************************************
#  Old File Format
#
name = "With All My Heart My Thanks I'll Bring"
Author = "The Book of Psalms for Singing, 1973"
key = keys.C
beats_per_measure = 4
tempo = 120

measures = [
    [
        [E4(2), E4, E4],
        [C4(2), C4, C4],
        [G3(2), G3, G3],
        [C3(2), C3, C3]
    ],
    [
        [G4(3), C5],
        [E4(3), C4],
        [C4(3), G3],
        [C3(3), E3]
    ],
    [
        [C5, A4, A4, F4],
        [F4(2), F4, D4],
        [A3, C4, C4, A3],
        [F3(2), F3(2)]
    ],
    [
        [E4(2), D4, R],
        [C4(2), B3, R],
        [G3(3), R],
        [G3(3), R]
    ]
]


# ****************************************************************************
#
#  New File Format
#

new_file_format = """
Name       With All My Heart My Thanks I'll Bring
Author     The Book of Psalms for Singing, 1973
Tune       WESLEY (L.M.)
Composer   Isaac B. Woodbury
Number     182
Key        C
Signature  4:4
Tempo      120

Soprano    e/2 e e | g/2. c+ | c+ a a f | e/2 d R | d#/1              | a
Alto       c/2 c c | e/2. c  | f/2  f d | c/2 b R | bb. c/8 d/2       | b
Tenor      g/2 g g | c/2. g  | a  c c a | g/2.  R | en(3)             | c
Bass       c/2 c c | c/2. e  | f/2  f/2 | g/2.  R | g#+/32.(3.8125)   | d

Verse      With all my heart my thanks I'll bring,
Verse      For though a - bove Thy name a - dored
Verse      All kings of earth shall thanks ac - cord 
"""

if __name__ == '__main__':
	try:
		shutil.copy('test.py', 'songs/test.py')
		test_song('test.py')
		with open('songs/test', 'w') as song_file:
			song_file.write(new_file_format)
		test_song('test')
		song = midi.Song('test')
		assert type(song.measures[-2][0][0]) == D4s
		print('success')
	finally:
		delete_midi()
