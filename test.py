import os
import cv2
import tkinter as tk
import time


database = {
    ("доброго", "ранку"): "hi",
    ("нуль", ): "0",
    ("один", ): "1",
    ("два", ): "2",
    ("три", ): "3",
    ("чотири", ): "4",
    ("п'ять", ): "5",
    ("шість", ): "6",
    ("сім", ): "7",
    ("вісім", ): "8",
    #("плюс", ): "+",
    ("з днем народження", ): "birthday",
    ("ласкаво просимо", ): "welcome",
}


chat_response = 'один плюс два'
chat_response_lower = chat_response.lower()
list_chat_response = chat_response_lower.split()
frameTime = 1

path = "C:/Users/Oleksyi/Desktop/project/videos"
dir_list = os.listdir(path)





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
    #cv2.destroyAllWindows()


i = 0
while i < len(list_chat_response):
    found = False
    for count in reversed(range(1, 4)):
        words_c = tuple(list_chat_response[i:i + count])

        if words_c in database:
            video_key = database[words_c]
            video_path_word = os.path.join(path, video_key + ".mp4")
            play_video(video_path_word)

            i += count
            found = True
            break

    if not found:
        i += 1
        word_path_2 = os.path.join(path, list_chat_response[i] + ".mp4")

        if os.path.exists(word_path_2):
            video_path_word_2 = word_path_2
            play_video(video_path_word_2)
        else: 
            for letter in list_chat_response[i]:
                path_letter = os.path.join(path, f"{letter}.mp4")

                if os.path.exists(path_letter):
                    video_path_letter = path_letter
                    play_video(video_path_letter)

#print(list_chat_response[i], "not found")
