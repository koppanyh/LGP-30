#!/usr/bin/env python3

# LGPAsm v4 by koppanyh, @copy 2025



# Things that can be turned into a number and take up memory
class Numerable:
	def toNum(self):
		raise Exception(f"Not implemented: {self}")
	def toLgpHex(self):
		h = hex(self.toNum() & ((1 << 32) - 1))[2:]
		cs = "0123456789fgjkqw"
		return ''.join([cs[int(x, 16)] for x in h])
	def size(self):
		return 1

class NumLit(Numerable):
	def __init__(self, num):
		super().__init__()
		self.num = num
	def toNum(self):
		return self.num

class CharLit(Numerable):
	def __init__(self, c):
		super().__init__()
		self.c = c.lower()
	def toNum(self):
		# Stolen from https://github.com/WizardOfHaas/LGP-30/blob/ae28b67a4864ae9008e06dda6b2616f9fb38633d/js-lgp-30/flexo.js#L31
		charMap = {
			# Numerical
			"0": 0b000010,
			"l": 0b000110,
			"1": 0b000110, #Patch for 1 == l
			"2": 0b001010,
			"3": 0b001110,
			"4": 0b010010,
			"5": 0b010110,
			"6": 0b011010,
			"7": 0b011110,
			"8": 0b100010,
			"9": 0b100110,
			"f": 0b101010,
			"g": 0b101110,
			"j": 0b110010,
			"k": 0b110110,
			"q": 0b111010,
			"w": 0b111110,
			# Commands
			"z": 0b000001,
			"b": 0b000101,
			"y": 0b001001,
			"r": 0b001101,
			"i": 0b010001,
			"d": 0b010101,
			"n": 0b011001,
			"m": 0b011101,
			"p": 0b100001,
			"e": 0b100101,
			"u": 0b101001,
			"t": 0b101101,
			"h": 0b110001,
			"c": 0b110101,
			"a": 0b111001,
			"s": 0b111101,
			# Controls
			"'": 0b100000,
			" ": 0b000011,
			# The rest
			";": 0b001111,
			"/": 0b010011,
			".": 0b010111,
			"v": 0b011111,
			"o": 0b100011,
			"x": 0b100111
		}
		if self.c not in charMap:
			raise Exception(f"Character '{self.c}' not a valid LGP char")
		return charMap[self.c]



# Base address class
class Addr(Numerable):
	def __init__(self, track, sector):
		super().__init__()
		self.track = track
		self.sector = sector
	def toNum(self):
		return (self.track << 8) + (self.sector << 2)
	@staticmethod
	def toAddr(val):
		if isinstance(val, tuple):
			if isinstance(val[0], str):
				return LabAddr(*val)
			else:
				return AbsAddr(*val)
		elif isinstance(val, str):
			return LabAddr(val)
		else:
			return val
	def __repr__(self):
		return f"{self.__class__.__name__}({self.track}, {self.sector})"

class AbsAddr(Addr):
	def __init__(self, track, sector):
		super().__init__(track, sector)
		if track < 0 or track > 63 or sector < 0 or sector > 63:
			raise Exception(f"Track/sector must be between 0 and 63: {self}")
	def __add__(self, other):
		sector = self.sector + other.sector
		carry = sector // 64
		sector %= 64
		track = self.track + other.track + carry
		return AbsAddr(track, sector)
	def __str__(self):
		return f"{self.track:02}{self.sector:02}"

class LabAddr(Addr):
	def __init__(self, name, offX=0, offY=0):
		# Use the track and sector to save the offsets
		super().__init__(offX, offY)
		self.name = name
	def toNum(self):
		raise Exception(f"LabAddr cannot be turned into number: {self}")
	def toAbsAddr(self, labels):
		addr = labels[self.name]
		return addr + Addr(self.track, self.sector)
	def __repr__(self):
		if self.track == 0 and self.sector == 0:
			return f"LabAddr({repr(self.name)})"
		return f"LabAddr({repr(self.name)}, {self.track}, {self.sector})"



