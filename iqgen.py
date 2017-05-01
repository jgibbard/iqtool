#!/usr/bin/env python

#Copyright (c) 2017 James Gibbard

#Generates an IQ data file based on provided parameters
#Tested with python 2.7 and 3.6
#Requires numpy and matplotlib

import argparse
from sys import byteorder
import numpy as np
import matplotlib.pyplot as plt

def generateTone(fs, toneFreq, numSamples, amplitude):
    #Generates a sinusoidal signal with the specified
    #frequency and amplitude
    
    step = (float(toneFreq) / float(fs)) * 2.0 * np.pi
    
    phaseArray = np.array(range(0,numSamples)) * step
    
    #Euler's Formular: e^(j*theta) = cos(theta) + j * sin(theta)
    #For a complex sinusoidal theta = 2*pi*f*t where each time step is 1/fs    
    wave = np.exp(1.0j * phaseArray) * amplitude
    
    return wave

def generateRandom(numSamples, amplitude):
    #Generate random data from both I and Q
    scale = int(amplitude)
    realArray = np.random.randint(-scale, scale,numSamples)
    imagArray = np.random.randint(-scale, scale,numSamples)
    
    return realArray + 1j * imagArray

def generateImpulse(numSamples, amplitude):
    #Generates an impulse signal
    #Impulse is place in middle of array
    
    wave = np.zeros(numSamples, 'complex')
    wave[int(numSamples/2)] = amplitude + 1.0j * amplitude
    
    return wave
    
def complexToSingleArray(array, orderIQ):
    #Convert compex array to real array when 
    #I and Q are stored one after each other
    #This is done because numpy can only write 
    #complex numbers as to a file in certain data types     
    
    realArray = np.real(array)
    imagArray = np.imag(array)
    
    #Create array double length of input to hold both real and imag values
    output = np.zeros(realArray.size + imagArray.size)
    
    #Pack  real (I) and imag (Q) values in the correct order
    #By default numpy writes index 0 to an output file first
    if orderIQ:
        output[0::2] = realArray
        output[1::2] = imagArray
    else:
        output[1::2] = realArray
        output[0::2] = imagArray
        
    return output

if __name__ == '__main__':
    
    #Generate command line parser to parse inputs
    cliParser = argparse.ArgumentParser(description='Generates quadrature IQ samples')
    
    #The number of samples is the only compulsory option
    cliParser.add_argument('samples', type=int, help='number of output samples')
    
    #These options are mutually exclusive, i.e. only one may be picked
    outTypeGroup = cliParser.add_mutually_exclusive_group()
    outTypeGroup.add_argument('-t', '--tone', type=float, 
        help='output sinusoidal tone [Hz]')
                                
    outTypeGroup.add_argument('-i', '--impulse', action='store_true', 
        help='generate impulse')
                                
    outTypeGroup.add_argument('-r', '--random', action='store_true', 
        help='generate random data')
    
    #All these options are optional
    cliParser.add_argument('-fs', '--sampleRate', type=float, 
        help='sets the sample rate [sps] (default=1e6)',  default=1000000.0)
    
    cliParser.add_argument('-o', '--filename', type=str, help='output filename')
    
    cliParser.add_argument('-f', '--format', type=str, 
        help='Output format [int8 | int16 | int32] (default=int16)', 
        default='int16')
                        
    cliParser.add_argument('-a', '--amplitude', type=float,
        help='amplitude the output')
                                
    cliParser.add_argument('-be', '--bigendian', action='store_true', 
        help='output data in big endian format (default=False)')
                        
    cliParser.add_argument('-qi', '--orderQI', action='store_true', 
        help='store output data as Q then I (Default = I then Q)')
    cliParser.add_argument('-p', '--plot', action='store_true', 
        help='display a plot of the output')

    args = cliParser.parse_args()

    if args.tone == None and args.impulse == False and args.random == False:
        print("Output type not specified. Assuming impulse output")        
    
    #Set the scale value
    if args.amplitude != None:
        amplitude = args.amplitude
    else:
        if args.format == 'int16':
            amplitude = ((2.0**15) - 1)
        elif args.format == 'int32':
            amplitude = ((2.0**31) - 1)
        elif args.format == 'int8':
            amplitude = ((2.0**7) - 1)
        else:
            cliParser.error('Output format must be [int8 | int16 | int32]')          
            
    #Set the output type
    if args.tone != None:    
        #If the tone frequency is set then output a tone
        output = generateTone(args.sampleRate, args.tone, args.samples, amplitude)
        filename = "tone_" + str(args.tone) + "_fs_" + str(args.sampleRate)
    
    elif args.random:
        #If random is set output random data in both I and Q
        output = generateRandom(args.samples, amplitude)
        filename = "random"
    else:
        #Otherwise output an impulse signal
        output = generateImpulse(args.samples, amplitude)
        filename = "impulse"
    
    #Append whether I or Q comes first in the the filename
    if args.orderQI:
        filename += "_QI"
    else:
        filename += "_IQ"
        
    #Set output data type format
    if args.format == 'int16':
        output = complexToSingleArray(output, not args.orderQI).astype(np.int16)
    elif args.format == 'int32':
        output = complexToSingleArray(output, not args.orderQI).astype(np.int32)
    elif args.format == 'int8':
        output = complexToSingleArray(output, not args.orderQI).astype(np.int8) 
    
    #Add the data format to the filename
    filename += '_' + str(args.format) 
        
    #If system byteorder is different to desired output byte order
    #Then swich the endianness
    if byteorder == 'little':
        if args.bigendian == True:        
            output = output.byteswap()            
    elif byteorder == 'big':
        if args.bigendian == False:     
            output = output.byteswap()
    
    #Add the endianness to the filename
    if args.bigendian == False:
        filename += "_LE"
    else:
        filename += "_BE"
    
    filename += ".dat"
    
    #If a filename is set in the arguments then use it
    if args.filename != None:
        filename = args.filename        
        
    #Open the output file and write the data to it      
    with open(filename, 'wb') as f:
        output.tofile(f)
        
    #If plotting is enabled then generate a plot
    if args.plot:
        if args.orderQI:
            plt.plot(output[1::2], label='I')
            plt.plot(output[0::2], label='Q')
        else:
            plt.plot(output[0::2], label='I')
            plt.plot(output[1::2], label='Q')
        plt.grid(True)  
        plt.legend(loc='upper right', frameon=True)        
        plt.show()
        
        
