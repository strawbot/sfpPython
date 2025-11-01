from array import array

from numpy.ma.extras import average

# from PyQt6.QtWidgets.QWidget import sizeHint

from Pylibs.protocols.saleae_interface import is_number, get_transmission
import csv
import numpy

# csv_file = 'C:\\Projects\\CampbellScientific\\Testing\\AL200_TestFarm/Captures/analog.csv'
csv_file = '/Users/RobertChapman/Projects/AL200_Platforms/AL200_OSX/Scripts/alert1_data/good.csv'
csv_file2 = '/Users/RobertChapman/Projects/AL200_Platforms/AL200_OSX/Scripts/alert1_data/bad2ndblock.csv'
# good.csv
# bad1stblock.csv
# bad2ndblock.csv

def remove_dc(samples):
    ac = []
    # find min, max; get average; subtract from all: (min + range/2)
    ## mean
    # sum = 0
    # for sample in samples:
    #     sum += sample
    # average = sum / len(samples)
    ## mean of median of maxs and median of mins
    # s = sorted(samples)
    # average = (median(s[-100:]) + median(s[:100]))/2
    ## geometric mean
    average = (min(samples) + max(samples))/2
    for i in range(len(samples)): # shift all by average
        ac.append(samples[i] - average)
    return ac


def zero_crossings(times, samples):
    transitions = list()
    for i in range(len(samples) - 1):
        if samples[i + 1] == 0 or samples[i] * samples[i + 1] < 0:
            m = (samples[i + 1] - samples[i]) / (times[i + 1] - times[i])
            transitions.append(times[i] - samples[i] / m)
    return transitions


def get_deltas(transitions):
    return [transitions[i+1] - transitions[i] for i in range(len(transitions) - 1)]


def find_carrier_time():
    with open(csv_file, 'r') as f:
        csvreader = csv.DictReader(f, fieldnames=['Time', 'TX', 'PTT'])
        OFF, PTTLO, CAPTURE = range(3)
        state = OFF
        try:
            for row in csvreader:
                if state == OFF:
                    if not is_number(row['Time']):
                        continue
                    if float(row['Time']) < 0:
                        continue
                    else:
                        state = PTTLO
                if state == PTTLO:
                    if float(row['TX']) > 1.35 or float(row['TX']) < 1.15:
                        return float(row['Time'])
        except ValueError:
            pass
        return 0


def get_waveform():
    data = array('f')
    time = array('f')
    with open(csv_file, 'r') as f:
        csvreader = csv.DictReader(f, fieldnames=['Time', 'TX', 'PTT'])
        OFF, PTTLO, WAVEFORM = range(3)
        state = OFF
        rf_window = array("f")
        try:
            for row in csvreader:
                if state == OFF:
                    if not is_number(row['Time']):
                        continue
                    if float(row['Time']) < 0:
                        continue
                    else:
                        state = PTTLO
                if state == PTTLO:
                    if float(row['TX']) > 1.28 or float(row['TX']) < 1.17:
                        state = WAVEFORM
                if state == WAVEFORM:
                    rf_window.append(float(row['TX']))
                    if len(rf_window) > 100:
                        # if max(rf_window) < 1.25 or min(rf_window) > 1.2:
                        #     del (time[-100:])
                        #     del (data[-100:])
                        #     break
                        rf_window.pop(0)
                    time.append(float(row['Time']))
                    data.append(float(row['TX']))
            print(f"Waveform length (ms): {round(1000*(time[-1] - time[0]),1)}")
            return (time, data)
        except ValueError:
            pass
        return 0


def find_rftail_time():
    window = array("f")
    time = array("f")
    with open(csv_file, 'r') as f:
        csvreader = csv.DictReader(f, fieldnames=['Time', 'TX', 'PTT'])
        OFF, PTTLO, WAVEFORM, TAIL = range(4)
        state = OFF
        start = 0
        try:
            for row in csvreader:
                if state == OFF:
                    if not is_number(row['Time']):
                        continue
                    if float(row['Time']) < 0:
                        continue
                    else:
                        state = PTTLO
                if state == PTTLO:
                    if float(row['TX']) > 1.28 or float(row['TX']) < 1.17:
                        state = WAVEFORM
                if state == WAVEFORM:
                    time.append(float(row['Time']))
                    window.append(float(row['TX']))
                    if len(window) < 100:
                        continue
                    else:
                        if max(window) < 1.3 and min(window) > 1.15:
                            state = TAIL
                            start = time[-100]
                            continue
                        window.pop(0)
                if state == TAIL:
                    # time.append(float(row['Time']))
                    if float(row['PTT']) > 1.0:
                        end = float(row['Time'])
                        return end - start
        except ValueError:
            return 0


def get_full_tx():
    data = array('f')
    with open(csv_file, 'r') as f:
        csvreader = csv.DictReader(f, fieldnames=['Time', 'TX', 'PTT'])
        OFF, PTTLO = range(2)
        state = OFF
        try:
            for row in csvreader:
                if state == OFF:
                    if not is_number(row['Time']):
                        continue
                    if float(row['Time']) < 0:
                        continue
                    else:
                        state = PTTLO
                if state == PTTLO:
                    if float(row['PTT']) > 3:
                        return data
                    data.append(float(row['TX']))
            return data
        except ValueError:
            pass
        return 0

import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

def separate_message(samples): # separate carrier, message and tail
    threshold = max(samples)/8
    carrier = 0
    tail = len(samples) - 1
    for i in range(tail + 1):
        if abs(samples[i]) > threshold:
            carrier = i
            break
    for i in range(tail,-1,-1):
        if abs(samples[i]) > threshold:
            tail = i
            break
    return carrier, tail

