#!/usr/bin/env python3

import speech_recognition as sr
from Levenshtein import distance as lev
import os
import random

from data_preprocessing import questions
from magicMouth import MagicMouth

mouth = MagicMouth()

Gryffindor = 0
Ravenclaw = 0
Hufflepuff = 0
Slytherin = 0

r = sr.Recognizer() #as well shit variable name
with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source)

def play_audio(filename):
    mouth.speak(f'./Voicelines/{filename}.wav')

random_phrases = ['hmm', 'thank_you_for_looking_so_good', 'very_interesting']
def play_random_phrases():
    can_play = random.random()
    print(can_play)
    if can_play < 33:
        index = random.randrange(len(random_phrases))
        play_audio(random_phrases[index])

def get_index_of_most_likely_answer(distance):
        min_distance = distance[0][6]
        index = 0
        for i in range(len(distance)):
            print(distance[i][6])
            if(distance[i][6] < min_distance):
                min_distance = distance[i][6]
                index = i
        return index

play_audio('i-shall-place-the-sorting-hat-on-your-head-and-you-will-be-sorted-into-your-houses')
play_audio('000_introduction')

# Iteration through questions
repeat = True
for question in questions[1:-18]:
    user_input = ''
    repeat = True
    
    while repeat:
        repeat = False

        # prints literal question text
        print(question["data"][1]) 
        print('')

        play_audio(question["data"][2])
        display_answer_counter = 1
        for answer in question["answers"]:
            print(f'{display_answer_counter}. {answer[1]}')
            if len(answer) == 7:
                play_audio(answer[6])
            display_answer_counter += 1
        print('')
        
        # speech recognitiondff
        with sr.Microphone() as source:
            print("please tell your answer clearly")
            audio = r.listen(source,10, phrase_time_limit=10)
            print(audio)
            print("hmm let me think")
        try:
            user_input = r.recognize_google(audio)
            print(f'User input: {user_input}')
        except sr.UnknownValueError:
            print("I'm a bit old and my hearing is not the best anymore, please repeat")
            continue
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            continue

        if user_input == 'repeat' or user_input == 'please repeat': #this is bad and you know it
            repeat = True

    distance = []
    c = 0
    for answer in question["answers"]:
        lev_distance = lev(answer[1], user_input)
        answer.append(lev_distance)
        distance.append(answer)
        print(f'Answer {c + 1}: {distance[c][6]}')
        c += 1
        # distance =[['q_ID', 'a1_text', 'g', 'r', 'h', 's', distance]]
    print('')
        
    index = get_index_of_most_likely_answer(distance)
    print(f'index {index}')
    print(distance[index][1])

    Gryffindor = Gryffindor+ float(distance[index][2])
    Ravenclaw = Ravenclaw+ float(distance[index][3])
    Hufflepuff = Hufflepuff+ float(distance[index][4])
    Slytherin = Slytherin + float(distance[index][5])
        
    print(f'Gryffindor: {Gryffindor}')
    print(f'Ravenclaw: {Ravenclaw}')
    print(f'Hufflepuff: {Hufflepuff}')
    print(f'Slytherin: {Slytherin}')
    print('')
    play_random_phrases()

houses = []
houses.extend([Gryffindor, Ravenclaw, Hufflepuff, Slytherin])
sorted = max(houses)

print('===============================================')
print('')
play_audio('i_came_to_a_decision')
if (sorted == Gryffindor):
    print('You are sorted into GRYFFINDOR' + ' ' + '🦁')
    play_audio('gryffindor')
elif(sorted == Ravenclaw):
    print('You are sorted into RAVENCLAW' + ' ' + '🦅')
    play_audio('ravenclaw')
elif(sorted == Hufflepuff):
    print('You are sorted into HUFFLEPUFF' + ' ' + '🦡')
    play_audio('hufflepuff')
else:
    print('You are sorted into SLYTHERIN' + ' ' + '🐍')
    play_audio('slytherin')
print('')
print('===============================================')