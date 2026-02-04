# kopForth

This is a port of the
[kopForth v0.3](https://github.com/koppanyh/kopForth/tree/v0.3)
interpreter made to run on the LGP-30.

Due to major architectural differences between the LGP and modern processors,
this isn't an exact 1-to-1 port, but it should be mostly similar. It is also not
implementing all of the words found in the official kopForth due to memory
constraints.

## Build Instructions

Run the `main.py` program which will link all the kopForth libraries together
and emit the tape program.

Example command to save to tape file:
`python main.py > kopForth.tx`

## Run Instructions

Within Simh, run the following:
```
load kopForth.tx
set cpu manual
set cpu 6b
co
```

Alternatively, call Simh with the `kopForth.simh` file as an input.

[Simh builds](https://github.com/simh/Development-Binaries) can be found here
and contain the `lgp.exe` emulator executable used to develop this port.

## Quickstart

### Text Entry

Due to the strangeness of how text input works on the LGP-30, text must be
entered with no more than 5 characters at a time.

This is because LGP text input works by shifting the accumulator left 6 bits,
then writes the current 6 bit character input into the now-empty lower 6 bits.
This is a hardware behavior.

As such, the 31-ish bit words of the LGP can hold 5 6-bit characters each.

The input characters are also limited to the following set: `0123456789fgjkqwzbyridnmpeuthcas +-;/.,vox` \
With `1` and `l` being the same character.

There is also no backspace, so don't mess up...

Simh presents text input as starting with a backtick:
```
`
```
And you finish entering characters by terminating with a single quote: `'`.

Enter individual words (i.e. tokens) as groups of 5 characters separated by a single space token. \
For example, `5 compile,` would look like this:
```
`5'` '`compi'`le,'`'
```
The empty token at the end tells this port to process the line.

It's important that larger words be grouped in 5 characters, since
```
`compi'`le,`
```
Is treated as a different word than
```
`comp'`ile,'
```

### Words

The following words are implemented in this forth. If a word is in the `LGP`
column, then use that name when referencing the word. Words that are not in
the `Standard` column are specific to this forth implementation. Words with a
`*` in the last column are not standard compliant (mostly due to memory architecture differences).

| Standard      | LGP           |   |
|---------------|---------------|---|
| exit          |               |   |
|               | literal-c     |   |
| -             |               |   |
| .             |               |   |
| @             | peek          |   |
| !             | poke          |   |
| c@            | c-peek        | * |
| c!            | c-poke        | * |
| >r            | r-push        |   |
| r>            | r-pop         |   |
| drop          |               |   |
| dup           |               |   |
| swap          |               |   |
|               | branch        |   |
|               | 0branch       |   |
| emit          |               | * |
| key           |               | * |
| accept        |               | * |
| type          |               | * |
|               | create-c      |   |
| find          |               |   |
| =             | eq            |   |
| <             | lss           |   |
|               | nand          |   |
|               | s-quot-c      |   |
| .s            |               |   |
| dump          |               |   |
|               | clr-in-source |   |
|               | clr-ret-stack |   |
|               | clr-dat-stack |   |
|               | err-not-imp   |   |
|               | err-name-long |   |
| cells         | num2addr      |   |
|               | addr2num      |   |
|               | halt          |   |
|               | nodebug       |   |
|               | yesdebug      |   |
|               | dp            |   |
|               | lp            |   |
|               | pp            |   |
| state         |               |   |
|               | srcpt         |   |
| >in           | in-ptr        |   |
| #tib          | tib-len       |   |
|               | tp            |   |
|               | debug         |   |
| here          |               |   |
| latest        |               |   |
| pad           |               |   |
|               | tib-end       |   |
| true          |               |   |
| false         |               |   |
| source-id     |               |   |
| tib           |               |   |
|               | tib-avail     |   |
| over          |               |   |
| rot           |               |   |
| 2drop         |               |   |
| 2dup          |               |   |
| +             |               |   |
| invert        |               |   |
| or            |               |   |
| and           |               |   |
| 0=            | 0eq           |   |
| >             | gtr           |   |
| >=            | geq           |   |
| r@            | r-peek        |   |
| rshift        |               |   |
| +!            | +poke         |   |
| allot         |               | * |
| ,             |               |   |
| compile,      |               |   |
| execute       |               |   |
| move          |               | * |
| cr            |               |   |
| bl            |               | * |
| space         |               |   |
| count         |               |   |
| /string       |               |   |
|               | xt-skip       |   |
|               | spread-chars  |   |
|               | is-digit      |   |
|               | 10*           |   |
| >number       | to-number     |   |
|               | s-to-number   |   |
| abort         |               |   |
| source        |               |   |
| refill        |               |   |
|               | skipchar      |   |
|               | isskipchar    |   |
|               | isnotskipchar |   |
| parse-name    |               |   |
|               | padword       |   |
| word          |               |   |
|               | err-not-found |   |
| [             | intp-mode     |   |
| ]             | comp-mode     |   |
| >name         | name-ptr      |   |
| >flags        | flags-ptr     |   |
|               | err-not-intp  |   |
|               | interpret     |   |
| quit          |               |   |
| reveal        |               |   |
| >link         | link-ptr      |   |
| >code         | code-ptr      |   |
| >body         | body-ptr      |   |
|               | unreveal      |   |
|               | dodoes        |   |
|               | does-def-c    |   |
| does>         | does-def      |   |
| create        |               |   |
| :             | def           |   |
| ;             |               |   |
| immediate     |               |   |
|               | compile-only  |   |
| if            |               |   |
| then          |               |   |
| else          |               |   |
| i             |               |   |
|               | do-c          |   |
| do            |               |   |
| leave         |               |   |
|               | +loop-c       |   |
| +loop         |               |   |
| loop          |               |   |
| begin         |               |   |
| again         |               |   |
| until         |               |   |
| while         |               |   |
| repeat        |               |   |
| bye           |               |   |
