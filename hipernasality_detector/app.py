# import std libraries
import numpy as np
import pandas as pd
import time
from IPython.display import HTML
import pickle
import json
import streamlit as st
from st_aggrid import AgGrid
import utils
from scipy.io import wavfile

# from utils import load_audio, predict
from tqdm import tqdm

# from pydub import AudioSegment

# sidebar
with st.sidebar:
    # title
    st.title("Hypernasality Detector")
    # image
    st.image("hands_image.jpeg")
    # blank space

st.image("waves_streamlit.png")
st.title("Hypernasal or Not?")


uploaded_file = st.file_uploader("Upload your .wav file", type=["wav"])

if uploaded_file is not None:
    # with open('tmp/uploaded_wavefile.wav', 'w') as

    rate, wav = wavfile.read(uploaded_file)

    sampling_rate = 16000
    sample_duration_sec = 0.3
    sample_length = sample_duration_sec * sampling_rate

    config = utils.Config(
        mode="conv",
        n_classes=2,
        sample_length=sample_length - 1,
        n_train_samples=2000,
        n_val_samples=400,
    )
    st.audio(uploaded_file)

    with open("cnn_model.pkl", "rb") as model_file:
        cnn_model = pickle.load(model_file)

    X = utils.generate_feature_samples(config, uploaded_file)
    prediction = cnn_model.predict(X)
    prediction = list(prediction)
    st.markdown("#### Prediction:")

    classes = ["Normal", "Hypernasal"]
    result = np.argmax(prediction[0])

    st.markdown(f"## {classes[result]}: {prediction[0][result]:.2%}")
    # st.write(type(prediction))
