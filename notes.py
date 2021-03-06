"""
MIDI Notes

REQUIREMENTS
- Concisely capture sufficient information to convert a song to MIDI
- Capture the information in an intuitive way
- Capture time signature, measures & slurs (through the words)
"""

import inspect

class Note(object):
	def __init__(self, pitch, beats, accidental=None):
		self.pitch = pitch
		self.beats = beats
		self.accidental = accidental
		self.fermata_beats = 0
		self.tie = False
		self.slur = False

	def __repr__(self):
		return type(self).__name__ + '(' + str(self.beats) + ')'

class R(Note):
	def __init__(self, beats=1):
		super(R, self).__init__(0, beats)
class A0(Note):
	def __init__(self, beats=1):
		super(A0, self).__init__(21, beats)
class A0n(Note):
	def __init__(self, beats=1):
		super(A0n, self).__init__(21, beats, accidental='n')
class A0s(Note):
	def __init__(self, beats=1):
		super(A0s, self).__init__(22, beats, accidental='#')
class B0b(Note):
	def __init__(self, beats=1):
		super(B0b, self).__init__(22, beats, accidental='b')
class B0(Note):
	def __init__(self, beats=1):
		super(B0, self).__init__(23, beats)
class B0n(Note):
	def __init__(self, beats=1):
		super(B0n, self).__init__(23, beats, accidental='n')
class B0s(Note):
	def __init__(self, beats=1):
		super(B0s, self).__init__(24, beats, accidental='#')
class C1b(Note):
	def __init__(self, beats=1):
		super(C1b, self).__init__(23, beats, accidental='b')
class C1(Note):
	def __init__(self, beats=1):
		super(C1, self).__init__(24, beats)
class C1n(Note):
	def __init__(self, beats=1):
		super(C1n, self).__init__(24, beats, accidental='n')
class C1s(Note):
	def __init__(self, beats=1):
		super(C1s, self).__init__(25, beats, accidental='#')
class D1b(Note):
	def __init__(self, beats=1):
		super(D1b, self).__init__(25, beats, accidental='b')
class D1(Note):
	def __init__(self, beats=1):
		super(D1, self).__init__(26, beats)
class D1n(Note):
	def __init__(self, beats=1):
		super(D1n, self).__init__(26, beats, accidental='n')
class D1s(Note):
	def __init__(self, beats=1):
		super(D1s, self).__init__(27, beats, accidental='#')
class E1b(Note):
	def __init__(self, beats=1):
		super(E1b, self).__init__(27, beats, accidental='b')
class E1(Note):
	def __init__(self, beats=1):
		super(E1, self).__init__(28, beats)
class E1n(Note):
	def __init__(self, beats=1):
		super(E1n, self).__init__(28, beats, accidental='n')
class E1b(Note):
	def __init__(self, beats=1):
		super(E1b, self).__init__(29, beats, accidental='#')
class F1b(Note):
	def __init__(self, beats=1):
		super(F1b, self).__init__(28, beats, accidental='b')
class F1(Note):
	def __init__(self, beats=1):
		super(F1, self).__init__(29, beats)
class F1n(Note):
	def __init__(self, beats=1):
		super(F1n, self).__init__(29, beats, accidental=True)
class F1s(Note):
	def __init__(self, beats=1):
		super(F1s, self).__init__(30, beats, accidental=True)
class G1b(Note):
	def __init__(self, beats=1):
		super(G1b, self).__init__(30, beats, accidental=True)
class G1(Note):
	def __init__(self, beats=1):
		super(G1, self).__init__(31, beats)
class G1n(Note):
	def __init__(self, beats=1):
		super(G1n, self).__init__(31, beats, accidental=True)
class G1s(Note):
	def __init__(self, beats=1):
		super(G1s, self).__init__(32, beats, accidental=True)
class A1b(Note):
	def __init__(self, beats=1):
		super(A1b, self).__init__(32, beats, accidental=True)
class A1(Note):
	def __init__(self, beats=1):
		super(A1, self).__init__(33, beats)
class A1n(Note):
	def __init__(self, beats=1):
		super(A1n).__init__(34, beats, accidental=True)
class A1s(Note):
	def __init__(self, beats=1):
		super(A1s, self).__init__(34, beats, accidental=True)
class B1b(Note):
	def __init__(self, beats=1):
		super(B1b, self).__init__(34, beats, accidental=True)
class B1(Note):
	def __init__(self, beats=1):
		super(B1, self).__init__(35, beats)
