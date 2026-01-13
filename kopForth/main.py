#!/usr/bin/env python3

from utils import *
from lgpasm import *

from kopForth import *



a = Assembler(
	ORIG((4, 0)),
# Setup
	MACRO(setupKopForth),
# Initialization
	LABEL("start"),
	MACRO(kopForthInit),
# Run Forth
	LABEL("forth_loop"),
	MACRO(kopForthTick),
	JMP("forth_loop"),
	LABEL("program_end"), HLT("program_end"),
	EXEC("start"),
)



#print(a)
debug = False
#debug = True
r = a.assemble(debug=debug)
c = 0
for o in r:
	if c:  # Collapse DATA outputs
		print(o, end='')
		c -= 1
	else:
		print(o)
		if o.startswith(','):
			c = int(o[1:-1]) - 1
