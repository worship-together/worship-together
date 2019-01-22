"""
Events

REQUIREMENTS
- Model midi events
"""

import array
import struct

default_velocity = 60


class Event(object):
	def __init__(self, tick=0):
		self.tick = tick
		
	def to_bytes(self):
		tick = _get_var_len(int(self.tick))
		return tick
		
		
class NoteEvent(Event):
	def __init__(self, voice, tick, pitch, velocity):
		super(NoteEvent, self).__init__(tick)
		self.voice = voice
		self.pitch = pitch
		self.velocity = velocity
		
	def __repr__(self):
		return '(%7s %4s, %2s, %s' % \
		    	self.voice.name, self.tick, self.pitch, \
				"On" if type(self) == NoteOnEvent else "Off"
		
	def code(self):
		raise NotImplementedError('must override code method')
		
	def to_bytes(self):
		code = self.code()
		channel = self.voice
		sts_msg = struct.pack('B', (code & 0xf0) + (channel & 0x0f))
		pitch = struct.pack('B', self.pitch)
		velocity = struct.pack('B', self.velocity)
		return super(NoteEvent, self).to_bytes() + sts_msg + pitch + velocity
		
		
class NoteOnEvent(NoteEvent):
	def code(self):
		return 0x90
		
		
class NoteOffEvent(NoteEvent):
	def code(self):
		return 0x80
		
		
class RestEvent(Event):
	pass
	
	
class MetaEvent(Event):
	def __init__(self, code, data):
		super(MetaEvent, self).__init__()
		self.code = code
		self.data = data
		
	def to_bytes(self):
		code_bytes = struct.pack('BB', 0xff, self.code)
		data_len = struct.pack('B', len(self.data))
		data_bytes = array.array('B', self.data).tobytes()
		return super(MetaEvent, self).to_bytes() + code_bytes + data_len + data_bytes
		
		
class SmpteOffsetEvent(MetaEvent):
	def __init__(self):
		super(SmpteOffsetEvent, self).__init__(code=0x54, data=[0, 0, 0, 0, 0])
		
		
class TimeSignatureEvent(MetaEvent):
	def __init__(self):
		super(TimeSignatureEvent, self).__init__(code=0x58, data=[4, 2, 24, 8])
		
		
class KeySignatureEvent(MetaEvent):
	def __init__(self):
		super(KeySignatureEvent, self).__init__(code=0x59, data=[0, 0])
		
		
class SetTempoEvent(MetaEvent):
	def __init__(self, beats_per_minute):
		seconds_per_beat = 60 / beats_per_minute
		microseconds_per_beat = int(seconds_per_beat * 1000000)
		data_0 = microseconds_per_beat & 0xFF
		data_1 = (microseconds_per_beat & 0xFF00) >> 8
		data_2 = (microseconds_per_beat & 0xFF0000) >> 16
		super(SetTempoEvent, self).__init__(code=0x51, data=[data_2, data_1, data_0])
		
		
class EndOfTrackEvent(MetaEvent):
	def __init__(self):
		super(EndOfTrackEvent, self).__init__(code=0x2F, data=[])
		self.tick = 34
		
def _get_var_len(value, low_order_byte=True):
	prefix_bit = (0 if low_order_byte else 0x80)
	byte = struct.pack('B', prefix_bit | (value & 0x7f))
	shifted = value >> 7
	if shifted > 0:
		return _get_var_len(shifted, low_order_byte=False) + byte
	else:
		return byte

