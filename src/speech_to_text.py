import io
from scipy.io import wavfile
from deepgram import (
    DeepgramClient,
    PrerecordedOptions

)
import os


def transcribe_audio(client, audio_data, sample_rate=1600):
    byte_io = io.BytesIO()
    wavfile.write(byte_io, sample_rate, audio_data)
    audio_bytes = byte_io.getvalue()

    source = {"buffer": audio_bytes, "mimetype": "audio/wav"}
    options = PrerecordedOptions(model="nova", language="en-US")

    response = client.listen.prerecorded.v("1").transcribe_file(source, options)
    return response.results.channels[0].alternatives[0].transcript

# if __name__=="__main__":
#     DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
#     SAMPLE_RATE = 16000 
#     CHANNELS = 1 
#     client = DeepgramClient(api_key=DEEPGRAM_API_KEY)

