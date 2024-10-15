import streamlit as st
import streamlit.components.v1 as components
import os
from dotenv import load_dotenv
from deepgram import DeepgramClient, PrerecordedOptions, SpeakOptions
from src.text_to_speech import text_to_speech
import base64
# Load environment variables
load_dotenv()

# Initialize the Deepgram client
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
deepgram = DeepgramClient(DEEPGRAM_API_KEY)
filename = "textspeech.wav"

# Audio recorder component with download functionality
def audio_recorder():
    audio_recorder_html = """
    <div>
        <button id="start">Start Recording</button>
        <button id="stop" disabled>Stop Recording</button>
        <audio id="audio" controls style="display:none;"></audio>
        <a id="download" style="display:none;">Download Recording</a>
    </div>
    <script>
        var audioData = null;
        const start = document.getElementById('start');
        const stop = document.getElementById('stop');
        const audio = document.getElementById('audio');
        const downloadLink = document.getElementById('download');
        let recorder;
        let chunks = [];

        // Start recording
        start.addEventListener('click', () => {
            start.disabled = true;
            stop.disabled = false;
            chunks = [];
            navigator.mediaDevices.getUserMedia({audio: true})
                .then(stream => {
                    recorder = new MediaRecorder(stream);
                    recorder.addEventListener('dataavailable', e => {
                        chunks.push(e.data);
                    });
                    recorder.start();
                });
        });

        // Stop recording and create downloadable link
        stop.addEventListener('click', () => {
            start.disabled = false;
            stop.disabled = true;
            recorder.stop();
            recorder.addEventListener('stop', () => {
                const blob = new Blob(chunks, { type: 'audio/wav' });
                audio.src = URL.createObjectURL(blob);
                audio.style.display = 'block';
                
                // Create download link
                downloadLink.href = audio.src;
                downloadLink.download = 'recorded_audio.wav';
                downloadLink.style.display = 'block';
                downloadLink.innerText = 'Download your audio file';
            });
        });
    </script>
    """
    components.html(audio_recorder_html, height=300)

    
# Function to transcribe uploaded audio file
def transcribe_audio_from_file(uploaded_file):
    audio_bytes = uploaded_file.read()
    source = {"buffer": audio_bytes, "mimetype": "audio/wav"}
    options = PrerecordedOptions(model="nova", language="en-US")
    
    response = deepgram.listen.prerecorded.v("1").transcribe_file(source, options)
    return response.results.channels[0].alternatives[0].transcript

# Main Streamlit App
st.title("Speech-to-Text and Text-to-Speech App")

option = st.radio("Choose an option:", ("Speech to Text", "Text to Speech"))

if option == "Speech to Text":
    st.subheader("Speech to Text")
    
    # Audio recording interface
    st.write("Record your audio and download it as a file:")
    audio_recorder()

    # File uploader for uploaded audio
    uploaded_audio = st.file_uploader("Upload the recorded audio (.wav)", type=["wav"])

    # Transcribe button
    if st.button("Transcribe") and uploaded_audio is not None:
        with st.spinner("Transcribing..."):
            transcript = transcribe_audio_from_file(uploaded_audio)
            st.subheader("Transcription:")
            st.write(transcript)
    elif st.button("Transcribe"):
        st.warning("Please upload a recorded audio file first.")

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
