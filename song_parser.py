"""
Song Parser

Requirements
- Note names are based on voice range
	C5 common, C4 rare...
	- Soporano: e to d = E4 to D5, e+ to d+ = E5 to D6, e- to d- = E3 to D4
	- Alto:     a to g = A3 to G4, a+ to b+ = A4 to G5, a- to g- = A2 to G3
	- Tenor:    e to d = E3 to D4, e+ to d+ = E4 to D5, e- to d+ = E2 to D3
	- Bass:     a to g = A2 to G3, a+ to b+ = A3 to G4, a- to g- = A1 to G2

TBD: Convert VoiceStream.__iter__ to count time correctly.  It is calling
     a quarter note a 'beat'.  The Note class should contain a 'Value' member
     instead of a 'Beats' member.  The total value of a measure should always
     equal one.
"""

import re

import keys
import notes


class NewSong:
	def __init__(self, attributes):
		self.name = attributes['name']
		self.number = attributes['number']
		self.key = attributes['key']
		self.measures = attributes['measures']
		self.beats_per_measure = attributes['beats_per_measure']
		self.beat_value = attributes['beat_value']
		self.tempo = int(attributes['tempo'])
		if 'psalm' in attributes:
			self.psalm = attributes['psalm']


attribute_re = re.compile(r'(?P<name>[a-zA-Z]+)\s+(?P<value>[^\n]+)')
note_re = re.compile(r'^'
                     r'(?P<name>[a-gR])' +
					 r'(?P<accidental>[#bn])?'
					 r'(?P<octave_shift>[\+\-])?'
                     r'(/(?P<note_value>[0-9]+))?'
                     r'(?P<dot>\.)?'
                     r'(\((?P<fermata>[0-9]+(\.[0-9]+)?)\))?'
                     r'$')
time_signature_re = re.compile(r'(?P<beats_per_measure>[0-9])\s*:\s*'
                               r'(?P<beat_value>[1-9])')


def create_note(voice, octave_shift, short_name, accidental):
	short_name = short_name.upper()
	if short_name == 'R':
		octave = ''
	else:
		if voice == 'soprano' or voice == 'unison':
			octave = 5 if short_name >= 'C' and short_name <= 'D' else 4
		elif voice == 'alto':
			octave = 3 if short_name >= 'A' and short_name <= 'B' else 4
		elif voice == 'tenor':
			octave = 4 if short_name >= 'C' and short_name <= 'D' else 3
		else:
			octave = 2 if short_name >= 'A' and short_name <= 'B' else 3
		if octave_shift == '+':
			octave += 1
		elif octave_shift == '-':
			octave -= 1
	if accidental == '#':
		accidental = 's'
	elif not accidental:
		accidental = ''
	return short_name + str(octave) + accidental


def parse_notes(beat_value, voice, line):
	measures = list()
	measures.append([])
	for symbol in line.split():
		if symbol == '|':
			measures.append([])
		else:
			match = note_re.match(symbol)
			if not match:
				raise RuntimeError('Cannot parse note \'' + symbol + '\'')
			short_name = match.group('name')
			octave_shift = match.group('octave_shift')
			accidental = match.group('accidental')
			note_name = create_note(voice, octave_shift, short_name, accidental)
			note_type = getattr(notes, note_name)
			note_value = match.group('note_value')
			beats = 1.0
			if note_value:
				beats = beat_value / int(note_value)
			if match.group('dot'):
				beats = beats * 1.5
			note = note_type(beats)
			fermata = match.group('fermata')
			if fermata:
				note.fermata_beats = float(fermata)
			measures[-1].append(note)
	return measures


def is_comment(line):
	return line[0] == '#'

def parse_line(line, attributes):
	line = line.strip()
	if line and not is_comment(line):
		match = attribute_re.match(line)
		if match:
			name = match.group('name').lower()
			raw_value = match.group('value')
			if name == 'key':
				value = getattr(keys, raw_value)
			elif name == 'signature':
				signature = time_signature_re.match(raw_value)
				beats_per_measure = signature.group('beats_per_measure')
				beat_value = int(signature.group('beat_value'))
				attributes['beats_per_measure'] = int(beats_per_measure)
				attributes['beat_value'] = int(beat_value)
				value = raw_value
			elif name in ['soprano', 'alto', 'tenor', 'bass', 'unison']:
				value = attributes[name] if name in attributes else []
				value += parse_notes(attributes['beat_value'], name, raw_value)
			else:
				value = raw_value
			attributes[name] = value
		else:
			raise RuntimeError('Cannot parse attribute')

def parse_song(filename):
	with open(filename, 'r') as song_file:
		attributes = {}
		for number, line in enumerate(song_file):
			try:
				parse_line(line, attributes)
			except Exception as e:
				raise RuntimeError(
					f'Error parsing file {filename}@{number+1}: {line} ' +
					str(e))
		if 'unison' in attributes:
			attributes['measures'] = [(measure, [], [], [])
			                          for measure in attributes['unison']]
		else:
			attributes['measures'] = [measure for measure in
		                            zip(attributes['soprano'],
		                                attributes['alto'],
		                                attributes['tenor'],
		                                attributes['bass'])]
		song = NewSong(attributes)
		#print(song.measures)
		return song
