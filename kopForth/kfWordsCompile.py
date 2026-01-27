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
			# TODO
			"kfWord_err-not-imp",
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
			# TODO
			"kfWord_err-not-imp",
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"body-ptr",  # >BODY
		), [
			# TODO
			"kfWord_err-not-imp",
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"unreveal",
		), [
			# TODO
			"kfWord_err-not-imp",
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"dodoes",
		), [
			# TODO
			"kfWord_err-not-imp",
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"does-def-c",  # (DOES>)
		), [
			# TODO
			"kfWord_err-not-imp",
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"does-def",  # DOES>
		), [
			# TODO
			"kfWord_err-not-imp",
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"create",
		), [
			# TODO
			"kfWord_err-not-imp",
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"def",  # :
		), [
			# TODO
			"kfWord_err-not-imp",
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"undef",  # ;
		), [
			# TODO
			"kfWord_err-not-imp",
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"immediate",
		), [
			# TODO
			"kfWord_err-not-imp",
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"compile-only",
		), [
			# TODO
			"kfWord_err-not-imp",
			"kfWord_exit"
		]], prefix),
		
		#####################
		# Conditional words #
		#####################
		#################################################
		MACRO(kfWord, [*link.new(
			"if",
		), [
			# TODO
			"kfWord_err-not-imp",
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"else",
		), [
			# TODO
			"kfWord_err-not-imp",
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"then",
		), [
			# TODO
			"kfWord_err-not-imp",
			"kfWord_exit"
		]], prefix),
		
		#####################
		# Finite loop words #
		#####################
		#################################################
		MACRO(kfWord, [*link.new(
			"i",
		), [
			# TODO
			"kfWord_err-not-imp",
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"j",
		), [
			# TODO
			"kfWord_err-not-imp",
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"do-c",  # (DO)
		), [
			# TODO
			"kfWord_err-not-imp",
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"do",
		), [
			# TODO
			"kfWord_err-not-imp",
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"leave",
		), [
			# TODO
			"kfWord_err-not-imp",
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"+loop-c",  # (+LOOP)
		), [
			# TODO
			"kfWord_err-not-imp",
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"+loop",
		), [
			# TODO
			"kfWord_err-not-imp",
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"loop",
		), [
			# TODO
			"kfWord_err-not-imp",
			"kfWord_exit"
		]], prefix),
		
		#########################
		# Indefinite loop words #
		#########################
		#################################################
		MACRO(kfWord, [*link.new(
			"begin",
		), [
			# TODO
			"kfWord_err-not-imp",
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"again",
		), [
			# TODO
			"kfWord_err-not-imp",
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"until",
		), [
			# TODO
			"kfWord_err-not-imp",
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"while",
		), [
			# TODO
			"kfWord_err-not-imp",
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"repeat",
		), [
			# TODO
			"kfWord_err-not-imp",
			"kfWord_exit"
		]], prefix),
	]
