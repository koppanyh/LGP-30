#!/usr/bin/env python3

from utils import *
from lgpasm import *

from kfBios import *



def setupKfWord(params, prefix):
	return [
		DEBUG("----- kfWord -----", '\n'),
		DATA(
			# Word field offsets.
			LABEL("KF_WORD_NAME_LEN_OFFSET"),  Addr(0, KF_WORD_NAME_LEN_OFFSET),
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
			LABEL("KF_MAX_NAME_SIZE"), KF_MAX_NAME_SIZE*2,
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
KF_WORD_NAME_LEN_OFFSET  = 0
KF_WORD_NAME_OFFSET  = KF_WORD_NAME_LEN_OFFSET + 1
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
	chars = MACRO(PackStringData, [name], prefix)
	if chars[-1].addr() == 0:
		chars = chars[:-1]
	chars_len = len(chars)
	if chars_len > KF_MAX_NAME_SIZE:
		raise Exception(f"Name {repr(name)} doesn't fit in {KF_MAX_NAME_SIZE} words.")
	for _ in range(KF_MAX_NAME_SIZE - chars_len):
		chars.append(HEX(0))
	return [
		DEBUG(f"kfWord({repr(name)})"),
		LABEL(prefix),
		DATA(
			# How long the name is (not including \0).
			LABEL(prefix+"_name_len"), chars_len*2,
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



# Class to help with linking words automatically.
class Linker:
	def __init__(self):
		self.prev = 0
	def new(self, name, flags=KF_FLAG_MASK_NONE, code_override=None):
		link = self.prev
		self.prev = name
		code = code_override or f"kfWord_{name}_data"
		#eprint(name, link, flags, code)
		return [
			name,
			link,
			flags,
			code,
		]



# Usage: DATA(*PrintString("hello"))
def PrintString(text):
	return [
		"kfWord_s-quot-c",
		*kopForthAddString(text),
		"kfWord_type",
	]

# Usage: DATA(*kopForthAddString("hello"))
def kopForthAddString(text):
	chars = MACRO(PackStringData, [text], '')
	return [
		len(chars)*2,
		*chars
	]
