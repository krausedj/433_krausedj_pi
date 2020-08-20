#!/usr/bin/env python3 

import argparse
from wavepitools import *

parser = argparse.ArgumentParser(description='Trim and remove offests from waves')
parser.add_argument('--remove_offset', '-r', action='store_true', help='Remove the offset from the input file')
parser.add_argument('--vcd', action='store_true', help='output in vcd format')
parser.add_argument('input', type=str, help='input file to read from')
parser.add_argument('output', type=str, help='output file to read from')

args = parser.parse_args()

wave = Wave.load_csv(args.input)

if args.remove_offset != False:
    wave.remove_offset()

if args.vcd != False:
    wave.save_vcd(args.output)
else:
    wave.save_csv(args.output)