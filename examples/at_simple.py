#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# at_simple.py
# simple usage of ATProtocol
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

import serial
from at_protocol import ATProtocol

def test_simple(*args, **kw):
	ser = serial.serial_for_url(*args, **kw)
	reader = serial.threaded.ReaderThread(ser, ATProtocol)
	reader.start()
	at = reader.protocol
	print(at.command('AT', timeout=1))
	print(at.multiline('ATI'))
	print(at.singleline('AT+CSQ', '+CSQ:'))
	reader.close()

if __name__ == '__main__':
	test_simple('/dev/ttyUSB0', baudrate=115200)
