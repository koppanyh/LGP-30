#!/usr/bin/env python3

from utils import *
from lgpasm import *

from kfWord import *



def kfPopulateWordsVarAddrConst(params, prefix):
	link = params[0]
	return [
		DEBUG("----- kfPopulateWordsVarAddrConst -----", '\n'),
		
		#############
		# Variables #
		#############
		#################################################
		MACRO(kfWord, [*link.new(
			"dp",
		), [
			"kfWord_literal-c", LabAddr("kopForth_here"),
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"lp",
		), [
			"kfWord_literal-c", LabAddr("kopForth_latest"),
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"pp",
		), [
			"kfWord_literal-c", LabAddr("kopForth_pending"),
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"state",
		), [
			"kfWord_literal-c", LabAddr("kopForth_state"),
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"srcpt",
		), [
			"kfWord_literal-c", LabAddr("kopForth_in_src_source_id"),
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"in-ptr",  # >IN
		), [
			"kfWord_literal-c", LabAddr("kopForth_in_src_in_offset"),
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"tib-len",  # #TIB
		), [
			"kfWord_literal-c", LabAddr("kopForth_in_src_in_len"),
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"tp",
		), [
			"kfWord_literal-c", LabAddr("kopForth_in_src_buf"),
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"debug",
		), [
			"kfWord_literal-c", LabAddr("kopForth_debug"),
			"kfWord_exit"
		]], prefix),
		
		#############
		# Addresses #
		#############
		#################################################
		MACRO(kfWord, [*link.new(
			"here",
		), [
			"kfWord_dp",
			"kfWord_peek",
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"latest",
		), [
			"kfWord_lp",
			"kfWord_peek",
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"pad",
		), [
			"kfWord_here",
			"kfWord_literal-c", Addr(0, 64),
			"kfWord_+",
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"tib-end",
		), [
			"kfWord_literal-c", LabAddr("kopForth_in_buf", 0, KF_IN_BUF_SIZE),
			"kfWord_exit"
		]], prefix),
		
		#############
		# Constants #
		#############
		#################################################
		MACRO(kfWord, [*link.new(
			"true",
		), [
			"kfWord_literal-c", -1,
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"false",
		), [
			"kfWord_literal-c", 0,
			"kfWord_exit"
		]], prefix),
		
		##########
		# Values #
		##########
		#################################################
		MACRO(kfWord, [*link.new(
			"source-id",
		), [
			"kfWord_srcpt",
			"kfWord_peek",
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"tib",
		), [
			"kfWord_tp",
			"kfWord_peek",
			"kfWord_exit"
		]], prefix),
		#################################################
		MACRO(kfWord, [*link.new(
			"tib-avail",
		), [
			"kfWord_tib-end",
			"kfWord_tib",
			"kfWord_-",
			"kfWord_exit"
		]], prefix),
	]
