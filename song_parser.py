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
import os


def parse_song(filename):
	lines = _Import.expand(filename)
	lines = [_Comment.strip(line) for line in lines]
	lines = _Repeat.expand(lines)
	song_lines, tune_lines = _Splitter.split(lines)
	song = Song(song_lines)
	tune = Tune(tune_lines)
	return song


class Song:
	def __init__(self, lines):
		self.title = _Attribute.get('title', lines)
		if not self.title:
			raise RuntimeError('Song ' + lines[0].filename +
							   ' must have title attribute')
		self.page = _Attribute.get('page', lines)
		self.author = _Attribute.get('author', lines)
		self.translator = _Attribute.get('translator', lines)
		self.psalm = _Attribute.get('psalm', lines)
		# if 'page' in attributes:
		# 	self.page = attributes['page']
		# self.key = attributes['key']
		# self.measures = attributes['measures']
		# self.beats_per_measure = attributes['beats_per_measure']
		# self.beat_value = attributes['beat_value']
		# self.tempo = int(attributes['tempo'])
		# if 'psalm' in attributes:
		# 	self.psalm = attributes['psalm']
		# self.is_unison = 'unison' in attributes

	# def _parse_lines(lines, attributes):
	# 	for line in lines:
	# 		if line:
	# 			try:
	# 				parse_line(line, attributes)
	# 			except Exception as e:
	# 				raise RuntimeError(
	# 					'Error parsing file ' + line.filename + ' at line ' +
	# 					str(line.number) + ': ' + str(e))


class Tune:
	def __init__(self, lines):
		self._lines = lines
		self.name = self._get('tune')
		self.composer = self._get('composer')
		self.meter = self._get('meter')
		unison = self._get_lines('unison')
		if unison:
			self.measures = [(measure, [], [], [])
							 for measure in self._parse_measures(unison)]
		else:
			self.measures = zip(
				*(self._parse_measures(self._get_lines(voice))
				  for voice in ['soprano', 'alto', 'tenor', 'bass'])
			)
		# self.key = attributes['key']
		# self.measures = attributes['measures']
		# self.beats_per_measure = attributes['beats_per_measure']
		# self.beat_value = attributes['beat_value']
		# self.tempo = int(attributes['tempo'])

	def _get(self, attribute_name):
		return _Attribute.get(attribute_name, self._lines)

	def _get_lines(self, voice):
		attribute_names = [voice, 'key', 'rhythm', 'tempo', 'repeat']
		return _Attribute.get_lines(attribute_names, self._lines)

	def _parse_measures(self, lines):
		return []


	# def _parse_lines(lines, attributes):
	# 	for line in lines:
	# 		if line:
	# 			try:
	# 				parse_line(line, attributes)
	# 			except Exception as e:
	# 				raise RuntimeError(
	# 					'Error parsing file ' + line.filename + ' at line ' +
	# 					str(line.number) + ': ' + str(e))

	# def parse_line(line, attributes):
	# 	match = attribute_re.match(line)
	# 	if match:
	# 		name = match.group('name').lower()
	# 		raw_value = match.group('value')
	# 		if name == 'key':
	# 			if len(raw_value) > 1:
	# 				if raw_value.endswith('b'):
	# 					raw_value = raw_value[0:-1] + '_Flat'
	# 				elif raw_value.endswith('#'):
	# 					raw_value = raw_value[0:-1] + '_Sharp'
	# 			value = getattr(keys, raw_value)
	# 		elif name == 'rhythm':
	# 			rhythm = rhythm_re.match(raw_value)
	# 			beats_per_measure = rhythm.group('beats_per_measure')
	# 			beat_value = int(rhythm.group('beat_value'))
	# 			attributes['beats_per_measure'] = int(beats_per_measure)
	# 			attributes['beat_value'] = int(beat_value)
	# 			value = raw_value
	# 		elif name in ['soprano', 'alto', 'tenor', 'bass', 'unison']:
	# 			value = attributes[name] if name in attributes else []
	# 			if 'beat_value' not in attributes:
	# 				raise RuntimeError('missing "rhythm" attribute')
	# 			elif 'key' not in attributes:
	# 				raise RuntimeError('key must be declared before notes')
	# 			beat_value = attributes['beat_value']
	# 			key = attributes['key']
	# 			value += parse_notes(beat_value, key, name, raw_value)
	# 		else:
	# 			value = raw_value
	# 			if name in attributes:
	# 				non_list_attributes = [ 'tempo', 'beats' ]
	# 				if name in non_list_attributes:
	# 					raise RuntimeError('Error: Multiple {name} attributes')
	# 				if not attributes[name] is list:
	# 					value = [attributes[name], value]
	# 				else:
	# 					value = attributes[name].append(value)
	# 		attributes[name] = value
	# 	else:
	# 		raise RuntimeError('Cannot parse attribute')


