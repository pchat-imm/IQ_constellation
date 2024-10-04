import numpy as np
import scipy
import matplotlib.pyplot as plt 
from py3gpp import *
import csv
# import sigmf

delta_f = 0				# frequency offset
mu = 1					# for SCS
f = 1					# signal modulation
apply_fine_CFO = 0		# apply fine carrier frequency offset


input_file = '/home/tiwat/workarea/IQ_constellation/iq_python/input/IQDataFile_SPEEDTEST_10MS.csv'
# input_file = '/home/tiwat/workarea/IQ_constellation/iq_python/input/IQDataFile_SPEEDTEST.csv'
# input_file = '/home/tiwat/workarea/IQ_constellation/iq_python/input/IQDataFile_SPOTIFY.csv'
# input_file = '/home/tiwat/workarea/IQ_constellation/iq_python/input/IQDataFile_SPOTIFY2.csv'



with open(input_file, 'r') as f:
	reader = csv.reader(f)

	for _ in range(19):			# skip header
		next(reader)
	
	iq_val = []
	for row in reader:
		i_val = float(row[0])
		q_val = float(row[1])
		iq_val.append(complex(i_val, q_val))		# I+jQ
	
	waveform = np.array(iq_val[:230401])			# 10 ms
	# waveform = np.array(iq_val)			

print("len(waveform)", len(waveform))

dec_factor = 8			# decimated factor, to downsample
waveform = scipy.signal.decimate(waveform, dec_factor, ftype='fir') 
waveform /= max(waveform.real.max(), waveform.imag.max()) # scale max amplitude to 1
fs = 23.04e6 // dec_factor		# sampling rate 23.04 MHz, to 2.88 MSPS

waveform =  waveform * np.exp(-1j*2*np.pi*delta_f/fs*(np.arange(len(waveform))))
np.random.seed(69) # to get reproducible noise
noise = ((np.random.rand(waveform.shape[0]) - 0.5) + 1j*(np.random.rand(waveform.shape[0]) - 0.5))*0.8
SNR = 10*np.log10((np.linalg.norm(waveform) / np.linalg.norm(noise)))
waveform += noise
print(f'SNR = {SNR} dB')
print("waveform w/ noise:",waveform)
print("len(waveform):", len(waveform))

carrier = nrCarrierConfig(NSizeGrid = 20, SubcarrierSpacing = 15 * 2**mu)
info = nrOFDMInfo(carrier)
Nfft = info['Nfft']

peak_value = np.zeros(3)
peak_index = np.zeros(3, 'int')
pssIndices = np.arange((119-63), (119+64))
fig, axs = plt.subplots(3, 1, facecolor='w', sharex=True, sharey=True)
for current_NID2 in np.arange(3, dtype='int'):
    slotGrid = nrResourceGrid(carrier)
    slotGrid = slotGrid[:, 0]
    slotGrid[pssIndices] = nrPSS(current_NID2)
    [refWaveform, info] = nrOFDMModulate(carrier, slotGrid, SampleRate = fs)
    refWaveform = refWaveform[info['CyclicPrefixLengths'][0]:]; # remove CP

    temp = scipy.signal.correlate(waveform[:int(25e-3 * fs)], refWaveform, 'valid')  # correlate over 25 ms
    peak_index[current_NID2] = np.argmax(np.abs(temp))
    peak_value[current_NID2] = np.abs(temp[peak_index[current_NID2]])
    t_corr = np.arange(temp.shape[0])/fs*1e3
    axs[current_NID2].plot(t_corr, np.abs(temp))
detected_NID2 = np.argmax(peak_value)
print(f'detected NID2 is {detected_NID2}')
# plt.show()

nrbSSB = 20
scsSSB = 15 * 2**(mu)
nSlot = 0
rxSampleRate = fs
if True:
    timingOffset = 274 + int(0.02 * fs)
    print("if")
else:
    nrbSSB = 20
    refGrid = np.zeros((nrbSSB*12, 2))
    refGrid[nrPSSIndices(), 1] = nrPSS(detected_NID2)
    timingOffset = nrTimingEstimate(waveform = waveform, nrb = nrbSSB, scs = scsSSB, initialNSlot = nSlot, refGrid = refGrid, SampleRate = rxSampleRate)
print("Timing offset: ", timingOffset)

# modulate about 8 symbols, only has to be at least 5
a = waveform[57874:]
# a = waveform[timingOffset:]
# [:np.min((len(waveform),(2048*8)//dec_factor))]
print(a)
# rxGrid = nrOFDMDemodulate(waveform = waveform[timingOffset:][:np.min((len(waveform), (2048*8)//dec_factor))], nrb = nrbSSB, scs = scsSSB, initialNSlot = nSlot, SampleRate=rxSampleRate, CyclicPrefixFraction=0.5)
# print(rxGrid)
# rxGrid = rxGrid[:,1:5]
# rxGrid /= np.max((rxGrid.real.max(), rxGrid.imag.max()))


