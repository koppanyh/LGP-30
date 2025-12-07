# LGP-30 P104 Documentation

## Transcription

These are the pages from the official papertapes/P104/p10_4_0{n}.pdf files found on ftp://ftp.informatik.uni-stuttgart.de/pub/cm/lgp30/papertapes/P104/

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
