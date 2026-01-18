#!/usr/bin/env python3

from utils import *
from lgpasm import *

from kfBios import *
from kfStatus import *
from kfStack import *
from kfWord import *



def kfPopulateWordsNative(params, prefix):
	return [
		DEBUG("----- kfPopulateWordsNative -----", '\n'),
		DATA(
			LABEL("kfWordsNative_tmpA"), 0,
			LABEL("kfWordsNative_tmpB"), 0,
			LABEL("kfWordsNative_tmpC"), 0,
		),
		#################################################
		MACRO(kfWord, ["exit",
			"boot",
			KF_FLAG_MASK_NATIVE | KF_FLAG_MASK_COMPILE,
			"kfWordsNative_exit",
		[]], prefix),
		LABEL("kfWordsNative_exit"),
		MACRO(kfStackPop, [r_stack], prefix),
		JMP("rtn_to_kopForthTick"),
		#################################################
		MACRO(kfWord, ["(literal)",
			"exit",
			KF_FLAG_MASK_NATIVE | KF_FLAG_MASK_COMPILE,
			"kfWordsNative_(literal)",
		[]], prefix),
		LABEL("kfWordsNative_(literal)"),
		MACRO(kfStackPop, [r_stack], prefix),
		REP("kfWordsNative_(literal)_lda1"),
		ADD("0001"),
		MACRO(kfStackPush, [r_stack], prefix),
		LABEL("kfWordsNative_(literal)_lda1"), LDA((0, 0)),
		MACRO(kfStackPush, [d_stack], prefix),
		JMP("rtn_to_kopForthTick"),
		#################################################
		MACRO(kfWord, ["-",
			"(literal)",
			KF_FLAG_MASK_NATIVE,
			"kfWordsNative_-",
		[]], prefix),
		LABEL("kfWordsNative_-"),
		MACRO(kfStackPop, [d_stack], prefix),
		STC("kfWordsNative_tmpB"),
		MACRO(kfStackPop, [d_stack], prefix),
		SUB("kfWordsNative_tmpB"),
		MACRO(kfStackPush, [d_stack], prefix),
		JMP("rtn_to_kopForthTick"),
		#################################################
		MACRO(kfWord, ["*",
			"-",
			KF_FLAG_MASK_NATIVE,
			"kfWordsNative_*",
		[]], prefix),
		LABEL("kfWordsNative_*"),
		# TODO
		MACRO(kfStatusErr, ["KF_SYSTEM_NOT_IMP"], prefix),
		JMP("rtn_to_kopForthTick"),
		#################################################
		MACRO(kfWord, [".",
			"*",
			KF_FLAG_MASK_NATIVE,
			"kfWordsNative_.",
		[]], prefix),
		LABEL("kfWordsNative_."),
		MACRO(kfStackPop, [d_stack], prefix),
		MACRO(kfBiosPrintIsize, [], prefix),
		MACRO(HardcodeText, [" "], prefix),
		JMP("rtn_to_kopForthTick"),
		#################################################
		MACRO(kfWord, ["peek",  # @
			".",
			KF_FLAG_MASK_NATIVE,
			"kfWordsNative_peek",
		[]], prefix),
		LABEL("kfWordsNative_peek"),
		MACRO(kfStackPop, [d_stack], prefix),
		REP("kfWord_peek_lda"),
		LABEL("kfWord_peek_lda"), LDA((0, 0)),
		MACRO(kfStackPush, [d_stack], prefix),
		JMP("rtn_to_kopForthTick"),
		#################################################
		MACRO(kfWord, ["poke",  # !
			"peek",
			KF_FLAG_MASK_NATIVE,
			"kfWordsNative_poke",
		[]], prefix),
		LABEL("kfWordsNative_poke"),
		MACRO(kfStackPop, [d_stack], prefix),
		REP("kfWord_poke_stc"),
		MACRO(kfStackPop, [d_stack], prefix),
		LABEL("kfWord_poke_stc"), STC((0, 0)),
		JMP("rtn_to_kopForthTick"),
		#################################################
		MACRO(kfWord, ["cpeek",  # C@
			"poke",
			KF_FLAG_MASK_NATIVE,
			"kfWordsNative_cpeek",
		[]], prefix),
		LABEL("kfWordsNative_cpeek"),
		# TODO
		MACRO(kfStatusErr, ["KF_SYSTEM_NOT_IMP"], prefix),
		JMP("rtn_to_kopForthTick"),
		#################################################
		MACRO(kfWord, ["cpoke",  # C!
			"cpeek",
			KF_FLAG_MASK_NATIVE,
			"kfWordsNative_cpoke",
		[]], prefix),
		LABEL("kfWordsNative_cpoke"),
		# TODO
		MACRO(kfStatusErr, ["KF_SYSTEM_NOT_IMP"], prefix),
		JMP("rtn_to_kopForthTick"),
		#################################################
		MACRO(kfWord, ["rpush",  # >R
			"cpoke",
			KF_FLAG_MASK_NATIVE,
			"kfWordsNative_rpush",
		[]], prefix),
		LABEL("kfWordsNative_rpush"),
		MACRO(kfStackPop, [r_stack], prefix),
		STC("kfWordsNative_tmpA"),
		MACRO(kfStackPop, [d_stack], prefix),
		MACRO(kfStackPush, [r_stack], prefix),
		LDA("kfWordsNative_tmpA"),
		MACRO(kfStackPush, [r_stack], prefix),
		JMP("rtn_to_kopForthTick"),
		#################################################
		MACRO(kfWord, ["rpop",  # R>
			"rpush",
			KF_FLAG_MASK_NATIVE,
			"kfWordsNative_rpop",
		[]], prefix),
		LABEL("kfWordsNative_rpop"),
		MACRO(kfStackPop, [r_stack], prefix),
		STC("kfWordsNative_tmpA"),
		MACRO(kfStackPop, [r_stack], prefix),
		MACRO(kfStackPush, [d_stack], prefix),
		LDA("kfWordsNative_tmpA"),
		MACRO(kfStackPush, [r_stack], prefix),
		JMP("rtn_to_kopForthTick"),
		#################################################
		MACRO(kfWord, ["drop",
			"rpop",
			KF_FLAG_MASK_NATIVE,
			"kfWordsNative_drop",
		[]], prefix),
		LABEL("kfWordsNative_drop"),
		MACRO(kfStackPop, [d_stack], prefix),
		JMP("rtn_to_kopForthTick"),
		#################################################
		MACRO(kfWord, ["dup",
			"drop",
			KF_FLAG_MASK_NATIVE,
			"kfWordsNative_dup",
		[]], prefix),
		LABEL("kfWordsNative_dup"),
		MACRO(kfStackPop, [d_stack], prefix),
		STA("kfWordsNative_tmpA"),
		MACRO(kfStackPush, [d_stack], prefix),
		LDA("kfWordsNative_tmpA"),
		MACRO(kfStackPush, [d_stack], prefix),
		JMP("rtn_to_kopForthTick"),
		#################################################
		MACRO(kfWord, ["swap",
			"dup",
			KF_FLAG_MASK_NATIVE,
			"kfWordsNative_swap",
		[]], prefix),
		LABEL("kfWordsNative_swap"),
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
		MACRO(kfWord, ["branch",
			"swap",
			KF_FLAG_MASK_NATIVE | KF_FLAG_MASK_COMPILE,
			"kfWordsNative_branch",
		[]], prefix),
		LABEL("kfWordsNative_branch"),
		MACRO(kfStackPop, [r_stack], prefix),
		REP("kfWord_branch_lda"),
		LABEL("kfWord_branch_lda"), LDA((0, 0)),
		MACRO(kfStackPush, [r_stack], prefix),
		JMP("rtn_to_kopForthTick"),
		#################################################
		MACRO(kfWord, ["0branch",
			"branch",
			KF_FLAG_MASK_NATIVE | KF_FLAG_MASK_COMPILE,
			"kfWordsNative_0branch",
		[]], prefix),
		LABEL("kfWordsNative_0branch"),
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
		MACRO(kfWord, ["emit",
			"0branch",
			KF_FLAG_MASK_NATIVE,
			"kfWordsNative_emit",
		[]], prefix),
		LABEL("kfWordsNative_emit"),
		MACRO(kfStackPop, [d_stack], prefix),
		MACRO(kfBiosWriteChars, [], prefix),
		JMP("rtn_to_kopForthTick"),
		#################################################
		MACRO(kfWord, ["key",
			"emit",
			KF_FLAG_MASK_NATIVE,
			"kfWordsNative_key",
		[]], prefix),
		LABEL("kfWordsNative_key"),
		MACRO(kfBiosReadChars, [], prefix),
		MACRO(kfStackPush, [d_stack], prefix),
		JMP("rtn_to_kopForthTick"),
		#################################################
		MACRO(kfWord, ["accept",
			"key",
			KF_FLAG_MASK_NATIVE,
			"kfWordsNative_accept",
		[]], prefix),
		LABEL("kfWordsNative_accept"),
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
		# Break if chars contain terminator.
		LDA("kfWordsNative_tmpC"),
		AND("kfBiosTerminatorMask"),
		MACRO(EqualsZero, [], prefix),
		BLZ("kfWord_accept_break"),
		# End loop.
		JMP("kfWord_accept_loop"),
		LABEL("kfWord_accept_break"),
		# Push u2 and return.
		LDA("kfWordsNative_tmpB"),
		MACRO(kfStackPush, [d_stack], prefix),
		JMP("rtn_to_kopForthTick"),
		#################################################
		MACRO(kfWord, ["type",
			"accept",
			KF_FLAG_MASK_NATIVE,
			"kfWordsNative_type",
		[]], prefix),
		LABEL("kfWordsNative_type"),
		MACRO(kfStackPop, [d_stack], prefix),
		STC("kfBiosWriteStrLen_len"),
		MACRO(kfStackPop, [d_stack], prefix),
		MACRO(kfBiosWriteStrLen, [], prefix),
		JMP("rtn_to_kopForthTick"),
	]

