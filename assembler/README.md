# Assembler

This is an assembler thingy that'll output tape programs in the P104 format.
It's basically a Python library for writing programs that'll generate programs.

Run `python3 demo.py` to generate a program that'll print "kop wuz here" when run.

## Usage

Too tired to write this documentation, so just look at `demo.py` and the bottom of `lgpasm.py` for examples of how it works (specifically `demo.py` since it's more correct).

## Mnemonics

Refer to [programming](https://en.wikipedia.org/wiki/LGP-30#Programming) section
on Wikipedia for more information about what each opcode does.

| Mnemonic | Op  | Description
|----------|-----|-------------
| LDA      | b   | **L**oa**D** from **A**ddr
| STA      | h   | **ST**ore to **A**ddr
| STC      | c   | **ST**ore to addr and **C**lear acc
| REP      | y   | **REP**lace addr bits at addr with those from acc
| JMP      | u   | unconditional **J**u**MP**
| RTA      | r   | write **R**e**T**urn addr bits to **A**ddr
| BLZ      | t   | **B**ranch if acc **L**ess than **Z**ero
| HLT      | z   | **H**a**LT**
| PRT      | p   | **PR**in**T** character to terminal
| INP      | i   | **INP**ut from terminal/tape
| ADD      | a   | **ADD** value at addr to acc
| SUB      | s   | **SUB**tract value at addr from acc
| MUP      | m   | **M**ultiply acc by value at addr and keep **UP**per result
| MLO      | n   | **M**ultiply acc by value at addr and keep **LO**wer result
| DIV      | d   | **DIV**ide acc by value at addr
| AND      | e   | apply bitwise **AND** between acc and value at addr
| RAW      | N/A | input a **RAW** string into the program output

*addr is short for address* \
*acc is short for accumulator*

## Conventions

### Subroutines

Because of how strange they are on this computer, this is the recommended approach.

Define your subroutine as a macro and define a caller macro for it:

```
def defExampleSubroutine(params, prefix):
	return [
		DEBUG("defExampleSubroutine"),
		LABEL("exampleSubroutine"),
		#
		# Insert all your logic here.
		#
		LABEL("exampleSubroutine_rtn"),
		JMP((0, 0)),
	]

# Call the example subroutine.
# Usage: MACRO(exampleSubroutine)
def exampleSubroutine(params, prefix):
	return [
		DEBUG(f"exampleSubroutine()"),
		RTA("exampleSubroutine_rtn"),
		JMP("exampleSubroutine"),
	]

```

Then in your working code, call the subroutine definition macro to populate it
into the code, then you can call the subroutine as needed:

```
Assembler(
	# Populate the subroutine logic into the main program.
	MACRO(defExampleSubroutine),
	...
	# Call the subroutine as needed.
	MACRO(exampleSubroutine),
)
```

It will return to the point after that caller macro, but be wary of nesting since
this method doesn't use a return stack, so recursive calls will overwrite the
return address.

Also assume that the acc will be modified, unless otherwise stated by the
subroutine's documentation.
