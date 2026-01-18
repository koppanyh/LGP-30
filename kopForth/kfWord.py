#!/usr/bin/env python3

from utils import *
from lgpasm import *

from kfBios import *



def setupKfWord(params, prefix):
	return [
		DEBUG("----- kfWord -----", '\n'),
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
			# Other constants.
			LABEL("KF_MAX_NAME_SIZE"), KF_MAX_NAME_SIZE,
		),
	]



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
	max_name_chars = KF_MAX_NAME_SIZE * 5
	name_chars = TextToLGPChars(name)
	if len(name_chars) > max_name_chars:
		raise Exception(f"Name {repr(name)} doesn't fit in {KF_MAX_NAME_SIZE} words.")
	name_chars += "\0" * (max_name_chars - len(name_chars))
	# This is totally a hack
	chars = MACRO(PackString, [name_chars], prefix)[1][1:][:-1]
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
