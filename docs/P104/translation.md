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

## Transcription

These are the pages from the official papertapes/P104/p10_4_0{n}.pdf files found on [LINK](ftp://link).

Initially transcribed by Gemma 3 and manually corrected by koppanyh.

### Page 1

| Eurocomp GmbH <br> ELEKTRONISCHE RECHENANLAGEN | LGP-30 <br> Programmbeschreibung |
|---|---|
| PROGRAMMEINGABE <br> (ursprünglich: 10.3, abgeändert vom Rice Institute) | 10.4 |

Die Hauptfunktionen dieses Planes ist das Einlesen von Programmen (von Lochstreifen oder von Hand). Ein Programm besteht aus Befahls- und Datenwörtern. Der vorliegende Plan behandelt ausschließlich Befehle und hexadezimale Daten. Dezimale Zahlen können nicht durch 10.4 eingelesen werden.

1.  Am einfachster ist die Eingabe von Befehlen in den LGP-30, wenn sie dual verschlüsselt sind. Da aber das Programmieren in diesem System recht schwierig ist, zieht man die dezimale Schreibweise vor.  Dann muß man aber für eine nachträgliche Umwandlung im Dualsystem sorgen, da die Befehlsadressen dual gespeichert werden müssen.

2.  Die meisten Programme enthalten Befehle, die sich auf Stellen dieser Programme beziehen. Will man nun die Anfangsadresse eines Programmes offen lassen (das ist z. B. bei Unterprogrammen die Regel), so muß man solche. Adressen umrechnen (modifizieren).

3.  Manchmal ist es sehr vorteilhaft, Konstanten, die im Programm benötigt werden, von Hand ins Dualsystem zu übertragen und im Programm einzubauen. Will man dezimale Befehle und hexadezimale Daten nebeneinander eingeben, muß ein Kennzeichen für hexadezimale (oder dezimale) Wörter existieren.

4.  Gelegentlich (besonders während des Testens) ist es notwendig, Daten oder Befehle eines gespeicherten Programmes zu ändern.

Der vorliegende Plan 10.4 erlaubt, die unter 1 bis 4 beschriebenen Arbeiten in einfacher Weise durchzuführen. Er benutzt

10.4-1/6

### Page 2

dazu sieben Typen von Codewörtern. Sie bestehen sämtlich aus 8 Zeichen, von denen einige dezimale Ziffern sein können (z. B. dezimale Adressen). Das erste der acht Zeichen bestimmt den Typ des Codewortes. Nach der Eingabe wird es entschlüsselt und der entsprechende Teil des Programmes aufgerufen. Im folgenden werden die Codewörter und die von ihnen ausgelösten Funktionen beschrieben.

1. **Befehl (0)**
   Die Adresse des Befehls wird dualisiert und der ganze Befehl in einer gegebenen Zelle gespeichert. Steht vor dem Operationsteil kein x, so wird die Adresse zuvor um den Inhalt des Modifiers (s. unter 4) erhöht (relative Adresse). Andernfalls unterbleibt die Modifizierung (absolute Adresse). Z. B. wird der Befehl b 2436 modifiziert, xC 6300 dagegen nicht. Das x wird nicht gespeichert.

2. **Command (+)**
   Die letzten sieben Stellen dieses Codewortes werden von 10.4 als Befehl aufgefaßt. Dieser wird ausgeführt, wenn das folgende Wort im ACC steht. Die Befehlsadresse des Commandwortes ist dezimal und wird nicht modifiziert. Das Objekt des Commandbefehls (das folgende Wort) wird als hexadezimal angesehen. Beispiel: Das Codewort +00C6314 gefolgt von 73W08 veranlaßt den Plan, das hex. Wort 00073W08 in Sektor 14 von Spur 63 zu speichern.

3. **Start fill (;)**
   Das Codewort gibt an, in welcher Zelle das nächste Befehlsoder Datenwort gespeichert werden soll. Die nachfolgenden Wörter werden in aufeinanderfolgenden Zellen gespeichert, bis ein Codewort ihre Folge unterbricht. Der Adreßteil des Codewortes ist dezimal und besteht aus Spur- und Zellennummer. Beispiel: Das Codewort: ;0002035 veranlaßt den Plan das nächste Wort (nicht Codewort) in die Zelle 2035 zu legen, das folgende in 2036, das dritte in 2037 usw.

10.4-2/6

### Page 3

| Eurocomp GmbH <br> ELEKTRONISCHE RECHENANLAGEN | LGP-30 <br> Programmbeschreibung |
|---|---|
|  |  |

4. **Modifier setzen (/)**
   Die Adresse des Codewortes wird in einer Zelle gespeichert, die Modifier heißt. Sie wird zu den Adressen aller Befehlswörter addiert, deren Befehlsteil nicht durch ein vorgesetztes x kenntlich gemacht wurde. Der Modifier kann nur durch ein zweites Modifier-Codewort geändert werden. Die Adresse des Codewortes wird dezimal eingegeben. Gewönlich folgt der Modifier dem Start-fill und besitzt die gleiche Adresse. Beispiel: Das Codewort /0001500 veranlaßt den Plan, alle relativen Adressen der noch einzulesenden Befehlswörter um 1500 zu erhöhen. So wird aus B 2738 der Befehl B 4238, während xH 6300 unverändert bleibt.

5. **Halt und Sprung (.)**
   Dieses Codewort bewirkt zwei Dinge. Zunächst wird die Maschine gestoppt. Nach Betätigung des Startknopfes erfolgt ein Sprung zu der Zelle, die durch die Adresse des Codewortes bestimmt ist. Das Anhalten kann durch Niederdrücken des Schalters "KEIN HALT 32" verhindert werden. Beispiel: Das Codewort .0001700 erzwingt einen Stop; nach erneutem Start erfolgt ein Sprung zum Sektor 00 von Spur 17.

6. **Hexadezimale Wörter (,)**
   Dieses Codewort veranlaßt das Programm, die nächsten Wörter als hexadezimale Konstanten zu speichern (die Umrechnung des Adreßteiles unterbleibt). Die Anzahl der hex. Wörter wird durch den Sektorteil der Adresse des Codewortes angegeben (der Spurteil ist immer Null). Beispiel: Das Codewort ,0000014 veranlaßt den Plan, die nächsten 14 Wörter als hex. Wörter zu speichern. Mit einem Codewort können bis zu 63 hex. Wörter eingelesen werden.

7. **Hex. fill (v)**
   Dieses Codewort veranlaßt die Maschine, die nächsten n Wörter zu lesen und als hex. Daten in aufeinanderfolgenden Zellen, beginnend bei m, zu speichern (m und n sind hexadezimale

10.4-3/6

### Page 4

Zahlen). Während des Einlesens werden die dualen Wörter addiert; aus ihnen wird eine Kontrollsumme gebildet. Nach der Eingabe aller m Wörter vergleicht die Maschine die errechnete Zahl mit der Kontrollsumme von Lochstreifen. Durch Niederdrücken des Schalters "SPRUNG" kann man den Test verhindern. Sind die Zahlen gleich, so ist die Operation beendet; andernfalls stoppt die Maschine und druckt "error". Das Codewort hat die folgende Form:

V n n n m m m m

nnn ist die hex. Anzahl der einzulesenden Wörter und mmmm die hex. Adresse für das erste Wort. Beispiel: V1J02W00 heißt: die nächsten 448 Wörter werden eingelesen und in Zelle 4700 und folgende gespeichert. Mit einem Codewort können bis zu 2047 hex. Wörter eingegeben werden.

Allgemeines:
Linksseitige Nullen brauchen nicht mitgelocht zu werden, da der Akkumulator vor jeder Eingabe gelöscht wird. Alle anderen Nullen müssen eingegeben werden. Z. B.: / 0001700 muß vollständig gelocht werden, von 000B1700 braucht nur B1700 gelocht werden. Wenn die Maschine ein fehlerhaftes Codewort liest, führt sie einen Wagenrücklauf durch, druckt "error" und stoppt. Das letzte gelesene Wort enthält den Fehler.

Während der Eingabe führt die Maschine keinen Wagenrücklauf durch. Diese müssen im Streifen enthalten sein. Fehlen einige Rücklaufsymbole auf den Streifen, kann ein Stopp die Folge sein. Nach Betätigung der Wagenrücklauftaste fährt die Maschine mit Einlesen ohne Fehler fort.

Zeitbedarf:
Eine Spur kann in 60-79 sec. mit Befehlen gefüllt werden. Bei Eingabe mit Hex. fill wird eine Spur in 50-60 sec. gefüllt.

10.4-4/6

### Page 5

| Eurocomp GmbH <br> ELEKTRONISCHE RECHENANLAGEN | LGP-30 <br> Programmbeschreibung |
|---|---|
|  |  |

Speicherbedarf:
Die Routine belegt die Spuren 00 bis 03 und benutzt keine Zwischenspeicher aus Spur 63.

Halt:
Die Maschine stoppt bei 0062, wenn ein fehlerhaftes Codewort gelesen wird oder wenn die Kontrollsummen nicht gleich sind.

Im folgenden bedeutet tt eine Spur-Nr. ss eine Sektor-Nr. und W einen der 16 LGP-30 Befehle.

| Codewort | Interpretation |
|---|---|
| 000Wttss | modifizierter Befehl |
| 00xWttxx | nicht modifizierter Befehl |
| 800Wttss | modifizierter negativer Befehl |
| 80xWttss | nicht modifizierter negativer Befehl |
| +00Wttss | Nach Einlesen des nächsten Wortes in den ACC wird der Befehl Wttss ausgeführt |
| ;000ttss | Das erste Eingabewort wird in Zelle ttss gespeichert |
| /000ttss | Die Adresse ttss wird gespeichert und zu allen Adressen der folgenden Befehle addiert, wenn diese nicht durch ein "x" kenntlich gemacht wurden. |
| .000ttss | Die Maschine stoppt, wenn Schalter "KEIN HALT 32" nicht niedergedrückt ist. Bei Betätigung des Startknopfes springt sie nach Zelle ss der Spur tt. |
| ,00000NN | Die nächsten NN Wörter werden hexadezimal gespeichert, für NN gilt die Bedingung 1 ≤ NN ≤ 63. |

10.4-5/6

### Page 6

V nnn mmmm

Die nächsten nnn Wörter werden in aufeinanderfolgenden Zellen, beginnend mit der Adresse mmmm, gespeichert. Während des Einlesens wird eine Kontrollsumme berechnet, die mit einer hex. Zahl des Lochstreifens verglichen wird. Bei gedrücktem Schalter "SPRUNG" unterbleibt das Lesen und Vergleichen der Kontrollsumme. nnn und mmmm sind hex. Zahlen mit 1 ≤ nnn ≤ 2047.

10.4-6/6
