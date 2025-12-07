# LGP-30 P104 Documentation

Translated from German to English by Gemini 2.5 Pro

## Translation

| Eurocomp Ltd. <br> ELECTRONIC COMPUTERS | LGP-30 <br> Program Description |
|---|---|
| PROGRAM INPUT <br> (originally: 10.3, modified by Rice Institute) | 10.4 |

The main function of this routine is to read in programs (from paper tape or by hand). A program consists of instruction and data words. The present routine handles exclusively instructions and hexadecimal data. Decimal numbers cannot be read in by 10.4.

1.  The easiest way to input instructions into the LGP-30 is if they are binary coded. But since programming in this system is quite difficult, the decimal notation is preferred. However, one must then provide for a subsequent conversion into the binary system, as the instruction addresses must be stored in binary.

2.  Most programs contain instructions that refer to locations within these programs. If one wants to leave the starting address of a program open (this is the rule for subroutines, for example), then such addresses must be recalculated (modified).

3.  Sometimes it is very advantageous to transfer constants needed in the program into the binary system by hand and build them into the program. If one wants to input decimal instructions and hexadecimal data alongside each other, there must be an identifier for hexadecimal (or decimal) words.

4.  Occasionally (especially during testing), it is necessary to change data or instructions of a stored program.

The present routine 10.4 allows the tasks described under 1 to 4 to be carried out in a simple manner. It uses seven types of codewords for this purpose. They all consist of 8 characters, some of which can be decimal digits (e.g., decimal addresses). The first of the eight characters determines the type of the codeword. After input, it is decoded, and the corresponding part of the program is called. The codewords and the functions they trigger are described below.

1.  **Instruction (0)**
    The address of the instruction is converted to binary, and the entire instruction is stored in a given cell. If there is no 'x' before the operation part, the address is first incremented by the content of the modifier (see under 4) (relative address). Otherwise, the modification is omitted (absolute address). E.g., the instruction b 2436 is modified, whereas xC 6300 is not. The 'x' is not stored.

2.  **Command (+)**
    The last seven digits of this codeword are interpreted by 10.4 as an instruction. This is executed when the following word is in the ACC. The instruction address of the command word is decimal and is not modified. The object of the command instruction (the following word) is considered hexadecimal. Example: The codeword +00C6314 followed by 73W08 causes the routine to store the hex word 00073W08 in sector 14 of track 63.

3.  **Start fill (;)**
    The codeword specifies in which cell the next instruction or data word should be stored. The subsequent words are stored in consecutive cells until a codeword interrupts their sequence. The address part of the codeword is decimal and consists of the track and cell number. Example: The codeword: ;0002035 causes the routine to place the next word (not a codeword) in cell 2035, the following in 2036, the third in 2037, etc.

4.  **Set Modifier (/)**
    The address of the codeword is stored in a cell called the modifier. It is added to the addresses of all instruction words whose instruction part was not marked by a preceding 'x'. The modifier can only be changed by a second modifier codeword. The address of the codeword is entered in decimal. Usually, the modifier follows the start fill and has the same address. Example: The codeword /0001500 causes the routine to increase all relative addresses of the instruction words still to be read in by 1500. Thus, B 2738 becomes the instruction B 4238, while xH 6300 remains unchanged.

5.  **Halt and Jump (.)**
    This codeword does two things. First, the machine is stopped. After pressing the start button, a jump is made to the cell determined by the address of the codeword. The stop can be prevented by depressing the "NO HALT 32" switch. Example: The codeword .0001700 forces a stop; after restarting, a jump to sector 00 of track 17 occurs.

6.  **Hexadecimal Words (,)**
    This codeword causes the program to store the next words as hexadecimal constants (the conversion of the address part is omitted). The number of hex words is indicated by the sector part of the codeword's address (the track part is always zero). Example: The codeword ,0000014 causes the routine to store the next 14 words as hex words. Up to 63 hex words can be read in with one codeword.

7.  **Hex. fill (v)**
    This codeword causes the machine to read the next n words and store them as hex data in consecutive cells, beginning at m (m and n are hexadecimal numbers). During the read-in, the binary words are added; a checksum is formed from them. After inputting all m words, the machine compares the calculated number with the checksum from the paper tape. By depressing the "JUMP" switch, the test can be prevented. If the numbers are equal, the operation is finished; otherwise, the machine stops and prints "error". The codeword has the following form:

    V n n n m m m m

    nnn is the hex number of words to be read in, and mmmm is the hex address for the first word. Example: V1J02W00 means: the next 448 words are read in and stored in cell 4700 and the following ones. Up to 2047 hex words can be input with one codeword.

**General:**
Leading zeros do not need to be punched, as the accumulator is cleared before each input. All other zeros must be entered. E.g.: / 0001700 must be punched completely, but for 000B1700, only B1700 needs to be punched. If the machine reads an incorrect codeword, it performs a carriage return, prints "error", and stops. The last word read contains the error.

During input, the machine does not perform a carriage return. These must be included on the tape. If some carriage return symbols are missing from the tape, a stop may result. After pressing the carriage return key, the machine continues reading without error.

**Time requirements:**
One track can be filled with instructions in 60-79 sec. When inputting with Hex. fill, one track is filled in 50-60 sec.

**Memory requirements:**
The routine occupies tracks 00 to 03 and uses no temporary storage on track 63.

**Halt:**
The machine stops at 0062 if an incorrect codeword is read or if the checksums are not equal.

In the following, tt means a track no., ss a sector no., and W one of the 16 LGP-30 instructions.

| Codeword | Interpretation |
|---|---|
| 000Wttss | modified instruction |
| 00xWttxx | unmodified instruction |
| 800Wttss | modified negative instruction |
| 80xWttss | unmodified negative instruction |
| +00Wttss | After reading the next word into the ACC, the instruction Wttss is executed |
| ;000ttss | The first input word is stored in cell ttss |
| /000ttss | The address ttss is stored and added to all addresses of the following instructions, if they are not marked with an "x". |
| .000ttss | The machine stops if switch "NO HALT 32" is not depressed. When the start button is pressed, it jumps to cell ss of track tt. |
| ,00000NN | The next NN words are stored as hexadecimal, with the condition 1 $\le$ NN $\le$ 63. |
| V nnn mmmm | The next nnn words are stored in consecutive cells, beginning with address mmmm. During read-in, a checksum is calculated, which is compared with a hex number from the paper tape. If the "JUMP" switch is pressed, the reading and comparison of the checksum are omitted. nnn and mmmm are hex numbers with 1 $\le$ nnn $\le$ 2047. |
