#!/usr/bin/env python3

from utils import *
from lgpasm import *



def setupKfStatus(params, prefix):
	return [
		DEBUG("----- kfStatus -----", '\n'),
		DEBUG("Status Constants"),
		DATA(
			LABEL("KF_SYSTEM_DONE"),           0b_000000_000000_00,
			LABEL("KF_DATA_STACK_OVERFLOW"),  -0b_000000_000001_00,  # 1
			LABEL("KF_DATA_STACK_UNDERFLOW"), -0b_000000_000010_00,  # 2
			LABEL("KF_RETN_STACK_OVERFLOW"),  -0b_000000_000011_00,  # 3
			LABEL("KF_RETN_STACK_UNDERFLOW"), -0b_000000_000100_00,  # 4
			#KF_TEST_PTR_WIDTH
			#KF_TEST_STRUCT
			#KF_SYSTEM_COMP_ONLY
			#KF_SYSTEM_NOT_IMP
			#KF_SYSTEM_NULL
		),
		MACRO(defKfStatusErr, [], prefix),
	]



# Throw an error based on a code.
# Usage: MACRO(kfStatusErr, ["KF_DATA_STACK_OVERFLOW"])
def kfStatusErr(params, prefix):
	err = params[0]
	return [
		DEBUG("kfStatusErr()"),
		LDA(err),
		JMP("kfStatusErr"),
	]
def defKfStatusErr(params, prefix):
	return [
		DEBUG("defKfStatusErr"),
		LABEL("kfStatusErr"),
		MACRO(outputText, ["\n\x0e22 "], prefix),
		
		BLZ("kfStatusErr_printerr"),
		MACRO(outputText, ["done"], prefix),
		JMP("kfStatusErr_done"),
		
		LABEL("kfStatusErr_printerr"),
		MACRO(outputText, ["err; "], prefix),
		ADD("kfStatusErr_jumptable"), # Calculate the offset
		REP("kfStatusErr_printerr1"), # Jump to it
		LABEL("kfStatusErr_printerr1"),
		JMP((0, 0)),
		
		# Jump table, in reverse order
		JMP("kfStatusErr_retn_stack_underflow"),
		JMP("kfStatusErr_retn_stack_overflow"),
		JMP("kfStatusErr_data_stack_underflow"),
		JMP("kfStatusErr_data_stack_overflow"),
		LABEL("kfStatusErr_jumptable"),
		LabAddr("kfStatusErr_jumptable"),
		
		# Text errors
		LABEL("kfStatusErr_data_stack_overflow"),
		MACRO(outputText, ["dso"], prefix),
		JMP("kfStatusErr_done"),
		LABEL("kfStatusErr_data_stack_underflow"),
		MACRO(outputText, ["dsu"], prefix),
		JMP("kfStatusErr_done"),
		LABEL("kfStatusErr_retn_stack_overflow"),
		MACRO(outputText, ["rso"], prefix),
		JMP("kfStatusErr_done"),
		LABEL("kfStatusErr_retn_stack_underflow"),
		MACRO(outputText, ["rsu"], prefix),
		JMP("kfStatusErr_done"),
		
		LABEL("kfStatusErr_done"),
		MACRO(outputText, [" 22\x0f"], prefix),
		LABEL("kfStatusErr_done2"),
		HLT(),
		JMP("kfStatusErr_done2"),
	]
