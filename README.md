# iqtool
A set of python applications for generating and viewing quadrature IQ binary files. 
Intended for use with software defined radios and lab test equipment.

## Requirements
* Tested with Python 2.7 and 3.6
* Requires numpy and matplotlib

# iqgen
Generates an binary IQ file of a user specified size.

Usage: **python iqgen.py *numberOfSamples***

## Settings
### Signal type
iqgen can generate files with three types of signal:
1. Impulse signal **[-i]** (Default)
2. Tone signal **[-t Freq (Hz)]**
3. Random signal **[-r]**

### Sample rate
* When generating the tone signal the sample rate can be specified using the **[-t FREGUENCY (Hz)]** option
* By default the sample rate is set to 1 MHz

### Data format
* The output data type can be set to **[int8 | int16 | int32]** using the **[-f intX]** option
* By default the output type is set to int16

### Output amplitude
* The amplitude of each signal can be set using the **[-a AMPLITUDE]** option.
* By default the amplitude is set to the full scale value to the selected data type

### Endianness
* By default the endian is set to little endian.
* Big endian output can be selected using **[-be]**

### Output order
* By default the I value is saved into the output file first
* Q can be saved first by using the option **[-qi]**

### Output file name
* A suitable output filename is automatically generated based on the options selected
* The default filename can be overridden using the **[-o FILENAME]** option
