import speech_recognition as sr
from Levenshtein import distance as lev
import os
import random

from data_preprocessing import questions

G = 0 #shit variable names
R = 0
H = 0
S = 0

r = sr.Recognizer() #as well shit variable name
with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source)

def play_audio(filename):
    os.system("afplay " + f'./Voicelines/{filename}.wav') #security issue but we keep for now

random_phrases = ['hmm', 'thank_you_for_looking_so_good', 'very_interesting']

def play_random_phrases():
    can_play = random.random()
    if can_play < 33:
        index = random.randrange(len(random_phrases))
        play_audio(random_phrases[index])

def get_index_of_most_likely_answer(distance):
        min_distance = distance[0][6]
        index = 0
        for i in range(len(distance)):
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

        play_audio(question["data"][2])
        counter2 = 1
        for answer in question["answers"]:
            if len(answer) == 7:
                play_audio(answer[6])
            counter2 += 1
        
        # speech recognition
        with sr.Microphone() as source:
            audio = r.listen(source,10, phrase_time_limit=10)
        try:
            user_input = r.recognize_google(audio)
        except sr.UnknownValueError:
            print("I'm a bit old and my hearing is not the best anymore, please repeat")
            continue
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            continue

        if user_input == 'repeat' or user_input == 'please repeat': #this is bad and you know it
            repeat = True

    distance = []
    c = 0 #variable name
    for answer in question["answers"]:
        lev_distance = lev(answer[1], user_input)
        answer.append(lev_distance)
        distance.append(answer)
        c += 1
        
    index = get_index_of_most_likely_answer(distance)

    G = G + float(distance[index][2])
    R = R + float(distance[index][3])
    H = H + float(distance[index][4])
    S = S + float(distance[index][5])
        
    play_random_phrases()

houses = []
houses.extend([G, R, H, S])
sorted = max(houses)

play_audio('i_came_to_a_decision')
if (sorted == G):
    play_audio('gryffindor')
elif(sorted == R):
    play_audio('ravenclaw')
elif(sorted == H):
    play_audio('hufflepuff')
else:
    play_audio('slytherin')