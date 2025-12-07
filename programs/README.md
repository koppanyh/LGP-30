# Programs

## bkjck.tx

This is a copy of the blackjack program from [The Story of Mel](https://www.pbm.com/~lindahl/mel.html)

Copied from here: ftp://ftp.informatik.uni-stuttgart.de/pub/cm/lgp30/papertapes/Games/bkjck.tx

### How to run

```
$ lgp.exe

LGP30 simulator V4.0-0 Current        git commit id: 670a3728
sim> load bkjck.tx
sim> set cpu manual
sim> go 4500


STOP, C: 5062 (P 1600)
sim> co


        5 - c|  7 - s
|       4 - s
Card? `
```

### How to play

Not entirely sure how it works, but you type in `yes'` to get a new card and `no'` when you're done, then it somehow does blackjack things and gives you a score, then the program stops.

```
        5 - c|  7 - s
|       4 - s
Card? `yes'     9 - s
Card? `no'      |       Q - h|
        tota1 - 18      |tota1 - 17|    score = $1.00

STOP, C: 5062 (P 1600)
```

To keep going, use the `co` command.