# Things that can hold parameters
class Paramable:
	def __init__(self, *args):
		self.params = args
	def addr(self):
		return self.params[0]
	def size(self):
		return len(self.params)
	def resolveLabels(self, ctx):
		newParams = []
		for param in self.params:
			if isinstance(param, Paramable):
				newParams.append(param.resolveLabels(ctx))
			elif isinstance(param, LabAddr):
				newParams.append(param.toAbsAddr(ctx.labels))
			else:
				newParams.append(param)
		return self.__class__(*newParams)
	def apply(self, ctx):
		raise Exception(f"Not implemented: {self}")
	def compile(self, ctx):
		raise Exception(f"Not implemented: {self}")
	def __repr__(self):
		return f"{self.__class__.__name__}({', '.join(map(repr, self.params))})"



# Actual CPU instructions (or data that take up space in memory)
class Instr(Paramable, Numerable):
	def __init__(self, *args):
		super().__init__(*map(Addr.toAddr, args))
	def toNum(self):
		# LGP instruction format:
		# 00-11: 0
		# 12-15: order
		# 16-17: 0
		# 18-23: track
		# 24-29: sector
		#    30: 0
		#    31: N/A
		orders = {
			"z": 0b0000, "b": 0b0001, "y": 0b0010, "r": 0b0011,
			"i": 0b0100, "d": 0b0101, "n": 0b0110, "m": 0b0111,
			"p": 0b1000, "e": 0b1001, "u": 0b1010, "t": 0b1011,
			"h": 0b1100, "c": 0b1101, "a": 0b1110, "s": 0b1111}
		bits = orders[self.__class__.Order.lower()]
		a = self.addr()
		return (bits << 16) + (a.track << 8) + (a.sector << 2)
	def apply(self, ctx):
		pass
	def compile(self, ctx):
		ctx.append(f"{self.__class__.Order}{self.addr()}'")

class LDA(Instr):  # Load from addr
	Order = "b"
	def __init__(self, addr):
		super().__init__(addr)

class STA(Instr):  # Store to addr
	Order = "h"
	def __init__(self, addr):
		super().__init__(addr)

class STC(Instr):  # Store to addr and clear acc
	Order = "c"
	def __init__(self, addr):
		super().__init__(addr)

class REP(Instr):  # Replace addr bits with those from acc
	Order = "y"
	def __init__(self, addr):
		super().__init__(addr)

class JMP(Instr):  # Unconditional jump
	Order = "u"
	def __init__(self, addr):
		super().__init__(addr)

class RTA(Instr):  # Write return address to address
	Order = "r"
	def __init__(self, addr):
		super().__init__(addr)

class BLZ(Instr):  # Branch if acc is less than 0
	Order = "t"
	def __init__(self, addr):
		super().__init__(addr)

class HLT(Instr):  # Halt
	Order = "z"
	def __init__(self, addr=AbsAddr(0, 0)):
		super().__init__(addr)
	def __repr__(self):
		a = self.addr()
		if type(a) in [Addr, AbsAddr] and a.track == 0 and a.sector == 0:
			return "HLT()"
		return f"HLT({repr(a)})"

class PRT(Instr):  # Print
	Order = "p"
	def __init__(self, addr):
		super().__init__(addr)

class INP(Instr):  # Input
	Order = "i"
	def __init__(self, addr):
		super().__init__(addr)

class ADD(Instr):  # Add
	Order = "a"
	def __init__(self, addr):
		super().__init__(addr)

class SUB(Instr):  # Subtract
	Order = "s"
	def __init__(self, addr):
		super().__init__(addr)

class MUP(Instr):  # Multiply upper
	Order = "m"
	def __init__(self, addr):
		super().__init__(addr)

class MLO(Instr):  # Multiply lower
	Order = "n"
	def __init__(self, addr):
		super().__init__(addr)

