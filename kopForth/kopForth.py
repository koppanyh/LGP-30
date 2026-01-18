#!/usr/bin/env python3

from utils import *
from lgpasm import *

from kfBios import *
from kfStatus import *
from kfStack import *
from kfWord import *

from kfWordsNative import *



def setupKopForth(params, prefix):
	return [
	# Setup others.
		MACRO(setupUtils, [], prefix),
		MACRO(setupKfBios, [], prefix),
		MACRO(setupKfStatus, [], prefix),
		MACRO(setupKfStack, [], prefix),
		MACRO(setupKfWord, [], prefix),
	# Setup self
		DEBUG("----- kopForth -----", '\n'),
		MACRO(kopForth, [], prefix),
		LabAddr("kopForth_wordsused"), LABEL("kopForth_wordsused"), MACRO(PackString, [" words used, "], prefix),
		LabAddr("kopForth_wordsfree"), LABEL("kopForth_wordsfree"), MACRO(PackString, [" words free."], prefix),
		LabAddr("kopForth_progend"), LABEL("kopForth_progend"), MACRO(PackString, ["Program end: "], prefix),
	]

def kfPopulateWords(params, prefix):
	return [
		MACRO(kfWord, ["boot",
			-1,
			KF_FLAG_MASK_NONE,
			"kfWord_boot_data",
			[
				"kfWord_(literal)", 69420*2,
				"kfWord_.",
				"kfWord_(literal)", 0b_001000_011010_000100_00,
				"kfWord_emit",
				"kfWord_key",
				"kfWord_dup",
				"kfWord_dup",
				"kfWord_emit",
				"kfWord_.",
				"kfWord_0branch", "asdfasdf",
				"kfWord_(literal)", "kopForth_mem_here",
				"kfWord_(literal)", "kopForth_mem_here",
				"kfWord_(literal)", 3*2,
				"kfWord_accept",
				"kfWord_type",
				LABEL("asdfasdf"),
				"kfWord_bye"
			]
		], prefix),
		
		MACRO(kfPopulateWordsNative, [], prefix),
		
		MACRO(kfWord, ["bye",
			"boot",  # TODO set this pointer to be correct
			KF_FLAG_MASK_NATIVE,
			"kopForth_bye",
			[]
		], prefix),
		LABEL("kopForth_bye"),
		MACRO(kfStatusErr, ["KF_SYSTEM_DONE"], prefix),
		JMP("rtn_to_kopForthTick"),
	]

# The data needed to keep track of what the current input source is.
# It's the number of fields in the kfInputSource struct.
KF_INPUT_SOURCE_COUNT = 4
def kfInputSource(params, prefix):
	return [
		DEBUG(f"kfInputSource()"),
		# The source ID value, 0=user input device, -1=string (via EVALUATE)
		LABEL("kopForth_in_src_source_id"), HLT(),
		# The index for the next character to read from the input buffer.
		LABEL("kopForth_in_src_in_offset"), HLT(),
		# The total size of the text in the input buffer.
		LABEL("kopForth_in_src_in_len"), HLT(),
		# The address of the start of the input buffer.
		LABEL("kopForth_in_src_buf"), LabAddr("kopForth_in_buf"),
	]

# This is the main struct from which an instance of kopForth is created.
# Maintain the core/heap/stacks ordering of the fields.
def kopForth(params, prefix):
	return [
		DEBUG("kopForth()"),
	# Core system fields
		# Pointer to the next available `mem` byte.
		LABEL("kopForth_here"), LabAddr("kopForth_mem_here"),
		# Pointer to the latest active word in `mem`. FIND starts searching here.
		LABEL("kopForth_latest"), LabAddr("kfWord_bye"),
		# Pointer to the most recently defined word, but not necessarily the latest active word.
		LABEL("kopForth_pending"), LabAddr("kfWord_bye"),
		# The compilation state, true=compiling, false=interpret. Uses `isize` so Forth programs can just use `@` and `!`.
		LABEL("kopForth_state"), HLT(),
		# Program counter for forth inner loop.
		LABEL("kopForth_pc"), LabAddr("kfWord_boot"),
	# Data heap
		# The general memory space where the word dictionary is held.
		DEBUG("kopForth_mem"),
		LABEL("kopForth_mem_ptr"), LabAddr("kopForth_mem"),
		LABEL("kopForth_mem"),
		MACRO(kfPopulateWords, [], prefix),
		LABEL("kopForth_mem_here"),
		# TODO maybe put disposable memory here
		ORIG(("kopForth_mem", 0, KF_MEM_SIZE)),  # Reserve space for mem.
		LABEL("kopForth_mem_end"), LabAddr("kopForth_mem_end"),
	# Stacks + input buffer region
		# The data stack.
		MACRO(allocKfStack, [d_stack, KF_DATA_STACK_SIZE], prefix),
		# The return stack.
		MACRO(allocKfStack, [r_stack, KF_RETN_STACK_SIZE], prefix),
		# The current input source definition.
		MACRO(kfInputSource, [], prefix),
		# The input buffer, shared between terminal and files.
		LABEL("kopForth_in_buf"), DATA(*([0]*KF_IN_BUF_SIZE)),
	]

def kfDebug(params, prefix):
	return [
		# Print pointer.
		LDA("kopForth_pc"),
		MACRO(kfBiosPrintPointer, [], prefix),
		# Print ':'.
		MACRO(HardcodeText, [":"], prefix),
		# Print word name.
		LDA("KF_MAX_NAME_SIZE"),
		STC("kfBiosWriteStrLen_len"),
		LDA("kopForth_pc"),
		MACRO(kfBiosWriteStrLen, [], prefix),
		MACRO(kfBiosCR, [], prefix),
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
		# Debug stuff.
		#MACRO(kfDebug, [], prefix),
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
		# Call native word.
		LABEL("kopForthTick_jmp1"), JMP((0, 0)),
		LABEL("rtn_to_kopForthTick"),
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
