#!/usr/bin/env python3

from datetime import datetime
from utils import *
from lgpasm import *



################
# BIOS Params ##
################

#
# Versioning params.
#

KF_VER_MAJOR = 0
KF_VER_MINOR = 3
KF_VER_PATCH = 0
KF_YEAR_STR  = "2025"

KF_VER_STR = f"v{KF_VER_MAJOR}.{KF_VER_MINOR}.{KF_VER_PATCH}"

#
# Memory allocation params.
#

# How many items to allocate for the data stack.
KF_DATA_STACK_SIZE = 32
# How many items to allocate for the return stack.
KF_RETN_STACK_SIZE = 32
# How many cells to allocate for the input buffer.
KF_IN_BUF_SIZE     = 32
# How many cells to allocate for the working memory (plus word definitions).
KF_MEM_SIZE        = 2048 + 1024 + 64
# How many cells to allocate for the names of words (including \0).
KF_MAX_NAME_SIZE   = 3

#
# Terminal params.
#

# The character to use for newline (terminal output).
KF_NL = '\n'



def setupKfBios(params, prefix):
	return [
		DEBUG("----- kfBios -----", '\n'),
		DEBUG("BIOS Constants"),
		DATA(
			LABEL("kfBiosTrackMask"), 0b_111111_000000_00,
			LABEL("kfBiosSectorMask"), 0b_000000_111111_00,
			LABEL("kfBiosTerminatorMask"), 0b_111111_000000_000000_000000_000000_00,
			LABEL("TRK10"), 0b_001010_000000_00,
			LABEL("SEC10"), 0b_000000_001010_00,
			LABEL("10q4"), 0b0_10100000000_0000_00_000000_000000_00,
		),
		LABEL("kfBiosSetup_str"), MACRO(PackString, [
			f"kopForth {KF_VER_STR}, 31 Bit, LGP-30 Edition\n" +
			f"Copyright {KF_YEAR_STR}, compiled {datetime.now().date()}\n"
		], prefix),
		LABEL("kfBiosSetup_str_ptr"), LabAddr("kfBiosSetup_str"),
		MACRO(defKfBiosPrintIsize,       [], prefix),
		MACRO(defKfBiosPrintPointer,     [], prefix),
		MACRO(defKfBiosWriteChar,        [], prefix),
		MACRO(defKfBiosWriteChars,       [], prefix),
		MACRO(defKfBiosReadChars,        [], prefix),
		MACRO(defKfBiosWriteStr,         [], prefix),
		MACRO(defKfBiosWriteStrLen,      [], prefix),
		MACRO(defKfBiosWriteStrUnpacked, [], prefix),
		MACRO(defKfBiosDumpMem,          [], prefix),
	]



####################
# BIOS Terminal IO #
####################

# Print the 31 bit signed int held in the acc.
# Usage: MACRO(kfBiosPrintIsize)
# NOTE: Breaks for numbers >= 10q4 or <= than negative of that.
def kfBiosPrintIsize(params, prefix):
	return [
		DEBUG("kfBiosPrintIsize()"),
		RTA("kfBiosPrintIsize_rtn"),
		JMP("kfBiosPrintIsize"),
	]