class DIV(Instr):  # Divide
	Order = "d"
	def __init__(self, addr):
		super().__init__(addr)

class AND(Instr):  # And
	Order = "e"
	def __init__(self, addr):
		super().__init__(addr)

class RAW(Instr):
	def __init__(self, *args):
		# Bypass the address resolution in Instr
		Paramable.__init__(self, *args)
	def resolveLabels(self, ctx):
		return self
	def compile(self, ctx):
		ctx.extend([f"{r}'" for r in self.params])
	def __repr__(self):
		return f"RAW({', '.join(map(repr, self.params))})"

class HEX(Instr):
	def __init__(self, num):
		super().__init__(num)
	def compile(self, ctx):
		v = self.addr()
		if isinstance(v, Numerable):
			v = v.toLgpHex()
		elif isinstance(v, int):
			v = NumLit(v).toLgpHex()
		else:
			raise Exception(f"Unknown number type: {v}")
		ctx.append(v + "'")



# Commands for the tape loader
class Cmd(Paramable):
	def __init__(self, addr):
		super().__init__(Addr.toAddr(addr))

class ORIG(Cmd):
	def __init__(self, addr):
		super().__init__(addr)
	def apply(self, ctx):
		ctx.addr = self.addr()
	def compile(self, ctx):
		ctx.append(f";000{self.addr()}'")

class EXEC(Cmd):
	def __init__(self, addr):
		super().__init__(addr)
	def apply(self, ctx):
		pass
	def compile(self, ctx):
		ctx.append(f".000{self.addr()}'")



# Assembler stuff

class LabelPrefix:
	counter = -1
	@staticmethod
	def get(macroDef, prefix):
		LabelPrefix.counter += 1
		return f"{prefix}{macroDef.__name__}_{LabelPrefix.counter:04}/"

def MACRO(macroDef, params, prefix=""):
	return macroDef(params, LabelPrefix.get(macroDef, prefix))

def DATA(*args):
	out = [f",00000{len(args):02}'"]
	out.extend([HEX(Addr.toAddr(d)) for d in args])
	return out

class LABEL:
	def __init__(self, name):
		self.name = name
	def __repr__(self):
		return f"LABEL({repr(self.name)})"

class AsmCtx:
	def __init__(self, ops):
		self.output = ops
		self.labels = {}
		self.addr = AbsAddr(0, 0)
	def append(self, val):
		self.output.append(val)
	def extend(self, val):
		self.output.extend(val)
	def flush(self):
		outp = self.output
		self.output = []
		return outp

class Assembler:
	def __init__(self, *args):
		self.ops = []
		self.unwrap(args)
	def unwrap(self, ops):
		for op in ops:
			if isinstance(op, list):
				self.unwrap(op)
			else:
				self.ops.append(op)
	def assemble(self):
		ctx = AsmCtx(self.ops)
		# stage 1: calculate label addresses
		for op in ctx.flush():
			if isinstance(op, LABEL):
				ctx.labels[op.name] = ctx.addr
				#ctx.append(op)
			else:
				if isinstance(op, Cmd):
					op.apply(ctx)
				elif isinstance(op, Numerable):
					ctx.addr += Addr(0, op.size())
				ctx.append(op)
		# stage 2: set label addresses
		for op in ctx.flush():
			if isinstance(op, Paramable):
				ctx.append(op.resolveLabels(ctx))
			else:
				ctx.append(op)
		# stage 3: compile to tape
		for op in ctx.flush():
			if isinstance(op, Paramable):
				op.compile(ctx)
			elif isinstance(op, AbsAddr):
				HLT(op).compile(ctx)
			elif isinstance(op, str):
				ctx.append(op)
			else:
				raise Exception(f"Cannot compile op: {op}")
		return ctx.flush()
	def __repr__(self):
		return f"Assembler({', '.join(map(repr, self.ops))})"



