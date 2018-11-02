#Waarom sommige tonen goed samen klinken

Dit is een deel van de presentatie voor de Continuum tribe day.

##De grondtoon

De laagste frequentie waarmee een snaar kan trillen, de golflengte is het dubbel van de lengte van de snaar. Bij conventie is de la vastgelegd op 440Hz dus laten we met deze beginnen. In Supercollider start de server en speel een sinus van 440Hz:

'''
s.boot; //boot server

{ SinOsc.ar(440, 0, 0.5) }.play; //play 440Hz sine wave, parameters are frequency, phase and amplitude multiplicator
'''

Op een osciloscoop, in dit geval x42-scope, ziet dat er zo uit: