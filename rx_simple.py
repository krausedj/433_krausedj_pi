#!/usr/bin/env python3
import pigpio
from wavepitools import *

class WaveListener(object):
    def __init__(self):
        self.last_cbk_tick = 0
        self.state = 1
        self.total_cbks = 0
        self.wave = Wave()

    def rx_cbk(self, gpio, level, tick):
        self.last_cbk_tick = tick
        self.total_cbks = self.total_cbks + 1
        if level != 2:
            #Dont update if this is just a watchdog timeout
            self.state = level
        self.wave.points.append(Point(state=bool(self.state), time_us=tick))

    def reset_wave(self):
        self.wave = Wave()
    
    def save(self, file_name):
        with open(file_name, 'w') as file_ptr:
            for point in self.wave.points:
                file_ptr.write("{0},{1}\n".format(point.time_us,int(point.state)))
        self.wave = Wave()

wave_lis = WaveListener()
pi = pigpio.pi()
pi.set_mode(17, pigpio.INPUT)
pi.set_pull_up_down(17, pigpio.PUD_OFF)
pi.set_glitch_filter(17, 20)
pi.callback(17, pigpio.EITHER_EDGE, wave_lis.rx_cbk)

cmd = None
while cmd != 'x':
    if cmd == 't':
        print('Total Callbacks: {0}'.format(wave_lis.total_cbks))
    elif cmd == 'f':
        file_name = input("Filename: ")
        wave_lis.save(file_name)
        wave_lis.reset_wave()
    elif cmd == 'r':
        wave_lis.reset_wave()
    else:
        print('h: help\nx: exit\nr: reset collected data\nt: print current callback count\nf: save current data to csv file and restart wave from scratch\n')
    cmd = input("Input Command: ")

pi.stop()

