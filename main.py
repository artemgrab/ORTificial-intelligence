import os
from openai import OpenAI
from dotenv import load_dotenv
import cv2
import sounddevice as sd
import wave
import time
import asyncio
import tkinter as tk

load_dotenv()
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)
path = "C:/Users/Oleksyi/Desktop/project/videos"
dir_list = os.listdir(path)
frameTime = 40

database = {
    ("доброго", "ранку"): "hi",
    ("добрий", "ранок"): "hi",
    ("доброго", "ранок"): "hi",
    ("добрий", "ранку"): "hi",
    ("нуль",): "0",
    ("один",): "1",
    ("два",): "2",
    ("три",): "3",
    ("чотири",): "4",
    ("п'ять",): "5",
    ("шість",): "6",
    ("сім",): "7",
    ("вісім",): "8",
    ("0",): "0",
    ("1",): "1",
    ("2",): "2",
    ("3",): "3",
    ("4",): "4",
    ("5",): "5",
    ("6",): "6",
    ("7",): "7",
    ("8",): "8",
    ("плюс",): "плюс",
    ("мінус",): "мінус",
    ("з днем народження",): "birthday",
    ("ласкаво просимо",): "welcome",
    ("+",): "плюс",
    ("-",): "мінус",
    ("математика",): "математика",
    ("математики",): "математика",
    ("математикам",): "математика",
    ("ранок", "добрий"): "hi",
    ("урок",): "урок",
    ("дорівнює",): "дорівнює",
    ("матика",): "математика",
    
    
}

exit_flag = False
buffer = []

def play_video(video_path):
    cap = cv2.VideoCapture(video_path)

    cv2.namedWindow('Video', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Video', 420, 260)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow('Video', frame)

        if cv2.waitKey(frameTime) & 0xFF == ord('q'):
            break

    cap.release()

def sanitize(text):
    return text.replace(".", " ").replace(",", " ").replace("!", " ").replace("?", " ").replace(";", " ").replace("у нас", " ")

async def transcribe_audio(filename):
    
    audio_file = buffer.pop(0)
    with open(audio_file, "rb") as file:
        global transcription
        transcription = client.audio.transcriptions.create(model="whisper-1", language='uk', file=file).text
        transcription = sanitize(transcription)
        print(transcription)
            
async def record_and_transcribe(filename, segment_duration, total_duration, samplerate=44100):
    global transcription
    audio_filename = filename
    i = 0
    transcription = ""  

    while time.time() - start_time < total_duration and not exit_flag:
        record_task = asyncio.create_task(record_audio(audio_filename, segment_duration, samplerate))
        transcribe_task = asyncio.create_task(transcribe_audio(audio_filename))

        await asyncio.gather(record_task, transcribe_task)
        

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f'''Кілька прикладів особливостей жестової (візуальної) мови. Заперечення показують наприкінці речення: «Я не розумію» буде як «Я розумію ні». Спочатку кажуть про фон, а потім про решту, тобто жести «Парта. Олівець. Під» означатиме «Олівець під партою».

                                    Якщо йдеться про якийсь об'єкт, ми кажемо «Він, його», але в розмові може виникнути плутанина «Учитель зустрів учня, і він його похвалив». У жестовій мові таких непорозумінь не виникає одна рука показуватиме, приміром, «учитель», а інша зробить низку жестів це розповідь про вчителя.
                                    ось приклади, як правильно переробляти порядок слів для жестової мови:
                                    
                                    Ти любиш дивитися бейсбол?
                                    БЕЙСБОЛ ДИВИТИСЬ ТИ ЛЮБИТИ?

                                    Моя донька дала мені красиві квіти.
                                    КРАСИВО КВІТИ МОЯ ДОНЬКА ДАТИ-МЕНІ.

                                    Я шукаю нового лікаря.
                                    НОВИЙ ЛІКАР ШУКАТИ Я.

                                    Я хочу попити води.
                                    ВОДА ПИТИ Я ХОТІТИ.

                                    Моя донька завжди щаслива
                                    МОЯ ДОНЬКА ВОНА ЗАВЖДИ ЩАСТЯ.

                                    Я купив нового капелюха.
                                    НОВИЙ КАПЕЛЮХ Я КУПИТИ ЗАКІНЧИТИ.

                                    Я чув ти звільняєшся з роботи.
                                    ТВОЯ РОБОТА ТИ ЗВІЛЬНЯТИСЬ Я ЧУВ.

                                    Моя сестра народжує ще одну дитину.
                                    ЩЕ ОДНА ДИТИНА МОЯ СЕСТРА НАРОДИТИ-БУДЕ.

                                    Твоя ідея це абсурд!
                                    ТВОЯ ІДЕЯ АБСУРД!

                                    Перепиши наступну фразу, так як би її сказали мовою жестів. Всі слова мають бути у базовій формі, не пиши ніяких пояснень, лише послідовність слів: {transcription}''',
                }
            ],
            model="gpt-3.5-turbo",
        )

        chat_response = chat_completion.choices[0].message.content
        chat_response_lower = chat_response.lower()
        print(chat_response_lower)
        list_chat_response = sanitize(chat_response_lower).split()
        print(list_chat_response)
        frameTime = 1

        while i < len(list_chat_response):
            found = False
            for count in reversed(range(1, 4)):
                words_c = tuple(list_chat_response[i:i + count])

                if words_c in database:
                    video_key = database[words_c]
                    video_path_word = os.path.join(path, video_key + ".mp4")
                    print("playing", video_path_word)
                    play_video(video_path_word)
                    print("end playing", video_path_word)
                    i += count
                    found = True
                    break

            if not found:
                for letter in list_chat_response[i]:
                    path_letter = os.path.join(path, f"{letter}.mp4")

                    if os.path.exists(path_letter):
                        video_path_letter = path_letter
                        print("playing", video_path_letter)
                        play_video(video_path_letter)
                        print("end playing", video_path_letter)

                i += 1


async def record_audio(filename, segment_duration, samplerate=44100):
    print("listening...")
    audio_data = sd.rec(int(samplerate * segment_duration), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()

    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(samplerate)
        wf.writeframes(audio_data.tobytes())
        print("Recording audio... written", len(audio_data.tobytes()), "bytes")
 
    buffer.append(filename)




if __name__ == "__main__":
    audio_filename = "C:/Users/Oleksyi/Desktop/project/sounds/recorded_audio.wav"
    segment_duration = 15
    total_duration = 300
    start_time = time.time()

    asyncio.run(record_and_transcribe(audio_filename, segment_duration, total_duration))

    print("Recording stopped.")
