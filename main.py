import csv
import re
import math

ARRAY_COUNT = 40
EXCLUDE_QUESION_INDEXES = [5]

col_questions = []
question_answers = {}
question_rows = []

# Load the answers
with open('responses.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for i, row in enumerate(spamreader):
        # First row read out the questions
        if i == 0:
            for question in row[1:]:
                question_answers[question] = []
                col_questions.append(question)
            continue
        else:
            question_rows.append(row[1:])
        for i, val in enumerate(row[1:]):
            question_answers[col_questions[i]].append(val)

# Load the possible questions and their respective weights
answer_weights = {}
with open('weights.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for i, row in enumerate(spamreader):
        if i != 0:
            if row[0] not in answer_weights:
                answer_weights[row[0]] = {}
            answer_weights[row[0]][row[1]] = row[2]

respondent_scores = []

EXCLUDE_INDEXES = [5, 8, 12, 14, 16, 18, 20, 24]

with open('result.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["indekss"] + col_questions + ["rezultāts"])
    for idx, row in enumerate(question_rows):
        score = 0
        score_row = []
        for i, answer_str in enumerate(row):
            answers = answer_str.split(";")
            question = col_questions[i]
            if i in EXCLUDE_INDEXES:
                score_row.append(0)
                continue
            answer_score = 0
            for k, answer in enumerate(answers):
                if answer == "":
                    continue
                if re.match(r'Cits: (\d)', answer):
                    answer_score = int(re.sub(r'Cits: (\d)', r'\g<1>', answer))
                else:
                    answer_score += int(answer_weights[question][answer])
            score += answer_score
            score_row.append(answer_score)
        writer.writerow([idx + 1] + score_row + [sum(score_row)])

# SELECTED_QUESTION = 32
# for answer in question_answers[col_questions[SELECTED_QUESTION]]:
#     answers = answer.split(";")
#     question = col_questions[SELECTED_QUESTION]
#     answer_weight = answer_weights.get(question)
#     if answer_weight:
#         select_answers = answer_weight.keys()
#         for a in answers:
#             if re.match(r'Cits: (\d)', a):
#                 print("Matched other: " + a)
#             elif a not in select_answers:
#                 print(a)
