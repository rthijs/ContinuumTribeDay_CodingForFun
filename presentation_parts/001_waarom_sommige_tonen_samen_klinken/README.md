# Waarom sommige tonen goed samen klinken

Dit is een deel van de presentatie voor de Continuum tribe day.

## De grondtoon

De laagste frequentie waarmee een snaar kan trillen, de golflengte is het dubbel van de lengte van de snaar. Bij conventie is de la vastgelegd op 440Hz dus laten we met deze beginnen. In Supercollider start de server en speel een sinus van 440Hz:

'''
s.boot; //boot server

{ SinOsc.ar(440, 0, 0.5) }.play; //play 440Hz sine wave, parameters are frequency, phase and amplitude multiplicator
'''

Op een osciloscoop, in dit geval x42-scope, ziet dat er zo uit:

[[https://github.com/rthijs/ContinuumTribeDay_CodingForFun/blob/master/presentation_parts/001_waarom_sommige_tonen_samen_klinken/images/grondtoon_440Hz.png|alt=grondtoon]]

Ik heb de twee cursors gezet op het begin en einde van een volledige golf, onderaan kan je zien dat dit overeenkomt met 440Hz (de 0,4 is een meetfoutje door de resolutie waarop we werken).