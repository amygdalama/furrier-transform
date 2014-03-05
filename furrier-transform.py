from sys import argv

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
from scikits import audiolab
import scipy.io.wavfile as wavfile

import lerp


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


def time(num_samples, sampling_rate=44100):
    return (1.0/sampling_rate)*np.arange(num_samples)


def amplitude(lum_spectrogram, SAMPLES_PER_WINDOW=326):
    num_rows, num_cols = lum_spectrogram.shape
    num_samples = num_cols * SAMPLES_PER_WINDOW
    a = np.zeros((num_rows, num_samples))
    for i in range(num_rows):
        X, Y = lerp.lerp(np.arange(num_cols), lum_spectrogram[i], nx=SAMPLES_PER_WINDOW, nBlend=15)
        a[i] = Y
    return a

def generate_from_image(filename, random_phases=False):
    SAMPLES_PER_WINDOW = 326
    SAMPLING_RATE = 44100
    spectrogram = mpimg.imread(filename)
    lum_spectrogram = luminosity(spectrogram)

    # mpimg reads in an image with an upside-down y-axis (i.e. 0 at the top and
    # max(y) at the bottom), so we need to flip it    
    lum_spectrogram = np.flipud(lum_spectrogram)    
    num_rows, num_cols = lum_spectrogram.shape
    num_samples = num_cols * SAMPLES_PER_WINDOW
    t = np.matrix(time(num_samples))
    f = np.matrix(np.apply_along_axis(frequency, 0, np.arange(num_rows)/float(num_rows)))
    f = f.transpose()
    if random_phases:
        phi = np.matrix(np.random.rand(num_rows)*2*np.pi)
        phi = phi.transpose()
    else:
        phi = np.random.random()*2*np.pi
    a = amplitude(lum_spectrogram)
    oscillators = np.multiply(a, np.sin(2*np.pi*f*t+phi))
    signal = oscillators.sum(axis=0)
    signal = signal / np.amax(np.absolute(signal))
    signal = np.squeeze(np.asarray(signal))
    wavfile.write("output_signal.wav", SAMPLING_RATE, signal)


def generate_from_sound(filename):
    samples_per_window = 128
    # violin, sampling_rate, encoding = audiolab.oggread(filename)
    sampling_rate, violin = wavfile.read(filename)
    Pxx, freqs, bins, im = plt.specgram(violin, Fs=sampling_rate)
    num_rows, num_cols = Pxx.shape
    num_samples = num_cols * samples_per_window
    f = np.matrix(freqs).transpose()
    print f
    t = np.matrix(np.linspace(bins[0], bins[-1], num_samples))
    a = amplitude(Pxx, samples_per_window)
    phi = np.random.random()*2*np.pi
    oscillators = np.multiply(a, np.sin(2*np.pi*f*t+phi))
    signal = oscillators.sum(axis=0)
    signal = signal / np.amax(np.absolute(signal))
    signal = np.squeeze(np.asarray(signal))
    wavfile.write("flute_signal_from_sound.wav", sampling_rate, signal)     


def main():
    generate_from_sound("flute.wav")
    # generate_from_image("original_violin_spectrogram.png")


if __name__ == "__main__":
    # argument is expected to be the filename (relative or absolute file path)
    # to an image to be converted to sound
    # add option for defining number of samples per window
    main()

