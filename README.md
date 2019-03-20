---
output: html_document
---

# Berry Buster

Berry Buster ist eine Revisited Version des Spieles Brick Breaker. Erstellt wurde dieses im Rahmen der Veranstaltung Ingenieurwissenschaften für Psychologen Human Factors WS2018/2019 von Ulrike Schäfer und Jenny Iseev.

Im folgenden werder alle wichtigen Notwendigkeiten und Bedingungen erläutert.

## Notwendigkeiten

Notwendig ist ein Raspberry Pi (geschrieben für Version 3B) mit installiertem Noobs, ein GrovePi und benötigte Hardware, welche in Hardware.png dargestellt wird inklusive Angaben für Sensoranschlüsse.
Geschrieben wurde in PyCharm und Geany. Gestartet werden kann der Berry Buster wie jedes andere Script. Daraufhin wird der Screen komplett ausgefüllt. Wie die Spielsteuerung/abbruch funktionieren wird im Tutorial ingame und in der PDF Poster_aufbau.pdf erläutert.
Zu beachten ist zudem, dass die Steuerung verändert ausgelegt ist, da ein Numpad verwendet wurde, es allerdings der Usability dienlicher ist, wenn mit dem Befehl ähnelnden Tasten gearbeitet wird. Daher wurden genutzte Taste überklebt. In der angehängten Dokumentation des Projektes befinden sich Bilder, wodurch dies imitierbar ist. Zudem können die Tasten im Code einfach ersetzt werden.

```
Betriebssystem:
noobs

Hardware:
RPi 3B + Ladekabel + SD-Karte
GrovePi+
  Distanzsensor (Ultrasonic)
  LED (drei wahlweise rot, grün und blau)
  LED-String
  Rotationssensor 1
  Rotationssensor 2
  Lichtsensor 
  mind. 8 Sensorkabel
Display (garantierte Bildauflösung 800x600pix; getestet auf 17 Zoll Display) + Ladekabel
HDMI-Kabel von RPi zu Display 
3.5-Klinken-Audiokabel
Numpad
Maus (falls benötigt zum starten des Scriptes; keine Verwendung InGame)

```

## Installing

Wie bereits erwähnt sollten Noobs und beispielsweise Geany als Interpreteur bereits installiert sein.
Wichtig ist zudem, dass mit Python 3.0+ gearbeitet wird, dieses sollte sowohl installiert als auch im Interpreteur ausgewählt sein.
```
sudo apt-get install python3
```

Des Weiteren werden folgende libraries benötigt:

```
import pygame
from pygame.locals import *
from pygame import *
import time
from random import randint
import csv
import grovepi as *
```
Teils werden diese vorinstalliert vorhanden sein, ansonsten kann mittels Terminal eine Installation vorgenommen werden.

## Software- und Quellenlinks

* [Noobs](https://www.raspberrypi.org/downloads/noobs/) - Betriebssystem RPi 3B
* [Geany](https://www.geany.org/download) - Interpreter Python
* [Krita](https://krita.org/en/) - Grafikdesign - verwendet für ingame Design
* [Credits - code](https://stackoverflow.com/questions/36164524/python-pygame-create-end-credits-like-the-ones-at-the-end-of-a-movie?rq=1) - Code für Credits - abgeleitet von stackoverflow von sloth
* [Mathematische Grundlage für Abprall-Berechnung](https://www.youtube.com/watch?v=uuww9w2W-c0) - Berechnungsgrundlage


## Versionierung

Versioning hatte keine Priorität, da es sich um ein kleiner Projekt handelt.
Es erfolgte lediglich eine Unterteilung in RPi Version mit und eine PC Version ohne Sensoren. Hierbei handelt es sich dabei um die RPi-Version. 

## Autoren

* **Ulrike Schäfer** - *Initial work* - [Akimasu](https://github.com/Akimasu)
* **Jenny Iseev** - *Initial work*

## Lizenz

Dieses Projekt ist unlizensiert [LICENSE.md](LICENSE).

## Danksagungen

* Freunde und Familie :)
* Inspiration waren alle bisherigen Brick Breaker, ohne denen wir sicherlich nicht auf diese Idee gekommen wären.

