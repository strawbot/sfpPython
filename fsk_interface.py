from array import array

from Pylibs.protocols.saleae_interface import is_number, get_transmission
import csv
import numpy

csv_file = 'C:\\Projects\\CampbellScientific\\Testing\\AL200_TestFarm/Captures/analog.csv'


def remove_dc(samples):
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
                        if max(rf_window) < 1.25 or min(rf_window) > 1.2:
                            del (time[-100:])
                            del (data[-100:])
                            break
                        rf_window.pop(0)
                    time.append(float(row['Time']))
                    data.append(float(row['TX']))
            print(f"Waveform start: {time[0]}")
            print(f"Waveform end: {time[-1]}")
            print(f"Waveform total: {(time[-1] - time[0])}")
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
            pass


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

def get_intervals(times, samples):
    samples = remove_dc(samples)
    samples = savgol_filter(samples, 11, 2)  # window size 51, polynomial order 3

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


    if samples[1] == 0 or samples[0] * samples[1] < 0:
        m = (samples[1] - samples[0]) / (times[1] - times[0])
        first = times[0] - samples[0] / m
    else:
        first = times[0]
    # first = 0
    transitions = zero_crossings(times, samples)
    # transitions.insert(0, times[0])  # add first time to get first interval
    # print(*transitions[:10])
    deltas = get_deltas(transitions)
    deltas = remove_dc(deltas)
    # print(*deltas[:10])
    frequencies = zero_crossings(transitions, deltas)
    frequencies.append(times[-1])  # add last time to get last interval
    frequencies.insert(0, transitions[0])
    intervals = get_deltas(frequencies)
    if intervals[0] < .001:  # remove any short interval
        del (intervals[0])
    # plt.plot(times[:len(transitions)], transitions, label='transitions')
    # plt.plot(times[:len(deltas)], deltas, label='deltas')
    # plt.plot(times[:len(frequencies)], frequencies, label='frequencies')
    # plt.plot(times[:len(intervals)], intervals, label='intervals')
    # plt.legend()
    # plt.show()
    return intervals


def get_preamble():
    times, samples = get_waveform()
    return round(get_intervals(times, samples)[0]*1000, 2)


def get_inter_packet_spacing():
    times, samples = get_waveform()
    intervals = get_intervals(times, samples)
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
    inter_packet_spacing = get_inter_packet_spacing()
    intervals = get_intervals(times, samples)
    msg = find_message(intervals)
    # carrier = round(find_carrier_time(), 3)
    # tail = round(find_rftail_time(), 3)
    # print(f"Measured carrier time: {carrier * 1000} ms")
    # print(f"Measured RF tail time: {tail * 1000} ms")
