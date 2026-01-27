#!/usr/bin/env python3

from utils import *
from lgpasm import *

from kfBios import *
from kfStatus import *



d_stack = "kopForth_data"
r_stack = "kopForth_retn"



def setupKfStack(params, prefix):
	return [
		DEBUG("----- kfStack -----", '\n'),
		MACRO(defKfStackPrint, [], prefix),
		MACRO(defKfStackPush, [], prefix),
		MACRO(defKfStackPop, [], prefix),
	]

def allocKfStack(params, prefix):
	name = params[0]
	size = params[1]
	stackval = "STACKVAL_" + name
	return [
		DEBUG(f"allocKfStack({repr(name)})"),
		DATA(
			*([0] * size),
			LABEL(stackval), LabAddr(stackval),  # Points to the stack head
			LABEL("STACKPTR_" + name), LabAddr(stackval),
			LABEL("STACKFULL_" + name), LabAddr(stackval, 0, -size),
		),
	]

# Reset the stack
# Usage: MACRO(kfStackReset, [kfDataStack])
def kfStackReset(params, prefix):
	name = params[0]
	return [
		DEBUG(f"kfStackReset({repr(name)})"),
		LDA("STACKPTR_" + name),  # Load the pointer of the stack val
		STC("STACKVAL_" + name),  # Write it to the stack val
	]



# Print the stack
# Usage: MACRO(kfStackPrint, [kfDataStack])
def kfStackPrint(params, prefix):
	name = params[0]
	return [
		DEBUG(f"kfStackPrint({repr(name)})"),
		LDA("STACKPTR_" + name),  # Load the pointer of the stack val
		RTA("kfStackPrint_rtn"),
		JMP("kfStackPrint"),
	]
def defKfStackPrint(params, prefix):
	return [
		DEBUG("defKfStackPrint"),
		LABEL("kfStackPrint"),
		# Save pointer value.
		REP("kfStackPrint_sub1"),  # STACKVAL
		REP("kfStackPrint_lda2"),
		ADD("0001"),
		REP("kfStackPrint_lda1"),  # STACKPTR
		# Calculate stack size.
		LABEL("kfStackPrint_lda1"), LDA((0, 0)),
		LABEL("kfStackPrint_sub1"), SUB((0, 0)),
		STA("kfStackPrint_val"),
		# Loop start.
		LABEL("kfStackPrint_loop"),
		# Decrement pointer.
		LDA("kfStackPrint_lda2"),
		SUB("0001"),
		REP("kfStackPrint_lda2"),
		# Decrement counter.
		LDA("kfStackPrint_val"),
		SUB("0001"),
		BLZ("kfStackPrint_rtn"),
		STC("kfStackPrint_val"),
		# Read value and print.
		LABEL("kfStackPrint_lda2"), LDA((0, 0)),
		MACRO(kfBiosPrintIsize, [], prefix),
		MACRO(HardcodeText, [", "], prefix),
		# Loop.
		JMP("kfStackPrint_loop"),
		LABEL("kfStackPrint_rtn"), JMP((0, 0)),
		# Params.
		LABEL("kfStackPrint_val"), HLT(),  # Stack size
	]

# Push acc to stack
# Usage: MACRO(kfStackPush, [kfDataStack])
def kfStackPush(params, prefix):
	name = params[0]
	return [
		DEBUG(f"kfStackPush({repr(name)})"),
		STC("kfStackPush_val"),  # Set the acc as the parameter to push
		LDA("STACKPTR_" + name),  # Load the pointer of the stack val
		RTA("kfStackPush_rtn"),
		JMP("kfStackPush"),
	]
def defKfStackPush(params, prefix):
	return [
		DEBUG("defKfStackPush"),
		LABEL("kfStackPush"),
		# Write all the data pointer addreses.
		REP("kfStackPush_ptr1"),
		REP("kfStackPush_ptr2"),
		REP("kfStackPush_ptr5"),
		ADD("0002"),
		REP("kfStackPush_ptr4"),
		# Check overflow condition.
		LABEL("kfStackPush_ptr4"), LDA((0, 0)),
		LABEL("kfStackPush_ptr5"), SUB((0, 0)),
		BLZ("kfStackPush_ptr1"),
		MACRO(kfStatusErr, ["KF_DATA_STACK_OVERFLOW"], prefix),
		# Decrement the data ptr.
		LABEL("kfStackPush_ptr1"), LDA((0, 0)),
		SUB("0001"),
		LABEL("kfStackPush_ptr2"), STA((0, 0)),
		REP("kfStackPush_ptr3"),
		# Save the value to the data address.
		LDA("kfStackPush_val"),
		LABEL("kfStackPush_ptr3"), STA((0, 0)),
		LABEL("kfStackPush_rtn"), JMP((0, 0)),
		# Params
		LABEL("kfStackPush_val"), HLT(),  # Value to push.
	]

# Pop stack to acc
# Usage: MACRO(kfStackPop, [kfDataStack])
def kfStackPop(params, prefix):
	name = params[0]
	return [
		DEBUG(f"kfStackPop({repr(name)})"),
		LDA("STACKPTR_" + name),
		RTA("kfStackPop_rtn"),
		JMP("kfStackPop"),
	]
def defKfStackPop(params, prefix):
	return [
		DEBUG("defKfStackPop"),
		LABEL("kfStackPop"),
		# Write all the data pointer addreses.
		REP("kfStackPop_ptr1"),
		REP("kfStackPop_ptr3"),
		REP("kfStackPop_ptr4"),
		REP("kfStackPop_ptr5"),
		# Check underflow condition: acc is already value at STACKPTR.
		LABEL("kfStackPop_ptr5"), SUB((0, 0)),
		SUB("0001"),
		BLZ("kfStackPop_underflow"),
		# Get the value from the data address.
		LABEL("kfStackPop_ptr1"), LDA((0, 0)),
		REP("kfStackPop_ptr2"),
		LABEL("kfStackPop_ptr2"), LDA((0, 0)),
		STC("kfStackPop_val"),
		# Increment the data ptr.
		LABEL("kfStackPop_ptr3"), LDA((0, 0)),
		ADD("0001"),
		LABEL("kfStackPop_ptr4"), STC((0, 0)),
		# Return the value.
		LDA("kfStackPop_val"),
		LABEL("kfStackPop_rtn"), JMP((0, 0)),
		LABEL("kfStackPop_underflow"),
		MACRO(kfStatusErr, ["KF_DATA_STACK_UNDERFLOW"], prefix),
		# Params
		LABEL("kfStackPop_val"), HLT(),  # Value to return
	]
