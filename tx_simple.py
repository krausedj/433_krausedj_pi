#!/usr/bin/env python3
import pigpio
from wavepitools import *
import time

wave = Wave.load_csv('data/on_zeroed.csv')

gpio_pin = 27

pulse_list = []

last_time = wave.points[0].time_us

for point in wave.points:
    delta_time = point.time_us - last_time
    if point.state == 0:
        pulse_list.append(pigpio.pulse(0, 1<<gpio_pin, delta_time))
    else:
        pulse_list.append(pigpio.pulse(1<<gpio_pin, 0, delta_time))

pi = pigpio.pi()
pi.wave_clear()
pi.wave_add_generic(pulse_list)
wave_pi = pi.wave_create()
pi.wave_send_repeat(wave_pi)
time.sleep(2)
pi.wave_stop_tx()
pi.wave_clear()
pi.stop()