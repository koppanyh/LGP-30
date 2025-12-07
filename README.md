# LGP-30

My collection of stuff related to the LGP-30 computer.

# Resources

- [Simh builds](https://github.com/simh/Development-Binaries) (contains lgp.exe emulator executable)
- [Using the SIMH LGP-30 emulator](https://obsolescenceguaranteed.blogspot.com/2016/06/using-simh-lgp-30-emulator.html)
- [LGP-30 Wikipedia entry](https://en.wikipedia.org/wiki/LGP-30)
- [Online LGP-30 emulator](https://lgp30.org/) (still very much a work in progress at the time of writing this, still fun to play with though)
  - [The source code for this emulator](https://github.com/WizardOfHaas/LGP-30)
- An FTP archive of assorted LGP-30 things: ftp://ftp.informatik.uni-stuttgart.de/pub/cm/lgp30/
- An FTP archive of LGP-30 manuals: ftp://bitsavers.informatik.uni-stuttgart.de/pdf/royalPrecision/LGP-30/

# Documentation

The `docs` folder contains some PDFs about how to operate the LGP-30.

The `P104` folder within has a translation of the German documentation to English.

# Assembler

I wrote a weird assembler thingy that'll output tape programs in the P104 format.
It's basically a Python library for writing programs that'll generate programs.
This can be found in the `assembler` folder.