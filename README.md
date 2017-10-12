# iqtool
A set of python applications for generating and viewing quadrature IQ binary files. 
Intended for use with software defined radios and lab test equipment.

## Requirements
* Tested with Python 2.7 and 3.6.
* Requires numpy and matplotlib.

# iqgen
Generates an binary IQ file of a user specified size.

Usage: **python iqgen.py *numberOfSamples***

## Settings
### Signal type
iqgen can generate files with three types of signal:
1. Impulse signal **[-i]** (Default).
2. Tone signal **[-t Freq (Hz)]**.
3. Random signal **[-r]**.

### Sample rate
* When generating the tone signal the sample rate can be specified using the **[-fs FREQUENCY (Hz)]** option.
* By default the sample rate is set to 1 MHz.

### Data format
* The output data type can be set to **[int8 | int16 | int32 | float16 | float32 | float64]** using the **[-f DATAFORMAT]** option.
* By default the output type is set to int16.

### Output amplitude
* The amplitude of each signal can be set using the **[-a AMPLITUDE]** option.
* By default the amplitude is set to the full scale value to the selected data type.

### Endianness
* By default the endian is set to little endian.
* Big endian output can be selected using **[-be]**.

### Output order
* By default the I value is saved into the output file first.
* Q can be saved first by using the option **[-qi]**.

### Output file name
* A suitable output filename is automatically generated based on the options selected.
* The default filename can be overridden using the **[-o FILENAME]** option.


# iqplot
Plots the I and Q data from a user specified binary file.

Usage: **python iqplot.py *filename***

## Settings
### Offset
* The offset in bytes from the beginning of the file can be set using the **[-o OFFSET (bytes)]** option.
* This can be used to skip headers, etc at the beginning of the binary file.
* By default the offset is set to 0.

### Plot Start Sample
* The start sample can be set using the **[-s STARTSAMPLE]** option.
* This can be used in combination with the NUMBEROFSAMPLES option to only plot a specific part of a file.
* By default the start sample is set to 0.

### Number of samples to plot
* The number of sample to plot is set using the **[-n NUMBEROFSAMPLES]** option.
* By default all samples from the STARTSAMPLE to the end of the file will be plotted.

### Sample rate
* When the sample rate can be specified using the **[-fs FREQUENCY (Hz)]** option.
* Setting the sample rate allows the the time and frequency axis labels to be correctly set.

### Data format
* The input data type can be set to **[int8 | int16 | int32 | uint8 | uint16 | uint32 | float16 | float32 | float 64]** using the **[-f DATAFORMAT]** option.
* By default the data type is set to int16.

### Endianness
* By default the endian is set to little endian.
* Big endian output can be selected using **[-be]**.

### Output order
* By default the I value is assumed to be the first sample in the input file.
* If Q is the first sample in the input file then use the option **[-qi]**.

### Plot Type
* By default a time domain plot of the I and Q data will be displayed.
* A power spectral density plot can be displayed using the option **-p psd**.
* A spectrogram plot can be displayed using the option **-p spec**.

### FFT Window Type
* The window used for the psd or spectrogram plots can be set to **[rectangular | bartlett | blackman | hamming | hanning]** using the command **[-w WINDOWTYPE]**.

### FFT Width
* When displaying a spectrogram plot the FFT width should be set using the option **-fw FFTWIDTH**.
* The overlap between each FFT in the spectrogram is set to FFTWIDTH/10.