class _Line:
	def __init__(self, filename, number, text):
		self.filename = filename
		self.number = number
		self.text = text


class _Import:
	@staticmethod
	def expand(filename):
		lines = _Import._read_lines(filename)
		return list(_Import._expand_imports(lines))

	@staticmethod
	def _read_lines(filename):
		with open(filename, 'r') as file:
			return [_Line(filename, number + 1, text.strip())
					for number, text in enumerate(file)]


	@staticmethod
	def _expand_imports(lines):
		regex = re.compile(r'import\s+(?P<filename>[^\n]+)')
		for line in lines:
			match = regex.match(line.text)
			if match:
				filename = match.group('filename')
				_Import._verify_file_exists(filename, line)
				yield from _Import._expand_imports(
					_Import._read_lines(filename))
			else:
				yield line

	@staticmethod
	def _verify_file_exists(filename, from_line):
		if not os.path.isfile(filename):
			message = 'Error importing ' + filename
			message += ' from ' + from_line.filename
			message += ' at line ' + str(from_line.number)
			raise RuntimeError(message)

	@staticmethod
	def _test():
		def write_test_file(filename, content):
			with open(filename, 'w') as file:
				file.write(content)

		def check_line(filename, index, number, text):
			assert lines[index].filename == filename
			assert lines[index].number == number
			assert lines[index].text == text

		print('testing _Import')

		write_test_file('songs/test_a', 'a b\nimport songs/test_b\nc d\n')
		write_test_file('songs/test_b', 'e f\nimport songs/test_c\ng h\n')
		write_test_file('songs/test_c', 'i j\n')
		write_test_file('songs/error', 'a b\nimport songs/missing_file\nc d')

		lines = list(_Import.expand('songs/test_a'))
		check_line('songs/test_a', index=0, number=1, text='a b')
		check_line('songs/test_b', index=1, number=1, text='e f')
		check_line('songs/test_c', index=2, number=1, text='i j')
		check_line('songs/test_b', index=3, number=3, text='g h')
		check_line('songs/test_a', index=-1, number=3, text='c d')

		try:
			_Import.expand('songs/error')
			raise AssertionError('Expected import error')
		except RuntimeError as e:
			assert 'Error importing' in str(e)
			assert 'at line 2' in str(e)

		os.remove('songs/test_a')
		os.remove('songs/test_b')
		os.remove('songs/test_c')
		os.remove('songs/error')


class _Comment:
	@staticmethod
	def strip(line):
		if '#' in line.text:
			line.text = line.text[0:line.text.find('#')].strip()

	@staticmethod
	def _test():
		print('testing _Comment')
		_Comment._verify_comment(text='no comment', result='no comment')
		_Comment._verify_comment(text='# full comment', result='')
		_Comment._verify_comment(text='a b # partial comment', result='a b')

	@staticmethod
	def _verify_comment(text, result):
		line = _Line('filename', number=1, text=text)
		_Comment.strip(line)
		assert line.text == result


class _Splitter:
	@staticmethod
	def split(lines):
		in_song = True
		song_lines = []
		tune_lines = []
		for line in lines:
			if in_song and not line.text.startswith('tune'):
				song_lines.append(line)
			else:
				in_song = False
				tune_lines.append(line)
		return song_lines, tune_lines

	@staticmethod
	def _test():
		print('testing _Splitter')
		lines = [
			_Line('file', number=1, text='title Food For Thought'),
			_Line('file', number=1, text='tune  A Lovely Day'),
			_Line('file', number=1, text='bass  c/2'),
		]
		song_lines, tune_lines = _Splitter.split(lines)
		assert len(song_lines) == 1
		assert len(tune_lines) == 2
		assert song_lines[0].text.startswith('title')
		assert tune_lines[0].text.startswith('tune')


