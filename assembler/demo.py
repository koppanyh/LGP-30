#!/usr/bin/env python3

# Demo program that generates a P104 tape that prints "kop wuz here".

from lgpasm import *

a = Assembler(
	ORIG((4, 0)),
	LABEL("start"),
	# Get the character being pointed to.
	LDA("pointer"),
	REP("loader"),
	LABEL("loader"),
	LDA((0,0)),
	REP("print"),
	# Break if it's 0.
	SUB("1"),
	BLZ("done"),
	# Print the character.
	LABEL("print"),
	PRT((0,0)),
	HLT(),
	# Incremement the pointer.
	LDA("pointer"),
	ADD("1"),
	STA("pointer"),
	# Loop.
	JMP("start"),
	# Exit.
	LABEL("done"),
	HLT(),

	ORIG((9, 0)),
	LABEL("pointer"),
	HLT("name"),
	LABEL("1"),
	HLT((0, 1)),

	ORIG((10, 0)),
	LABEL("name"),
	[HLT((CharLit(c).toNum(), 0)) for c in "Kop wuz here"],
	HLT(),

	EXEC("start")
)

for line in a.assemble():
	print(line)

# This is what the output should look like.
# Run it by saving it into a file and using `load <filename>` in simh, and then entering the `co` command.
#
# ;0000400'
# b0900'
# y0402'
# b0000'
# y0406'
# s0901'
# t0412'
# p0000'
# z0000'
# b0900'
# a0901'
# h0900'
# u0400'
# z0000'
# ;0000900'
# z1000'
# z0001'
# ;0001000'
# z5400'
# z3500'
# z3300'
# z0300'
# z6200'
# z4100'
# z0100'
# z0300'
# z4900'
# z3700'
# z1300'
# z3700'
# z0000'
# .0000400'
