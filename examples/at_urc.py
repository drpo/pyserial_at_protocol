#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# at_urc.py
# URC handler in ATProtocol
# Copyright (C) 2019  Dr. PO <drpo@users.noreply.github.com>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import time
import serial
from at_protocol import ATProtocol

def urc_creg(line):
	print("creg:", line)
	quit()

# some modem don't report +CREG
def test_urc(*args, **kw):
	ser = serial.serial_for_url(*args, **kw)
	with serial.threaded.ReaderThread(ser, ATProtocol) as at:
		at.register('+CREG', urc_creg)
		at.command('AT+CREG=1', timeout=1)
		at.command('AT+CFUN=0')
		at.command('AT+CFUN=1')
		print('waiting for +CREG...')
		time.sleep(30)

if __name__ == '__main__':
	test_urc('/dev/ttyUSB0', baudrate=115200)
