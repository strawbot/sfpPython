import pyaudio
import matplotlib.pyplot as plt
import numpy as np
import time

plt.style.use('ggplot')

def fft_calc(data_vec):
    fft_data_raw = (np.fft.fft(data_vec))
    fft_data = (fft_data_raw[0:int(np.floor(len(data_vec)/2))])/len(data_vec)
    fft_data[1:] = 2*fft_data[1:]
    return fft_data

audio = pyaudio.PyAudio() # create pyaudio instantiation
# for i in range(audio.get_device_count()):
#     print(audio.get_device_info_by_index(i))
#{'index': 0, 'structVersion': 2, 'name': 'ASUS MG28U', 'hostApi': 0, 'maxInputChannels': 0, 'maxOutputChannels': 2, 'defaultLowInputLatency': 0.01, 'defaultLowOutputLatency': 0.009541666666666667, 'defaultHighInputLatency': 0.1, 'defaultHighOutputLatency': 0.018875, 'defaultSampleRate': 48000.0}
# {'index': 1, 'structVersion': 2, 'name': 'USB Audio CODEC ', 'hostApi': 0, 'maxInputChannels': 0, 'maxOutputChannels': 2, 'defaultLowInputLatency': 0.01, 'defaultLowOutputLatency': 0.004354166666666667, 'defaultHighInputLatency': 0.1, 'defaultHighOutputLatency': 0.0136875, 'defaultSampleRate': 48000.0}
# {'index': 2, 'structVersion': 2, 'name': 'USB Audio CODEC ', 'hostApi': 0, 'maxInputChannels': 2, 'maxOutputChannels': 0, 'defaultLowInputLatency': 0.0057083333333333335, 'defaultLowOutputLatency': 0.01, 'defaultHighInputLatency': 0.015041666666666667, 'defaultHighOutputLatency': 0.1, 'defaultSampleRate': 48000.0}
# {'index': 3, 'structVersion': 2, 'name': 'USB Audio DAC   ', 'hostApi': 0, 'maxInputChannels': 0, 'maxOutputChannels': 2, 'defaultLowInputLatency': 0.01, 'defaultLowOutputLatency': 0.004354166666666667, 'defaultHighInputLatency': 0.1, 'defaultHighOutputLatency': 0.0136875, 'defaultSampleRate': 48000.0}
# {'index': 4, 'structVersion': 2, 'name': 'MacBook Pro Microphone', 'hostApi': 0, 'maxInputChannels': 1, 'maxOutputChannels': 0, 'defaultLowInputLatency': 0.044520833333333336, 'defaultLowOutputLatency': 0.01, 'defaultHighInputLatency': 0.05385416666666667, 'defaultHighOutputLatency': 0.1, 'defaultSampleRate': 48000.0}
# {'index': 5, 'structVersion': 2, 'name': 'MacBook Pro Speakers', 'hostApi': 0, 'maxInputChannels': 0, 'maxOutputChannels': 2, 'defaultLowInputLatency': 0.01, 'defaultLowOutputLatency': 0.0090625, 'defaultHighInputLatency': 0.1, 'defaultHighOutputLatency': 0.018395833333333333, 'defaultSampleRate': 48000.0}
# {'index': 6, 'structVersion': 2, 'name': 'Microsoft Teams Audio', 'hostApi': 0, 'maxInputChannels': 2, 'maxOutputChannels': 2, 'defaultLowInputLatency': 0.01, 'defaultLowOutputLatency': 0.0013333333333333333, 'defaultHighInputLatency': 0.1, 'defaultHighOutputLatency': 0.010666666666666666, 'defaultSampleRate': 48000.0}

# using the Behringer UCA202 as an audio acquisition system at 44.1kHz and 16-bit
form_1 = pyaudio.paInt16 # 16-bit resolution
chans = 1 # 1 channel
samp_rate = 48000
chunk = samp_rate*10 # 2^12 samples for buffer
rec_secs = 1
dev_index = 2 # device index found by audio.get_device_info_by_index(ii)

# create pyaudio stream
stream = audio.open(format = form_1,rate = samp_rate,channels = chans, \
                    input_device_index = dev_index,input = True, \
                    frames_per_buffer=chunk)
stream.stop_stream()
# record background noise
# input('press enter to record noise')
print('Recording noise')
stream.start_stream()
print('stream started')
captured = stream.read(chunk,exception_on_overflow = False)
print('captured')
noise = np.fromstring(captured,dtype=np.int16)
print('noise recorded')
stream.stop_stream()
print('stream stopped')
fft_noise =fft_calc(noise) # fft of noise

# record the actual bar vibrations
input('press to record actual data')
stream.start_stream()
data = []
# for ii in range(0,int(np.floor((rec_secs*samp_rate)/chunk))):
#     data.extend(np.fromstring(stream.read(chunk),dtype=np.int16))
stream.stop_stream()
print('finished recording')

