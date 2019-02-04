#Developed by Trey Walker for The Butterknife 
#---------------------------------------------------Init-----------------------------------------
import dataCollection as data
import sendResults as mail
import pandas as pd
import numpy as np
import operator

QT = {
'GI': 'What gender are you interested in? (Check all boxes that apply)', 
'AR': 'What age range are you interested in? (Check all boxes that apply)',
'STARTER': 'What would you rather eat?'}
questions = data.getSheet('B1:AC1')[0]
answers = data.getSheet('B2:AC')
qlen = len(questions)
alen = len(answers)
df = pd.DataFrame(answers,columns=questions)
df.set_index(['Email Address'])
for i in range(alen):
    df.loc[i][QT['GI']] = df.loc[i][QT['GI']].split(', ')
    df.loc[i][QT['AR']] = df.loc[i][QT['AR']].split(', ')

#------------------------------------------------------Functions----------------------------------
def canMatch(p1, p2): #Checks Genders and Grades
    if p1['Gender'] in p2[QT['GI']] and p2['Gender'] in p1[QT['GI']] and p1['Grade'] in p2[QT['AR']] and p2['Grade'] in p1[QT['AR']]:
        return(True)
    else:
        return(False)

def similarity(p1, p2): #Compares questions
    similarity = 0
    for i in range(questions.index(QT['STARTER']), qlen):
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
    df['All'], df['Best'] = [None]*(alen), [None]*(alen)
    for i in range(alen):
        add = {}
        for n in range(alen):
            if n != i:
                add[df.loc[n]['Email Address']] = similarity(df.loc[n], df.loc[i])
        df.loc[i]['All'] = add
        df.loc[i]['Best'] = bestMatches(add)

def sendResults():
    mail.connectSMPT()
    for i in range(1):
        mail.sendResult(df.loc[i], df)
    mail.disconnectSMPT()

if __name__ == '__main__':
    createMatches()
    sendResults()
    #print(df.shape)
    #print(df)