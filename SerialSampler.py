# import os, sys
# dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))+'/pylibs'
# print(dir)
# sys.path.append(dir)

from interface.serialHub import SerialPort as SerialPort
from interface.message import note as note
from scipy import signal
from numpy.fft import fft as fft
import numpy as np
import scipy.fftpack
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import traceback
from display_info import width_dots, height_dots
import queue
import sys,time

note('Serial Sampler V1')

# gathering
class Waves:
    def __init__(self):
        self.sampleq = queue.Queue()
        self.empty()

    def empty(self):
        self.sampleq.empty()
        self.tstamp = time.time()
        self.raw = bytearray()
        self.samps = []
        
    def textout(self, b): # input is:  08 9F  two bytes for 12 bit ADC
        self.sampleq.put((time.time(), bytearray(b)))
    
    def check_wad(self):
        while True:
            try:
                self.last_ts, ba = self.sampleq.get(block=False)
                self.raw.extend(ba)
            except queue.Empty:
                break

    def add_samp(self, samp):
        self.samps.append(samp)


# capture waveforms from serial port
waveforms = Waves()

def capture(seconds=0): # move into waveforms class
    end = time.time() + seconds
    waveforms.empty()
    while True:
        waveforms.check_wad()
        n = len(waveforms.raw)
        if n > 100: # ignore noise
            if time.time() - waveforms.last_ts < 1: # give extra time to get all the waveform
                continue

            raw = waveforms.raw

            # make sure to start with 1st byte as 4 bits of 12
            evens = np.sum(raw[0::2])
            odds = np.sum(raw[1::2])
            if evens > odds:
                raw.pop(0)
                n -= 1

            # combine bytes to make 12 bit samples
            for i in range(n // 2):
                sample = (raw[2 * i] << 8) | raw[2 * i + 1]
                if sample < 0x1000: # ignore samples with more than 12 bits defined
                    waveforms.add_samp(sample)
                else:
                    print("bad sample (X): ", sample, hex(sample))

            print("Added (samps): ", len(waveforms.samps))
            break
        elif seconds:
            if end > time.time():
                break
        else:
            time.sleep(.01)

    return waveforms.samps

# processing: TODO: turn into processing class or transformer class
def removeDC(samps):
    mean = np.mean(samps)
    return [x - mean for x in samps]

def resamp(samps):
    # resample to 9 samples/bit
    OVERSAMPLE = 18
    Fs = 35800
    w = fft(samps[50:len(samps)//4])
    freqs = np.fft.fftfreq(len(w))
    print('fmin:',freqs.min(), ' fmax:',freqs.max())

    # Find the peak in the coefficients
    idx = np.argmax(np.abs(w[1:]))
    f1 = abs(freqs[idx] * Fs)
    if f1 == 0.0:
        raise ValueError
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
    l = len(samps)
    trip = np.mean([abs(x) for x in samps[l//4:3*l//4]]) / 2
    start = 0
    last = len(samps) - 1
    while abs(samps[start]) < trip:
        start += 1
    end = start + 1
    seq = 0
    while end < last:
        if abs(samps[end]) < trip:
            seq += 1
            if seq > 50:
                end -= seq
                break
        else:
            seq = 0
        end += 1

    se = sign(samps[end])
    while end < last:
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

# repeat capture: turn into show class
def clear_lines():
    while waveforms.lines:
        line = waveforms.lines.pop()
        line.pop(0).remove()
        del line
    while waveforms.texts:
        text = waveforms.texts.pop()
        text.remove()
        del text

def capture_show():
    fig, axs = waveforms.fig, waveforms.axs
    clear_lines()
    fig.canvas.draw()
    fig.canvas.flush_events()
    time.sleep(.1)

    samples = capture()
    print("Transforming...")
    if samples:
        dataset = [samples]
        dataset.append(removeDC(dataset[-1]))
        fft, data = resamp(dataset[-1])
        dataset.append(fft[0::2])
        dataset.append(data)
        dataset.append(filt(dataset[-1]))
        dataset.append(trim(dataset[-1]))
        dataset.append(comb(dataset[-1]))
        dataset.append(clean(dataset[-1]))
        dataset.append(sync(dataset[-1]))
        dataset.append(frame_bytes(to_bytes(dataset[-1])))

        verify(dataset[-1][0])

        for i in range(len(axs)):
            data = dataset[i]
            plot = axs[i]
            if len(data) == 2:
                data,notes = data
                for i in range(0, len(notes), 2):
                    x = notes[i]
                    y = data[x]
                    waveforms.texts.append(plot.text(x, y, notes[i + 1]))

            waveforms.lines.append(plot.plot(range(len(data)), data,
                      marker='.', markersize=2.5, color='blue',
                      linestyle='-', linewidth=1))

        fig.canvas.draw()
    else:
        print('No samples captured')


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

    waveforms.fig, waveforms.axs = fig,[]
    iwave = 0
    waveforms.lines = []
    waveforms.texts = []
    for j in range(col):
        for i in range(n):
            plot = axs[i]
            if col > 1:
                plot = plot[j]

            waveforms.axs.append(plot)
            # plot.axis('off')
            plot.get_yaxis().set_visible(True)
            plot.get_xaxis().set_visible(False)

            if iwave == len(showbitz):
                break

            wave = showbitz[iwave]
            iwave += 1
            bits,title,notes = (*wave,[])  if  len(wave) == 2  else  wave

            plot.clear()
            waveforms.lines.append(plot.plot(range(len(bits)), bits,
                      marker='.',markersize=2.5, color='blue',
                      linestyle='-', linewidth=1))
            plt.subplots_adjust(left=0.02, right=0.98, top=0.95, bottom=0.05)
            plot.set_title(title)
            for i in range(0,len(notes),2):
                x = notes[i]
                y = bits[x]
                waveforms.texts.append(plot.text(x,y,notes[i+1]))

    if showbitz:
        dpival = fig.dpi
        winch = .9 * width_dots / dpival
        hinch = .9 * height_dots / dpival
        fig.set_size_inches(winch, hinch, forward=False)

    # add GUI
    pos = plt.axes([0.475, 0.02, 0.05, 0.02]) # (left, bottom, width, height)
    butt = Button(pos, "Capture", color='0.85', hovercolor='0.95')

    class test(object):
        def greet(self, event):
            print("Capture...")
            capture_show()
            print("Plot")

    callback = test()
    butt.on_clicked(callback.greet)
    plt.show()

def open_stream(port, baudrate=1000000):
    stream = SerialPort(port)
    stream.output.connect(waveforms.textout)
    stream.open(rate=baudrate)
    return stream

def get_frames(n, timeout=0):
    frames = []
    while n:
        print(n)
        n -= 1
        samples = capture(timeout)
        frame = to_bytes(sync(clean(comb(trim(filt(resamp(removeDC(samples))[1])))))) # need to do this in capture or in second thread pass through with a queue
        frames.append(frame)
    return frames

def frame_info(samples):
    start,end = trimmers(filt(resamp(removeDC(samples))[1]))
    frame = to_bytes(sync(clean(comb(samples[start,end+1]))))

def verify(frame):
    test_frame = [
        # consider how to send this with cli. perhaps the air command or frame: or frame building tools: empty append
        0xEB, 0x90, 0xB4, 0x33, 0xAA, 0xAA, 0x35, 0x2E, 0xF8, 0x53, 0x0D, 0xC5,
        0xD4, 0x21, 0x1A, 0xCC, 0x7D, 0x3C, 0x8D, 0xC1, 0x6A, 0x36, 0x58, 0x61,
        0xDD, 0xF9, 0x0E, 0x92, 0x08, 0xA0, 0x05, 0x4E, 0x5B, 0x62, 0x0C, 0x10,
        0xA8, 0xF1, 0x7F, 0xD3, 0x8D, 0xB3, 0x1F, 0x4F, 0xF2, 0x34, 0x40, 0x53,
        0xCF, 0xCC, 0xB3, 0x99, 0xA6, 0x59, 0x7A, 0x3D, 0xAC, 0x15, 0x0D, 0x3C,
        0x83, 0x78, 0xD1, 0x36, 0x6C, 0xD5, 0x1C, 0x8F, 0x92, 0xBA, 0xC9, 0xEF,
        0x37, 0x83, 0x75, 0xF1, 0x12, 0xA1, 0x73, 0xDC, 0xC7, 0xD3, 0xC8, 0x0E,
        0x14, 0x09, 0x33, 0x81, 0x88, 0xD5, 0x6E, 0xC0, 0xAA
    ]
    test = "check final result for expected content: "
    if frame == test_frame:
        print(test + "Pass")
    else:
        print(test + "Fail")

def process_metrics():
    times = [(time.time(),'start')]
    times.append((time.time(), 'empty_capture'))
    samples,title = capture()
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

    samples = capture()
    showbitz = []

    if samples == 0:
        sys.exit("No samples to analyze")
    try:
        showbitz.append([samples, 'raw'])
        waveforms.dc = removeDC(samples)
        showbitz.append([waveforms.dc, 'dc removed'])
        waveforms.fft,waveforms.re = resamp(waveforms.dc)
        showbitz.append(waveforms.fft)
        showbitz.append([waveforms.re, 'resampled'])
        waveforms.fi = filt(waveforms.re)
        showbitz.append([waveforms.fi, 'filtered'])
        waveforms.tr = trim(waveforms.fi)
        showbitz.append([waveforms.tr, 'Trimmed'])
        waveforms.ha = comb(waveforms.tr)
        showbitz.append([waveforms.ha, 'comb'])
        waveforms.bits = clean(waveforms.ha)
        showbitz.append([waveforms.bits, 'bits'])
        waveforms.sy = sync(waveforms.bits)
        showbitz.append([waveforms.sy, 'bit synced'])
        waveforms.by,waveforms.bynotes = frame_bytes(to_bytes(waveforms.sy))
        showbitz.append([waveforms.by, 'bytes', waveforms.bynotes])
        verify(waveforms.by)
    except Exception as e:
        print(e, file=sys.stderr)
        traceback.print_exc(file=sys.stderr)

    view_waveforms(showbitz)
    stream.close()
