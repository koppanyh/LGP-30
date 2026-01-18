#!/usr/bin/env python3

from utils import *
from lgpasm import *

from kfBios import *



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
			LABEL("KF_SYSTEM_NOT_IMP"),       -0b_000000_000101_00,  # 5
			#KF_TEST_PTR_WIDTH
			#KF_TEST_STRUCT
			#KF_SYSTEM_COMP_ONLY
			#KF_SYSTEM_NULL
		),
		LabAddr("ERR_START"), LABEL("ERR_START"), MACRO(PackString, ["\n** "], prefix),
		LabAddr("ERR_DONE"), LABEL("ERR_DONE"), MACRO(PackString, ["DONE"], prefix),
		LabAddr("ERR_ERR"), LABEL("ERR_ERR"), MACRO(PackString, ["ERROR: "], prefix),
		LabAddr("ERR_END"), LABEL("ERR_END"), MACRO(PackString, [" **"], prefix),
		LABEL("ERR_DSO"), MACRO(PackString, ["STACK OVERFLOW"], prefix),
		LABEL("ERR_DSU"), MACRO(PackString, ["STACK UNDERFLOW"], prefix),
		LABEL("ERR_RSO"), MACRO(PackString, ["RETURN OVERFLOW"], prefix),
		LABEL("ERR_RSU"), MACRO(PackString, ["RETURN UNDERFLOW"], prefix),
		LABEL("ERR_SNI"), MACRO(PackString, ["NOT IMPLEMENTED"], prefix),
		# These have to be in reverse order
		LabAddr("ERR_SNI"),
		LabAddr("ERR_RSU"),
		LabAddr("ERR_RSO"),
		LabAddr("ERR_DSU"),
		LabAddr("ERR_DSO"),
		LABEL("ERR_addrs"), LabAddr("ERR_addrs"),
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
		# Save code and print '\n** '.
		STC("kfStatusErr_code"),
		LDA(("ERR_START", 0, -1)),
		MACRO(kfBiosWriteStr, [], prefix),
		# Check if it's an error or print 'DONE' and quit.
		LDA("kfStatusErr_code"),
		BLZ("kfStatusErr_printerr"),
		LDA(("ERR_DONE", 0, -1)),
		MACRO(kfBiosWriteStr, [], prefix),
		JMP("kfStatusErr_done"),
		# Print 'ERR: '.
		LABEL("kfStatusErr_printerr"),
		LDA(("ERR_ERR", 0, -1)),
		MACRO(kfBiosWriteStr, [], prefix),
		# Get err str address and print.
		LDA("kfStatusErr_code"),
		ADD("ERR_addrs"),
		REP("kfStatusErr_printerr1"),
		LABEL("kfStatusErr_printerr1"), LDA((0, 0)),
		MACRO(kfBiosWriteStr, [], prefix),
		# Print ' **' and loop.
		LABEL("kfStatusErr_done"),
		LDA(("ERR_END", 0, -1)),
		MACRO(kfBiosWriteStr, [], prefix),
		LABEL("kfStatusErr_done2"),
		HLT(),
		JMP("kfStatusErr_done2"),
		# Params.
		LABEL("kfStatusErr_code"), HLT(),
	]
