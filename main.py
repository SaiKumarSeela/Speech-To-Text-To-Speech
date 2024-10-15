# main.py
from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import base64
import os
from dotenv import load_dotenv
from deepgram import DeepgramClient, PrerecordedOptions, SpeakOptions
from pydantic import BaseModel
from src.text_to_speech import text_to_speech

# Load environment variables
load_dotenv()

# Initialize the Deepgram client
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
deepgram = DeepgramClient(DEEPGRAM_API_KEY)
filename = "textspeech.wav"

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

class AudioData(BaseModel):
    audioData: str

class TextData(BaseModel):
    text: str

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

def transcribe_audio_from_file(audio_file_path):
    with open(audio_file_path, "rb") as f:
        audio_bytes = f.read()
    
    source = {"buffer": audio_bytes, "mimetype": "audio/wav"}
    options = PrerecordedOptions(model="nova", language="en-US")
    
    response = deepgram.listen.prerecorded.v("1").transcribe_file(source, options)
    return response.results.channels[0].alternatives[0].transcript

@app.post("/upload-audio")
async def upload_audio(audio_data: AudioData):
    # Decode the base64 audio data
    audio_bytes = base64.b64decode(audio_data.audioData)
    
    # Save the audio file
    audio_file_path = "output.wav"
    with open(audio_file_path, "wb") as f:
        f.write(audio_bytes)
    
    # Transcribe the audio
    transcript = transcribe_audio_from_file(audio_file_path)
    
    return {"status": "success", "transcript": transcript}

@app.post("/text-to-speech")
async def generate_speech(text_data: TextData):
    try:
        text_to_speech(client=deepgram, text=text_data.text, filename=filename)
        return {"status": "success", "audio_url": f"/audio/{filename}"}
    except Exception as e:
        print(f"Error in text-to-speech: {e}")
        return {"status": "error", "message": str(e)}

@app.get("/audio/{file_name}")
async def get_audio(file_name: str):
    file_path = f"{file_name}"
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="audio/wav", filename=file_name)
    return {"error": "File not found"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)