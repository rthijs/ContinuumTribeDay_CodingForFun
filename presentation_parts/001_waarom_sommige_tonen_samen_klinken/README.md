# Waarom sommige tonen goed samen klinken

Dit is een deel van de presentatie voor de Continuum tribe day.

## De grondtoon

De laagste frequentie waarmee een snaar kan trillen, de golflengte is het dubbel van de lengte van de snaar. Bij conventie is de la vastgelegd op 440Hz dus laten we met deze beginnen. In Supercollider start de server en speel een sinus van 440Hz:

```
s.boot; //boot server

{ SinOsc.ar(440, 0, 0.5) }.play; //play 440Hz sine wave, parameters are frequency, phase and amplitude multiplicator
```

Stop het afspelen door ctrl+. in te drukken.

Op een osciloscoop, in dit geval x42-scope, ziet dat er zo uit:

![grondtoon](images/grondtoon_440Hz.png "Grondtoon")

Ik heb de twee cursors gezet op het begin en einde van een volledige golf, onderaan kan je zien dat dit overeenkomt met 440Hz (de 0,4 is een meetfoutje door de resolutie waarop we werken).

Nu samen met deze noot willekeurige andere noten spelen klinkt waarschijnlijk niet aangenaam. Welke tonen gaan wel goed samen?

## Het oktaaf

De eerste boventoon is de noot waarvan de frequentie het dubbel is van de grondnoot. Er passen dus precies 2 golven in 1 golf van de grondnoot oftewel een verhouding van 2:1.

```
{ var grondtoon = 440;
	[ 
		SinOsc.ar(grondtoon, 0, 0.5),
		SinOsc.ar(grondtoon * 2, 0, 0.5)
	]
}.play; 
```

![oktaaf](images/oktaaf.png "Oktaaf")

In het groen de grondtoon, in het rood het oktaaf en in het blauw de som van de twee. De som is ook het signaal dat naar de speakers gaat.