def defKfBiosPrintIsize(params, prefix):
	return [
		DEBUG("defKfBiosPrintIsize"),
		LABEL("kfBiosPrintIsize"),
		# If it's negative, negate and print '-'.
		BLZ("kfBiosPrintIsize_prtneg"),
		JMP("kfBiosPrintIsize_init"),
		LABEL("kfBiosPrintIsize_prtneg"),
		NEG(),
		MACRO(HardcodeText, ["-"], prefix),
		LABEL("kfBiosPrintIsize_init"),
		# Save the positive version and reset the string pointer.
		STC("kfBiosPrintIsize_posval"),
		LDA("kfBiosPrintIsize_lastchar_ptr"),
		REP("kfBiosPrintIsize_lcr"),
		# Start of the stringify loop.
		LABEL("kfBiosPrintIsize_stringify"),
		LDA("kfBiosPrintIsize_posval"),
		# divval = int(posval / 10)
		DIV("10q4"),
		LSR(4),
		STA("kfBiosPrintIsize_divval"),
		# acc = -((divval * 10) - posval)
		LSL(4),
		MUP("10q4"),
		SUB("kfBiosPrintIsize_posval"),
		NEG(),
		# Turn number into char and save into string.
		LSL(9),
		ADD("512"),
		LABEL("kfBiosPrintIsize_lcr"), REP("kfBiosPrintIsize_lastchar"),
		# Exit stringify loop if done.
		LDA("kfBiosPrintIsize_divval"),
		SUB("2"),
		BLZ("kfBiosPrintIsize_print"),
		# Otherwise posval = divval.
		LDA("kfBiosPrintIsize_divval"),
		STC("kfBiosPrintIsize_posval"),
		# Decrement string pointer and loop.
		LDA("kfBiosPrintIsize_lcr"),
		SUB("0001"),
		REP("kfBiosPrintIsize_lcr"),
		JMP("kfBiosPrintIsize_stringify"),
		LABEL("kfBiosPrintIsize_print"),
		# Print the string.
		LDA("kfBiosPrintIsize_lcr"),
		MACRO(kfBiosWriteStrUnpacked, [], prefix),
		LABEL("kfBiosPrintIsize_rtn"), JMP((0, 0)),
		# Vars.
		LABEL("kfBiosPrintIsize_posval"), HLT(),
		LABEL("kfBiosPrintIsize_divval"), HLT(),
		DATA(  # Unpacked string storage.
			0, 0, 0, 0, 0, 0, 0, 0, 0,
			LABEL("kfBiosPrintIsize_lastchar"), 0,
			0,  # Unpacked string terminator.
			LABEL("kfBiosPrintIsize_lastchar_ptr"), LabAddr("kfBiosPrintIsize_lastchar"),
		),
	]

# Print the pointer held in the acc in the ttss format.
# Usage: MACRO(kfBiosPrintPointer)
def kfBiosPrintPointer(params, prefix):
	return [
		DEBUG("kfBiosPrintPointer()"),
		RTA("kfBiosPrintPointer_rtn"),
		JMP("kfBiosPrintPointer"),
	]
def defKfBiosPrintPointer(params, prefix):
	return [
		DEBUG("defKfBiosPrintPointer"),
		LABEL("kfBiosPrintPointer"),
		# Save pointer and print '$'.
		REP("kfBiosPrintPointer_ptr"),
		MACRO(HardcodeText, ["\x0f6\x0e"], prefix),
		# Extract track.
		AND("kfBiosTrackMask"),
		# If <10, print 0.
		SUB("TRK10"),
		BLZ("kfBiosPrintPointer_p01"),
		JMP("kfBiosPrintPointer_ptk"),
		LABEL("kfBiosPrintPointer_p01"),
		MACRO(HardcodeText, ["0"], prefix),
		LABEL("kfBiosPrintPointer_ptk"),
		ADD("TRK10"),
		# Print track.
		LSR(7),
		MACRO(kfBiosPrintIsize, [], prefix),
		# Extract sector.
		LDA("kfBiosPrintPointer_ptr"),
		AND("kfBiosSectorMask"),
		# If <10, print 0.
		SUB("SEC10"),
		BLZ("kfBiosPrintPointer_p02"),
		JMP("kfBiosPrintPointer_psc"),
		LABEL("kfBiosPrintPointer_p02"),
		MACRO(HardcodeText, ["0"], prefix),
		LABEL("kfBiosPrintPointer_psc"),
		ADD("SEC10"),
		# Print sector.
		LSR(1),
		MACRO(kfBiosPrintIsize, [], prefix),
		LABEL("kfBiosPrintPointer_rtn"), JMP((0, 0)),
		# Vars.
		LABEL("kfBiosPrintPointer_ptr"), HLT(),
	]

