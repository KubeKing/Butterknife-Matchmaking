#Developed by Trey Walker for The Butterknife 
#---------------------------------------------------Init-----------------------------------------
import dataCollection as data
import pandas as pd
import numpy as np
import operator

questions = data.getSheet('B1:AB1')[0]
answers = data.getSheet('B2:AB')
qlen = len(questions)
alen = len(answers)
df = pd.DataFrame(np.column_stack(answers),questions)
db = {}
for i in range(alen):
    df[i][4] = df[i][4].split(', ')
    df[i][5] = df[i][5].split(', ')

#------------------------------------------------------Functions----------------------------------
def canMatch(p1, p2): #Checks Genders and Grades
    if p1[2] in p2[4] and p2[2] in p1[4] and p1[1] in p2[5] and p2[1] in p1[5]:
        return(True)
    else:
        return(False)

def similarity(p1, p2): #Compares questions
    similarity = 0
    for i in range(6, qlen):
        if p1[i] == p2[i]:
            similarity += 1
    if canMatch(p1, p2) == True:
        return(round((((similarity/qlen)*100)), 2))
    else:
        return(0.0)

def bestMatches(p1): #Finds the top 5 matches
    sorted_by_value, add = sorted(p1.items(), key=lambda kv: kv[1]), {}
    sorted_by_value.reverse()
    for n in sorted_by_value[:5]:
        add[n[0]] = n[1]
    return(add)

def createMatches(): #Finds all matches
    for i in range(alen):
        add = {'All': {}}
        for n in range(alen):
            if n != i:
                add['All'][df[n][0]] = similarity(df[n], df[i])
        add['Best'], db[df[i][0]] = bestMatches(add['All']), add


if __name__ == '__main__':
    createMatches()
    print(db)