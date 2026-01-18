#!/usr/bin/env python3

import os
import sys

sys.path.insert(1, f"{sys.path[0]}{os.path.sep}..{os.path.sep}assembler")
from lgpasm import *



addrBits = 0b0_00000000000_0000_00_111111_111111_00



def setupUtils(params, prefix):
	return [
		DEBUG("----- utils -----", '\n'),
		DEBUG("util consts"),
		DATA(
			LABEL("devnull"), 0,
			LABEL("-2"), -2,
			LABEL("-1q-1"), 0b1_00000000000_0000_00_000000_000000_00,
			# 1 can't be included because it would fall in the dead bit.
			LABEL("2"), LABEL("1q30"), 2,
			LABEL("4"), LABEL("0001"), Addr(0, 1),  # 1 address unit
			LABEL("8"), LABEL("0002"), Addr(0, 2),  # 2 address units
			LABEL("16"), 16,
			#LABEL("32"), 32,
			LABEL("64"), 64,
			#LABEL("128"), 128,
			LABEL("256"), LABEL("0100"), 256,
			LABEL("512"), 512,
			LABEL("1024"), 1024,
			LABEL("LSR1"), 0x40000000,
			#LABEL("LSR2"), 0x20000000,
			#LABEL("LSR3"), 0x10000000,
			LABEL("LSR4"), 0x08000000,
			#LABEL("LSR5"), 0x04000000,
			LABEL("LSR6"), 0x02000000,
			LABEL("LSR7"), 0x01000000,
			#LABEL("LSR8"), 0x00800000,
			#LABEL("LSR9"), 0x00400000,
			#LABEL("LSR10"), 0x00200000,
			#LABEL("LSR11"), 0x00100000,
			LABEL("LSR12"), 0x00080000,
			#LABEL("LSR13"), 0x00040000,
			#LABEL("LSR14"), 0x00020000,
			#LABEL("LSR15"), 0x00010000,
			#LABEL("LSR16"), 0x00008000,
			#LABEL("LSR17"), 0x00004000,
			LABEL("LSR18"), 0x00002000,
			LABEL("addrBits"), addrBits,
		),
		MACRO(defEqualsZero, [], prefix),
	]



# Hardcode the commands to print a string.
# Should only be used for really small strings.
# Usage: MACRO(HardcodeText, ["hi!"])
def HardcodeText(params, prefix):
	text = params[0]
	return [
		DEBUG(f"HardcodeText({repr(text)})"),
		[[
			CharLit(c).print(),
			HLT()
		] for c in TextToLGPChars(text)],
	]

# Subroutine that sets acc negative if acc == 0, 0 otherwise.
# Usage: LDA("addr-of-value"),
#        MACRO(EqualsZero)
#  1 ->  0
#  0 -> -2
# -1 ->  0
def EqualsZero(params, prefix):
	return [
		DEBUG("EqualsZero()"),
		RTA("EqualsZero_rtn"),
		JMP("EqualsZero"),
	]
def defEqualsZero(params, prefix):
	return [
		DEBUG("defEqualsZero"),
		LABEL("EqualsZero"),
		BLZ("EqualsZero_no"),  # <0 -> 0
		SUB("2"),
		BLZ("EqualsZero_yes"),  # 0 -> -1
		LABEL("EqualsZero_no"),
		CLA(),
		JMP("EqualsZero_rtn"),
		LABEL("EqualsZero_yes"),
		LDA("-2"),
		LABEL("EqualsZero_rtn"), JMP((0, 0)),
	]

# Turn a string into a word-packed string.
# Usage: MACRO(PackString, ["hello"])
def PackString(params, prefix):
	text = params[0]
	force_lower = params[1] if len(params) > 1 else False
	text2 = TextToLGPChars(text, force_lower)
	# Pack each word with 5 chars.
	words = []
	word = 0
	cnt = 0
	for t in text2:
		word <<= 6
		word |= CharLit(t).toNum()
		cnt += 1
		if cnt == 5:
			cnt = 0
			words.append(word << 2)
			word = 0
	words.append(word << 2)
	# Return the assembly.
	return [
		DEBUG(f"PackString({repr(text)})  # {len(text2)} chars {len(words)} words"),
		DATA(*words),
	]
def TextToLGPChars(text, force_lower=False):
	uppercaseMap = {
		')': '0', 'L': 'l', '*': '2', '"': '3', 'Δ': '4',
		'%': '5', '$': '6', 'π': '7', 'Σ': '8', '(': '9',
		'F': 'f', 'G': 'g', 'J': 'j', 'K': 'k', 'Q': 'q',
		'W': 'w', 'Z': 'z', 'B': 'b', 'Y': 'y', 'R': 'r',
		'I': 'i', 'D': 'd', 'N': 'n', 'M': 'm', 'P': 'p',
		'E': 'e', 'U': 'u', 'T': 't', 'H': 'h', 'C': 'c',
		'A': 'a', 'S': 's', '=': '+', '_': '-', ':': ';',
		'?': '/', ']': '.', '[': ',', 'V': 'v', 'O': 'o',
		'X': 'x' }
	caseDontCare = "\x0e\x0f\r\n\b\t'\0 "
	text2 = ""
	cur_upper = False
	for t in text:
		is_upper = t in uppercaseMap
		if is_upper:
			t = uppercaseMap[t]
		if force_lower:
			is_upper = False
		# Insert upper/lower case commands into string.
		if is_upper != cur_upper and t not in caseDontCare:
			cur_upper = is_upper
			text2 += "\x0f" if is_upper else "\x0e"
		text2 += t
	if cur_upper:
		text2 += "\x0e"
	return text2



##############
# Pseudo Ops #
##############

# Pseudo op that does a logical left shift of the acc.
# Usage: LSL(<optional amount to shift by, defaults to 1>)
def LSL(bits=1):
	labl = ["2", "4", "8", "16", "32", "64", "128", "256", "512"]
	return MLO(labl[bits - 1])

# Pseudo op that does a logical right shift of the acc.
# The least significant bit is cleared if it lands in the spacer bit.
# Usage: LSR(<optional amount to shift by, defaults to 1>)
def LSR(bits=1):
	labl = ["LSR1", "LSR2", "LSR3", "LSR4", "LSR5", "LSR6", "LSR7", 0, 0, 0, 0, "LSR12", 0, 0, 0, 0, 0, "LSR18"]
	return MUP(labl[bits - 1])

# Pseudo op that clears acc.
# Usage: CLA()
def CLA():
	return STC("devnull")

# Pseudo op that negates the value in acc.
# Usage: NEG()
def NEG():
	return MUP("-1q-1")
