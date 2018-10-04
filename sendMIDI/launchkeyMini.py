#!/usr/bin/env python3

import launchpad_py
import time

from pygame import midi

def main():
    lk = launchpad_py.LaunchKeyMini()

    lk.Open(0,"LaunchKey")

    lk.ButtonFlush()

    print(" - Available methods:")
    for mName in sorted( dir( lk ) ):
        if mName.find("__") >= 0:
            continue
        if callable(getattr(lk, mName)):
            print("     "+ str(mName) + "() ")

    midi.init()

    player = midi.Output(0)
    #player.set_instrument(0, 15)
    #player.note_on(15, 127, 15)
    #time.sleep(1)
    player.note_on(15, 0x1F, 9)
    time.sleep(1)
    #del player
    #midi.quit()

    #for x in range(128):
    #    player.note_on(x, 127, 15)
    #    time.sleep(0.1)

if __name__ == '__main__':
    main()