class B1n(Note):
	def __init__(self, beats=1):
		super(B1, self).__init__(35, beats, accidental=True)
class B1s(Note):
	def __init__(self, beats=1):
		super(B1s, self).__init__(36, beats, accidental=True)

class C2b(Note):
	def __init__(self, beats=1):
		super(C2b, self).__init__(35, beats, accidental=True)
class C2(Note):
	def __init__(self, beats=1):
		super(C2, self).__init__(36, beats)
class C2n(Note):
	def __init__(self, beats=1):
		super(C2n, self).__init__(36, beats, accidental=True)
class C2s(Note):
	def __init__(self, beats=1):
		super(C2s, self).__init__(37, beats, accidental=True)
class D2b(Note):
	def __init__(self, beats=1):
		super(D2b, self).__init__(37, beats, accidental=True)
class D2(Note):
	def __init__(self, beats=1):
		super(D2, self).__init__(38, beats)
class D2n(Note):
	def __init__(self, beats=1):
		super(D2n, self).__init__(38, beats, accidental=True)
class D2s(Note):
	def __init__(self, beats=1):
		super(D2s, self).__init__(39, beats, accidental=True)
class E2b(Note):
	def __init__(self, beats=1):
		super(E2b, self).__init__(39, beats, accidental=True)
class E2(Note):
	def __init__(self, beats=1):
		super(E2, self).__init__(40, beats)
class E2n(Note):
	def __init__(self, beats=1):
		super(E2n, self).__init__(40, beats, accidental=True)
class E2s(Note):
	def __init__(self, beats=1):
		super(E2s, self).__init__(41, beats, accidental=True)
class F2b(Note):
	def __init__(self, beats=1):
		super(F2b, self).__init__(40, beats, accidental=True)
class F2(Note):
	def __init__(self, beats=1):
		super(F2, self).__init__(41, beats)
class F2n(Note):
	def __init__(self, beats=1):
		super(F2n, self).__init__(41, beats, accidental=True)
class F2s(Note):
	def __init__(self, beats=1):
		super(F2s, self).__init__(42, beats, accidental=True)
class G2b(Note):
	def __init__(self, beats=1):
		super(G2b, self).__init__(42, beats, accidental=True)
class G2(Note):
	def __init__(self, beats=1):
		super(G2, self).__init__(43, beats)
class G2n(Note):
	def __init__(self, beats=1):
		super(G2n, self).__init__(43, beats, accidental=True)
class G2s(Note):
	def __init__(self, beats=1):
		super(G2s, self).__init__(44, beats, accidental=True)
class A2b(Note):
	def __init__(self, beats=1):
		super(A2b, self).__init__(44, beats, accidental=True)
class A2(Note):
	def __init__(self, beats=1):
		super(A2, self).__init__(45, beats)
class A2n(Note):
	def __init__(self, beats=1):
		super(A2n, self).__init__(45, beats, accidental=True)
class A2s(Note):
	def __init__(self, beats=1):
		super(A2s, self).__init__(46, beats, accidental=True)
class B2b(Note):
	def __init__(self, beats=1):
		super(B2b, self).__init__(46, beats, accidental=True)
class B2(Note):
	def __init__(self, beats=1):
		super(B2, self).__init__(47, beats)
class B2n(Note):
	def __init__(self, beats=1):
		super(B2n, self).__init__(47, beats, accidental=True)
class B2s(Note):
	def __init__(self, beats=1):
		super(B2s, self).__init__(48, beats, accidental=True)

class C3b(Note):
	def __init__(self, beats=1):
		super(C3b, self).__init__(47, beats, accidental=True)
class C3(Note):
	def __init__(self, beats=1):
		super(C3, self).__init__(48, beats)
class C3n(Note):
	def __init__(self, beats=1):
		super(C3n, self).__init__(48, beats, accidental=True)
class C3s(Note):
	def __init__(self, beats=1):
		super(C3s, self).__init__(49, beats, accidental=True)
class D3b(Note):
	def __init__(self, beats=1):
		super(D3b, self).__init__(49, beats, accidental=True)
class D3(Note):
	def __init__(self, beats=1):
		super(D3, self).__init__(50, beats)
class D3n(Note):
	def __init__(self, beats=1):
		super(D3n, self).__init__(50, beats, accidental=True)
class D3s(Note):
	def __init__(self, beats=1):
		super(D3s, self).__init__(51, beats, accidental=True)
class E3b(Note):
	def __init__(self, beats=1):
		super(E3b, self).__init__(51, beats, accidental=True)
