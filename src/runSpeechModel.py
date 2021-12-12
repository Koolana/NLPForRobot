# -*- coding: utf-8 -*-

# Speech recognition and text to speech libraries
import speech_recognition as sr
from gtts import gTTS

# Library to play mp3
from pygame import mixer

import torch
from runModel import Translater

mixer.init()

# Microphone and recognition
r = sr.Recognizer()
m = sr.Microphone()

pathToRoberta = '../models/ruRoberta-large'
pathToModel = '../models/robot-brain-v2.pt'

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print('Use:', device)

translater = Translater(pathToRoberta, pathToModel, device)
print('Translater done!')

try:
    print("A moment of silence, please...")
    with m as source:
        r.adjust_for_ambient_noise(source)
    print("Set minimum energy threshold to {}".format(r.energy_threshold))
    while True:
        print("Say something!")
        with m as source:
            audio = r.listen(source)
        print("Got it! Now to recognize it...")
        try:
            statement = r.recognize_google(audio, language="ru_RU")

            print("You said: {}".format(statement))
            print("Your command: {}\n".format(translater.recognizeCmd(str(statement))))
        except sr.UnknownValueError:
            print("Oops! Didn't catch that")
        except sr.RequestError as e:
            print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
except KeyboardInterrupt:
    pass
