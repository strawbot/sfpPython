# import os, sys
# dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))+'/pylibs'
# print(dir)
# sys.path.append(dir)

from pylibs.protocols.interface.serialHub import SerialPort
from pylibs.protocols.interface.message import note
from scipy import signal
from numpy.fft import fft as fft
import numpy as np
import scipy.fftpack
import matplotlib.pyplot as plt
import time

note('Serial Sampler V1')
import sys,time

# gathering
class Waves:
    pass

samples = bytearray()
waveforms = Waves()
waveforms.samps = []
tstamp = 0

def textout(b): # input is:  08 9F  two bytes for 12 bit ADC
    global tstamp
    tstamp = time.time()
    samples.extend(b)

def check_wad():
    if time.time() - tstamp > .3: # tstamp set in serial thread action
        b = bytearray(samples) # pluck out current content possibly filled in by other thread
        n = len(b)
        samples[:n] = []  # data loss here unless edited carefully - likadis
        if n > 100: # neglect orphans
            waveform = []
            evens = sum(b[0::2])
            odds = sum(b[1::2])
            if evens > odds:
                b.pop(0)
            for i in range(len(b) // 2):
                sample = (b[2 * i] << 8) | b[2 * i + 1]
                if 1500 < sample < 2500:  # 0x1000:
                    waveform.append(sample)
                else:
                    print("bad sample (X): ", sample, hex(sample))

            waveform[:50] = [] # delete noise
            waveforms.samps.append([waveform, 'Waveform %i'%(len(waveforms.samps)+1)])
            print("Added (samps): ", len(waveform))
        elif n:
            print('orphan bytes: ', n)

# capture waveforms from serial port
def empty_capture():
    waveforms.samps[:] = []

def capture(n, timeout=0):
    while len(waveforms.samps) < n:
        for i in range(10): # poll for a second
            time.sleep(.1)
            check_wad()
        if timeout: # 0 is infinity
            if timeout == 1: # check for timeout
                break
            timeout -= 1

    samps = list(waveforms.samps[:n])
    waveforms.samps[:n] = []
    return samps

# processing
def removeDC(samps):
    mean = np.mean(samps)
    return [x - mean for x in samps]

def resamp(samps):
    # resample to 9 samples/bit
    OVERSAMPLE = 18
    Fs = 35700
    w = fft(samps)
    freqs = np.fft.fftfreq(len(w))
    print('fmin:',freqs.min(), ' fmax:',freqs.max())

    # Find the peak in the coefficients
    idx = np.argmax(np.abs(w))
    f1 = abs(freqs[idx] * Fs)
    print('f prime:',f1)

    # FFT for plot
    N = len(samps)
    yf = scipy.fftpack.fft(samps)
    fftresamp = list(2.0 / N * np.abs(yf[:N // 2]))
    index = fftresamp.index(max(fftresamp))
    fftre = [fftresamp,'FFT',[index,' Fmax = %iHz'%int(f1)]]
    Frs = f1*OVERSAMPLE*2 #43200 * 2
    resamps = list(signal.resample(samps, int(len(samps) * Frs / Fs)))
    return fftre,resamps

def filt(samps):
    # 71 point root raised cosine coefficients - 14 bit res
    COEF72 = [ -18,   -9,    5,   18,   23,   17,    1,  -17,
               -31,  -33,  -19,    5,   31,   45,   38,   11,
               -30,  -65,  -77,  -54,    1,   70,  122,  124,
                55,  -76, -228, -332, -302,  -62,  431, 1163,
              2062, 3001, 3827, 4394, 4595, 4394, 3827, 3001,
              2062, 1163,  431,  -62, -302, -332, -228,  -76,
                55,  124,  122,   70,    1,  -54,  -77,  -65,
               -30,   11,   38,   45,   31,    5,  -19,  -33,
               -31,  -17,    1,   17,   23,   18,    5,   -9]
    L = len(COEF72)
    n = len(samps)
    k = L//2

    pre = [samps[0]]*k
    post = [samps[-1]]*k

    buffer = np.array(pre + samps + post)
    coffs = np.array(COEF72)
    return [np.dot(coffs, buffer[i:i+L])  for i in range(n)]


def sign(n):
    return n < 0

def trimmers(samps):
    trip = np.mean([abs(x) for x in samps]) / 2
    start = 0
    end = len(samps) - 1
    while abs(samps[start]) < trip:
        start += 1
    while abs(samps[end]) < trip:
        end -= 1
    se = sign(samps[end])
    while end < len(samps) - 1:
        if sign(samps[end]) == se  and  abs(samps[end]) > trip/2:  # last waveform crosses zero
            end += 1
        else:
            break
    return start,end

def trim(samps):
    start,end = trimmers(samps)
    return samps[start:end+1]

def inflect(samps):
    try:
        trip,sign0,i = abs(samps[0]/2), sign(samps[0]), 1

        while sign(samps[i]) == sign0  or  abs(samps[i]) < trip:
            i += 1

        if sign0:
            while samps[i + 1] > samps[i]: i += 1
            return i

        while samps[i + 1] < samps[i]: i += 1
        return i

    except:
        return len(samps)

# replace with: average over agc until multibit sequence detected by 2;
# change to framing sequence: use mean to map out future points
# each point could be a median of local values if needed
# 2: in find state, count inflections until steady state is reached
# which is when mean is predicting inflections accurately. then hunt
# mode begins looking for where a stretch of at least 3 bit share the same sign
# this is the end of AGC and timing is set and now used to read all bits
# after. this will yield times for agc and frame for test
def comb(samps):
    N = len(samps)
    hair = []
    n = 0
    start = 0
    while start < N:
        i = inflect(samps[start:]) # find next bit flip
        if n > 10: # skip the first 10 samples
            avg = start/n
            j = round(avg) - 1
            k = round(i/avg)
        else:
            k = 1
            j = i - 1

        n += k

        # deal with multiple bits in a row
        value = samps[start]
        si = -1 if sign(value) else 1
        for z in range(k):
            hair.extend([0] * j + [si])
        start += i

    hair.extend([0]*(N-len(hair)))
    return hair

def clean(hair):
    return [x == 1  for x in hair  if x]

def longest(l1, l2):
    ba = bytearray(l1)
    bs = bytearray(l2)
    n = len(l2)
    index = 0
    for i in range(1,n):
        index = ba.find(bs[:i])
        if index == -1:
            return 0,i
    return index,n

# use BIT_SYNC pattern to find start of bytes:0xEB, 0x90, 0xB4, 0x33, 0xAA, 0xAA
mask = [0x80, 0x40, 0x20, 0x10, 0x08, 0x04, 0x02, 0x01]
bsyn = [1 if (mask[i] & b) else 0 for b in [0xEB, 0x90, 0xB4, 0x33, 0xAA, 0xAA] for i in range(8)]

def sync(bits):
    start,q = longest(bits,bsyn)
    if q == len(bsyn):
        bits = bits[start:]
    else:
        print("longest:", q)
        abits = [0 if b else 1 for b in bits]  # invert universe
        start,q = longest(abits,bsyn)
        if q == len(bsyn):
            bits = abits[start:]
            print("Inverted signal detected")
        else:
            print("No bit sync detected",q)
    return bits

def to_bytes(samps):
    byte_bits = (len(samps) // 8) * 8
    return [(sum(x * y for x, y in zip(samps[i:i + 8], mask))) for i in range(0, byte_bits, 8)]

def frame_bytes(bytes):
    notes = []
    for i in range(len(bytes)):
        notes.extend([i,' %02X'%bytes[i]])
    # note each byte is mapped to two ASCII characters; n*2
    alframe = ''.join(list(map(lambda x: '%02X' % x, bytes)))
    print('alframe', alframe)
    return bytes,notes

# viewing
def view_waveforms(showbitz):
    n = len(showbitz) # todo: add support for 1 or 0 waveforms

    # consider waveform and its processing in a single column
    # might still work out not too bad spill to columns on > 5 if kept balanced
    col = max(1,(n+4)//5) # max 5 in a column
    n = (n + col - 1) // col
    if col > 1:
        fig, axs = plt.subplots(ncols=col, nrows=n)
    elif n > 1:
        fig, axs = plt.subplots(n)
    else:
        fig = plt.figure(tight_layout=True)
        axs = fig.add_subplot()

    iwave = 0
    for j in range(col):
        for i in range(n):
            plot = axs[i]
            if col > 1:
                plot = plot[j]

            plot.axis('off')

            if iwave == len(showbitz):
                break

            wave = showbitz[iwave]
            iwave += 1
            bits,title,notes = (*wave,[])  if  len(wave) == 2  else  wave

            plot.plot(range(len(bits)), bits,
                      marker='.',markersize=2.5,
                      linestyle='-', linewidth=1)
            plt.subplots_adjust(left=0.02, right=0.98, top=0.95, bottom=0.05)
            plot.set_title(title)
            for i in range(0,len(notes),2):
                x = notes[i]
                y = bits[x]
                plot.text(x,y,notes[i+1])

    if showbitz:
        inches = min(25, col * 2.5 * max(1,len(showbitz[0][0])/200))
        fig.set_size_inches((inches,12)) # set width based on # of points
    # todo: factor in number of waveforms to generate 12
    plt.show()

def open_stream(port, baudrate=1000000):
    stream = SerialPort(port)
    stream.output.connect(textout)
    stream.open(rate=baudrate)
    return stream

def get_frames(n, timeout=0):
    empty_capture()
    frames = []
    while n:
        print(n)
        n -= 1
        samples,title = capture(1, timeout)[0]
        frame = to_bytes(sync(clean(comb(trim(filt(resamp(removeDC(samples))[1])))))) # need to do this in capture or in second thread pass through with a queue
        frames.append(frame)
    return frames

def frame_info(samples):
    start,end = trimmers(filt(resamp(removeDC(samples))[1]))
    frame = to_bytes(sync(clean(comb(samples[start,end+1]))))



def process_metrics():
    times = [(time.time(),'start')]
    empty_capture()
    times.append((time.time(), 'empty_capture'))
    samples,title = capture(1)[0]
    times.append((time.time(), 'capture'))
    waveforms.dc = removeDC(samples)
    times.append((time.time(), 'removeDC'))
    waveforms.fft, waveforms.re = resamp(waveforms.dc)
    times.append((time.time(), 'resamp'))
    waveforms.fi = filt(waveforms.re)
    times.append((time.time(), 'filt'))
    waveforms.tr = trim(waveforms.fi)
    times.append((time.time(), 'trim'))
    waveforms.ha = comb(waveforms.tr)
    times.append((time.time(), 'comb'))
    waveforms.bits = clean(waveforms.ha)
    times.append((time.time(), 'clean'))
    waveforms.sy = sync(waveforms.bits)
    times.append((time.time(), 'sync'))
    waveforms.by, waveforms.bynotes = frame_bytes(to_bytes(waveforms.sy))
    times.append((time.time(), 'frame_bytes'))
    start = times[0][0]
    for end,process in times:
        print(process, int((end - start)*1000), 'ms')
        start = end
    print('processing time: %i ms'%(1000*(times[-1][0] - times[2][0])))


if __name__ == '__main__':
    stream = open_stream('/dev/cu.usbserial-FT1Q5LVCB')

    # process_metrics()
    # stream.close()
    # sys.exit(0)

    waveforms.samps = capture(1)
    stream.close()
    showbitz = []
    for samples,title in waveforms.samps:
        waveforms.dc = removeDC(samples)
        waveforms.fft,waveforms.re = resamp(waveforms.dc)
        waveforms.fi = filt(waveforms.re)
        waveforms.tr = trim(waveforms.fi)
        waveforms.ha = comb(waveforms.tr)
        waveforms.bits = clean(waveforms.ha)
        waveforms.sy = sync(waveforms.bits)
        waveforms.by,waveforms.bynotes = frame_bytes(to_bytes(waveforms.sy))

        showbitz.append([samples, title])
        # showbitz.append([waveforms.dc, title + ':dc removed'])
        showbitz.append(waveforms.fft)
        # showbitz.append([waveforms.re, title + ':resampled'])
        showbitz.append([waveforms.fi, title + ':filtered'])
        showbitz.append([waveforms.tr, title + ':Trimmed'])
        showbitz.append([waveforms.ha, title + ':comb'])
        showbitz.append([waveforms.bits, title + ':bits'])
        # showbitz.append([waveforms.sy, title + ':bit synced'])
        showbitz.append([waveforms.by, title + ':bytes', waveforms.bynotes])

    # sys.exit(0)
    view_waveforms(showbitz)