class E3(Note):
	def __init__(self, beats=1):
		super(E3, self).__init__(52, beats)
class E3n(Note):
	def __init__(self, beats=1):
		super(E3n, self).__init__(52, beats, accidental=True)
class E3s(Note):
	def __init__(self, beats=1):
		super(E3s, self).__init__(53, beats, accidental=True)
class F3b(Note):
	def __init__(self, beats=1):
		super(F3b, self).__init__(52, beats, accidental=True)
class F3(Note):
	def __init__(self, beats=1):
		super(F3, self).__init__(53, beats)
class F3n(Note):
	def __init__(self, beats=1):
		super(F3n, self).__init__(53, beats, accidental=True)
class F3s(Note):
	def __init__(self, beats=1):
		super(F3s, self).__init__(54, beats, accidental=True)
class G3b(Note):
	def __init__(self, beats=1):
		super(G3b, self).__init__(54, beats, accidental=True)
class G3(Note):
	def __init__(self, beats=1):
		super(G3, self).__init__(55, beats)
class G3n(Note):
	def __init__(self, beats=1):
		super(G3n, self).__init__(56, beats, accidental=True)
class G3s(Note):
	def __init__(self, beats=1):
		super(G3s, self).__init__(56, beats, accidental=True)
class A3b(Note):
	def __init__(self, beats=1):
		super(A3b, self).__init__(56, beats, accidental=True)
class A3(Note):
	def __init__(self, beats=1):
		super(A3, self).__init__(57, beats)
class A3n(Note):
	def __init__(self, beats=1):
		super(A3n, self).__init__(57, beats, accidental=True)
class A3s(Note):
	def __init__(self, beats=1):
		super(A3s, self).__init__(58, beats, accidental=True)
class B3b(Note):
	def __init__(self, beats=1):
		super(B3b, self).__init__(58, beats, accidental=True)
class B3(Note):
	def __init__(self, beats=1):
		super(B3, self).__init__(59, beats)
class B3n(Note):
	def __init__(self, beats=1):
		super(B3n, self).__init__(59, beats, accidental=True)
class B3s(Note):
	def __init__(self, beats=1):
		super(B3s, self).__init__(60, beats, accidental=True)

class C4b(Note):
	def __init__(self, beats=1):
		super(C4b, self).__init__(59, beats, accidental=True)
class C4(Note):
	def __init__(self, beats=1):
		super(C4, self).__init__(60, beats)
class C4n(Note):
	def __init__(self, beats=1):
		super(C4n, self).__init__(60, beats, accidental=True)
class C4s(Note):
	def __init__(self, beats=1):
		super(C4s, self).__init__(61, beats, accidental=True)
class D4b(Note):
	def __init__(self, beats=1):
		super(D4b, self).__init__(61, beats, accidental=True)
class D4(Note):
	def __init__(self, beats=1):
		super(D4, self).__init__(62, beats)
class D4n(Note):
	def __init__(self, beats=1):
		super(D4n, self).__init__(62, beats, accidental=True)
class D4s(Note):
	def __init__(self, beats=1):
		super(D4s, self).__init__(63, beats, accidental=True)
class E4b(Note):
	def __init__(self, beats=1):
		super(E4b, self).__init__(63, beats, accidental=True)
class E4(Note):
	def __init__(self, beats=1):
		super(E4, self).__init__(64, beats)
class E4n(Note):
	def __init__(self, beats=1):
		super(E4n, self).__init__(64, beats, accidental=True)
class E4s(Note):
	def __init__(self, beats=1):
		super(E4s, self).__init__(65, beats, accidental=True)
class F4b(Note):
	def __init__(self, beats=1):
		super(F4b, self).__init__(64, beats, accidental=True)
class F4(Note):
	def __init__(self, beats=1):
		super(F4, self).__init__(65, beats)
class F4n(Note):
	def __init__(self, beats=1):
		super(F4n ,self).__init__(65, beats, accidental=True)
class F4s(Note):
	def __init__(self, beats=1):
		super(F4s, self).__init__(66, beats, accidental=True)
class G4b(Note):
	def __init__(self, beats=1):
		super(G4b, self).__init__(66, beats, accidental=True)
class G4(Note):
	def __init__(self, beats=1):
		super(G4, self).__init__(67, beats)
class G4n(Note):
	def __init__(self, beats=1):
		super(G4n, self).__init__(67, beats, accidental=True)
