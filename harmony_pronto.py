#!/usr/bin/python

from ctypes import *
import libconcord
import sys

class HarmonySession():
    def __init__(self, filename):
        xml = POINTER(c_ubyte)()
        xml_size = c_uint()
        libconcord.read_file(
            filename,
            byref(xml),
            byref(xml_size)
        )

        filetype = c_int()
        libconcord.identify_file(xml, xml_size, byref(filetype))
        filetype = filetype.value
        if filetype != libconcord.LC_FILE_TYPE_LEARN_IR:
            raise Exception('"%s" is not a file for learning IR codes (type %s, not %s)' % (filename, str(filetype), str(libconcord.LC_FILE_TYPE_LEARN_IR)));
        self.xml = xml
        self.xml_size = xml_size
        
        key_names = POINTER(c_char_p)()
        key_names_length = c_uint()
        libconcord.get_key_names(
            xml,
            xml_size,
            byref(key_names),
            byref(key_names_length)
        )
        try:
            self.key_names = []
            for i in range(key_names_length.value):
                self.key_names.append(key_names[i] + '')
        finally:
            libconcord.delete_key_names(key_names, key_names_length)
        
    def __str__(self):
        return str(self.__dict__)
    
    def post_code(self, irCode, keyname):
        post_string = c_char_p()
        libconcord.encode_for_posting(
            irCode.ir_carrier_clock,
            irCode.ir_signal,
            irCode.ir_signal_length,
            post_string
        )

        try:
            libconcord.post_new_code(
                    self.xml,
                    self.xml_size,
                    keyname,
                    post_string
                )
        finally:
            libconcord.delete_encoded_signal(post_string)
        

class IRCode():
    def __init__(self, pronto_code_string):
        bin = []
        str = ""
        str_idx = 0

        hex = pronto_code_string.strip().split(' ')
        for h in hex:
            b = int(h, 16)
            bin.append(b)

            str += "%04x " % b
            str_idx += 1
            if str_idx == 12:
                str += "\n"
                str_idx = 0

        if len(bin) < 4:
            raise Exception('Pronto code too short (missing header)')

        if bin[0] != 0:
            raise Exception('Not RAW')

        pronto_clock = 4145146
        # IR carrier frequency is given as number of Pronto clock cycles
        frequency = int(pronto_clock / bin[1])
        # Mark/space durations are given as a count of IR carrier cycles,
        # but we need them in microseconds
        carrier_cycle_us = 1000000.0 / frequency

        count_1 = 2 * bin[2]
        count_2 = 2 * bin[3]

        if len(bin) < 4 + count_1 + count_2:
            raise Exception('Pronto code too short (missing pulsetrain)')

        start_1 = 4
        start_2 = 4 + count_1

        repeats = 4
        count = count_1 + (repeats * count_2)

        self.ir_carrier_clock = c_uint(frequency)
        self.ir_signal = (c_uint * count)()
        self.ir_signal_length = c_uint(count)

        idx = 0

        for i in range(count_1):
            self.ir_signal[idx] = int(bin[start_1 + i] * carrier_cycle_us)
            idx += 1

        for j in range(repeats):
            for i in range(count_2):
                self.ir_signal[idx] = int(bin[start_2 + i] * carrier_cycle_us)
                idx += 1
    
    
    def __str__(self):
        s =     ['Carrier clock:          %u Hz\n' % self.ir_carrier_clock.value]
        pairs = self.ir_signal_length.value/2
        s.append('Total mark/space pairs: %u\n\n' % pairs)
        for i in range(pairs):
            mark = self.ir_signal[2*i]
            if mark < 250:
                s.append('|')
            elif mark < 1000:
                s.append('#')
            else:
                s.append('##')
            space = self.ir_signal[2*i+1]
            if space < 250:
                s.append('.')
            elif space < 1000:
                s.append('_')
            elif space < 10000:
                s.append('__')
            else:
                s.append('\n')
        return ''.join(s)
    
def main():
    filename = sys.argv[1]
    session = HarmonySession(filename)
    print ("Learning %i keys" % len(session.key_names))
    for keyname in session.key_names:
        print ("Please paste Pronto code for key '%s', all on one line:" % keyname)
        line = sys.stdin.readline()
        if not line:
            return
        irCode = IRCode(line)
        print irCode
        print "Uploading code"
        session.post_code(irCode, keyname)
        print "Success!"

if __name__ == '__main__':
    main()