# Print a character from acc.
# Character code must be in track bits of acc.
# Usage: LABEL("a_char"),        # Load character 'a' into acc.
#        CharLit("a").print(),
#        LDA("a_char"),
#        MACRO(kfBiosWriteChar)  # Call the subroutine
def kfBiosWriteChar(params, prefix):
	return [
		DEBUG("kfBiosWriteChar()"),
		RTA("kfBiosWriteChar_rtn"),
		JMP("kfBiosWriteChar"),
	]
def defKfBiosWriteChar(params, prefix):
	return [
		DEBUG("defKfBiosWriteChar"),
		LABEL("kfBiosWriteChar"),
		# Mask the input.
		AND("kfBiosTrackMask"),
		REP("kfBiosWriteChar_prt"),
		# Check that it's not 0.
		SUB("2"),
		BLZ("kfBiosWriteChar_rtn"),
		# Print.
		LABEL("kfBiosWriteChar_prt"), PRT((0, 0)),
		HLT(),
		LABEL("kfBiosWriteChar_rtn"), JMP((0, 0)),
	]

# Print a word-packed string from acc.
# Five characters encoded as: 0b_aaaaaa_bbbbbb_cccccc_dddddd_eeeeee_00
# Usage: LABEL("chars"),          # Load characters 'abcde' into acc.
#        DATA(0b_111001_000101_110101_010101_100101_00),
#        LDA("chars"),
#        MACRO(kfBiosWriteChars)  # Call the subroutine
def kfBiosWriteChars(params, prefix):
	return [
		DEBUG("kfBiosWriteChars()"),
		RTA("kfBiosWriteChars_rtn"),
		JMP("kfBiosWriteChars"),
	]
def defKfBiosWriteChars(params, prefix):
	return [
		DEBUG("defKfBiosWriteChars"),
		LABEL("kfBiosWriteChars"),
		# Save the chars to temp variable.
		STA("kfBiosWriteChars_var1"),
		# Extract 1st char and print.
		LSR(18),
		MACRO(kfBiosWriteChar, [], prefix),
		# Extract 2nd char and print.
		LDA("kfBiosWriteChars_var1"),
		LSR(12),
		MACRO(kfBiosWriteChar, [], prefix),
		# Extract 3rd char and print.
		LDA("kfBiosWriteChars_var1"),
		LSR(6),
		MACRO(kfBiosWriteChar, [], prefix),
		# Extract 4th char and print.
		LDA("kfBiosWriteChars_var1"),
		MACRO(kfBiosWriteChar, [], prefix),
		# Extract 5th char and print.
		LDA("kfBiosWriteChars_var1"),
		LSL(6),
		MACRO(kfBiosWriteChar, [], prefix),
		LABEL("kfBiosWriteChars_rtn"), JMP((0, 0)),
		# Vars.
		LABEL("kfBiosWriteChars_var1"), HLT(),
	]

# Print a newline character.
# Usage: MACRO(kfBiosCR)
def kfBiosCR(params, prefix):
	return [
		DEBUG("kfBiosCR()"),
		CharLit(KF_NL).print(),
		HLT(),
	]

# Read a word-packed string to acc.
# Must not surpass 5 characters as input.
# Up to five characters encoded as: 0b_aaaaaa_bbbbbb_cccccc_dddddd_eeeeee_00
# Usage: MACRO(kfBiosReadChars)
def kfBiosReadChars(params, prefix):
	return [
		DEBUG("kfBiosReadChars()"),
		RTA("kfBiosReadChars_rtn"),
		JMP("kfBiosReadChars"),
	]