'''
		#################################################
		MACRO(kfWord, ["",
			"",
			KF_FLAG_MASK_NATIVE,
			"kfWordsNative_",
		[]], prefix),
		LABEL("kfWordsNative_"),
		# TODO
		MACRO(kfStatusErr, ["KF_SYSTEM_NOT_IMP"], prefix),
		JMP("rtn_to_kopForthTick"),
'''

'''
    wn->pcr = kopForthAddNativeWord(forth, "(CREATE)",        W_Pcr, false);
    wn->cmp = kopForthAddNativeWord(forth, "COMPARE",         W_Cmp, false);
    wn->fnd = kopForthAddNativeWord(forth, "FIND",            W_Fnd, false);
    wn->mss = kopForthAddNativeWord(forth, "M*/",             W_Mss, false);
    wn->dpl = kopForthAddNativeWord(forth, "D+",              W_Dpl, false);
    wn->equ = kopForthAddNativeWord(forth, "=",               W_Equ, false);
    wn->lss = kopForthAddNativeWord(forth, "<",               W_Lss, false);
    wn->nan = kopForthAddNativeWord(forth, "NAND",            W_Nan, false);
    wn->psq = kopForthAddNativeWord(forth, "(S\")",           W_Psq, false);  // TODO make compile only.
    wn->squ = kopForthAddNativeWord(forth, "S\"",             W_Squ, true );  // TODO make compile only.
    wn->dqu = kopForthAddNativeWord(forth, ".\"",             W_Dqu, true );
    wn->dos = kopForthAddNativeWord(forth, ".S",              W_Dos, false);
    wn->dor = kopForthAddNativeWord(forth, ".R",              W_Dor, false);
    wn->dmp = kopForthAddNativeWord(forth, "DUMP",            W_Dmp, false);
    wn->ntr = kopForthAddNativeWord(forth, "N>R",             W_Ntr, false);
    wn->nrf = kopForthAddNativeWord(forth, "NR>",             W_Nrf, false);
    wn->sip = kopForthAddNativeWord(forth, "SAVE-INPUT",      W_Sip, false);
    wn->rip = kopForthAddNativeWord(forth, "RESTORE-INPUT",   W_Rip, false);
    wn->cis = kopForthAddNativeWord(forth, "(CLR-IN-SOURCE)", W_Cis, false);
    wn->crs = kopForthAddNativeWord(forth, "(CLR-RET-STACK)", W_Crs, false);
    wn->cds = kopForthAddNativeWord(forth, "(CLR-DAT-STACK)", W_Cds, false);
'''