#!/usr/bin/env python3

from utils import *
from lgpasm import *

from kfBios import *
from kfStatus import *
from kfStack import *
from kfType import *



def setupKopForth(params, prefix):
	return [
	# Setup others.
		MACRO(setupUtils),
		MACRO(setupKfBios),
		MACRO(setupKfStatus),
		MACRO(setupKfStack),
		MACRO(setupKfType),
	# Setup self
		DEBUG("----- kopForth -----", '\n'),
		LabAddr("kopForth_wordsused"), LABEL("kopForth_wordsused"), MACRO(PackString, [" words used, "], prefix),
		LabAddr("kopForth_wordsfree"), LABEL("kopForth_wordsfree"), MACRO(PackString, [" words free."], prefix),
		LabAddr("kopForth_progend"), LABEL("kopForth_progend"), MACRO(PackString, ["Program end: "], prefix),
	]



#############################
# Internal macros         ▲ #
#############################
# User-accessible macros  ▼ #
#############################



def kopForthInit(params, prefix):
	return [
		# Set up bios.
		MACRO(kfBiosSetup, [], prefix),
		DEBUG("kopForthInit()"),
		# Print used space.
		LDA("kopForth_here"),
		SUB("kopForth_mem_ptr"),
		LSR(1),
		MACRO(kfBiosPrintIsize, [], prefix),
		LDA(("kopForth_wordsused", 0, -1)),
		MACRO(kfBiosWriteStr, [], prefix),
		# Pring free space.
		LDA("kopForth_mem_end"),
		SUB("kopForth_here"),
		LSR(1),
		MACRO(kfBiosPrintIsize, [], prefix),
		LDA(("kopForth_wordsfree", 0, -1)),
		MACRO(kfBiosWriteStr, [], prefix),
		MACRO(kfBiosCR, [], prefix),
		# Print program end.
		LDA(("kopForth_progend", 0, -1)),
		MACRO(kfBiosWriteStr, [], prefix),
		LDA("program_end"),
		MACRO(kfBiosPrintPointer, [], prefix),
		MACRO(kfBiosCR),
	]

def kopForthTick(params, prefix):
	return [
		DEBUG("kopForthTick()"),
		#LDA("kopForth_pc"),
		#MACRO(kfBiosPrintPointer, [], prefix),
		# Check if it's native.
		LDA("kopForth_pc"),
		ADD("KF_WORD_FLAGS_OFFSET"),
		REP("kopForthTick_lda1"),
		LABEL("kopForthTick_lda1"), LDA((0, 0)),
		AND("KF_FLAG_MASK_NATIVE"),
		SUB("KF_FLAG_MASK_NATIVE"),
		BLZ("kopForthTick_not_nat"),
		# Get native word addr.
		LDA("kopForth_pc"),
		ADD("KF_WORD_CODE_OFFSET"),
		REP("kopForthTick_lda2"),
		LABEL("kopForthTick_lda2"), LDA((0, 0)),
		REP("kopForthTick_jmp1"),
		# Set reurn addr.
		SUB("0001"),
		REP("kopForthTick_rta1"),
		LABEL("kopForthTick_rta1"), RTA((0, 0)),
		# Call native subroutine.
		LABEL("kopForthTick_jmp1"), JMP((0, 0)),
		# Pop return addr and save to pc.
		MACRO(kfStackPop, [r_stack], prefix),
		STA("kopForth_pc"),
		JMP("kopForthTick_finalize"),
		# Get forth word addr and save to pc.
		LABEL("kopForthTick_not_nat"),
		LDA("kopForth_pc"),
		ADD("KF_WORD_CODE_OFFSET"),
		REP("kopForthTick_lda3"),
		LABEL("kopForthTick_lda3"), LDA((0, 0)),
		STA("kopForth_pc"),
		# Push next addr to return stack and set pc.
		LABEL("kopForthTick_finalize"),
		ADD("0001"),
		MACRO(kfStackPush, [r_stack], prefix),
		LDA("kopForth_pc"),
		REP("kopForthTick_lda4"),
		LABEL("kopForthTick_lda4"), LDA((0, 0)),
		STA("kopForth_pc"),
	]
	'''
	kfWord* cur_word = (kfWord*) forth->pc;
	if (cur_word->flags.bit_flags.is_native) {
		cur_word->code.native(forth);
		kfRetnStackPop(&forth->r_stack, (void**) &forth->pc);
	} else {
		forth->pc = (uint8_t*) cur_word->code.forth;
	}
	kfRetnStackPush(&forth->r_stack, forth->pc + sizeof(kfWord*));
	forth->pc = *(uint8_t**) forth->pc;
	'''
