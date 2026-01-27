#!/usr/bin/env python3

from utils import *
from lgpasm import *

from kfStack import *
from kfWord import *



def kfPopulateWordsString(params, prefix):
	link = params[0]
	return [
		DEBUG("----- kfPopulateWordsString -----", '\n'),
		
		#################################################
		MACRO(kfWord, [*link.new(
			"cr",
		), [
			"kfWord_literal-c", 0b010000_00,
			"kfWord_emit",
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"bl",
		), [
			"kfWord_literal-c", 0b000011_00,
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"space",
		), [
			"kfWord_bl",
			"kfWord_emit",
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"count",
		), [
			"kfWord_dup",
			"kfWord_literal-c", Addr(0, 1),
			"kfWord_+",
			"kfWord_swap",
			"kfWord_c-peek",
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"/string",
		), [
			"kfWord_dup",
			"kfWord_r-push",
			"kfWord_num2addr",
			"kfWord_r-push",
			"kfWord_swap",
			"kfWord_r-pop",
			"kfWord_+",
			"kfWord_swap",
			"kfWord_r-pop",
			"kfWord_-",
			"kfWord_dup",
			"kfWord_literal-c", 0,
			"kfWord_lss",
			"kfWord_0branch", LabAddr("kfWord_/string_b01"),
			"kfWord_num2addr",
			"kfWord_+",
			"kfWord_literal-c", 0,
			LABEL("kfWord_/string_b01"),
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"xt-skip",
		), [
			"kfWord_r-push",
			LABEL("kfWord_xt-skip_b00"),
			"kfWord_dup",
			"kfWord_0branch", LabAddr("kfWord_xt-skip_b03"),
			"kfWord_over",
			"kfWord_c-peek",
			"kfWord_r-peek",
			"kfWord_execute",
			"kfWord_branch", LabAddr("kfWord_xt-skip_b04"),
			LABEL("kfWord_xt-skip_b03"),
			"kfWord_false",
			LABEL("kfWord_xt-skip_b04"),
			"kfWord_0branch", LabAddr("kfWord_xt-skip_b07"),
			"kfWord_literal-c", 1*2,
			"kfWord_/string",
			"kfWord_branch", LabAddr("kfWord_xt-skip_b00"),
			LABEL("kfWord_xt-skip_b07"),
			"kfWord_r-pop",
			"kfWord_drop",
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"spread-chars",  # ( packed_chars a -- u )
			KF_FLAG_MASK_NATIVE,
		),[]], prefix),
		# Pop dest addr.
		MACRO(kfStackPop, [d_stack], prefix),
		REP("kfWord_spread-chars_stc"),
		# Pop packed chars.
		MACRO(kfStackPop, [d_stack], prefix),
		STC("kfWordsNative_tmpA"),
		# Set u to 0.
		CLA(),
		STC("kfWordsNative_tmpB"),
		LABEL("kfWord_spread-chars_loop"),
		# Break if chars empty.
		LDA("kfWordsNative_tmpA"),
		MACRO(EqualsZero, [], prefix),
		BLZ("kfWord_spread-chars_retn"),
		# Extract next char.
		# aaaaaa bbbbbb cccccc dddddd eeeeee 00
		LDA("kfWordsNative_tmpA"),
		LSR(18),
		AND("kfBiosTrackMask"),
		LSR(7),
		STC("kfWordsNative_tmpC"),
		# Shift packed chars.
		LDA("kfWordsNative_tmpA"),
		LSL(6),
		STC("kfWordsNative_tmpA"),
		# Loop if char is empty.
		LDA("kfWordsNative_tmpC"),
		MACRO(EqualsZero, [], prefix),
		BLZ("kfWord_spread-chars_loop"),
		# Write char to addr.
		LDA("kfWordsNative_tmpC"),
		LABEL("kfWord_spread-chars_stc"), STC((0, 0)),
		# Inc addr.
		LDA("kfWord_spread-chars_stc"),
		ADD("0001"),
		REP("kfWord_spread-chars_stc"),
		# Inc u.
		LDA("kfWordsNative_tmpB"),
		ADD("2"),
		STC("kfWordsNative_tmpB"),
		# Loop.
		JMP("kfWord_spread-chars_loop"),
		# Return u.
		LABEL("kfWord_spread-chars_retn"),
		LDA("kfWordsNative_tmpB"),
		MACRO(kfStackPush, [d_stack], prefix),
		JMP("rtn_to_kopForthTick"),
		#################################################
		MACRO(kfWord, [*link.new(
			"is-digit",  # DIGIT?  ( n1 -- n2 -1 | 0 )
		), [
			# Break if we're not ending in 0b10.
			"kfWord_dup",
			"kfWord_literal-c", 0b11_0,
			"kfWord_and",
			"kfWord_literal-c", 0b10_0,
			"kfWord_eq",  # ( n1 f )
			"kfWord_0branch", LabAddr("kfWord_is-digit_nope"),
			# Shift 2 right.
			"kfWord_literal-c", 2*2,
			"kfWord_rshift",  # ( n2 )
			# Check if less than 10.
			"kfWord_dup",
			"kfWord_literal-c", 10*2,
			"kfWord_lss",  # ( n2 f )
			# Break if not.
			"kfWord_0branch", LabAddr("kfWord_is-digit_nope"),
			# Return true.
			"kfWord_true",  # ( n2 -1 )
			"kfWord_exit",
			# Return false.
			LABEL("kfWord_is-digit_nope"),
			"kfWord_drop",
			"kfWord_literal-c", 0,  # ( 0 )
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"10*",
			KF_FLAG_MASK_NATIVE,
		), []], prefix),
		MACRO(kfStackPop, [d_stack], prefix),
		LSL(4),
		MUP("10q4"),
		MACRO(kfStackPush, [d_stack], prefix),
		JMP("rtn_to_kopForthTick"),
		#################################################
		MACRO(kfWord, [*link.new(
			"to-number",  # >NUMBER  ( u0 a1 u1 -- u3 a2 u2 )
		), [
			LABEL("kfWord_to-number_b00"),
			"kfWord_dup",
			"kfWord_0eq",
			"kfWord_0branch", LabAddr("kfWord_to-number_b02"),
			"kfWord_exit",
			LABEL("kfWord_to-number_b02"),
			"kfWord_over",
			"kfWord_c-peek",
			"kfWord_is-digit",
			"kfWord_0branch", LabAddr("kfWord_to-number_b05"),
			"kfWord_swap",
			"kfWord_literal-c", 1*2,
			"kfWord_-",
			"kfWord_r-push",
			"kfWord_swap",
			"kfWord_literal-c", Addr(0, 1),
			"kfWord_+",
			"kfWord_r-push",
			"kfWord_r-push",
			"kfWord_10*",
			"kfWord_r-pop",
			"kfWord_+",
			"kfWord_r-pop",
			"kfWord_r-pop",
			"kfWord_branch", LabAddr("kfWord_to-number_b00"),
			LABEL("kfWord_to-number_b05"),
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"s-to-number",  # S>NUMBER?  ( a1 u1 -- n 0 0 | a2 u2 )
		), [
			# Check if first char is '-'.
			"kfWord_over",
			"kfWord_peek",
			"kfWord_pad",
			"kfWord_spread-chars",  # ( a1 u1 n )
			"kfWord_pad",
			"kfWord_peek",
			"kfWord_literal-c", 0b000111_0,
			"kfWord_eq",
			"kfWord_0branch", LabAddr("kfWord_s-to-number_pos"),
			# ... negative condition.
			"kfWord_literal-c", -1*2,
			"kfWord_branch", LabAddr("kfWord_s-to-number_end_check"),
			# ... positive condition.
			LABEL("kfWord_s-to-number_pos"),
			"kfWord_literal-c", 0,
			LABEL("kfWord_s-to-number_end_check"),
			"kfWord_r-push",  # ( a1 u1 n ) [ -1|0 ]
			# Turn into adjusted ( u0 a1 u1 ) format for >number.
			"kfWord_literal-c", 0,
			"kfWord_swap",
			"kfWord_r-peek",
			"kfWord_+",  # ( a1 u1 0 u2 )
			"kfWord_pad",
			"kfWord_r-peek",
			"kfWord_num2addr",
			"kfWord_-",
			LABEL("kfWord_s-to-number_process"),
			"kfWord_swap",  # ( a1 u1 0 a2 u2 ) [ -1|0 ]
			# Process into number.
			"kfWord_to-number",  # ( a1 u1 u3 a2 u2 ) [ -1|0 ]
			"kfWord_0branch", LabAddr("kfWord_s-to-number_continue"),
			"kfWord_branch", LabAddr("kfWord_s-to-number_failed"),
			LABEL("kfWord_s-to-number_continue"),
			# Inc a1 and dec u2.
			"kfWord_drop",  # ( a1 u1 u3 ) [ -1|0 ]
			"kfWord_r-push",
			"kfWord_swap",
			"kfWord_literal-c", Addr(0, 1),
			"kfWord_+",
			"kfWord_swap",
			"kfWord_literal-c", 1*2,
			"kfWord_-",  # ( a1 u1 ) [ -1|0 u3 ]
			# Finalize if u1 is 0.
			"kfWord_dup",
			"kfWord_0branch", LabAddr("kfWord_s-to-number_finalize"),
			# Otherwise load next chars and loop.
			"kfWord_over",
			"kfWord_r-pop",  # ( a1 u1 a1 u3 ) [ -1|0 ]
			"kfWord_swap",
			"kfWord_peek",
			"kfWord_pad",
			"kfWord_spread-chars",
			"kfWord_pad",  # ( a1 u1 u3 n a2 ) [ -1|0 ]
			"kfWord_branch", LabAddr("kfWord_s-to-number_process"),
			LABEL("kfWord_s-to-number_finalize"),
			# Apply the negative if necessary.
			"kfWord_drop",
			"kfWord_drop",
			"kfWord_r-pop",
			"kfWord_r-pop",  # ( u3 -1|0 )
			"kfWord_0branch", LabAddr("kfWord_s-to-number_rtn"),
			"kfWord_literal-c", 0,
			"kfWord_swap",
			"kfWord_-",
			LABEL("kfWord_s-to-number_rtn"),
			# Return in the expected format.
			"kfWord_literal-c", 0,
			"kfWord_dup",  # ( u3 0 0 )
			"kfWord_exit",
			LABEL("kfWord_s-to-number_failed"),
			# Clear the working data, return failed address.
			"kfWord_r-pop",
			"kfWord_drop",
			"kfWord_drop",
			"kfWord_drop",  # ( a1 u1 )
			"kfWord_exit"
		]], prefix),
	]
