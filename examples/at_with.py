#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# at_with.py
# ATProtocol and with statement
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

def test_with(*args, **kw):
	ser = serial.serial_for_url(*args, **kw)
	with serial.threaded.ReaderThread(ser, ATProtocol) as at:
		print(at.command('AT', timeout=1))
		print(at.multiline('ATI'))
		print(at.singleline('AT+CSQ', '+CSQ:'))
		print(at.singleline('AT+CGSN'))

if __name__ == '__main__':
	test_with('/dev/ttyUSB0', baudrate=115200)