class _Attribute:
	@staticmethod
	def get(name, lines):
		value = ''
		for line in lines:
			match = _Attribute._regex.match(line.text)
			if match and name == match.group('name').lower():
				value += '\n' if value else ''
				value += match.group('value').strip()
		return value

	@staticmethod
	def get_lines(names, lines):
		for line in lines:
			match = _Attribute._regex.match(line.text)
			if match and match.group('name').lower() in names:
				yield line

	_regex = re.compile(r'(?P<name>[a-zA-Z\-_]+)\s+(?P<value>[^\n]+)')

	@staticmethod
	def _test():
		print('testing _Attribute')
		lines = [
			_Line('file', number=1, text='foo bar'),
			_Line('file', number=2, text='bop dim'),
			_Line('file', number=3, text='baz'),
			_Line('file', number=4, text='bop dum'),
			_Line('file', number=5, text='rum sap')
		]
		assert _Attribute.get('foo', lines) == 'bar'
		assert _Attribute.get('baz', lines) == ''
		assert _Attribute.get('bop', lines) == 'dim\ndum'
		assert _Attribute.get('bip', lines) == ''
		bops = list(_Attribute.get_lines(['bop'], lines))
		assert bops[0].number == 2
		assert bops[0].text == 'bop dim'
		assert bops[1].number == 4
		assert bops[1].text == 'bop dum'
		foo_rum = list(_Attribute.get_lines(['foo', 'rum'], lines))
		assert foo_rum[0].number == 1
		assert foo_rum[0].text == 'foo bar'
		assert foo_rum[1].number == 5
		assert foo_rum[1].text == 'rum sap'


class _Repeat:
	@staticmethod
	def expand(lines):
		repeated_lines = []
		inside_repeat = False
		for line in lines:
			directive = _Attribute.get('repeat', [line])
			if directive == 'begin':
				inside_repeat = True
			elif directive == 'end':
				inside_repeat = False
				yield from repeated_lines
				repeated_lines.clear()
			else:
				if inside_repeat:
					repeated_lines.append(line)
				yield line

	@staticmethod
	def _test():
		lines = [
			_Line('file', number=1, text='foo bar'),
			_Line('file', number=2, text='repeat begin'),
			_Line('file', number=3, text=''),
			_Line('file', number=4, text='bop dum'),
			_Line('file', number=5, text=''),
			_Line('file', number=6, text='repeat end'),
			_Line('file', number=7, text='rum sap')
		]
		lines = list(_Repeat.expand(lines))
		for line in lines:
			print(line.text)
		assert lines[0].text == 'foo bar'
		assert lines[1].text == ''
		assert lines[1].number == 3
		assert lines[2].text == 'bop dum'
		assert lines[2].number == 4
		assert lines[3].text == ''
		assert lines[3].number == 5
		assert lines[4].text == ''
		assert lines[4].number == 3
		assert lines[5].text == 'bop dum'
		assert lines[5].number == 4
		assert lines[6].text == ''
		assert lines[6].number == 5
		assert lines[7].text == 'rum sap'
		assert lines[7].number == 7


class _Note:
	note_re = re.compile(r'^'
						 r'(?P<name>[a-gR])' +
						 r'(?P<accidental>[#bn])?'
						 r'(?P<octave_shift>[\+\-])?'
						 r'(/(?P<note_value>[0-9]+))?'
						 r'(?P<dot>\.)?'
						 r'(\((?P<fermata>[0-9]+(\.[0-9]+)?)\))?'
						 r'$')
	rhythm_re = re.compile(r'(?P<beats_per_measure>[0-9])\s*:\s*'
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


	def parse_notes(beat_value, key, voice, line):
		measures = list()
		measures.append(key)
		measures.append([])
		prev_note = None
		for symbol in line.split():
			if symbol == '|':
				measures.append([])
			elif symbol == '=':
				if prev_note:
					prev_note.tie = True
			elif symbol == '-':
				if prev_note:
					prev_note.slur = True
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
					beats = beat_value / float(note_value)
				if match.group('dot'):
					beats = beats * 1.5
				note = note_type(beats)
				fermata = match.group('fermata')
				if fermata:
					note.fermata_beats = float(fermata)
				if prev_note and prev_note.tie and type(prev_note) != type(note):
					raise RuntimeError('Cannot tie two different pitches (' +
									   type(prev_note).__name__ + ' & ' +
									   type(note).__name__ + ')')
				prev_note = note
				measures[-1].append(note)
		return measures


def _run_parser_tests():
	_Import._test()
	_Comment._test()
	_Splitter._test()
	_Attribute._test()
	_Repeat._test()


if __name__ == '__main__':
	_run_parser_tests()
