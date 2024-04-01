from scipy.io import wavfile
import numpy as np
from sklearn.utils.class_weight import compute_class_weight
from tqdm import tqdm
from python_speech_features import mfcc
import random
from sklearn.model_selection import StratifiedKFold
import tqdm
import pickle
from numpy.random.mtrand import choice
import matplotlib.pyplot as plt
import streamlit as st


def normalize(x):
    x_normalized = (x - np.amin(x)) / (np.amax(x) - np.amin(x))
    return x_normalized


def standardize(x):
    x_standardized = (x - np.mean(x)) / np.std(x)
    return x_standardized


class Config:
    def __init__(
        self,
        mode="conv",
        nfilt=26,
        nfeat=13,
        nfft=512,
        rate=16000,
        sample_length=None,
        n_classes=2,
        n_train_samples=3000,
        n_val_samples=300,
    ):
        self.mode = mode
        self.nfilt = nfilt
        self.nfeat = nfeat
        self.nfft = nfft
        self.rate = rate
        self.sample_length = (
            int(sample_length) if rate is not None else int(rate / 10)
        )  # sample length in samples not seconds
        self.n_classes = n_classes
        self.n_train_samples = n_train_samples
        self.n_val_samples = n_val_samples


def generate_feature_samples(config, filename="/p_1_list_1_1.wav"):
    # _min, _max = float("inf"), -float("inf")
    rate, wav = wavfile.read(filename)

    # draw a random number which will serve as the beginning of the interval to sample (has to be in [0; total length - extraction window])
    sample_index = np.random.randint(0, wav.shape[0] - config.sample_length)

    # extract a sample corresponding to a length of config.sample_length, starting at sample_index
    sample = wav[sample_index : sample_index + config.sample_length]

    # compute the 'spectrogram' on the extracted sample
    sample_mfcc = mfcc(
        sample, rate, numcep=config.nfeat, nfilt=config.nfilt, nfft=config.nfft
    ).T

    # normalize every spectogram to range [0; 1]
    normalized_sample_mfcc = normalize(sample_mfcc)

    # normalize every spectogram to range [0; 1]
    standardized_sample_mfcc = standardize(sample_mfcc)

    sample_complete = np.concatenate(
        (sample_mfcc, normalized_sample_mfcc, standardized_sample_mfcc)
    )

    # convert lists of spectrograms and labels to arrays of arrays
    X = []

    # append sample spectrogram
    X.append(sample_complete if config.mode == "conv" else sample_complete.T)
    X = np.array(X)

    if config.mode == "conv":
        X = X.reshape(X.shape[0], X.shape[1], X.shape[2], 1)
    elif config.mode == "time":
        X = X.reshape(X.shape[0], X.shape[1], X.shape[2])

    return X
