#!/usr/env/bin python3
import pigpio
from wavepitools import *

class WaveListener(object):
    def __init__(self):
        self.last_cbk_tick = 0
        self.state = 1
        self.total_cbks = 0
        self.wave = wavepitools.Wave()

    def rx_cbk(self, gpio, level, tick):
        self.last_cbk_tick = tick
        self.total_cbks = self.total_cbks + 1
        if level != 0:
            #Dont update if this is just a watchdog timeout
            self.state = level
        wave.points.append(wavepitools.Point(state=bool(self.state), time_us=tick))

    def reset_wave(self):
        self.wave = wavepitools.Wave()
    
    def save(self, file_name):
        with open(file_name, 'w') as file_ptr:
            for point in wave.points:
                file_ptr.write(str(point))
                file_ptr.write('\n')

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
    else if cmd == 'f':
        file_name = input("Filename: ")
        wave_lis.save(file_name)
        wave_lis.reset_wave()
    else if cmd == 'r':
        wave_lis.reset_wave()
    else:
        print('h: help\nx: exit\nr: reset collected data\nt: print current callback count\nf: save current data to csv file and restart wave from scratch\n')
    cmd = input("Input Command: ")

pi.stop()

