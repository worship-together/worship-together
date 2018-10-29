from notes import *


class Key:
	def __init__(self):
		self.notes = {}
		
	def __getitem__(self, item):
		return self.notes[item] if item in self.notes else None
		
		
class C(Key):
	pass
	
	
class C_Sharp(Key):
	def __init__(self):
		super().__init__()
		raise NotImplemented()
		
		
class D_Flat(Key):
	def __init__(self):
		super().__init__()
		raise NotImplemented()
		
		
class G(Key):
	def __init__(self):
		super().__init__()
		self.notes.update({F1:F1s, F2:F2s, F3:F3s, F4:F4s, F5:F5s, F6:F6s, F7:F7s})
		
		
class D(G):
	def __init__(self):
		super().__init__()
		self.notes.update({C1:C1s, C2:C2s, C3:C3s, C4:C4s, C5:C5s, C6:C6s, C7:C7s})
		
		
class D_Sharp(Key):
	def __init__(self):
		super().__init__()
		raise NotImplemented()
		
		
class E_Flat(Key):
	def __init__(self):
		super().__init__()
		raise NotImplemented()
		
		
class E(Key):
	def __init__(self):
		super().__init__()
		raise NotImplemented()
		
		
class E_Sharp(Key):
	def __init__(self):
		super().__init__()
		raise NotImplemented()
		
		
class F_Flat(Key):
	def __init__(self):
		super().__init__()
		raise NotImplemented()
		
		
class F(Key):
	def __init__(self):
		super().__init__()
		self.notes.update({B0:B0b, B1:B1b, B2:B2b, B3:B3b, B4:B4b, B5:B5b, B6:B6b, B7:B7b})
		
		
class F_Sharp(Key):
	def __init__(self):
		super().__init__()
		raise NotImplemented()
		
		
class G_Flat(Key):
	def __init__(self):
		super().__init__()
		raise NotImplemented()
		
		
class G_Sharp(Key):
	def __init__(self):
		super().__init__()
		raise NotImplemented()
		
		
class A_Flat(Key):
	def __init__(self):
		super().__init__()
		raise NotImplemented()
		
		
class A(Key):
	def __init__(self):
		super().__init__()
		raise NotImplemented()
		
		
class A_Sharp(Key):
	def __init__(self):
		super().__init__()
		raise NotImplemented()
		
		
class B_Flat(F):
	def __init__(self):
		super().__init__()
		self.notes.update({E1:E1b, E2:E2b, E3:E3b, E4:E4b, E5:E5b, E6:E6b, E7:E7b})
		
		
class B(Key):
	def __init__(self):
		super().__init__()
		raise NotImplemented()
		
		
class B_Sharp(Key):
	def __init__(self):
		super().__init__()
		raise NotImplemented()
		
		
class C_Flat(Key):
	def __init__(self):
		super().__init__()
		raise NotImplemented()

