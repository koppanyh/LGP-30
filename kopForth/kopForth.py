#!/usr/bin/env python3

from utils import *
from lgpasm import *

from kfBios import *
from kfStatus import *
from kfStack import *



###############
# Test Macros #
###############

def pftos(params, prefix):
	return [
		MACRO(kfStackPop,      [kfDataStack], prefix),
		REP(prefix + "asdf"),
		LABEL(prefix + "asdf"), PRT((0, 0)),
		HLT(),
		#MACRO(kfBiosWriteChar, [],            prefix),
		MACRO(kfStackPush,     [kfDataStack], prefix),
	]

def pushWithOffset(params, prefix):
	offset = params[0]
	return [
		LDA(("chars", 0, offset)),
		MACRO(kfStackPush, [kfDataStack], prefix),
		MACRO(pftos, [], prefix),
	]



a = Assembler(
	ORIG((4, 0)),
# Constants
	DEBUG("Constants", '\n'),
	LABEL("chars"), [Addr(CharLit(c).toNum(), 0) for c in "abc"], HLT(),
	LABEL("packed"), MACRO(PackString, ["hello, world. today;\n"]),
	DATA(
		LABEL("chars_ptr"), LabAddr("chars"),
		LABEL("packed_ptr"), LabAddr("packed"), 5*2,
		LABEL("1243q30"), 1243*2,
		LABEL("fdsa"), 0b0_10011111111_1111_11_111111_111111_11,# + 1,
	),
# Setup
	MACRO(setupUtils),
	MACRO(setupKfBios),
	MACRO(setupKfStatus),
	MACRO(setupKfStack),
# System Functions
	DEBUG("System Functions", '\n'),
# Native Functions
	DEBUG("Native Functions", '\n'),
# Test Section
	DEBUG("Test Section", '\n'),
	LABEL("test"),
	#MACRO(kfBiosSetup),
	# print an integer
	LDA("1243q30"),
	LDA("fdsa"),
	MACRO(kfBiosPrintIsize),
	HLT(),
	# print a packed string
	LDA("packed_ptr"),
	MACRO(kfBiosWriteStr),#Len),
	# print a pointer
	LDA("asdf"),
	MACRO(kfBiosPrintPointer),
	MACRO(kfBiosCR),
	# write to stack
	MACRO(kfBiosCR),
	MACRO(pushWithOffset, [0]),
	MACRO(pushWithOffset, [1]),
	MACRO(pushWithOffset, [2]),
	# read from stack
	MACRO(HardcodeText, [" - "]),
	MACRO(kfStackPop, [kfDataStack]), MACRO(kfBiosWriteChar),
	MACRO(kfStackPop, [kfDataStack]), MACRO(kfBiosWriteChar),
	MACRO(kfStackPop, [kfDataStack]), MACRO(kfBiosWriteChar),
	MACRO(kfStackPop, [kfDataStack]), MACRO(kfBiosWriteChar),
	LABEL("asdf"), HLT("asdf"),
	EXEC("test"),
)



#print(a)
debug = False
#debug = True
r = a.assemble(debug=debug)
for i in range(len(r)):
	o = r[i]
	n = r[i + 1] if i < len(r) - 1 else ""
	if o == "0'" and n == "0'":  # Collapse zeros
		print(o, end='')
	else:
		print(o)
