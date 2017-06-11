#!/usr/bin/env python

#Copyright (c) 2017 James Gibbard

#Plot an IQ data file based on provided parameters
#Tested with python 2.7 and 3.6
#Requires numpy and matplotlib

import argparse
from sys import byteorder
import numpy as np
import matplotlib.pyplot as plt

def plotIQ(data, Fs):
    
    
    if Fs == None:
        plt.plot(np.real(data), label='I')
        plt.plot(np.imag(data), label='Q')
    else:
        plt.plot(np.real(data), label='I')
        plt.plot(np.imag(data), label='Q')
        
    plt.grid(True)  
    plt.legend(loc='upper right', frameon=True)        
    plt.show()
    
def plotPSD(data,fftWindow, Fs):

    assert fftWindow in ['rectangular', 'bartlett', 'blackman', 
                         'hamming', 'hanning']
    
    N = len(data)
    
    #Generate the selected window
    if fftWindow == "rectangular":
        window = np.ones(N)
    elif fftWindow == "bartlett":
        window = np.bartlett(N)
    elif args.fftWindow == "blackman":
        window = np.blackman(N)
    elif fftWindow == "hamming":
        window = np.hamming(N)
    elif fftWindow == "hanning":
         window = np.hanning(N)         
         
    dft = np.fft.fft(data*window)    
    
    if Fs == None:
        #If the sample rate is known then plot PSD as
        #Power/Freq in (dB/Hz)
        plt.psd(data*window, NFFT=N)
        
    else:
        #If sample rate is not known then plot PSD as
        #Power/Freq as (dB/rad/sample)
        plt.psd(data*window, NFFT=N, Fs=Fs)

    plt.show()
    
def plotSpectrogram(data, fftWindow, fftSize, Fs):

    if fftSize == None:
        N = len(data)
    else:
        N = fftSize    
    
    if Fs == None:
        Fs = 2
    
    if fftWindow == "rectangular":
        plt.specgram(data, NFFT=N, Fs=Fs, 
        window=lambda data: data*np.ones(len(data)),  noverlap=int(N/10))
    elif fftWindow == "bartlett":
        plt.specgram(data, NFFT=N, Fs=Fs, 
        window=lambda data: data*np.bartlett(len(data)),  noverlap=int(N/10))
    elif args.fftWindow == "blackman":
        plt.specgram(data, NFFT=N, Fs=Fs, 
        window=lambda data: data*np.blackman(len(data)),  noverlap=int(N/10))
    elif fftWindow == "hamming":
        plt.specgram(data, NFFT=N, Fs=Fs, 
        window=lambda data: data*np.hamming(len(data)),  noverlap=int(N/10))
    elif fftWindow == "hanning":
         plt.specgram(data, NFFT=N, Fs=Fs, 
         window=lambda data: data*np.hanning(len(data)),  noverlap=int(N/10))

    plt.show()
    

if __name__ == '__main__':
    
    #Generate command line parser to parse inputs
    cliParser = argparse.ArgumentParser(description='Plots quadrature IQ signals')    
    
    #Get the filename of the input file
    cliParser.add_argument('filename', type=str, help='input filename')
    
    cliParser.add_argument('-s', '--startSample', type=int, 
        help='sample to begin plot from (default=0)',  default=0)    

    cliParser.add_argument('-o', '--offset', type=int, 
        help='offset in bytes from begining of file (default=0)',  default=0)

    cliParser.add_argument('-n', '--numberOfSamples', type=int, 
        help='number of samples to plot',  default=0)       

    cliParser.add_argument('-fs', '--sampleRate', type=float, 
        help='sets the sample rate [sps] (default=1e6)')    
    
    cliParser.add_argument('-f', '--format', type=str, 
        help='Output format (default=int16)', 
        choices=["int8", "int16", "int32", "uint8", "uint16", "uint32", 
        "float16", "float32", "float64"],
        default='int16')
                                
    cliParser.add_argument('-be', '--bigendian', action='store_true', 
        help='output data in big endian format (default=False)')
                        
    cliParser.add_argument('-qi', '--orderQI', action='store_true', 
        help='store output data as Q then I (Default = I then Q)')

    cliParser.add_argument('-p', '--plotType', type=str, 
        help='Plot Type (default=iq)', choices=['iq', 'psd', 'spec'],
        default='iq')

    cliParser.add_argument('-w', '--fftWindow', type=str, 
        help='FFT window type (default=rectangular)', 
        choices=['rectangular', 'bartlett', 'blackman', 'hamming', 'hanning'],
        default='rectangular')    

    cliParser.add_argument('-fw', '--fftWidth', type=int, 
        help='FFT width for spectrogram')

    args = cliParser.parse_args()
    
    #By default the file is read from an offset of 0 bytes
    fileOffset = 0
    
    #Set initial offset in bytes
    #Useful if the file has a header that should be ignored
    if args.offset != 0:
        fileOffset = args.offset
        
    #Convert sample offset to offset in bytes depending on datatype
    if args.startSample != 0:
        if args.format[-1:] == "8":
            fileOffset += 2 * 1 * args.startSample
        elif args.format[-2:] == "16":
            fileOffset += 2 * 2 * args.startSample 
        elif args.format[-2:] == "32":
            fileOffset += 2 * 4 * args.startSample 
        elif args.format[-2:] == "64":
            fileOffset += 2 * 8 * args.startSample 
    
    #Open the file in binary read mode    
    with open(args.filename, "rb") as f:
    
        #Seek to the absolue offset set by offset and startSample arguments
        f.seek(fileOffset, 0)
        
        if args.numberOfSamples != 0:
            #Read twice the number of samples as each sample has a 
            #real and imaginary part
            data = np.fromfile(f, dtype=args.format, 
            count=args.numberOfSamples*2)
        else:
            #If number of samples is not specified read to the end of the file
            data = np.fromfile(f, dtype=args.format)
    
    #If system byteorder is different to desired input byte order
    #Then swich the endianness
    if byteorder == 'little':
        if args.bigendian == True:        
            data = data.byteswap()            
    elif byteorder == 'big':
        if args.bigendian == False:     
            data = data.byteswap()    
    
    #Convert to complex data to complex128 data type
    #This is two double precision (64bit) floating point numbers
    if args.orderQI:
        data = data[1::2] + 1j * data[0::2]
    else:
        data = data[0::2] + 1j * data[1::2]
    
    #Select plotting function
    if args.plotType == 'iq':
        plotIQ(data, args.sampleRate)
    elif args.plotType == 'psd':
        plotPSD(data, args.fftWindow, args.sampleRate)
    elif args.plotType == 'spec':
        plotSpectrogram(data, args.fftWindow, args.fftWidth, args.sampleRate)
        
