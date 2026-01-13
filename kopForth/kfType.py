#!/usr/bin/env python3

from utils import *
from lgpasm import *

from kfBios import *
from kfStack import *



def setupKfType(params, prefix):
	return [
		DEBUG("----- kfType -----", '\n'),
		DATA(
			# Word field offsets.
			LABEL("KF_WORD_NAME_OFFSET"),  Addr(0, KF_WORD_NAME_OFFSET),
			LABEL("KF_WORD_LINK_OFFSET"),  Addr(0, KF_WORD_LINK_OFFSET),
			LABEL("KF_WORD_FLAGS_OFFSET"), Addr(0, KF_WORD_FLAGS_OFFSET),
			LABEL("KF_WORD_CODE_OFFSET"),  Addr(0, KF_WORD_CODE_OFFSET),
			LABEL("KF_WORD_DATA_OFFSET"),  Addr(0, KF_WORD_DATA_OFFSET),
			# Flag constants.
			LABEL("KF_FLAG_MASK_NATIVE"),    KF_FLAG_MASK_NATIVE,
			LABEL("KF_FLAG_MASK_IMMEDIATE"), KF_FLAG_MASK_IMMEDIATE,
			LABEL("KF_FLAG_MASK_COMPILE"),   KF_FLAG_MASK_COMPILE,
		),
		MACRO(kopForth, [], prefix),
	]

def kfPopulateWords(params, prefix):
	return [
		JMP((0, 0)),
		LABEL("byeNative"),
		MACRO(kfStatusErr, ["KF_SYSTEM_DONE"], prefix),
		JMP(("byeNative", 0, -1)),
		
		JMP((0, 0)),
		LABEL("testNative"),
		MACRO(HardcodeText, ["hello\n"], prefix),
		JMP(("testNative", 0, -1)),
		
		MACRO(kfWord, ["boot",
			-1,
			KF_FLAG_MASK_NONE,
			"kfWord_boot_data",
			["kfWord_test", "kfWord_bye"]
		], prefix),
		MACRO(kfWord, ["bye",
			"boot",
			KF_FLAG_MASK_NATIVE,
			"byeNative",
			[]
		], prefix),
		MACRO(kfWord, ["test",
			"bye",
			KF_FLAG_MASK_NATIVE,
			"testNative",
			[]
		], prefix),
	]



#####################
# Interpreter stuff #
#####################

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
d_stack = "kopForth_data"
r_stack = "kopForth_retn"
in_src = "kopForth_in_src"
def kopForth(params, prefix):
	return [
		DEBUG("kopForth()"),
	# Core system fields
		# Pointer to the next available `mem` byte.
		LABEL("kopForth_here"), LabAddr("kfWord_boot_end"),
		# Pointer to the latest active word in `mem`. FIND starts searching here.
		LABEL("kopForth_latest"), LabAddr("kfWord_boot"),
		# Pointer to the most recently defined word, but not necessarily the latest active word.
		LABEL("kopForth_pending"), LabAddr("kfWord_boot"),
		# The compilation state, true=compiling, false=interpret. Uses `isize` so Forth programs can just use `@` and `!`.
		LABEL("kopForth_state"), HLT(),
		# Program counter for forth inner loop.
		LABEL("kopForth_pc"), LabAddr("kfWord_boot"),
	# Data heap
		# The general memory space where the word dictionary is held.
		DEBUG("kopForth_mem"), LABEL("kopForth_mem_ptr"), LabAddr("kopForth_mem"),
		LABEL("kopForth_mem"),
		MACRO(kfPopulateWords, [], prefix),
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



##############
# Word stuff #
##############

KF_FLAG_MASK_NONE      = 0
KF_FLAG_MASK_NATIVE    = 2
KF_FLAG_MASK_IMMEDIATE = 4
KF_FLAG_MASK_COMPILE   = 8

# This is the word definition type that defines the name and flags and overall
# functionality of each Forth word in memory.
# Must be packed so that we know the field offsets and the words defined in
# forth will be able to know where to access a field with pointer arithmetic.
KF_WORD_NAME_OFFSET  = 0
KF_WORD_LINK_OFFSET  = KF_WORD_NAME_OFFSET + KF_MAX_NAME_SIZE
KF_WORD_FLAGS_OFFSET = KF_WORD_LINK_OFFSET + 1
KF_WORD_CODE_OFFSET  = KF_WORD_FLAGS_OFFSET + 1
KF_WORD_DATA_OFFSET  = KF_WORD_CODE_OFFSET + 1
def kfWord(params, prefix):
	name = params[0]
	link = params[1]
	flags = params[2]
	code = params[3]
	data = params[4]
	prefix = f"kfWord_{name}"
	if isinstance(link, str) and not link.startswith("kfWord_"):
		link = "kfWord_" + link
	# Pad the name until it fits
	max_name_chars = KF_MAX_NAME_SIZE * 5 - 1
	name_chars = TextToLGPChars(name)
	if len(name_chars) > max_name_chars:
		raise Exception(f"Name {repr(name)} doesn't fit in {KF_MAX_NAME_SIZE} words.")
	name_chars += "\0" * (max_name_chars - len(name_chars))
	# This is totally a hack
	chars = MACRO(PackString, [name_chars], prefix)[1][1:]
	return [
		DEBUG(f"kfWord({repr(name)})"),
		LABEL(prefix),
		DATA(
			# The name of the word.
			LABEL(prefix+"_name"), *chars,
			# Linked-list pointer to the previous word.
			LABEL(prefix+"_link"), link,
			# The flags used for runtime and compile time behaviors.
			LABEL(prefix+"_flags"), flags,
			# Code pointer, says what to run when word is executed.
			LABEL(prefix+"_code"), code,
			# It's important that `data` comes at the end of the `kfWord` so it can be
			# expanded past its boundary of 1 item without colliding with any of the
			# other fields in the word definition.
			# The non-native word definition.
			LABEL(prefix+"_data"), *data,
		),
		LABEL(prefix + "_end"),
	]



##########
# Macros #
##########

# Macros for defining words and stuff in kopForth.

def kopForthCreateWord(params, prefix):
	name  = params[0]
	flags = params[1]
	code  = params[2]
	data  = params[3]
	return [
		LABEL("WRD_" + name),  # Global label starting with WRD_
		DATA(0, 0),    # name
		AbsAddr(0, 0), # link  # TODO
		DATA(flags),
		Addr.toAddr(code),
		data,
	]

def kopForthAddWord(params, prefix):
	name  = params[0]
	flags = params[1]
	data  = params[2]
	return [
		MACRO(worddef, [
			name,
			flags,
			("WRD_" + name, 0, KF_WORD_DATA_OFFSET),
			data
		], prefix)
	]

def kopForthAddNativeWord(params, prefix):
	name    = params[0]
	funcPtr = params[1]
	flags   = params[2]
	return [
		MACRO(worddef, [name, flags | kfFlag.native, fnaddr, []], prefix)
	]