class G4s(Note):
	def __init__(self, beats=1):
		super(G4s, self).__init__(68, beats, accidental=True)
class A4b(Note):
	def __init__(self, beats=1):
		super(A4b, self).__init__(68, beats, accidental=True)
class A4(Note):
	def __init__(self, beats=1):
		super(A4, self).__init__(69, beats)
class A4n(Note):
	def __init__(self, beats=1):
		super(A4n, self).__init__(69, beats, accidental=True)
class A4s(Note):
	def __init__(self, beats=1):
		super(A4s, self).__init__(70, beats, accidental=True)
class B4b(Note):
	def __init__(self, beats=1):
		super(B4b, self).__init__(70, beats, accidental=True)
class B4(Note):
	def __init__(self, beats=1):
		super(B4, self).__init__(71, beats)
class B4n(Note):
	def __init__(self, beats=1):
		super(B4n, self).__init__(71, beats, accidental=True)
class B4s(Note):
	def __init__(self, beats=1):
		super(B4s, self).__init__(72, beats, accidental=True)

class C5b(Note):
	def __init__(self, beats=1):
		super(C5b, self).__init__(71, beats, accidental=True)
class C5(Note):
	def __init__(self, beats=1):
		super(C5, self).__init__(72, beats)
class C5n(Note):
	def __init__(self, beats=1):
		super(C5n, self).__init__(72, beats, accidental=True)
class C5s(Note):
	def __init__(self, beats=1):
		super(C5s, self).__init__(73, beats, accidental=True)
class D5b(Note):
	def __init__(self, beats=1):
		super(D5b, self).__init__(73, beats, accidental=True)
class D5(Note):
	def __init__(self, beats=1):
		super(D5, self).__init__(74, beats)
class D5n(Note):
	def __init__(self, beats=1):
		super(D5n, self).__init__(74, beats, accidental=True)
class D5s(Note):
	def __init__(self, beats=1):
		super(D5s, self).__init__(75, beats, accidental=True)
class E5b(Note):
	def __init__(self, beats=1):
		super(E5b, self).__init__(75, beats, accidental=True)
class E5(Note):
	def __init__(self, beats=1):
		super(E5, self).__init__(76, beats)
class E5n(Note):
	def __init__(self, beats=1):
		super(E5n, self).__init__(76, beats, accidental=True)
class E5s(Note):
	def __init__(self, beats=1):
		super(E5s, self).__init__(77, beats, accidental=True)
class F5b(Note):
	def __init__(self, beats=1):
		super(F5b, self).__init__(76, beats, accidental=True)
class F5(Note):
	def __init__(self, beats=1):
		super(F5, self).__init__(77, beats)
class F5n(Note):
	def __init__(self, beats=1):
		super(F5n, self).__init__(77, beats, accidental=True)
class F5s(Note):
	def __init__(self, beats=1):
		super(F5s, self).__init__(78, beats, accidental=True)
class G5b(Note):
	def __init__(self, beats=1):
		super(G5b, self).__init__(78, beats, accidental=True)
class G5(Note):
	def __init__(self, beats=1):
		super(G5, self).__init__(79, beats)
class G5n(Note):
	def __init__(self, beats=1):
		super(G5n, self).__init__(79, beats, accidental='n')
class G5s(Note):
	def __init__(self, beats=1):
		super(G5s, self).__init__(80, beats, accidental='#')
class A5b(Note):
	def __init__(self, beats=1):
		super(A5b, self).__init__(80, beats, accidental='b')
class A5(Note):
	def __init__(self, beats=1):
		super(A5, self).__init__(81, beats)
class B5b(Note):
	def __init__(self, beats=1):
		super(B5b, self).__init__(82, beats, accidental='b')
class B5(Note):
	def __init__(self, beats=1):
		super(B5, self).__init__(83, beats)

class C6b(Note):
	def __init__(self, beats=1):
		super(C6b, self).__init__(83, beats, accidental='b')
class C6(Note):
	def __init__(self, beats=1):
		super(C6, self).__init__(84, beats)
class C6n(Note):
	def __init__(self, beats=1):
		super(C6n, self).__init__(84, beats, accidental='n')
class C6s(Note):
	def __init__(self, beats=1):
		super(C6s, self).__init__(85, beats, accidental='#')
class D6b(Note):
	def __init__(self, beats=1):
		super(D6b, self).__init__(85, beats, accidental='b')
class D6(Note):
	def __init__(self, beats=1):
		super(D6, self).__init__(86, beats)
