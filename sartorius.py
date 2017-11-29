# -*- coding: utf-8 -*-

"""
Python Interface for
Sartorius Serial Interface for
CPA, GCA and GPA scales.

Originally by Robert Gieseke - robert.gieseke@gmail.com
Modified by Zhen Kang Pang - zhenkangpang@gmail.com
See LICENSE.
"""

import serial

class Sartorius(serial.Serial):
    def __init__(self, com_port):
        """
        Initialise Sartorius device.
            Example:
            scale = Sartorius('COM1')
        """
        serial.Serial.__init__(self, com_port)
        self.baudrate = 9600
        self.bytesize = serial.SEVENBITS
        self.parity = serial.PARITY_ODD
        self.stopbits = serial.STOPBITS_ONE
        self.xonxoff = True
        self.timeout = 0.5

    def value(self):
        """
        Return displayed scale value.
        """
        try:
            if self.inWaiting() == 0:
                self.write('\x1bP\r\n'.encode("ascii"))
            answer = self.readline().decode("ascii")
            if len(answer) == 16: # menu code 7.2.1
                answer = float(answer[0:11].replace(' ', ''))
            else: # menu code 7.2.2
                answer = float(answer[6:17].replace(' ',''))
            return answer
        except:
            return "NA"

    def display_unit(self):
        """
        Return unit.
        """
        self.write('\x1bP\r\n'.encode("ascii"))
        answer = self.readline()
        try:
            answer = answer[11].strip()
        except:
            answer = ""
        return answer

    def tare(self):
        """
        (TARE) Key.
        """
        self.write('\x1bT\r\n'.encode("ascii"))

    def block(self):
        """
        Block keys.
        """
        self.write('\x1bO\r\n'.encode("ascii"))

    def unblock(self):
        """
        Unblock Keys.
        """
        self.write('x1bR\r\n'.encode("ascii"))

    def restart(self):
        """
        Restart/self-test.
        """
        self.write('x1bS\r\n'.encode("ascii"))

    def ical(self):
        """
        Internal calibration/adjustment.
        """
        self.write('x1bZ\r\n'.encode("ascii"))
