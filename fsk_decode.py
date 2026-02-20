csvfile = "./alert1_data/two_packets.csv"
glitch = "./alert1_data/glitch_data.csv"

binfile = "./alert1_data/analog_11.bin"
# binfile = "./alert1_data/analog_alert1_msg1.bin"
# binfile = "./alert1_data/analog_iflows_2316_142.bin"
# binfile = "./alert1_data/analog_iflows2_2316_142.bin"
# binfile = "./alert1_data/analog_iflows_1_0.bin"
# binfile = "./alert1_data/analog_2316_142.bin"
# binfile = "./alert1_data/analog_8191_2047.bin"
# binfile = "./alert1_data/analog_1_0.bin"

import array
import struct
import sys
from collections import namedtuple
import csv
from fsk_interface import get_waveform, get_intervals
import matplotlib.pyplot as plt

# def remove_carrier(times, samples): # assume DC removed

def remove_dc(samples):
    sum = 0
    for sample in samples:
        sum += sample
    average = sum/len(samples)
    for i in range(len(samples)):
        samples[i] -= average
    return samples

def zero_crossings(times, samples):
    transitions = list()
    for i in range(len(samples) - 1):
        if samples[i + 1] == 0 or samples[i] * samples[i + 1] < 0:
            m = (samples[i + 1] - samples[i]) / (times[i + 1] - times[i])
            transitions.append(times[i] - samples[i] / m)
    return transitions

def get_deltas(transitions):
    return [transitions[i+1] - transitions[i] for i in range(len(transitions) - 1)]

def csv_file(csvfile): # return times and samples
    print(csvfile)
    with open(csvfile) as cf:
        rows = csv.reader(cf)
        next(rows)
        times = array.array('f')
        samples = array.array('f')
        for row in rows:
            times.append(float(row[0]))
            samples.append(float(row[1]))
    return (times, samples)

def parse_analog(f):
    TYPE_DIGITAL = 0
    TYPE_ANALOG = 1
    expected_version = 0
    AnalogData = namedtuple('AnalogData', ('begin_time', 'sample_rate', 'downsample', 'num_samples', 'samples'))

    # Parse header
    identifier = f.read(8)
    if identifier != b"<SALEAE>":
        raise Exception("Not a saleae file")

    version, datatype = struct.unpack('=ii', f.read(8))

    if version != expected_version or datatype != TYPE_ANALOG:
        raise Exception("Unexpected data type: {}".format(datatype))

    # Parse analog-specific data
    begin_time, sample_rate, downsample, num_samples = struct.unpack('=dqqq', f.read(32))

    # Parse samples
    samples = array.array("f")
    samples.fromfile(f, num_samples)

    return AnalogData(begin_time, sample_rate, downsample, num_samples, samples)

def binary_file(filename):
    print(filename)
    with open(filename, 'rb') as f:
        data = parse_analog(f)
    stime = data.downsample/data.sample_rate
    times = [data.begin_time + i * stime for i in range(data.num_samples)]
    return (times, data.samples)

def find_messages(times, samples):
    samples = remove_dc(samples)
    # plt.plot(times, samples)
    # plt.show()
    # print(*times[:10],'\n',*samples[:10])
    transitions = zero_crossings(times, samples)
    transitions.insert(0, times[0]) # add first time to get first interval
    # plt.plot(transitions)
    # plt.show()
    # print(*transitions[:10])
    deltas = get_deltas(transitions)
    deltas = remove_dc(deltas)
    # print(*deltas[:10])
    frequencies = zero_crossings(transitions, deltas)
    frequencies.append(times[-1]) # add last time to get last interval
    frequencies.insert(0, transitions[0])
    intervals = get_deltas(frequencies)
    if intervals[0] < .001: # remove any short interval
        del(intervals[0])
    bits = [round(bit/(1/300),1) for bit in intervals] # generate bit length
    print(*bits)
    bits = [int(round(bit)) for bit in bits]
    print(*bits, 'sum:', sum(bits))
    preamble = round(intervals[0]*1000,1) # convert to ms
    if (preamble > 30):
        print('Preamble: ', preamble, 'ms')
        del(bits[0])
        del(intervals[0])
    print("Message: ", round(sum(bits)/.300,1), "ms")
    level = 0
    messagecsv = array.array("i")
    for bit in bits:
        messagecsv.extend([level]*bit)
        level = 0 if level else 1
    return messagecsv

def binary(bytes):
    print("Binary message")
    address = bytes[2][7:8] + bytes[1][2:8] + bytes[0][2:8]
    data = bytes[3][2:8] + bytes[2][2:7]
    return (address, data)

def iflows(bytes):
    print("IFLOWS message, CRC:", *bytes[3][0:6])
    address = bytes[1][1:8] + bytes[0][2:8]
    data = bytes[3][6:8] + bytes[2][0:8] + bytes[1][0:1]
    return (address, data)

def get_messages(message):

        # for i in range(len(message)):
        #     p = i % 10
        #     print(message[i], end=" ")
        #     if p == 0 or p == 8:
        #         print(end=" ")
        #     if p == 9:
        #         print("")

        # 40 bits[0,1,2...] map to 4 bytes stripping start and end bits
        # bit order is reverse of received bits
        def get_message(bytes):
            print("#bits:", len(message))
            print(*message)
            for byte in bytes:
                print(*byte)

            if [*bytes[0][0:2]] == [0, 1]:
                address, data = binary(bytes)
            elif [*bytes[0][0:2]] == [1, 1]:
                address, data = iflows(bytes)
            else:
                print("Decode not possible")
                return
            address.reverse()
            data.reverse()
            a = d = 0
            for i in range(len(address)):
                a += address[i] << i
            for i in range(len(data)):
                d += data[i] << i
            print(a, d)

        while len(message) >= 40:
            bytes = [message[8:0:-1], message[18:10:-1], message[28:20:-1], message[38:30:-1]]
            get_message(bytes)
            del(message[:40])
            im = 0
            while message:
                bit = message.pop(0)
                im += 1
                if message and message[0] != bit:
                    print("Inter packet spacing:", round(im/.300,1), "ms")
                    break
                else:
                    print(end=".")
        if message:
            print("Leftover message: ", len(message), message, type(message))


if __name__ == '__main__':
    # print_message(find_message(*binary_file(binfile)))
    # print_message(find_message(times, samples)) # check the csv message
    # plt.plot(times, samples, marker='*')
    # plt.show()
    # times, samples = get_waveform(csvfile)
    times, samples = get_waveform(glitch)
    r = get_intervals(times, samples)
    # plt.plot(r.times, r.samples, marker='*')
    # plt.show()
    get_messages(find_messages(r.times, r.samples))

'''
Improvements:
 - detect, report and remove carrier and tail times
 - detect multiple messages and determine interpacket timing
 - remove or adapt binary file parser and remove magic numbers
'''