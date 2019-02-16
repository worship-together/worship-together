from notes import *


class Key(object):
	def __init__(self):
		self.notes = {}
		
	def __getitem__(self, item):
		return self.notes[item] if item in self.notes else None

	def _not_implemented(self):
		raise NotImplementedError('Key ' + self.__class__.__name__ +
		                          ' not yet implemented')
		
		
class C(Key):
	pass
	
	
class C_Sharp(Key):
	def __init__(self):
		super(C_Sharp, self).__init__()
		self._not_implemented()
		
		
class G(C):
	def __init__(self):
		super(G, self).__init__()
		self.notes.update({F1:F1s, F2:F2s, F3:F3s, F4:F4s, F5:F5s, F6:F6s, F7:F7s})
		
		
class D(G):
	def __init__(self):
		super(D, self).__init__()
		self.notes.update({C1:C1s, C2:C2s, C3:C3s, C4:C4s, C5:C5s, C6:C6s, C7:C7s})
		
		
class D_Sharp(Key):
	def __init__(self):
		super(D_Sharp, self).__init__()
		self._not_implemented()
		
		
class F_Flat(Key):
	def __init__(self):
		super(F_Flat, self).__init__()
		self._not_implemented()
		
		
class F(Key):
	def __init__(self):
		super(F, self).__init__()
		self.notes.update({B1:B1b, B2:B2b, B3:B3b, B4:B4b, B5:B5b, B6:B6b, B7:B7b})
		
		
class F_Sharp(Key):
	def __init__(self):
		super(F_Sharp, self).__init__()
		self._not_implemented()
		
		
class G_Sharp(Key):
	def __init__(self):
		super(G_Sharp, self).__init__()
		self._not_implemented()


class A(D):
	def __init__(self):
		super(A, self).__init__()
		self.notes.update({G1:G1s, G2:G2s, G3:G3s, G4:G4s, G5:G5s, G6:G6s, G7:G7s})
		
		
class A_Sharp(Key):
	def __init__(self):
		super(A_Sharp, self).__init__()
		self._not_implemented()


class E(A):
    def __init__(self):
        super(E, self).__init__()
        self.notes.update({D1: D1s, D2: D2s, D3: D3s, D4: D4s, D5: D5s, D6: D6s, D7: D7s})


class E_Sharp(Key):
    def __init__(self):
        super(E_Sharp, self).__init__()
        self._not_implemented()


class B_Flat(F):
	def __init__(self):
		super(B_Flat, self).__init__()
		self.notes.update({E1: E1b, E2: E2b, E3: E3b, E4: E4b, E5: E5b, E6: E6b, E7: E7b})
		
		
class E_Flat(B_Flat):
	def __init__(self):
		super(E_Flat, self).__init__()
		self.notes.update({A1: A1b, A2: A2b, A3: A3b, A4: A4b, A5: A5b, A6: A6b, A7: A7b})


class A_Flat(E_Flat):
	def __init__(self):
		super(A_Flat, self).__init__()
		self.notes.update({D1: D1b, D2: D2b, D3: D3b, D4: D4b, D5: D5b, D6: D6b, D7: D7b})


class D_Flat(A_Flat):
	def __init__(self):
		super(D_Flat, self).__init__()
		self.notes.update({G1:G1b, G2:G2b, G3:G3b, G4:G4b, G5:G5b})


class G_Flat(D_Flat):
	def __init__(self):
		super(G_Flat, self).__init__()
		self.notes.update({C1:C1b, C2:C2b, C3:C3b, C4:C4b, C5:C5b, C6:C6b, C7:C7b})


class B(Key):
	def __init__(self):
		super(B, self).__init__()
		self._not_implemented()
		
		
class B_Sharp(Key):
	def __init__(self):
		super(B_Sharp, self).__init__()
		self._not_implemented()
		
		
class C_Flat(Key):
	def __init__(self):
		super(C_Flat, self).__init__()
		self._not_implemented()

