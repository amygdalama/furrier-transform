import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
from sys import argv


SAMPLES_PER_WINDOW = 326
SAMPLING_RATE = 44100


def linear_luminance(rgb):
    # rgb should be an array of length 3 with red, green, and blue values
    return 0.2126*rgb[0] + 0.7152*rgb[1] + 0.0722*rgb[2]


def luminosity(spectrogram):
    # Apply linear_luminance to the 3rd dimension array (i.e. the RGB values) of the spectrogram
    return np.apply_along_axis(linear_luminance, 2, spectrogram)


def frequency(normalized_row_index):
    # normalized_row_index should be the row index divided by the total number of rows
    # frequency is a function f: normalized row indices -> frequency
    # such that the range of frequencies is from 20Hz to 20000Hz (the range of human hearing)
    # and such that most of the high amplitude frequencies are <1000Hz
    return 120*np.exp(5.125*normalized_row_index)-100


def time(num_samples, sampling_rate=SAMPLING_RATE):
    return (1.0/sampling_rate)*np.arange(num_samples)


def transform(lum_spectrogram):
    num_rows, num_cols = lum_spectrogram.shape
    num_samples = num_cols * SAMPLES_PER_WINDOW
    t = time(num_samples)
    f = np.apply_along_axis(frequency, 0, np.arange(num_cols)/float(num_cols))
    print f


def main(image_filename):
    spectrogram = mpimg.imread(image_filename)
    lum_spectrogram = luminosity(spectrogram)
    output_signal = transform(lum_spectrogram)


if __name__ == "__main__":
    # argument is expected to be the filename (relative or absolute file path)
    # to an image to be converted to sound
    # add option for defining number of samples per window
    image_filename = "original_violin_spectrogram.png"
    main(image_filename)