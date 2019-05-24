# -*- coding: utf-8 -*-
#
# at_protocol.py
# AT command protocol with pyserial
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

import logging
import threading

import serial
import serial.threaded


class ATProtocol(serial.threaded.LineReader):
	COLON = ':'

	# V.250 – Result codes, https://www.itu.int/rec/T-REC-V.250-200307-I/en
	RESULT_CODE = {
		'OK': 0,
		'CONNECT': 1,
		'RING': 2,
		'NO CARRIER': 3,
		'ERROR': 4,
		'NO DIALTONE': 6,
		'BUSY': 7,
		'NO ANSWER': 8,
	}

	TERMINATOR = b'\r\n'

	def __init__(self):
		super().__init__()
		self.urc_handler = {}
		self.lines = []
		self.final = threading.Condition()
		self.waiting = False

	@classmethod
	def result_code(cls, line):
		'''result code of line in ITU-T V.25ter, return -1 if line is not a result code'''
		return cls.RESULT_CODE[line] if line in cls.RESULT_CODE else -1

	@classmethod
	def is_final(cls, line):
		'''return True if line is the final response'''
		if cls.COLON in line:
			prefix, extra = line.split(cls.COLON, 1)
			if prefix in ('+CME ERROR', '+CMS ERROR'):
				logging.warning('got error: %s', line)
				return True
		return cls.result_code(line) >= 0

	def handle_line(self, line):
		if not line: return
		with self.final:
			if not self.waiting:
				self.handle_urc(line)
				return
			self.lines.append(line)
			if self.is_final(line):
				self.final.notify()

	def handle_urc(self, line):
		if cls.COLON in line:
			prefix = line.split(cls.COLON, 1)[0]
			if prefix in self.urc_handler:
				self.urc_handler[prefix](line)
				return
		logging.warning('unhandled line: %s', line)

	def register(self, prefix, handler):
		'''register a URC handler for PREFIX, HANDLER has signature handler(line)'''
		self.urc_handler[prefix] = handler

	def unregister(self, prefix):
		'''unregister URC handler for PREFIX'''
		self.urc_handler.pop(prefix, None)

	def _send(self, cmd, timeout=None):
		with self.final:
			self.write_line(cmd)

			self.waiting = True
			self.final.wait(timeout)
			self.waiting = False

			resp = self.lines
			self.lines = []
			return resp

	def command(self, cmd, timeout=None):
		'''send at command CMD and return the result code'''
		resp = self._send(cmd, timeout=timeout)
		return self.result_code(resp[-1]) if len(resp) > 0 else -1

	def multiline(self, cmd, prefix='', timeout=None):
		'''send CMD and get lines with prefix PREFIX'''
		resp = self._send(cmd, timeout=timeout)
		if not resp:
			return -1
		result = self.result_code(resp[-1])
		if 0 != result:
			return result
		start = 1 if resp[0].startswith(cmd) else 0
		return list(line for line in resp[start:-1] if line.startswith(prefix))

	def singleline(self, cmd, prefix='', timeout=None):
		'''send get first line with prefix PREFIX, prefix is removed'''
		result = self.multiline(cmd, prefix=prefix, timeout=timeout)
		if not isinstance(result, list):
			return result
		return result[0][len(prefix):].strip() if len(result) > 0 else None