class D6n(Note):
	def __init__(self, beats=1):
		super(D6n, self).__init__(86, beats, accidental='n')
class D6s(Note):
	def __init__(self, beats=1):
		super(D6s, self).__init__(87, beats, accidental='#')
class E6b(Note):
	def __init__(self, beats=1):
		super(E6b, self).__init__(87, beats, accidental='b')
class E6(Note):
	def __init__(self, beats=1):
		super(E6, self).__init__(88, beats)
class E6s(Note):
	def __init__(self, beats=1):
		super(E6s, self).__init__(89, beats, accidental='#')
class F6b(Note):
	def __init__(self, beats=1):
		super(F6b, self).__init__(88, beats, accidental='b')
class F6(Note):
	def __init__(self, beats=1):
		super(F6, self).__init__(89, beats)
class F6s(Note):
	def __init__(self, beats=1):
		super(F6s, self).__init__(90, beats, accidental='#')
class G6(Note):
	def __init__(self, beats=1):
		super(G6, self).__init__(91, beats)
class G6s(Note):
	def __init__(self, beats=1):
		super(G6s, self).__init__(92, beats, accidental='#')
class A6b(Note):
	def __init__(self, beats=1):
		super(A6b, self).__init__(92, beats, accidental='b')
class A6(Note):
	def __init__(self, beats=1):
		super(A6, self).__init__(93, beats)
class B6b(Note):
	def __init__(self, beats=1):
		super(B6b, self).__init__(94, beats, accidental='b')
class B6(Note):
	def __init__(self, beats=1):
		super(B6, self).__init__(95, beats)

class C7b(Note):
	def __init__(self, beats=1):
		super(C7b, self).__init__(96, beats, accidental='b')
class C7(Note):
	def __init__(self, beats=1):
		super(C7, self).__init__(96, beats)
class C7n(Note):
	def __init__(self, beats=1):
		super(C7n, self).__init__(96, beats, accidental='n')
class C7s(Note):
	def __init__(self, beats=1):
		super(C7s, self).__init__(96, beats, accidental='#')
class D7b(Note):
	def __init__(self, beats=1):
		super(D7b, self).__init__(97, beats, accidental='b')
class D7(Note):
	def __init__(self, beats=1):
		super(D7, self).__init__(98, beats)
class D7s(Note):
	def __init__(self, beats=1, accidental='#'):
		super(D7s, self).__init__(99, beats)
class E7b(Note):
	def __init__(self, beats=1):
		super(E7b, self).__init__(99, beats, accidental='b')
class E7(Note):
	def __init__(self, beats=1):
		super(E7, self).__init__(100, beats)
class F7(Note):
	def __init__(self, beats=1):
		super(F7, self).__init__(101, beats)
class F7s(Note):
	def __init__(self, beats=1):
		super(F7s, self).__init__(102, beats, accidental='#')
class G7(Note):
	def __init__(self, beats=1):
		super(G7, self).__init__(103, beats)
class G7s(Note):
	def __init__(self, beats=1):
		super(G7s, self).__init__(104, beats, accidental='#')
class A7b(Note):
	def __init__(self, beats=1):
		super(A7b, self).__init__(104, beats, accidental='b')
class A7(Note):
	def __init__(self, beats=1):
		super(A7, self).__init__(105, beats)
class B7b(Note):
	def __init__(self, beats=1):
		super(B7b, self).__init__(106, beats)
class B7(Note):
	def __init__(self, beats=1):
		super(B7, self).__init__(107, beats)

class C8(Note):
	def __init__(self, beats=1):
		super(C8, self).__init__(108, beats)


def fermata(note, additional_beats=1):
	if inspect.isclass(note):
		note = note()
	note.fermata_beats = additional_beats
	return note

