import streamlit as st
import numpy as np
import sounddevice as sd
from scipy.io import wavfile
import os
from dotenv import load_dotenv
from deepgram import DeepgramClient
from src.text_to_speech import text_to_speech
from src.speech_to_text import transcribe_audio
import time

# Load environment variables
load_dotenv()

# Initialize the Deepgram client
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
deepgram = DeepgramClient(DEEPGRAM_API_KEY)

# Audio recording parameters
SAMPLE_RATE = 16000  # 16 kHz sample rate for better compatibility
CHANNELS = 1  # Mono channel

filename = "output.wav"


# Initialize session state variables
if 'audio_data' not in st.session_state:
    st.session_state.audio_data = None
if 'recording' not in st.session_state:
    st.session_state.recording = False
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'audio_file' not in st.session_state:
    st.session_state.audio_file = None

def record_audio():
    st.session_state.audio_data = sd.rec(int(60 * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=CHANNELS, dtype='int16')

def stop_recording():
    sd.stop()
    duration = time.time() - st.session_state.start_time
    st.session_state.audio_data = st.session_state.audio_data[:int(SAMPLE_RATE * duration)].flatten()
    
    # Save the recorded audio to a file
    wavfile.write(filename, SAMPLE_RATE, st.session_state.audio_data)
    st.session_state.audio_file = filename

st.title("Speech-to-Text and Text-to-Speech App")

option = st.radio("Choose an option:", ("Speech to Text", "Text to Speech"))

if option == "Speech to Text":
    st.subheader("Speech to Text")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Start Recording"):
            st.session_state.recording = True
            st.session_state.start_time = time.time()
            record_audio()
            st.success("Recording started.")
    
    with col2:
        if st.button("Stop Recording"):
            if st.session_state.recording:
                stop_recording()
                st.session_state.recording = False
                st.success("Recording stopped.")
            else:
                st.warning("No active recording to stop.")
    
    if st.session_state.audio_file:
        st.audio(st.session_state.audio_file)
    
    if st.button("Transcribe"):
        if st.session_state.audio_data is not None:
            with st.spinner("Transcribing..."):
                transcript = transcribe_audio(client= deepgram,audio_data=st.session_state.audio_data, sample_rate= SAMPLE_RATE)
                st.subheader("Transcription:")
                st.write(transcript)
        else:
            st.warning("Please record audio first.")

elif option == "Text to Speech":
    st.subheader("Text to Speech")
    
    text_input = st.text_area("Enter text to convert to speech:")
    
    if st.button("Generate Speech"):
        if text_input:
            text_to_speech(client=deepgram, text= text_input,filename= filename)
            st.session_state.audio_file = filename
            if st.session_state.audio_file:
                st.audio(st.session_state.audio_file)
        else:
            st.warning("Please enter some text to convert to speech.")