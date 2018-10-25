import midi
import os
import shutil

from notes import *
import keys

midi.Song('cc_334.py').write_midi('cc_334.midi', [60, 60, 60, 60])
midi.Song('cc_182.py').write_midi('cc_182.midi', [60, 60, 60, 60])
midi.Song('cc_192.py').write_midi('cc_192.midi', [60, 60, 60, 60])
midi.Song('cc_150.py').write_midi('cc_150.midi', [60, 60, 60, 60])
midi.Song('cc_368.py').write_midi('cc_368.midi', [60, 60, 60, 60])


def generate_midi(input):
	midi.Song(input).write_midi('full.midi', [60, 60, 60, 60])
	midi.Song(input).write_midi('soprano.midi', [60, 0, 0, 0])
	midi.Song(input).write_midi('soprano_bass.midi', [60, 0, 0, 60])
	
	
def remove(filename):
	if os.path.exists(filename):
		os.remove(filename)
		
		
def delete_midi():
	remove('songs/test.py')
	remove('full.midi')
	remove('soprano.midi')
	remove('soprano_bass.midi')
	
	
def size(filename):
	return os.stat(filename).st_size
	
if __name__ == '__main__':
	try:
		shutil.copy('test.py', 'songs/test.py')
		generate_midi('test.py')
		assert size('soprano.midi') < size('full.midi') / 2
		assert size('soprano.midi') > size('full.midi') / 4
		assert size('soprano_bass.midi') < size('full.midi') * 3 / 4
		assert size('soprano_bass.midi') > size('full.midi') / 2
		print('success')
	finally:
		delete_midi()
		
key = keys.C

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