def defKfBiosReadChars(params, prefix):
	return [
		DEBUG("defKfBiosReadChars"),
		LABEL("kfBiosReadChars"),
		# Read and shift.
		CLA(),
		PRT((0, 0)),
		INP(),
		LSL(2),
		LABEL("kfBiosReadChars_rtn"), JMP((0, 0)),
	]

# Print the word-packed string being pointed to by the acc.
# String must end with \0 on the last word.
# Usage: LDA("pointer-to-string-pointer"),
#        MACRO(kfBiosWriteStr)
def kfBiosWriteStr(params, prefix):
	return [
		DEBUG("kfBiosWriteStr()"),
		RTA("kfBiosWriteStr_rtn"),
		JMP("kfBiosWriteStr"),
	]
def defKfBiosWriteStr(params, prefix):
	return [
		DEBUG("defKfBiosWriteStr"),
		LABEL("kfBiosWriteStr"),
		# Save the ptr.
		REP("kfBiosWriteStr_lda1"),
		REP("kfBiosWriteStr_lda2"),
		# Load chars and print them.
		LABEL("kfBiosWriteStr_lda1"), LDA((0, 0)),
		MACRO(kfBiosWriteChars, [], prefix),
		# Load chars and exit if they end with \0.
		LABEL("kfBiosWriteStr_lda2"), LDA((0, 0)),
		AND("kfBiosTerminatorMask"),
		MACRO(EqualsZero, [], prefix),
		BLZ("kfBiosWriteStr_rtn"),
		# Increment address and loop.
		LDA("kfBiosWriteStr_lda1"),
		ADD("0001"),
		JMP("kfBiosWriteStr"),
		LABEL("kfBiosWriteStr_rtn"), JMP((0, 0)),
	]

# Print the word-packed string being pointed to by the acc.
# The amount of words to print is passed in as a parameter.
# Acc should hold n*2 because of dead bit.
# Usage: LDA("str-len"),
#        STC("kfBiosWriteStrLen_len"),
#        LDA("pointer-to-string-pointer"),
#        MACRO(kfBiosWriteStrLen)
def kfBiosWriteStrLen(params, prefix):
	return [
		DEBUG("kfBiosWriteStrLen()"),
		RTA("kfBiosWriteStrLen_rtn"),
		JMP("kfBiosWriteStrLen"),
	]
def defKfBiosWriteStrLen(params, prefix):
	return [
		DEBUG("defKfBiosWriteStrLen"),
		LABEL("kfBiosWriteStrLen"),
		# Save the string ptr.
		REP("kfBiosWriteStrLen_ptr"),
		# Decrement and exit if len is <=0.
		LDA("kfBiosWriteStrLen_len"),
		SUB("2"),
		STA("kfBiosWriteStrLen_len"),
		BLZ("kfBiosWriteStrLen_rtn"),
		# Load chars and print.
		LABEL("kfBiosWriteStrLen_ptr"), LDA((0, 0)),
		MACRO(kfBiosWriteChars, [], prefix),
		# Increment string ptr and loop.
		LDA("kfBiosWriteStrLen_ptr"),
		ADD("0001"),
		JMP("kfBiosWriteStrLen"),
		LABEL("kfBiosWriteStrLen_rtn"), JMP((0, 0)),
		# Vars.
		LABEL("kfBiosWriteStrLen_len"), HLT(),
	]

# Print the unpacked string (every char is a whole word) being pointed to by the acc.
# String must end with \0 on the last word.
# Usage: LDA("pointer-to-string-pointer"),
#        MACRO(kfBiosWriteStrUnpacked)
def kfBiosWriteStrUnpacked(params, prefix):
	return [
		DEBUG("kfBiosWriteStrUnpacked()"),
		RTA("kfBiosWriteStrUnpacked_rtn"),
		JMP("kfBiosWriteStrUnpacked"),
	]
