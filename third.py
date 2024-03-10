import sounddevice as sd
import wave
import time
from openai import OpenAI
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

exit_flag = False
buffer = []

async def record_and_transcribe(filename, segment_duration, total_duration, samplerate=44100):
    print(f"Recording and transcribing audio from microphone to {filename}...")

    start_time = time.time()

    while time.time() - start_time < total_duration and not exit_flag:
        record_task = asyncio.create_task(record_audio(filename, segment_duration, samplerate))
        transcribe_task = asyncio.create_task(transcribe_audio(filename))

        await asyncio.gather(record_task, transcribe_task)
        

async def record_audio(filename, segment_duration, samplerate=44100):
    audio_data = sd.rec(int(samplerate * segment_duration), samplerate=samplerate, channels=2, dtype='int16')
    sd.wait()

    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(samplerate)
        wf.writeframes(audio_data.tobytes())

    # Добавляем записанный сегмент в буфер
    buffer.append(filename)

async def transcribe_audio(filename):
    if buffer:
        audio_file = buffer.pop(0)
        with open(audio_file, "rb") as file:
            transcription = client.audio.transcriptions.create(model="whisper-1", file=file)
            print(transcription.text)

if __name__ == "__main__":
    audio_filename = "C:/Users/Oleksyi/Desktop/project/sounds/recorded_audio.wav"
    segment_duration = 2
    total_duration = 300

    asyncio.run(record_and_transcribe(audio_filename, segment_duration, total_duration))

    print("Recording stopped.")