# **************************************
#
#  jithon representation
#
#
# # Pitch
#
# REST = -1
# C_1  = 0
# CS_1 = 1
# DF_1 = 1
# D_1  = 2
# DS_1 = 3
# EF_1 = 3
# E_1  = 4
# ES_1 = 5
# FF_1 = 4
# F_1  = 5
# FS_1 = 6
# GF_1 = 6
# G_1  = 7
# GS_1 = 8
# AF_1 = 8
# A_1  = 9
# AS_1 = 10
# BF_1 = 10
# B_1  = 11
# BS_1 = 12
# CF0  = 11
# C0   = 12
# CS0  = 13
# DF0  = 13
# D0   = 14
# DS0  = 15
# EF0  = 15
# E0   = 16
# ES0  = 17
# FF0  = 16
# F0   = 17
# FS0  = 18
# GF0  = 18
# G0   = 19
# GS0  = 20
# AF0  = 20
# A0   = 21
# AS0  = 22
# BF0  = 22
# B0   = 23
# BS0  = 24
# CF1  = 23
# C1   = 24
# CS1  = 25
# DF1  = 25
# D1   = 26
# DS1  = 27
# EF1  = 27
# E1   = 28
# ES1  = 29
# FF1  = 28
# F1   = 29
# FS1  = 30
# GF1  = 30
# G1   = 31
# GS1  = 32
# AF1  = 32
# A1   = 33
# AS1  = 34
# BF1  = 34
# B1   = 35
# BS1  = 36
# CF2  = 35
# C2   = 36
# CS2  = 37
# DF2  = 37
# D2   = 38
# DS2  = 39
# EF2  = 39
# E2   = 40
# ES2  = 41
# FF2  = 40
# F2   = 41
# FS2  = 42
# GF2  = 42
# G2   = 43
# GS2  = 44
# AF2  = 44
# A2   = 45
# AS2  = 46
# BF2  = 46
# B2   = 47
# BS2  = 48
# CF3  = 47
# C3   = 48
# CS3  = 49
# DF3  = 49
# D3   = 50
# DS3  = 51
# EF3  = 51
# E3   = 52
# ES3  = 53
# FF3  = 52
# F3   = 53
# FS3  = 54
# GF3  = 54
# G3   = 55
# GS3  = 56
# AF3  = 56
# A3   = 57
# AS3  = 58
# BF3  = 58
# B3   = 59
# BS3  = 60
# CF4  = 59
# C4   = 60
# CS4  = 61
# DF4  = 61
# D4   = 62
# DS4  = 63
# EF4  = 63
# E4   = 64
# EN4  = 64
# ES4  = 65
# FF4  = 64
# F4   = 65
# FS4  = 66
# GF4  = 66
# G4   = 67
# GS4  = 68
# AF4  = 68
# A4   = 69
# AS4  = 70
# BF4  = 70
# B4   = 71
# BS4  = 72
# CF5  = 71
# C5   = 72
# CS5  = 73
# DF5  = 73
# D5   = 74
# DS5  = 75
# EF5  = 75
# E5   = 76
# ES5  = 77
# FF5  = 76
# F5   = 77
# FS5  = 78
# GF5  = 78
# G5   = 79
# GS5  = 80
# AF5  = 80
# A5   = 81
# AS5  = 82
# BF5  = 82
# B5   = 83
# BS5  = 84
# CF6  = 83
# C6   = 84
# CS6  = 85
# DF6  = 85
# D6   = 86
# DS6  = 87
# EF6  = 87
# E6   = 88
# ES6  = 89
# FF6  = 88
# F6   = 89
# FS6  = 90
# GF6  = 90
# G6   = 91
# GS6  = 92
# AF6  = 92
# A6   = 93
# AS6  = 94
# BF6  = 94
# B6   = 95
# BS6  = 96
# CF7  = 95
# C7   = 96
# CS7  = 97
# DF7  = 97
# D7   = 98
# DS7  = 99
# EF7  = 99
# E7   = 100
# ES7  = 101
# FF7  = 100
# F7   = 101
# FS7  = 102
# GF7  = 102
# G7   = 103
# GS7  = 104
# AF7  = 104
# A7   = 105
# AS7  = 106
# BF7  = 106
# B7   = 107
# BS7  = 108
# CF8  = 107
# C8   = 108
# CS8  = 109
# DF8  = 109
# D8   = 110
# DS8  = 111
# EF8  = 111
# E8   = 112
# ES8  = 113
# FF8  = 112
# F8   = 113
# FS8  = 114
# GF8  = 114
# G8   = 115
# GS8  = 116
# AF8  = 116
# A8   = 117
# AS8  = 118
# BF8  = 118
# B8   = 119
# BS8  = 120
# CF9  = 119
# C9   = 120
# CS9  = 121
# DF9  = 121
# D9   = 122
# DS9  = 123
# EF9  = 123
# E9   = 124
# ES9  = 125
# FF9  = 124
# F9   = 125
# FS9  = 126
# GF9  = 126
# G9   = 127
#
# # Duration
#
# WN = 4.0
# DHN = 3.0
# HN = 2.0
# DQN = 1.5
# QN = 1.0
# DEN = 0.75
# EN = 0.5
# DSN = 0.375
# SN = 0.25

