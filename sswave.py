#!/usr/bin/env python3

from clize import run
from struct import unpack
import matplotlib.pyplot as plots
import numpy
import os
import soundfile as sf


NAMES_ADDRESS = 0x0f009b
NAME_LENGTH = 8

WAVETABLES_ADDRESS = 0x10009b
WAVETABLE_COUNT = 128

WAVEFORM_COUNT = 8
WAVEFORM_SAMPLES = 512
WAVEFORM_BYTES = 2
WAVEFORM_LENGTH = WAVEFORM_SAMPLES * WAVEFORM_BYTES
WAVEFORM_AMPLITUDE = 65536  # peak to peak value range

OUT_SAMPLERATE = 44100


def reverse_bits(byte):
    """
    Reverse the bits of a byte, return string of binary digits
    """

    return '{:08b}'.format(byte)[::-1]


def get_names(firmware_file):
    """
    Read and return the wavetable names from a Shapeshifter firmware file
    """

    with open(firmware_file, 'rb') as f:

        # read wavetable names
        f.seek(NAMES_ADDRESS)
        names = []
        for i in range(WAVETABLE_COUNT):

            data = f.read(NAME_LENGTH)
            # reverse each bit
            data = [int(reverse_bits(byte), 2) for byte in data]
            # join chr value of each byte to a string
            name = ''.join(chr(byte) for byte in data)
            names.append(name)

    return names


def get_wavetables(firmware_file):
    """
    Read and return the wavetable data from a Shapeshifter firmware file
    """

    with open(firmware_file, 'rb') as f:

        # read wavetable data
        f.seek(WAVETABLES_ADDRESS)
        wavetables = []
        for i in range(WAVETABLE_COUNT):
            waveforms = []
            for j in range(WAVEFORM_COUNT):

                data = f.read(WAVEFORM_LENGTH)
                # reverse each bit
                data = [int(reverse_bits(byte), 2) for byte in data]
                # unpack 512 * 2 bytes little-endian
                data = unpack('<%ih' % WAVEFORM_SAMPLES, bytes(data))
                waveforms.append(data)

            wavetables.append(waveforms)

    return wavetables


def list_(infile):
    """
    List the wavetable names from a Shapeshifter firmware file

    :param infile: Path to firmware file (.jic)
    """

    names = get_names(infile)
    for name in names:
        print(name)


def plot(infile, outfile='wavetables.pdf'):
    """
    Plot the wavetable data from a Shapeshifter firmware file.

    :param infile: Path to firmware file (.jic)
    :param outfile: Filename for output. Format is deduced from extension, one of png, pdf, svg.
    """

    # This part is unconventional for matplotlib;
    # matplotlib performs terribly with a large number of subplots.
    # Instead, we plot all waveforms to a single plot.

    print('Plotting wavetables to %s...' % outfile)

    names = get_names(infile)
    wavetables = get_wavetables(infile)

    fig_rows = WAVETABLE_COUNT
    fig_cols = WAVEFORM_COUNT

    figure = plots.figure(figsize=(fig_cols, fig_rows), tight_layout=True)

    x_padding = WAVEFORM_SAMPLES / 5   # adjust for spacing
    y_padding = WAVEFORM_AMPLITUDE / 5 # adjust for spacing
    x_offset = WAVEFORM_SAMPLES + x_padding
    y_offset = WAVEFORM_AMPLITUDE + y_padding
    x_min = -1000                   # offset for text
    y_min = -WAVEFORM_AMPLITUDE / 2 # offset for negative amplitude
    x_max = fig_cols * x_offset
    y_max = fig_rows * y_offset - WAVEFORM_AMPLITUDE / 2

    axis = plots.subplot(1, 1, 1)
    axis.set_axis_off()
    axis.set_xlim([x_min, x_max])
    axis.set_ylim([y_max, y_min]) # axis is reversed here

    x_range = numpy.arange(WAVEFORM_SAMPLES)

    for i, (name, wavetable) in enumerate(zip(names, wavetables)):

        plots.text(x_min, i * y_offset, name, size='x-large')

        for j, waveform in enumerate(wavetable):

            # x_data is derived from a simple range
            # y_data is derived from waveform data and reversed (due to axis)
            x_data = x_range + j * x_offset
            y_data = numpy.negative(numpy.array(waveform)) + i * y_offset

            axis.plot(x_data, y_data, color='blue')

    plots.savefig(outfile)


def export(infile, *names, all_:'a'=False, singles:'s'=False, path:'p'='.'):
    """
    Export wavetables and a set of single-cycle wave files from a Shapeshifter firmware file

    :param infile: Path to firmware file (.jic)
    :param names: Names of the wavetables you want exported
    :param all: Export all waveforms from all wavetables
    :param path: Path where you want .wav files exported
    """

    fw_names = [name.strip() for name in get_names(infile)]
    wavetables = get_wavetables(infile)

    # collect in a dict to allow easier lookup
    wavetable_dict = {name: data for name, data in zip(fw_names, wavetables)}

    if all_:
        names = fw_names

    for name in names:

        wavetable = wavetable_dict.get(name, [])

        if not wavetable:
            print('Wavetable %s not found.')
            continue

        if singles:
            for index, waveform in enumerate(wavetable):
                data = numpy.int16(waveform)

                basename = '%(name)s_%(index)i.wav' % locals()
                filename = os.path.join(path, basename)

                sf.write(filename, data, OUT_SAMPLERATE)

        else:
            waveforms = numpy.array([numpy.int16(waveform) for waveform in wavetable])
            data = numpy.concatenate(waveforms)

            basename = '%(name)s.wav' % locals()
            filename = os.path.join(path, basename)

            sf.write(filename, data, OUT_SAMPLERATE)


def import_(infile, *imports):
    """
    Import a wavetable or a set of single-cycle wave files to a given wavetable

    :param infile: Path to firmware file (.jic)
    :param imports: A set of one to eight single-cycle wave files to import
    :param index: Zero-based start index from which to write waveforms
    :param name: Name of the wavetable to write to (see "list" command)
    :param newname: New name of the wavetable
    """

    INT_RANGE = 2**15
    SF_SUBTYPE_BITRATE_FACTOR = {
        'PCM_16': 1,
        'PCM_24': 1.5,
        'FLOAT': 2
    }

    fw_names = [name.strip() for name in get_names(infile)]

    # collect names and wave data
    names = []
    wavetables = []
    for file in imports:

        try:
            info = sf.info(file)
        except TypeError as e:
            print(e, file)

        if info.channels > 1:
            print('Stereo files are not supported (%s).' % file)
            continue

        if info.subtype == 'FLOAT':
            data, samplerate = sf.read(file)
            data = [int(x * INT_RANGE) for x in data]  # convert to 16-bit integer
        else:
            data, samplerate = sf.read(file, dtype='int16')


        basename = os.path.basename(file)

        names.append(name)
        wavetables.append(data)

    for name, wavetable in zip(names, wavetables):

        # TODO
        pass


def main():
    run(list_, plot, export, import_)


if __name__ == '__main__':
    main()
