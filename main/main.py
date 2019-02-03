#Developed by Trey Walker for The Butterknife 
import dataCollection as data
import pandas as pd
import numpy as np

questions = data.getSheet('B1:AB1')[0]
answers = data.getSheet('B2:AB')
qlen = len(questions)
df = pd.DataFrame(np.column_stack(answers),questions)
db = {}
for i in range(len(answers)):
    df[i][4] = df[i][4].split(', ')
    df[i][5] = df[i][5].split(', ')

def canMatch(p1, p2): #Checks Genders and Grades
    if p1[2] in p2[4] and p2[2] in p2[4] and p1[1] in p2[5] and p2[1] in p2[5]:
        print('Can match!')
    else:
        print('Can not match!')

def similarity(p1, p2):
    similarity = 0
    for i in range(6, qlen):
        if p1[i] == p2[i]:
            similarity += 1
    return(str(similarity/qlen))

if __name__ == '__main__':
    print(similarity(df[0], df[2]))