def psk_decode(results):
    one = average(results.deltas[1:10])
    results.pskbits = [int(round(d/one, 0)) for d in results.deltas]

def airlink_frame(results):
    i = 0
    for x in results.pskbits:
        if x > 1:
            break
        i += 1
    results.airframe = results.pskbits[i:]

def get_intervals(times, raw):
    class Results(object):
        pass

    r = Results()
    r.rawfilt = savgol_filter(raw, 11, 2)  # window size 51, polynomial order 3
    samples = remove_dc(r.rawfilt)
    # find and strip carrier and tail
    carrier, tail = separate_message(samples)
    print("Carrier time (ms): ", round(1000*(times[carrier] - times[0]),1))
    print("Message time (ms): ", round(1000*(times[tail] - times[carrier]),1))
    print("Tail time (ms): ", round(1000*(times[-1] - times[tail]),1))
    r.times = times[carrier:tail]
    r.samples = samples[carrier:tail]
    # print(*times[:10],'\n',*samples[:10])

    # n = len(times)//100
    # x, y = times[:n], samples[:n]
    # plt.plot(x, y, label='Raw')
    # for window in range(11, 12):
    #     for poly in range(2,3):
    #         yhat = savgol_filter(y, window, poly)  # window size 51, polynomial order 3
    #         plt.plot(x, yhat, label='w={} p={}'.format(window, poly))
    # plt.show()
    # samples = yhat


    if r.samples[1] == 0 or r.samples[0] * r.samples[1] < 0:
        m = (samples[1] - samples[0]) / (times[1] - times[0])
        # first = times[0] - samples[0] / m
    # else:
    #     first = r.times[0]
    # first = 0
    r.transitions = zero_crossings(r.times, r.samples)
    # transitions.insert(0, r.times[0])  # add first time to get first interval
    # print(*r.transitions[:10])
    r.deltas = get_deltas(r.transitions)

    r.referenced = remove_dc(r.deltas)
    # print(*r.deltas[:10])
    r.frequencies = zero_crossings(r.transitions, r.referenced)
    r.frequencies.append(r.times[-1])  # add last time to get last interval
    r.frequencies.insert(0, r.transitions[0])
    r.intervals = get_deltas(r.frequencies)
    if r.intervals[0] < .001:  # remove any short interval
        del (r.intervals[0])
    psk_decode(r)
    airlink_frame(r)

    # plt.plot(r.times[:1000], raw[:1000], label='raw')
    # plt.legend()
    # plt.show()
    # plt.plot(r.times, r.samples, label='samples')
    # plt.legend()
    # plt.show()
    # plt.plot(r.times[:len(r.transitions)], r.transitions, label='transitions')
    # plt.legend()
    # plt.show()
    # plt.plot(r.times[:len(r.deltas)], r.deltas, 'b.', label='r.deltas')
    # plt.legend()
    # plt.show()
    # plt.plot(r.times[:len(r.pskbits)], r.pskbits, 'b.', label='r.pskbits')
    # plt.legend()
    # plt.show()
    # plt.plot(r.times[:len(r.airframe)], r.airframe, 'b.', label='r.airframe')
    # plt.legend()
    # plt.show()
    # plt.plot(r.times[:len(r.referenced)], r.referenced, label='referenced')
    # plt.legend()
    # plt.show()
    # plt.plot(r.times[:len(r.frequencies)], r.frequencies, label='frequencies')
    # plt.legend()
    # plt.show()
    # plt.plot(r.times[:len(r.intervals)], r.intervals, label='intervals')
    # plt.legend()
    # plt.show()
    return r


def get_preamble():
    times, samples = get_waveform()
    return round(get_intervals(times, samples).intervals[0]*1000, 2)


def get_inter_packet_spacing():
    times, samples = get_waveform()
    intervals = get_intervals(times, samples).intervals
    int_time = 0
    spacing = 0
    for i in intervals[1:]:
        int_time += i
        if int_time > .1333:
            spacing = int_time - .1333
            break
    # if intervals[20] < .0035:
    #     return 0
    return round(spacing*1000, 2)


def find_message(intervals):
    bits = [round(bit / (1 / 300), 1) for bit in intervals]
    bits = [int(round(bit)) for bit in bits]
    # print(*bits, 'sum:', sum(bits))
    preamble = round(intervals[0] * 1000, 1)  # convert to ms
    if (preamble > 30):
        print('Preamble: ', preamble, 'ms')
        del (bits[0])
    level = 0
    messagecsv = array("i")
    for bit in bits:
        messagecsv.extend([level]*bit)
        level = 0 if level else 1
    return messagecsv

if __name__ == "__main__":
    # full_tx = get_full_tx()
    # print(f"Full TX standard dev: {numpy.std(full_tx)}")
    times, samples = get_waveform()
    # preamble = get_preamble()
    # inter_packet_spacing = get_inter_packet_spacing()
    results = get_intervals(times, samples)
    # print("PSK bit pattern: ", results.pskbits)
    msg = find_message(results.intervals)

    csv_file = csv_file2
    times2, samples2 = get_waveform()
    results2 = get_intervals(times2, samples2)
    msg2 = find_message(results.intervals)
    print("Deltas: ", [a-b for a,b in zip(results.airframe, results2.airframe)])
    print("MSG1: ", *msg)
    print("MSG2: ", *msg2)

    #
    # carrier = find_carrier_time()
    # tail = find_rftail_time()
    # print(f"Measured carrier time: {carrier * 1000} ms")
    # print(f"Measured RF tail time: {tail * 1000} ms")
