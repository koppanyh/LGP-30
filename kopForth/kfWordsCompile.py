#!/usr/bin/env python3

from utils import *
from lgpasm import *

from kfStack import *
from kfWord import *



def kfPopulateWordsCompile(params, prefix):
	link = params[0]
	return [
		DEBUG("----- kfPopulateWordsCompile -----", '\n'),
		
		###################
		# Compiling words #
		###################
		#################################################
		MACRO(kfWord, [*link.new(
			"reveal",
		), [
			"kfWord_pp",
			"kfWord_peek",
			"kfWord_lp",
			"kfWord_poke",
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"link-ptr",  # >LINK
		), [
			"kfWord_literal-c", Addr(0, KF_WORD_LINK_OFFSET),
			"kfWord_+",
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"code-ptr",  # >CODE
		), [
			"kfWord_literal-c", Addr(0, KF_WORD_CODE_OFFSET),
			"kfWord_+",
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"body-ptr",  # >BODY
		), [
			"kfWord_literal-c", Addr(0, KF_WORD_DATA_OFFSET),
			"kfWord_+",
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"unreveal",
		), [
			"kfWord_latest",
			"kfWord_link-ptr",
			"kfWord_peek",
			"kfWord_lp",
			"kfWord_poke",
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"dodoes",
		), [
			"kfWord_r-pop",
			"kfWord_r-pop",
			"kfWord_dup",
			"kfWord_r-push",
			"kfWord_swap",
			"kfWord_r-push",
			"kfWord_literal-c", Addr(0, 1),
			"kfWord_-",
			"kfWord_peek",
			"kfWord_body-ptr",
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"does-def-c",  # (DOES>)
		), [
			"kfWord_r-pop",
			"kfWord_pp",
			"kfWord_peek",
			"kfWord_code-ptr",
			"kfWord_poke",
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"does-def",  # DOES>
			KF_FLAG_MASK_IMMEDIATE | KF_FLAG_MASK_COMPILE,
		), [
			"kfWord_literal-c", LabAddr("kfWord_does-def-c"),
			"kfWord_compile,",
			"kfWord_literal-c", LabAddr("kfWord_dodoes"),
			"kfWord_compile,",
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"create",
		), [
			"kfWord_bl",
			"kfWord_word",
			"kfWord_drop",
			"kfWord_create-c",
			"kfWord_does-def-c",
			"kfWord_dodoes",
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"def",  # :
		), [
			"kfWord_create",
			"kfWord_unreveal",
			"kfWord_comp-mode",
			"kfWord_here",
			"kfWord_pp",
			"kfWord_peek",
			"kfWord_code-ptr",
			"kfWord_poke",
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			";",
			KF_FLAG_MASK_IMMEDIATE | KF_FLAG_MASK_COMPILE,
		), [
			"kfWord_literal-c", LabAddr("kfWord_exit"),
			"kfWord_compile,",
			"kfWord_reveal",
			"kfWord_intp-mode",
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"immediate",
			KF_FLAG_MASK_IMMEDIATE
		), [
			"kfWord_pp",
			"kfWord_peek",
			"kfWord_flags-ptr",
			"kfWord_dup",
			"kfWord_c-peek",
			"kfWord_literal-c", KF_FLAG_MASK_IMMEDIATE,
			"kfWord_or",
			"kfWord_swap",
			"kfWord_c-poke",
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"compile-only",
			KF_FLAG_MASK_IMMEDIATE
		), [
			"kfWord_pp",
			"kfWord_peek",
			"kfWord_flags-ptr",
			"kfWord_dup",
			"kfWord_c-peek",
			"kfWord_literal-c", KF_FLAG_MASK_COMPILE,
			"kfWord_or",
			"kfWord_swap",
			"kfWord_c-poke",
			"kfWord_exit"
		]], prefix),
		
		#####################
		# Conditional words #
		#####################
		#################################################
		MACRO(kfWord, [*link.new(
			"if",
			KF_FLAG_MASK_IMMEDIATE | KF_FLAG_MASK_COMPILE,
		), [
			"kfWord_literal-c", LabAddr("kfWord_0branch"),
			"kfWord_compile,",
			"kfWord_here",
			"kfWord_literal-c", 0,
			"kfWord_,",
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"then",
			KF_FLAG_MASK_IMMEDIATE | KF_FLAG_MASK_COMPILE,
		), [
			"kfWord_here",
			"kfWord_swap",
			"kfWord_poke",
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"else",
			KF_FLAG_MASK_IMMEDIATE | KF_FLAG_MASK_COMPILE,
		), [
			"kfWord_literal-c", LabAddr("kfWord_branch"),
			"kfWord_compile,",
			"kfWord_here",
			"kfWord_swap",
			"kfWord_literal-c", 0,
			"kfWord_,",
			"kfWord_then",
			"kfWord_exit"
		]], prefix),
		
		#####################
		# Finite loop words #
		#####################
		#################################################
		MACRO(kfWord, [*link.new(
			"i",
			KF_FLAG_MASK_COMPILE,
		), [
			"kfWord_r-pop",
			"kfWord_r-peek",
			"kfWord_swap",
			"kfWord_r-push",
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"do-c",  # (DO)
			KF_FLAG_MASK_COMPILE,
		), [
			"kfWord_swap",
			"kfWord_r-pop",
			"kfWord_dup",
			"kfWord_peek",
			"kfWord_r-push",
			"kfWord_swap",
			"kfWord_r-push",
			"kfWord_swap",
			"kfWord_r-push",
			"kfWord_literal-c", 0b_000000_000001_00,
			"kfWord_+",
			"kfWord_r-push",
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"do",
			KF_FLAG_MASK_IMMEDIATE | KF_FLAG_MASK_COMPILE,
		), [
			"kfWord_literal-c", "kfWord_do-c",
			"kfWord_compile,",
			"kfWord_here",
			"kfWord_literal-c", 0,
			"kfWord_,",
			"kfWord_here",
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"leave",
			KF_FLAG_MASK_COMPILE,
		), [
			"kfWord_r-pop",
			"kfWord_drop",
			"kfWord_r-pop",
			"kfWord_drop",
			"kfWord_r-pop",
			"kfWord_drop",
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"+loop-c",  # (+LOOP)
			KF_FLAG_MASK_COMPILE,
		), [
			"kfWord_r-pop",
			"kfWord_peek",
			"kfWord_swap",
			"kfWord_r-pop",
			"kfWord_over",
			"kfWord_+",
			"kfWord_r-pop",
			"kfWord_rot",
			"kfWord_literal-c", 0,
			"kfWord_lss",
			"kfWord_0branch", LabAddr("kfWord_+loop-c_b02"),
			"kfWord_2dup",
			"kfWord_lss",
			"kfWord_branch", LabAddr("kfWord_+loop-c_b03"),
			LABEL("kfWord_+loop-c_b02"),
			"kfWord_2dup",
			"kfWord_geq",
			LABEL("kfWord_+loop-c_b03"),
			"kfWord_0branch", LabAddr("kfWord_+loop-c_b05"),
			"kfWord_drop",
			"kfWord_drop",
			"kfWord_drop",
			"kfWord_exit",
			LABEL("kfWord_+loop-c_b05"),
			"kfWord_r-push",
			"kfWord_r-push",
			"kfWord_r-push",
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"+loop",
			KF_FLAG_MASK_IMMEDIATE | KF_FLAG_MASK_COMPILE,
		), [
			"kfWord_literal-c", LabAddr("kfWord_+loop-c"),
			"kfWord_compile,",
			"kfWord_compile,",
			"kfWord_here",
			"kfWord_swap",
			"kfWord_poke",
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"loop",
			KF_FLAG_MASK_IMMEDIATE | KF_FLAG_MASK_COMPILE,
		), [
			"kfWord_literal-c", LabAddr("kfWord_literal-c"),
			"kfWord_compile,",
			"kfWord_literal-c", 1*2,
			"kfWord_,",
			"kfWord_+loop",
			"kfWord_exit"
		]], prefix),
		
		#########################
		# Indefinite loop words #
		#########################
		#################################################
		MACRO(kfWord, [*link.new(
			"begin",
			KF_FLAG_MASK_IMMEDIATE | KF_FLAG_MASK_COMPILE,
		), [
			"kfWord_here",
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"again",
			KF_FLAG_MASK_IMMEDIATE | KF_FLAG_MASK_COMPILE,
		), [
			"kfWord_literal-c", LabAddr("kfWord_branch"),
			"kfWord_compile,",
			"kfWord_,",
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"until",
			KF_FLAG_MASK_IMMEDIATE | KF_FLAG_MASK_COMPILE,
		), [
			"kfWord_literal-c", LabAddr("kfWord_0branch"),
			"kfWord_compile,",
			"kfWord_,",
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"while",
			KF_FLAG_MASK_IMMEDIATE | KF_FLAG_MASK_COMPILE,
		), [
			"kfWord_literal-c", LabAddr("kfWord_0branch"),
			"kfWord_compile,",
			"kfWord_here",
			"kfWord_swap",
			"kfWord_literal-c", 0,
			"kfWord_,",
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"repeat",
			KF_FLAG_MASK_IMMEDIATE | KF_FLAG_MASK_COMPILE,
		), [
			"kfWord_literal-c", LabAddr("kfWord_branch"),
			"kfWord_compile,",
			"kfWord_,",
			"kfWord_here",
			"kfWord_swap",
			"kfWord_poke",
			"kfWord_exit"
		]], prefix),
	]
