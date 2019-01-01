"""
MIDI Gen

REQUIREMENTS
- Convert notes into MIDI events
- Utilize ticks & velocities similar to Finale output
  - Attack and linger on the downbeat of each measure, as well as the
    secondary beat
- Verify count of beats per measure for each voice (seperate step?)

DESIGN
- Create a voice stream which stitches together all meausures for that voice
  - Always shows what the next event will be
- Mesh & sort the resulting events
- Determine which voice contains the next note event
  - And which type of event it is (on vs off)
"""

import enum
import itertools
import struct
import os
import importlib

import notes
import events
import song_parser

ticks_per_beat = 1024
ticks_between_beats = 0 # 34


class Voice(enum.IntEnum):
	Soprano = 0
	Alto = 1
	Tenor = 2
	Bass = 3
	Count = 4


class VoiceStream:
	"""Stream of events for one voice for whole song"""

	def __init__(self, song, voice, velocity):
		self.song = song
		self.voice = voice
		self.velocity = velocity[self.voice]

	def map_note_using_key(self, note):
		note_type = note if type(note) is type else type(note)
		new_note_type = self.song.key[note_type]
		if new_note_type:
			note_type = new_note_type
		if type(note) is type:
			return note_type()
		elif type(note) == note_type:
			return note
		else:
			new_note = note_type(note.beats)
			new_note.fermata_beats = note.fermata_beats
			return new_note

	def __iter__(self):
		if self.velocity > 0:
			if type(self.song.key) is type:
				self.song.key = self.song.key()
			tick = 0
			for measure_num, measure in enumerate(self.song.measures):
				total_measure_beats = 0
				for note in measure[self.voice]:
					if type(note) is type:
						note_name = note.__name__
					else:
						note_name = type(note).__name__
					note = self.map_note_using_key(note)
					total_measure_beats += note.beats
					note_ticks = (note.beats + note.fermata_beats) * \
                                 ticks_per_beat
					if type(note) != notes.R:
						on = tick
						off = tick + note_ticks - ticks_between_beats
						yield events.NoteOnEvent(self.voice, on, note.pitch,
						                         self.velocity)
						yield events.NoteOffEvent(self.voice, off, note.pitch,
						                          self.velocity)
					tick += note_ticks
				if total_measure_beats > 0:
					self.verify_beats_per_measure(measure_num, total_measure_beats)

	def verify_beats_per_measure(self, measure_num, total_measure_beats):
		# TBD: should not count note beats, but note values
		#      note values must always sum to 1.0
		if self.song.beats_per_measure > 0:
			beat_value = 1.0
			if hasattr(self.song, 'beat_value'):
				beat_value = 4.0 / self.song.beat_value
			expected_total_time = (self.song.beats_per_measure *
			                       beat_value)
			if total_measure_beats != expected_total_time:
				first_measure = measure_num == 0
				last_measure = measure_num == len(self.song.measures) - 1
				if not first_measure and not last_measure:
					raise RuntimeError(f'{total_measure_beats} beats for '
					                   f'{self.voice.name} in measure '
					                   f'{measure_num + 1}, expected '
					                   f'{expected_total_time} '
					                   f'({self.song.number} {self.song.name})')


def make_tick_relative(events):
	prev_tick = 0
	for event in events:
		yield type(event)(event.voice, event.tick - prev_tick, event.pitch,
		                  event.velocity)
		prev_tick = event.tick


def generate_note_events(song, velocities):
	events = itertools.chain(
		VoiceStream(song, Voice.Soprano, velocities),
		VoiceStream(song, Voice.Alto, velocities),
		VoiceStream(song, Voice.Tenor, velocities),
		VoiceStream(song, Voice.Bass, velocities))
	sorted_events = sorted(events, key=lambda event: (event.tick, event.voice))
	return make_tick_relative(sorted_events)


def midi_header(track_count):
	file_magic_number = b'MThd'
	header_size = struct.pack('>I', 6)
	_format = struct.pack('>H', 0)
	track_count = struct.pack('>H', track_count)
	resolution = struct.pack('>H', ticks_per_beat)
	return file_magic_number + header_size + _format + track_count + resolution


def get_meta_events(tempo):
	yield events.SmpteOffsetEvent()
	yield events.TimeSignatureEvent()
	yield events.KeySignatureEvent()
	yield events.SetTempoEvent(tempo)


def midi_track(tempo, note_events):
	track_magic_number = b'MTrk'
	event_bytes = b''
	for event in get_meta_events(tempo):
		event_bytes += event.to_bytes()
	for event in note_events:
		event_bytes += event.to_bytes()
	event_bytes += events.EndOfTrackEvent().to_bytes()
	track_len = struct.pack('>I', len(event_bytes))
	return track_magic_number + track_len + event_bytes


def midi_from_module(module, velocities, tempo_multiplier):
	events = list(generate_note_events(module, velocities))
	return midi_header(track_count=1) + midi_track(module.tempo * tempo_multiplier, events)


def import_song(filename):
	return importlib.import_module('songs.' + os.path.splitext(filename)[0])


def is_song(filename):
	non_songs = ['__init__.py', 'test.py', '__pycache__']
	return filename not in non_songs


class Song:
	def __init__(self, filename):
		song_path = os.path.join('songs', filename)
		self.module = song_parser.parse_song(song_path)

	@property
	def name(self):
		return self.module.name

	@property
	def number(self):
		return self.module.number

	@property
	def psalm(self):
		return self.module.psalm if hasattr(self.module, 'psalm') else None

	def __repr__(self):
		return self.number + ': ' + self.name

	def write_midi(self, filename, volumes=[60, 60, 60, 60], tempo_multiplier=1.0):
		with open(filename, 'wb') as file:
			file.write(midi_from_module(self.module, volumes, tempo_multiplier))

	@property
	def measures(self):
		return self.module.measures


songs = [Song(filename)
         for filename in os.listdir('./songs')
         if is_song(filename)]

