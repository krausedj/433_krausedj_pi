#!/usr/bin/env python3

import pigpio
import time

def rx_cbk(gpio, level, tick):
    print("Event {1} {0}\n".format(tick, level) )

pi = pigpio.pi()
pi.set_mode(17, pigpio.INPUT)
pi.set_pull_up_down(17, pigpio.PUD_OFF)
pi.set_glitch_filter(17, 20)
pi.callback(17, pigpio.EITHER_EDGE, rx_cbk)

input("Press a key to exit\n")

pi.stop()
