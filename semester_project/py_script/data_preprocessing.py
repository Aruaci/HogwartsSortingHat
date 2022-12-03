import csv
import re

file_q = open('./csv_files/questions.csv')
file_a = open('./csv_files/answers.csv')

csvreader_q = csv.reader(file_q, delimiter=';')
csvreader_a = csv.reader(file_a, delimiter=';')

questions = []
for row in csvreader_q:
    question = {}
    question["data"] = row
    question["answers"] = []
    questions.append(question)

answers = []
for row in csvreader_a:
        answers.append(row)

file_a.close()
file_q.close()

c = 1
for answer in answers:
    for i in range(2,len(answer)):
        match = re.search('\d', answer[i])
        if (match):
            corrected = answer[i].replace(',', '.')
            c += 1
            answer[i] = answer[i].replace(answer[i], corrected)
            
counter = 1
for question in questions[1:]:
    while answers[counter][0] == question["data"][0] and counter < 124:
        question["answers"].append(answers[counter])
        counter += 1