if __name__ == "__main__":
	# Ignore this part, it's just here for testing that the assembler works.

	def Mac1(par, pre):
		# Local label defs
		hi = f"{pre}hi"
		bye = f"{pre}bye"
		# Macro program
		return [
			LDA((0, 0)),     # Absolute address
			JMP(par[0]),
			JMP(par[2]),
			LABEL(hi),
			# TODO maybe implement this at some point
			#LDA(5),             # Constant (creates a data section)
			LDA(hi),         # Local label
			LDA((hi,)),       # Local label
			LDA((hi, 0, 1)),  # Local label with offset
			LDA((hi, 1, 2)),  # Local label with offset
			LDA(par[1]),  # Macro parameter
			HLT(),
			DATA(2, 3, 0x4, HLT(bye), 6, 7, AbsAddr(10, 0), hi, par[1]),
			LABEL(bye)
		]

	def macro2(par, pre):
		test = f"{pre}test"
		return [
			HLT(),
			MACRO(Mac1, ["start", par[0], test], pre),  # Contains global label
			LABEL(test),
			# TODO maybe implement this at some point
			# JMP((".", 1))  # Points to here+1
		]

	def whilee(par, pre):
		return [
			ORIG(par[0]),
			LABEL("start"),  # Global label
			"while",
			par[0],
			*par[1],  # Dynamic code injection
			LABEL(f"{pre}done"),  # Local label
			EXEC(par[0])
		]

	a = Assembler(
		"Program 1",
		ORIG((4, 0)),
		MACRO(macro2, [(0, 5)]),
		"test",
		MACRO(whilee, [
			AbsAddr(11, 0),
			[
				"print 1",
				"print 2"
			]
		]),
		JMP("done!"),
		EXEC("start"),
		RAW("z0000"),
		LABEL("done!")
	)

	print(a)
	for o in a.ops:
		print(o)
	#"Program 1"
	#ORIG(AbsAddr(4, 0))
	#	HLT()
	#		LDA(AbsAddr(0, 0))
	#		JMP(LabAddr("*start"))
	#		JMP(LabAddr("macro2-0000_test"))
	#		LDA(LabAddr("macro2-0000_Mac1-0001_hi"))
	#		LDA(LabAddr("macro2-0000_Mac1-0001_hi"))
	#		LDA(LabAddr("macro2-0000_Mac1-0001_hi", 0, 1))
	#		LDA(LabAddr("macro2-0000_Mac1-0001_hi", 1, 2))
	#		LDA(AbsAddr(0, 5))
	#		HLT()
	#		",0000009'"
	#		HexLit(0x2)
	#		HexLit(0x3)
	#		HexLit(0x4)
	#		HLT(LabAddr("macro2-0000_Mac1-0001_bye"))    !!!!!!!
	#		HexLit(0x6)
	#		HexLit(0x7)
	#		AbsAddr(10, 0)  !!!!!!!!
	#		LabAddr("macro2-0000_Mac1-0001_hi")  !!!!!
	#		AbsAddr(0, 5)  !!!!!
	#"test"
	#	ORIG(AbsAddr(11, 0))
	#	"while"
	#	AbsAddr(11, 0)
	#	"print 1"
	#	"print 2"
	#	EXEC(AbsAddr(11, 0))
	#JMP(LabAddr("done!"))
	#EXEC(AbsAddr(4, 0))
	#RAW("z0000")

	o = a.assemble()
	for i in o:
		print(i)
	#Program 1
	#;0000400'
	#z0000'
	#b0000'
	#u1100'
	#u0419'
	#b0404'
	#b0404'
	#b0405'
	#b0506'
	#b0005'
	#z0000'
	#,0000009'
	#2'
	#3'
	#4'
	#44j'
	#6'
	#7'
	#f00'
	#410'
	#14'
	#test
	#;0001100'
	#while
	#z1100'
	#print 1
	#print 2
	#.0001100'
	#u1103'
	#.0001100'
	#z0000'
