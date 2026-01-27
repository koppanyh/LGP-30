#!/usr/bin/env python3

from utils import *
from lgpasm import *

from kfStack import *
from kfWord import *



def kfPopulateWordsInterpret(params, prefix):
	link = params[0]
	return [
		DEBUG("----- kfPopulateWordsInterpret -----", '\n'),
		
		#################################################
		MACRO(kfWord, [*link.new(
			"abort",
		), [
			"kfWord_latest",
			"kfWord_pp",
			"kfWord_peek",
			"kfWord_lss",
			"kfWord_0branch", LabAddr("kfWord_abort_b02"),
			"kfWord_pp",
			"kfWord_peek",
			"kfWord_dp",
			"kfWord_poke",
			"kfWord_latest",
			"kfWord_pp",
			"kfWord_poke",
			LABEL("kfWord_abort_b02"),
			"kfWord_clr-dat-stack",
			*PrintString(" ok"),
			"kfWord_cr",
			"kfWord_quit",
			"kfWord_exit"
		]], prefix),
		
		#######################
		# Input parsing words #
		#######################
		#################################################
		MACRO(kfWord, [*link.new(
			"source",
		), [
			"kfWord_tib",
			"kfWord_tib-len",
			"kfWord_peek",
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"refill",
		), [
			"kfWord_source-id",
			"kfWord_0eq",
			"kfWord_0branch", LabAddr("kfWord_refill_b01"),
			"kfWord_tib",
			"kfWord_tib-avail",
			"kfWord_accept",
			"kfWord_tib-len",
			"kfWord_poke",
			"kfWord_literal-c", 0,
			"kfWord_in-ptr",
			"kfWord_poke",
			"kfWord_space",
			"kfWord_true",
			"kfWord_exit",
			LABEL("kfWord_refill_b01"),
			"kfWord_source-id",
			*PrintString("ERROR: SOURCE-ID of "),
			"kfWord_.",
			*PrintString("is invalid."),
			"kfWord_abort",
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"skipchar",
		), [
			"kfWord_literal-c", LabAddr("kfWord_skipchar_b01"),
			"kfWord_exit",
			LABEL("kfWord_skipchar_b01"), 0
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"isskipchar",
		), [
			"kfWord_skipchar",
			"kfWord_peek",
			"kfWord_eq",
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"isnotskipchar",
		), [
			"kfWord_isskipchar",
			"kfWord_0eq",
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"parse",
		), [
			# TODO
			"kfWord_err-not-imp",
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"parse-name",
		), [
			"kfWord_source",
			"kfWord_in-ptr",
			"kfWord_peek",
			"kfWord_/string",
			"kfWord_bl",
			"kfWord_skipchar",
			"kfWord_poke",
			"kfWord_literal-c", LabAddr("kfWord_isskipchar"),
			"kfWord_xt-skip",
			"kfWord_over",
			"kfWord_swap",
			"kfWord_literal-c", LabAddr("kfWord_isnotskipchar"),
			"kfWord_xt-skip",
			"kfWord_drop",
			"kfWord_2dup",
			"kfWord_swap",
			"kfWord_-",
			"kfWord_addr2num",
			"kfWord_swap",
			"kfWord_literal-c", Addr(0, 1),
			"kfWord_+",
			"kfWord_tib",
			"kfWord_-",
			"kfWord_addr2num",
			"kfWord_in-ptr",
			"kfWord_poke",
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"padword",
		), [
			# 3 1 here +  ( 3 addr )
			"kfWord_literal-c", KF_MAX_NAME_SIZE*2,
			"kfWord_literal-c", Addr(0, 1),
			"kfWord_here",
			"kfWord_+",
			# begin
			LABEL("kfWord_padword_loop"),
			# 0 over !  ( 3 addr )
			"kfWord_literal-c", 0,
			"kfWord_over",
			"kfWord_poke",
			# 1 + swap  ( addr 3 )
			"kfWord_literal-c", Addr(0, 1),
			"kfWord_+",
			"kfWord_swap",
			# 1 - dup exit-if-zero  ( addr 2 )
			"kfWord_literal-c", 2,
			"kfWord_-",
			"kfWord_dup",
			"kfWord_0branch", LabAddr("kfWord_padword_rtn"),
			# swap again  ( 2 addr )
			"kfWord_swap",
			"kfWord_branch", LabAddr("kfWord_padword_loop"),
			# 2drop
			LABEL("kfWord_padword_rtn"),
			"kfWord_2drop",
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"word",
		), [
			"kfWord_padword",
			"kfWord_drop",
			"kfWord_parse-name",  # ( addr u )
			"kfWord_literal-c", KF_MAX_NAME_SIZE*2,
			"kfWord_over",  # ( 3 u )
			"kfWord_lss",  # 0->0, 1->0, 2->0, 3->0, 4->1, 5->1
			"kfWord_0branch", LabAddr("kfWord_word_cont"),
			"kfWord_err-name-long",
			LABEL("kfWord_word_cont"),
			"kfWord_dup",
			"kfWord_here",
			"kfWord_c-poke",
			"kfWord_here",
			"kfWord_literal-c", Addr(0, 1),
			"kfWord_+",
			"kfWord_swap",
			"kfWord_move",
			"kfWord_here",
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"err-not-found",  # (ERR-NOT-FOUND)
		), [
			"kfWord_cr",
			*PrintString("ERROR: "),
			"kfWord_count",
			"kfWord_type",
			*PrintString(" word not found"),
			"kfWord_cr",
			"kfWord_abort"
		]], prefix),
		
		########################
		# Interpretation words #
		########################
		#################################################
		MACRO(kfWord, [*link.new(
			"intp-mode",  # [
			KF_FLAG_MASK_IMMEDIATE,
		), [
			"kfWord_false",
			"kfWord_state",
			"kfWord_poke",
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"comp-mode",  # ]
		), [
			# TODO
			"kfWord_err-not-imp",
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"name-ptr",  # >NAME
		), [
			"kfWord_literal-c", Addr(0, KF_WORD_NAME_LEN_OFFSET),
			"kfWord_+",
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"flags-ptr",  # >FLAGS
		), [
			"kfWord_literal-c", Addr(0, KF_WORD_FLAGS_OFFSET),
			"kfWord_+",
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"err-not-intp",  # (ERR-NOT-INTP)
		), [
			"kfWord_cr",
			*PrintString("ERROR: "),
			"kfWord_name-ptr",
			"kfWord_count",
			"kfWord_type",
			*PrintString(" word is compile-only"),
			"kfWord_cr",
			"kfWord_abort"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"interpret",
		), [
			LABEL("kfWord_interpret_b00"),
			"kfWord_bl",
			"kfWord_word",
			"kfWord_dup",
			"kfWord_count",
			"kfWord_swap",
			"kfWord_drop",
			"kfWord_0branch", LabAddr("kfWord_interpret_b31"),
				#*PrintString("findstart"),
			"kfWord_find",
				#*PrintString("findend"),
			"kfWord_state",
			"kfWord_peek",
			"kfWord_0branch", LabAddr("kfWord_interpret_b17"),
			"kfWord_dup",
			"kfWord_0branch", LabAddr("kfWord_interpret_b09"),
			"kfWord_literal-c", 1*2,
			"kfWord_eq",
			"kfWord_0branch", LabAddr("kfWord_interpret_b06"),
			"kfWord_execute",
			"kfWord_branch", LabAddr("kfWord_interpret_b07"),
			LABEL("kfWord_interpret_b06"),
			"kfWord_compile,",
			LABEL("kfWord_interpret_b07"),
			"kfWord_branch", LabAddr("kfWord_interpret_b15"),
			LABEL("kfWord_interpret_b09"),
			"kfWord_drop",
			"kfWord_dup",
			"kfWord_count",
			"kfWord_s-to-number",
			"kfWord_0branch", LabAddr("kfWord_interpret_b12"),
			"kfWord_drop",
			"kfWord_err-not-found",
			"kfWord_branch", LabAddr("kfWord_interpret_b15"),
			LABEL("kfWord_interpret_b12"),
			# TODO implement double handling.
			"kfWord_drop",
			"kfWord_literal-c", LabAddr("kfWord_literal-c"),
			"kfWord_compile,",
			"kfWord_,",
			"kfWord_drop",
			LABEL("kfWord_interpret_b15"),
			"kfWord_branch", LabAddr("kfWord_interpret_b29"),
			LABEL("kfWord_interpret_b17"),
			"kfWord_0branch", LabAddr("kfWord_interpret_b22"),
			"kfWord_dup",
			"kfWord_flags-ptr",
			"kfWord_c-peek",
			"kfWord_literal-c", KF_FLAG_MASK_COMPILE,
			"kfWord_and",
			"kfWord_0branch", LabAddr("kfWord_interpret_b20"),
			"kfWord_err-not-intp",
			LABEL("kfWord_interpret_b20"),
			"kfWord_execute",
			"kfWord_branch", LabAddr("kfWord_interpret_b29"),
			LABEL("kfWord_interpret_b22"),
			"kfWord_dup",
			"kfWord_count",
			"kfWord_s-to-number",
			"kfWord_0branch", LabAddr("kfWord_interpret_b24"),
			"kfWord_drop",
			"kfWord_err-not-found",
			LABEL("kfWord_interpret_b24"),
			# TODO implement double handling.
			"kfWord_drop",
			"kfWord_swap",
			"kfWord_drop",
			LABEL("kfWord_interpret_b29"),
			"kfWord_branch", LabAddr("kfWord_interpret_b00"),
			LABEL("kfWord_interpret_b31"),
			"kfWord_drop",
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"evaluate",
		), [
			# TODO
			"kfWord_err-not-imp",
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"quit",
		), [
			"kfWord_clr-ret-stack",
			"kfWord_clr-in-source",
			"kfWord_intp-mode",
			LABEL("kfWord_quit_b00"),
			"kfWord_refill",
			"kfWord_0branch", LabAddr("kfWord_quit_b03"),
			"kfWord_interpret",
			*PrintString(" ok"),
			"kfWord_cr",
			"kfWord_branch", LabAddr("kfWord_quit_b00"),
			LABEL("kfWord_quit_b03"),
			"kfWord_exit"
		]], prefix),
	]
