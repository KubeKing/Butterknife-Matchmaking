#Developed by Trey Walker for The Butterknife 
#---------------------------------------------------Init-----------------------------------------
import dataCollection as data
import sendResults as mail
import pandas as pd
import numpy as np
import operator

questions = data.getSheet('B1:AC1')[0]
answers = data.getSheet('B2:AC')
qlen = len(questions)
alen = len(answers)
df = pd.DataFrame(np.column_stack(answers),questions)
db = {}
for i in range(alen):
    df[i][5] = df[i][5].split(', ')
    df[i][6] = df[i][6].split(', ')

#------------------------------------------------------Functions----------------------------------
def canMatch(p1, p2): #Checks Genders and Grades
    if p1[3] in p2[5] and p2[3] in p1[5] and p1[2] in p2[6] and p2[2] in p1[6]:
        return(True)
    else:
        return(False)

def similarity(p1, p2): #Compares questions
    similarity = 0
    for i in range(7, qlen):
        if p1[i] == p2[i]:
            similarity += 1
    if canMatch(p1, p2):
        return(round((((similarity/qlen)*100)), 0))
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
                add['All'][df[n][1]] = similarity(df[n], df[i])
        add['Best'], db[df[i][1]] = bestMatches(add['All']), add

def sendResults():
    mail.connectSMPT()
    for i in range(2):
        src = df[i]
        mail.sendResult(src, db[src[1]]['Best'])
    mail.disconnectSMPT()

if __name__ == '__main__':
    createMatches()
    sendResults()
    #print(db)
    #print(df)