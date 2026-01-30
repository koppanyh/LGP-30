#!/usr/bin/env python3

from utils import *
from lgpasm import *

from kfBios import *
from kfStatus import *
from kfStack import *
from kfWord import *



def kfPopulateWordsNative(params, prefix):
	link = params[0]
	return [
		DEBUG("----- kfPopulateWordsNative -----", '\n'),
		DATA(
			LABEL("kfWordsNative_tmpA"), 0,
			LABEL("kfWordsNative_tmpB"), 0,
			LABEL("kfWordsNative_tmpC"), 0,
			LABEL("kfWordsNative_tmpD"), 0,
		),
		#################################################
		MACRO(kfWord, [*link.new(
			"exit",
			KF_FLAG_MASK_NATIVE | KF_FLAG_MASK_COMPILE,
		), []], prefix),
		MACRO(kfStackPop, [r_stack], prefix),
		JMP("rtn_to_kopForthTick"),
		#################################################
		MACRO(kfWord, [*link.new(
			"literal-c",  # (LITERAL)
			KF_FLAG_MASK_NATIVE | KF_FLAG_MASK_COMPILE,
		), []], prefix),
		MACRO(kfStackPop, [r_stack], prefix),
		REP("kfWordsNative_(literal)_lda1"),
		ADD("0001"),
		MACRO(kfStackPush, [r_stack], prefix),
		LABEL("kfWordsNative_(literal)_lda1"), LDA((0, 0)),
		MACRO(kfStackPush, [d_stack], prefix),
		JMP("rtn_to_kopForthTick"),
		#################################################
		MACRO(kfWord, [*link.new(
			"-",
			KF_FLAG_MASK_NATIVE,
		), []], prefix),
		MACRO(kfStackPop, [d_stack], prefix),
		STC("kfWordsNative_tmpB"),
		MACRO(kfStackPop, [d_stack], prefix),
		SUB("kfWordsNative_tmpB"),
		MACRO(kfStackPush, [d_stack], prefix),
		JMP("rtn_to_kopForthTick"),
		#################################################
		MACRO(kfWord, [*link.new(
			".",
			KF_FLAG_MASK_NATIVE,
		), []], prefix),
		MACRO(kfStackPop, [d_stack], prefix),
		MACRO(kfBiosPrintIsize, [], prefix),
		MACRO(HardcodeText, [" "], prefix),
		JMP("rtn_to_kopForthTick"),
		#################################################
		MACRO(kfWord, [*link.new(
			"peek",  # @
			KF_FLAG_MASK_NATIVE,
		), []], prefix),
		MACRO(kfStackPop, [d_stack], prefix),
		REP("kfWord_peek_lda"),
		LABEL("kfWord_peek_lda"), LDA((0, 0)),
		MACRO(kfStackPush, [d_stack], prefix),
		JMP("rtn_to_kopForthTick"),
		#################################################
		MACRO(kfWord, [*link.new(
			"poke",  # !
			KF_FLAG_MASK_NATIVE,
		), []], prefix),
		MACRO(kfStackPop, [d_stack], prefix),
		REP("kfWord_poke_stc"),
		MACRO(kfStackPop, [d_stack], prefix),
		LABEL("kfWord_poke_stc"), STC((0, 0)),
		JMP("rtn_to_kopForthTick"),
		#################################################
		MACRO(kfWord, [*link.new(
			"c-peek",  # C@
			KF_FLAG_MASK_NATIVE,
			"kfWord_peek_data"
		), []], prefix),
		# TODO make this legit, maybe.
		#################################################
		MACRO(kfWord, [*link.new(
			"c-poke",  # C!
			KF_FLAG_MASK_NATIVE,
			"kfWord_poke_data"
		), []], prefix),
		# TODO make this legit, maybe.
		#################################################
		MACRO(kfWord, [*link.new(
			"r-push",  # >R
			KF_FLAG_MASK_NATIVE,
		), []], prefix),
		MACRO(kfStackPop, [r_stack], prefix),
		STC("kfWordsNative_tmpA"),
		MACRO(kfStackPop, [d_stack], prefix),
		MACRO(kfStackPush, [r_stack], prefix),
		LDA("kfWordsNative_tmpA"),
		MACRO(kfStackPush, [r_stack], prefix),
		JMP("rtn_to_kopForthTick"),
		#################################################
		MACRO(kfWord, [*link.new(
			"r-pop",  # R>
			KF_FLAG_MASK_NATIVE,
		), []], prefix),
		MACRO(kfStackPop, [r_stack], prefix),
		STC("kfWordsNative_tmpA"),
		MACRO(kfStackPop, [r_stack], prefix),
		MACRO(kfStackPush, [d_stack], prefix),
		LDA("kfWordsNative_tmpA"),
		MACRO(kfStackPush, [r_stack], prefix),
		JMP("rtn_to_kopForthTick"),
		#################################################
		MACRO(kfWord, [*link.new(
			"drop",
			KF_FLAG_MASK_NATIVE,
		), []], prefix),
		MACRO(kfStackPop, [d_stack], prefix),
		JMP("rtn_to_kopForthTick"),
		#################################################
		MACRO(kfWord, [*link.new(
			"dup",
			KF_FLAG_MASK_NATIVE,
		), []], prefix),
		MACRO(kfStackPop, [d_stack], prefix),
		STA("kfWordsNative_tmpA"),
		MACRO(kfStackPush, [d_stack], prefix),
		LDA("kfWordsNative_tmpA"),
		MACRO(kfStackPush, [d_stack], prefix),
		JMP("rtn_to_kopForthTick"),
		#################################################
		MACRO(kfWord, [*link.new(
			"swap",
			KF_FLAG_MASK_NATIVE,
		), []], prefix),
		MACRO(kfStackPop, [d_stack], prefix),
		STA("kfWordsNative_tmpB"),
		MACRO(kfStackPop, [d_stack], prefix),
		STA("kfWordsNative_tmpA"),
		LDA("kfWordsNative_tmpB"),
		MACRO(kfStackPush, [d_stack], prefix),
		LDA("kfWordsNative_tmpA"),
		MACRO(kfStackPush, [d_stack], prefix),
		JMP("rtn_to_kopForthTick"),
		#################################################
		MACRO(kfWord, [*link.new(
			"branch",
			KF_FLAG_MASK_NATIVE | KF_FLAG_MASK_COMPILE,
		), []], prefix),
		MACRO(kfStackPop, [r_stack], prefix),
		REP("kfWord_branch_lda"),
		LABEL("kfWord_branch_lda"), LDA((0, 0)),
		MACRO(kfStackPush, [r_stack], prefix),
		JMP("rtn_to_kopForthTick"),
		#################################################
		MACRO(kfWord, [*link.new(
			"0branch",
			KF_FLAG_MASK_NATIVE | KF_FLAG_MASK_COMPILE,
		), []], prefix),
		MACRO(kfStackPop, [d_stack], prefix),
		MACRO(EqualsZero, [], prefix),
		BLZ("kfWord_0branch_is0"),
		MACRO(kfStackPop, [r_stack], prefix),
		ADD("0001"),
		MACRO(kfStackPush, [r_stack], prefix),
		JMP("rtn_to_kopForthTick"),
		LABEL("kfWord_0branch_is0"),
		MACRO(kfStackPop, [r_stack], prefix),
		REP("kf_word_0branch_lda"),
		LABEL("kf_word_0branch_lda"), LDA((0, 0)),
		MACRO(kfStackPush, [r_stack], prefix),
		JMP("rtn_to_kopForthTick"),
		#################################################
		MACRO(kfWord, [*link.new(
			"emit",
			KF_FLAG_MASK_NATIVE,
		), []], prefix),
		MACRO(kfStackPop, [d_stack], prefix),
		MACRO(kfBiosWriteChars, [], prefix),
		JMP("rtn_to_kopForthTick"),
		#################################################
		MACRO(kfWord, [*link.new(
			"key",
			KF_FLAG_MASK_NATIVE,
		), []], prefix),
		MACRO(kfBiosReadChars, [], prefix),
		MACRO(kfStackPush, [d_stack], prefix),
		JMP("rtn_to_kopForthTick"),
		#################################################
		MACRO(kfWord, [*link.new(
			"accept",
			KF_FLAG_MASK_NATIVE,
		), []], prefix),
		# Save u1.
		MACRO(kfStackPop, [d_stack], prefix),
		STC("kfWordsNative_tmpA"),
		# Set u2 to 0.
		STC("kfWordsNative_tmpB"),
		# Save addr.
		MACRO(kfStackPop, [d_stack], prefix),
		REP("kfWord_accept_stc"),
		# Start loop.
		LABEL("kfWord_accept_loop"),
		# Break if u2 >= u1
		LDA("kfWordsNative_tmpA"),
		SUB("kfWordsNative_tmpB"),
		MACRO(EqualsZero, [], prefix),
		BLZ("kfWord_accept_break"),
		LDA("kfWordsNative_tmpA"),
		SUB("kfWordsNative_tmpB"),
		BLZ("kfWord_accept_break"),
		# Get chars.
		MACRO(kfBiosReadChars, [], prefix),
		STA("kfWordsNative_tmpC"),
		# Break if chars empty.
		MACRO(EqualsZero, [], prefix),
		BLZ("kfWord_accept_break"),
		# Write chars to addr.
		LDA("kfWordsNative_tmpC"),
		LABEL("kfWord_accept_stc"), STC((0, 0)),
		# Increment addr.
		LDA("kfWord_accept_stc"),
		ADD("0001"),
		REP("kfWord_accept_stc"),
		# Increment u2.
		LDA("kfWordsNative_tmpB"),
		ADD("2"),
		STC("kfWordsNative_tmpB"),
		# End loop.
		JMP("kfWord_accept_loop"),
		LABEL("kfWord_accept_break"),
		# Push u2 and return.
		LDA("kfWordsNative_tmpB"),
		MACRO(kfStackPush, [d_stack], prefix),
		JMP("rtn_to_kopForthTick"),
		#################################################
		MACRO(kfWord, [*link.new(
			"type",
			KF_FLAG_MASK_NATIVE,
		), []], prefix),
		MACRO(kfStackPop, [d_stack], prefix),
		STC("kfBiosWriteStrLen_len"),
		MACRO(kfStackPop, [d_stack], prefix),
		MACRO(kfBiosWriteStrLen, [], prefix),
		JMP("rtn_to_kopForthTick"),
		#################################################
		MACRO(kfWord, [*link.new(
			"create-c",  # (CREATE)
			KF_FLAG_MASK_NATIVE,
		), []], prefix),
		# Set new word addrs.
		LDA("kopForth_here"),
		ADD("KF_WORD_LINK_OFFSET"),
		REP("kfWord_create-c_stc1"),
		LDA("kopForth_here"),
		ADD("KF_WORD_FLAGS_OFFSET"),
		REP("kfWord_create-c_stc3"),
		LDA("kopForth_here"),
		ADD("KF_WORD_CODE_OFFSET"),
		REP("kfWord_create-c_stc2"),
		# Set link.
		LDA("kopForth_pending"),
		LABEL("kfWord_create-c_stc1"), STC((0, 0)),
		# Update latest and pending.
		LDA("kopForth_here"),
		STA("kopForth_pending"),
		STA("kopForth_latest"),
		# Alloc word mem in here.
		ADD("sizeof_kfWord"),
		STA("kopForth_here"),
		# Set code pointer.
		LABEL("kfWord_create-c_stc2"), STC((0, 0)),
		# Clear flags.
		LABEL("kfWord_create-c_stc3"), STC((0, 0)),
		JMP("rtn_to_kopForthTick"),
		#################################################
		MACRO(kfWord, [*link.new(
			"find",
			KF_FLAG_MASK_NATIVE,
		), []], prefix),
		# Pop addr from stack and save ptr and len.
		MACRO(kfStackPop, [d_stack], prefix),
		#ADD("KF_WORD_NAME_LEN_OFFSET"),
		REP("kfWord_find_lda1"),
		#SUB("KF_WORD_NAME_LEN_OFFSET"),
		ADD("KF_WORD_NAME_OFFSET"),
		STC("kfWordsNative_tmpA"),  # c ptr
		LABEL("kfWord_find_lda1"), LDA((0, 0)),
		STA("kfWordsNative_tmpB"),  # len
		SUB("2"),
		BLZ("kfWord_find_not_found"),
		# Init latest addr.
		LDA("kopForth_latest"),
		LABEL("kfWord_find_loop"),
		STA("kfWordsNative_tmpC"),  # latest
		# Get word len.
		#ADD("KF_WORD_NAME_LEN_OFFSET"),
		REP("kfWord_find_lda3"),
		LABEL("kfWord_find_lda3"), LDA((0, 0)),
		STA("kfWordsNative_tmpD"),  # latest len
		STC("Equals_a"),
		LDA("kfWordsNative_tmpB"),
		MACRO(Equals, [], prefix),
		BLZ("kfWord_find_len_eq"),
		JMP("kfWord_find_next"),
		# Load the string addresses.
		LABEL("kfWord_find_len_eq"),
		LDA("kfWordsNative_tmpC"),
		ADD("KF_WORD_NAME_OFFSET"),
		REP("kfWord_find_latest_c_ptr"),
		LDA("kfWordsNative_tmpA"),
		REP("kfWord_find_c_ptr"),
		LABEL("kfWord_find_subloop"),
		# Dec latest len.
		LDA("kfWordsNative_tmpD"),
		SUB("2"),
		BLZ("kfWord_find_found"),
		STC("kfWordsNative_tmpD"),
		# Compare the chars.
		LABEL("kfWord_find_latest_c_ptr"), LDA((0, 0)),
		STC("Equals_a"),
		LABEL("kfWord_find_c_ptr"), LDA((0, 0)),
		MACRO(Equals, [], prefix),
		BLZ("kfWord_find_chars_eq"),
		JMP("kfWord_find_next"),
		LABEL("kfWord_find_chars_eq"),
		# Inc the addrs.
		LDA("kfWord_find_latest_c_ptr"),
		ADD("0001"),
		REP("kfWord_find_latest_c_ptr"),
		LDA("kfWord_find_c_ptr"),
		ADD("0001"),
		REP("kfWord_find_c_ptr"),
		# Subloop.
		JMP("kfWord_find_subloop"),
		# Get next word in the list or return.
		LABEL("kfWord_find_next"),
		LDA("kfWordsNative_tmpC"),
		ADD("KF_WORD_LINK_OFFSET"),
		REP("kfWord_find_lda4"),
		LABEL("kfWord_find_lda4"), LDA((0, 0)),
		BLZ("kfWord_find_not_found"),
		# Loop.
		JMP("kfWord_find_loop"),
		# Return the original addr and 0.
		LABEL("kfWord_find_not_found"),
		LDA("kfWordsNative_tmpA"),
		SUB("0001"),
		MACRO(kfStackPush, [d_stack], prefix),
		CLA(),
		MACRO(kfStackPush, [d_stack], prefix),
		JMP("rtn_to_kopForthTick"),
		# Return the xt and if it's immediate.
		LABEL("kfWord_find_found"),
		LDA("kfWordsNative_tmpC"),
		MACRO(kfStackPush, [d_stack], prefix),
		LDA("kfWordsNative_tmpC"),
		ADD("KF_WORD_FLAGS_OFFSET"),
		REP("kfWord_find_lda2"),
		LABEL("kfWord_find_lda2"), LDA((0, 0)),
		AND("KF_FLAG_MASK_IMMEDIATE"),
		MACRO(EqualsZero, [], prefix),
		BLZ("kfWord_find_not_imm"),
		LDA("2"),
		JMP("kfWord_find_done"),
		LABEL("kfWord_find_not_imm"),
		LDA("-2"),
		LABEL("kfWord_find_done"),
		MACRO(kfStackPush, [d_stack], prefix),
		JMP("rtn_to_kopForthTick"),
		#################################################
		MACRO(kfWord, [*link.new(
			"eq",  # =
			KF_FLAG_MASK_NATIVE,
		), []], prefix),
		MACRO(kfStackPop, [d_stack], prefix),
		STC("kfWordsNative_tmpA"),
		MACRO(kfStackPop, [d_stack], prefix),
		SUB("kfWordsNative_tmpA"),
		MACRO(EqualsZero, [], prefix),
		MACRO(kfStackPush, [d_stack], prefix),
		JMP("rtn_to_kopForthTick"),
		#################################################
		MACRO(kfWord, [*link.new(
			"lss",  # <
			KF_FLAG_MASK_NATIVE,
		), []], prefix),
		MACRO(kfStackPop, [d_stack], prefix),
		STC("kfWordsNative_tmpB"),
		MACRO(kfStackPop, [d_stack], prefix),
		SUB("kfWordsNative_tmpB"),
		BLZ("kfWord_lss_isless"),
		CLA(),
		JMP("kfWord_lss_push"),
		LABEL("kfWord_lss_isless"),
		LDA("-2"),
		LABEL("kfWord_lss_push"),
		MACRO(kfStackPush, [d_stack], prefix),
		JMP("rtn_to_kopForthTick"),
		#################################################
		MACRO(kfWord, [*link.new(
			"nand",
		), [
			"kfWord_and",
			"kfWord_invert",
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"s-quot-c",  # (S")
			KF_FLAG_MASK_NATIVE | KF_FLAG_MASK_COMPILE,
		), []], prefix),
		# Get string length.
		MACRO(kfStackPop, [r_stack], prefix),
		STA("kfWordsNative_tmpA"),
		REP("kfWord_s-quot-c_lda1"),
		LABEL("kfWord_s-quot-c_lda1"), LDA((0, 0)),
		STA("kfWordsNative_tmpB"),
		# Recalculate return addr.
		ADD("2"),
		LSL(1),
		ADD("kfWordsNative_tmpA"),
		MACRO(kfStackPush, [r_stack], prefix),
		# Push string addr.
		LDA("kfWordsNative_tmpA"),
		ADD("4"),
		MACRO(kfStackPush, [d_stack], prefix),
		# Push string length.
		LDA("kfWordsNative_tmpB"),
		MACRO(kfStackPush, [d_stack], prefix),
		JMP("rtn_to_kopForthTick"),
		#################################################
		MACRO(kfWord, [*link.new(
			".s",
			KF_FLAG_MASK_NATIVE,
		), []], prefix),
		MACRO(kfStackPrint, [d_stack], prefix),
		JMP("rtn_to_kopForthTick"),
		#################################################
		MACRO(kfWord, [*link.new(
			"dump",
			KF_FLAG_MASK_NATIVE,
		), []], prefix),
		# TODO
		MACRO(kfStackPop, [d_stack], prefix),
		STC("kfBiosDumpMem_u"),
		MACRO(kfStackPop, [d_stack], prefix),
		MACRO(kfBiosDumpMem, [], prefix),
		JMP("rtn_to_kopForthTick"),
		#################################################
		MACRO(kfWord, [*link.new(
			"clr-in-source",  # (CLR-IN-SOURCE)
			KF_FLAG_MASK_NATIVE,
		), []], prefix),
		CLA(),
		STA("kopForth_in_src_source_id"),
		STA("kopForth_in_src_in_offset"),
		STA("kopForth_in_src_in_len"),
		LDA("kopForth_in_buf_ptr"),
		STC("kopForth_in_src_buf"),
		JMP("rtn_to_kopForthTick"),
		#################################################
		MACRO(kfWord, [*link.new(
			"clr-ret-stack",  # (CLR-RET-STACK)
			KF_FLAG_MASK_NATIVE,
		), []], prefix),
		MACRO(kfStackPop, [r_stack], prefix),
		STA("kfWordsNative_tmpA"),
		MACRO(kfStackReset, [r_stack], prefix),
		LDA("kfWordsNative_tmpA"),
		MACRO(kfStackPush, [r_stack], prefix),
		JMP("rtn_to_kopForthTick"),
		#################################################
		MACRO(kfWord, [*link.new(
			"clr-dat-stack",  # (CLR-DAT-STACK)
			KF_FLAG_MASK_NATIVE,
		), []], prefix),
		MACRO(kfStackReset, [d_stack], prefix),
		JMP("rtn_to_kopForthTick"),
		
		###############################
		# Custom words for the LGP-30 #
		###############################
		
		#################################################
		MACRO(kfWord, [*link.new(
			"err-not-imp",
			KF_FLAG_MASK_NATIVE,
		), []], prefix),
		MACRO(kfStatusErr, ["KF_SYSTEM_NOT_IMP"], prefix),
		JMP("rtn_to_kopForthTick"),
		#################################################
		MACRO(kfWord, [*link.new(
			"err-name-long",
			KF_FLAG_MASK_NATIVE,
		), []], prefix),
		MACRO(kfStatusErr, ["KF_NAME_TOO_LONG"], prefix),
		JMP("rtn_to_kopForthTick"),
		#################################################
		MACRO(kfWord, [*link.new(
			"num2addr",
			KF_FLAG_MASK_NATIVE,
		), []], prefix),
		MACRO(kfStackPop, [d_stack], prefix),
		LSL(1),
		MACRO(kfStackPush, [d_stack], prefix),
		JMP("rtn_to_kopForthTick"),
		#################################################
		MACRO(kfWord, [*link.new(
			"addr2num",
			KF_FLAG_MASK_NATIVE,
		), []], prefix),
		MACRO(kfStackPop, [d_stack], prefix),
		LSR(1),
		MACRO(kfStackPush, [d_stack], prefix),
		JMP("rtn_to_kopForthTick"),
		#################################################
		MACRO(kfWord, [*link.new(
			"halt",
			KF_FLAG_MASK_NATIVE,
		), []], prefix),
		HLT(),
		JMP("rtn_to_kopForthTick"),
		#################################################
		MACRO(kfWord, [*link.new(
			"nodebug",
			KF_FLAG_MASK_NATIVE,
		), []], prefix),
		CLA(),
		STC("kopForth_debug"),
		JMP("rtn_to_kopForthTick"),
		#################################################
		MACRO(kfWord, [*link.new(
			"yesdebug",
			KF_FLAG_MASK_NATIVE,
		), []], prefix),
		LDA("-2"),
		STC("kopForth_debug"),
		JMP("rtn_to_kopForthTick"),
	]
