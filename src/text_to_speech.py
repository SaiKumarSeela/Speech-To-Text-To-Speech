
import os
from dotenv import load_dotenv
from deepgram import (
    DeepgramClient,
    SpeakOptions,
)


def text_to_speech(client, text, filename="output.wav"):
    SPEAK_OPTIONS = {}
    SPEAK_OPTIONS['text'] = text
    try:
        # Configure the options (such as model choice, audio configuration)
        options = SpeakOptions(
            model="aura-asteria-en",
            encoding="linear16",
            container="wav"
        )

        # Call the save method on the speak property
        response = client.speak.v("1").save(filename, SPEAK_OPTIONS, options)
        print(response.to_json(indent=4))

    except Exception as e:
        print(f"Exception: {e}")

if __name__=="__main__":
    load_dotenv()

    text = "Hello, how can I help you today?"
    filename = "output.wav"

    DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
    client = DeepgramClient(api_key=DEEPGRAM_API_KEY)
    text_to_speech(client, text,filename )



