#!/usr/bin/env python3

from utils import *
from lgpasm import *

from kfWord import *
from kfStack import *



def kfPopulateWordsStackMem(params, prefix):
	link = params[0]
	return [
		DEBUG("----- kfPopulateWordsStackMem -----", '\n'),
		
		####################################
		# Stack manipulators and operators #
		####################################
		#################################################
		MACRO(kfWord, [*link.new(
			"over",
		), [
			"kfWord_r-push",
			"kfWord_dup",
			"kfWord_r-pop",
			"kfWord_swap",
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"rot",
		), [
			"kfWord_r-push",
			"kfWord_swap",
			"kfWord_r-pop",
			"kfWord_swap",
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"2drop",
		), [
			"kfWord_drop",
			"kfWord_drop",
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"2dup",
		), [
			"kfWord_over",
			"kfWord_over",
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"+",
		), [
			"kfWord_literal-c", 0,
			"kfWord_swap",
			"kfWord_-",
			"kfWord_-",
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"invert",
			KF_FLAG_MASK_NATIVE,
		),[]], prefix),
		MACRO(kfStackPop, [d_stack], prefix),
		NEG(),
		SUB("2"),
		MACRO(kfStackPush, [d_stack], prefix),
		JMP("rtn_to_kopForthTick"),
		#################################################
		MACRO(kfWord, [*link.new(
			"or",
		), [
			"kfWord_invert",
			"kfWord_swap",
			"kfWord_invert",
			"kfWord_nand",
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"and",
			KF_FLAG_MASK_NATIVE,
		),[]], prefix),
		MACRO(kfStackPop, [d_stack], prefix),
		STC("kfWordsNative_tmpB"),
		MACRO(kfStackPop, [d_stack], prefix),
		AND("kfWordsNative_tmpB"),
		MACRO(kfStackPush, [d_stack], prefix),
		JMP("rtn_to_kopForthTick"),
		#################################################
		MACRO(kfWord, [*link.new(
			"0eq",  # 0=
		), [
			"kfWord_false",
			"kfWord_eq",
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"gtr",  # >
		), [
			"kfWord_swap",
			"kfWord_lss",
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"geq",  # >=
		), [
			"kfWord_lss",
			"kfWord_0eq",
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"r-peek",  # R@
		), [
			"kfWord_r-pop",
			"kfWord_r-pop",
			"kfWord_dup",
			"kfWord_r-push",
			"kfWord_swap",
			"kfWord_r-push",
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"rshift",  # ( x1 u -- x2 )
			KF_FLAG_MASK_NATIVE,
		),[]], prefix),
		# Pop the params.
		MACRO(kfStackPop, [d_stack], prefix),
		STC("kfWordsNative_tmpB"),
		MACRO(kfStackPop, [d_stack], prefix),
		STC("kfWordsNative_tmpA"),
		LABEL("kfWord_rshift_loop"),
		# Break if u is 0.
		LDA("kfWordsNative_tmpB"),
		SUB("2"),
		BLZ("kfWord_rshift_done"),
		STC("kfWordsNative_tmpB"),
		# Shift x right by 1.
		LDA("kfWordsNative_tmpA"),
		LSR(),
		STC("kfWordsNative_tmpA"),
		# Loop.
		JMP("kfWord_rshift_loop"),
		# Return.
		LABEL("kfWord_rshift_done"),
		LDA("kfWordsNative_tmpA"),
		MACRO(kfStackPush, [d_stack], prefix),
		JMP("rtn_to_kopForthTick"),
		
		#######################
		# Memory manipulators #
		#######################
		#################################################
		MACRO(kfWord, [*link.new(
			"+poke",  # +!
		), [
			"kfWord_dup",
			"kfWord_peek",
			"kfWord_rot",
			"kfWord_+",
			"kfWord_swap",
			"kfWord_poke",
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"allot",
		), [
			"kfWord_num2addr",
			"kfWord_dp",
			"kfWord_+poke",
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			",",
		), [
			"kfWord_here",
			"kfWord_poke",
			"kfWord_literal-c", 1*2,
			"kfWord_allot",
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"compile,",
			code_override="kfWord_,_data"
		), [
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"execute",
		), [
			"kfWord_literal-c", LabAddr("kfWord_execute_b01"),
			"kfWord_poke",
			LABEL("kfWord_execute_b01"), 0,
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"move",
			KF_FLAG_MASK_NATIVE,
		),[]], prefix),
		MACRO(kfStackPop, [d_stack], prefix),  # num
		STC("kfWordsNative_tmpC"),
		MACRO(kfStackPop, [d_stack], prefix),  # dest
		REP("kfWord_move_dest"),
		AND("addrBits"),
		STC("kfWordsNative_tmpB"),
		MACRO(kfStackPop, [d_stack], prefix),  # src
		REP("kfWord_move_src"),
		AND("addrBits"),
		# Find direction.
		SUB("kfWordsNative_tmpB"),
		BLZ("kfWord_move_dir_upper"),
		LDA("0001"),
		JMP("kfWord_move_dir"),
		LABEL("kfWord_move_dir_upper"),
		LDA("kfWordsNative_tmpC"),
		LSL(1),
		ADD("kfWord_move_src"),
		SUB("0001"),
		REP("kfWord_move_src"),
		LDA("kfWordsNative_tmpC"),
		LSL(1),
		ADD("kfWord_move_dest"),
		SUB("0001"),
		REP("kfWord_move_dest"),
		LDA("-0001"),
		LABEL("kfWord_move_dir"),
		STC("kfWordsNative_tmpB"),  # dir
		# Iterate until num is 0.
		LABEL("kfWord_move_loop"),
		# Decrement num.
		LDA("kfWordsNative_tmpC"),
		SUB("2"),
		BLZ("kfWord_move_rtn"),
		STC("kfWordsNative_tmpC"),
		# Move word.
		LABEL("kfWord_move_src"), LDA((0, 0)),
		LABEL("kfWord_move_dest"), STC((0, 0)),
		# Increment pointers.
		LDA("kfWord_move_src"),
		ADD("kfWordsNative_tmpB"),
		REP("kfWord_move_src"),
		LDA("kfWord_move_dest"),
		ADD("kfWordsNative_tmpB"),
		REP("kfWord_move_dest"),
		# Loop.
		JMP("kfWord_move_loop"),
		# Return.
		LABEL("kfWord_move_rtn"),
		JMP("rtn_to_kopForthTick"),
	]