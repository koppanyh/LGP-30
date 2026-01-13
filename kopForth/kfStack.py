#!/usr/bin/env python3

from utils import *
from lgpasm import *

from kfBios import *
from kfStatus import *



def setupKfStack(params, prefix):
	return [
		DEBUG("----- kfStack -----", '\n'),
		MACRO(defKfStackPush, [], prefix),
		MACRO(defKfStackPop, [], prefix),
	]

def allocKfStack(params, prefix):
	name = params[0]
	size = params[1]
	stackval = "STACKVAL_" + name
	return [
		DEBUG(f"allocKfStack({repr(name)})"),
		DATA(*([0] * size)),
		LABEL(stackval),
		LabAddr(stackval),  # Points to the stack head
		LABEL("STACKPTR_" + name),
		LabAddr(stackval),
		LABEL("STACKFULL_" + name),
		LabAddr(stackval, 0, -size),
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
		REP("kfStackPush_ptr1"),  # Write all the data pointer addreses
		REP("kfStackPush_ptr2"),
		REP("kfStackPush_ptr5"),
		
		# Check overflow condition
		ADD("0002"),
		REP("kfStackPush_ptr4"),
		LABEL("kfStackPush_ptr4"),
		LDA((0, 0)),
		LABEL("kfStackPush_ptr5"),
		SUB((0, 0)),
		BLZ("kfStackPush_ptr1"),
		MACRO(kfStatusErr, ["KF_DATA_STACK_OVERFLOW"], prefix),
		
		LABEL("kfStackPush_ptr1"),
		LDA((0, 0)),  # Load the data ptr
		SUB("0001"),  # Decrement it
		LABEL("kfStackPush_ptr2"),
		STA((0, 0)),  # Save the data ptr
		REP("kfStackPush_ptr3"),  # Write the data address
		
		LDA("kfStackPush_val"),
		LABEL("kfStackPush_ptr3"),
		STA((0, 0)),  # Save the value to the data address
		
		LABEL("kfStackPush_rtn"),
		JMP((0, 0)),
		# Params
		LABEL("kfStackPush_val"), HLT(),  # Value to push
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
		REP("kfStackPop_ptr1"),
		REP("kfStackPop_ptr3"),
		REP("kfStackPop_ptr4"),
		REP("kfStackPop_ptr5"),
		
		# Check underflow condition
		# acc is already value at STACKPTR
		LABEL("kfStackPop_ptr5"),
		SUB((0, 11)),
		SUB("0001"),
		BLZ("kfStackPop_underflow"),
		
		LABEL("kfStackPop_ptr1"),
		LDA((0, 0)),  # Load the data ptr
		REP("kfStackPop_ptr2"),
		LABEL("kfStackPop_ptr2"),
		LDA((0, 0)),  # Load the data
		STC("kfStackPop_val"),  # Save the data for output
		
		LABEL("kfStackPop_ptr3"),
		LDA((0, 0)),  # Load the data ptr
		ADD("0001"),  # Increment it
		LABEL("kfStackPop_ptr4"),
		STC((0, 0)),  # Save the data ptr
		LDA("kfStackPop_val"),  # Load the data
		
		LABEL("kfStackPop_rtn"),
		JMP((0, 0)),
		# Params
		LABEL("kfStackPop_val"), HLT(),  # Value to return
		
		LABEL("kfStackPop_underflow"),
		MACRO(kfStatusErr, ["KF_DATA_STACK_UNDERFLOW"], prefix),
	]