def defKfBiosWriteStrUnpacked(params, prefix):
	return [
		DEBUG("defKfBiosWriteStrUnpacked"),
		LABEL("kfBiosWriteStrUnpacked"),
		# Save the ptr.
		REP("kfBiosWriteStrUnpacked_lda"),
		# Load char and prepare to print.
		LABEL("kfBiosWriteStrUnpacked_lda"), LDA((0, 0)),
		AND("kfBiosTrackMask"),
		REP("kfBiosWriteStrUnpacked_prt"),
		# If it's zero, return early.
		SUB("0100"),
		BLZ("kfBiosWriteStrUnpacked_rtn"),
		# Otherwise, print it.
		LABEL("kfBiosWriteStrUnpacked_prt"), PRT((0, 0)),
		HLT(),
		# Increment the ptr and loop.
		LDA("kfBiosWriteStrUnpacked_lda"),
		ADD("0001"),
		JMP("kfBiosWriteStrUnpacked"),
		LABEL("kfBiosWriteStrUnpacked_rtn"), JMP((0, 0)),
	]

# Set up the bios.
# Usage: MACRO(kfBiosSetup)
def kfBiosSetup(params, prefix):
	return [
		DEBUG("kfBiosSetup()"),
		LABEL("kfBiosSetup"),
		# Intro credits.
		LDA("kfBiosSetup_str_ptr"),
		MACRO(kfBiosWriteStr, [], prefix),
	]



##############
# BIOS Debug #
##############

# Dump a section of memory for debugging.
# Usage: LDA("u"),
#        STC("kfBiosDumpMem_u"),
#        LDA("addr"),
#        MACRO(kfBiosDumpMem)
def kfBiosDumpMem(params, prefix):
	return [
		DEBUG("kfBiosDumpMem()"),
		RTA("kfBiosDumpMem_rtn"),
		JMP("kfBiosDumpMem"),
	]
def defKfBiosDumpMem(params, prefix):
	return [
		DEBUG("defKfBiosWriteChars"),
		LABEL("kfBiosDumpMem"),
		# Store pointer and reset interval.
		REP("kfBiosDumpMem_ptr"),
		CLA(),
		STC("kfBiosDumpMem_intv"),
		LABEL("kfBiosDumpMem_loop"),
		# Break if u is 0.
		LDA("kfBiosDumpMem_u"),
		SUB("2"),
		BLZ("kfBiosDumpMem_brk"),
		STC("kfBiosDumpMem_u"),
		# Decrement intv.
		LDA("kfBiosDumpMem_intv"),
		SUB("2"),
		BLZ("kfBiosDumpMem_nl"),
		STC("kfBiosDumpMem_intv"),
		JMP("kfBiosDumpMem_prchr"),
		# Print newline and line header and reset intv.
		LABEL("kfBiosDumpMem_nl"),
		MACRO(kfBiosCR, [], prefix),
		LDA("kfBiosDumpMem_ptr"),
		MACRO(kfBiosPrintPointer, [], prefix),
		MACRO(HardcodeText, [" "], prefix),
		LDA("14"),  # set to 7 so it prints 8
		STC("kfBiosDumpMem_intv"),
		# Print the value at ptr and inc ptr.
		LABEL("kfBiosDumpMem_prchr"),
		LABEL("kfBiosDumpMem_ptr"), LDA((0, 0)),
		MACRO(kfBiosPrintIsize, [], prefix),
		MACRO(HardcodeText, [" "], prefix),
		LDA("kfBiosDumpMem_ptr"),
		ADD("0001"),
		STC("kfBiosDumpMem_ptr"),
		# Loop.
		JMP("kfBiosDumpMem_loop"),
		# Print newline and return.
		LABEL("kfBiosDumpMem_brk"),
		MACRO(kfBiosCR, [], prefix),
		LABEL("kfBiosDumpMem_rtn"), JMP((0, 0)),
		# Vars.
		LABEL("kfBiosDumpMem_u"), HLT(),
		LABEL("kfBiosDumpMem_intv"), HLT(),
	]
