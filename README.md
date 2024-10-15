# Speech-to-Text and Text-to-Speech Application

This project is a versatile web-based application that allows users to record speech, transcribe it into text, or convert text into speech. It is developed using **Streamlit** and **FastAPI**, with two approaches for audio recording:
1. **Sounddevice Library**: Suitable for production environments.
2. **JavaScript-based Audio Recording**: A fallback option to support browsers or environments where sounddevice may not work.

## Features

- **Speech-to-Text**: Record audio, transcribe it into text using Deepgram's API.
- **Text-to-Speech**: Enter text and convert it into an audio file (WAV format).
- Developed in both **Streamlit** and **FastAPI** for frontend flexibility.
  
## Project Structure

- **Streamlit Version**:
  - Audio recording using the `sounddevice` library for direct microphone access.
  - Integration with Deepgram API for transcription and speech synthesis.
  - Simple UI built with Streamlit to allow easy interaction.
  
- **FastAPI Version**:
  - Audio processing using JavaScript for recording and base64 encoding.
  - FastAPI backend to handle file uploads, audio transcription, and speech synthesis.
  - Templates rendered using Jinja2 for serving HTML pages.

## Project Demo

[![SpeechToTextUI](https://github.com/user-attachments/assets/2eae02f2-16b1-4e8f-833d-89c477d25f0a)](https://github.com/user-attachments/assets/b098ad97-3ec3-40f9-b621-481e96d19bff)

## Setup Instructions

### Prerequisites
- Python 3.8+
- Install dependencies: `pip install -r requirements.txt`
- Create a `.env` file with your Deepgram API key:
  ```
  DEEPGRAM_API_KEY=your_api_key_here
  ```

### Running the Application

#### Streamlit Version
1. Clone the repository:
   ```bash
   git clone https://github.com/SaiKumarSeela/Speech-To-Text-To-Speech.git
   cd Speech-To-Text-To-Speech
   ```
2. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```
3. Open `http://localhost:8501` in your browser.

#### FastAPI Version
1. Run the FastAPI app:
   ```bash
   uvicorn main:app --reload
   ```
2. Open `http://localhost:8000` in your browser.

### Using the Application

#### Streamlit App
- Choose either **Speech to Text** or **Text to Speech** mode.
- Record audio or input text for processing.
- View the transcription or play the generated audio.

#### FastAPI App
- Upload audio in base64 format or enter text for speech generation.
- Receive the transcribed text or download the generated audio file.

## Technology Stack

- **Frontend**: Streamlit, JavaScript (for FastAPI version)
- **Backend**: FastAPI, Python
- **APIs**: Deepgram API for Speech-to-Text and Text-to-Speech
- **Libraries**: Sounddevice, Scipy, Jinja2, dotenv, Deepgram SDK
