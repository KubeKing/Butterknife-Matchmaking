#Developed by Trey Walker for The Butterknife 
#---------------------------------------------------Init-----------------------------------------
import dataCollection as data #Collects data via the google spread sheet attatched to the form
import sendResults as mail #Contains functions involving dissimination
import pandas as pd #Module used for data management
import jsonCollection
import operator

QT = {
'GI': 'What gender are you interested in? (Check all boxes that apply)', 
'AR': 'What age range are you interested in? (Check all boxes that apply)',
'STARTER': 'What would you rather eat?'} #Encodes long questions
questions = data.getSheet('B1:AG1')[0] #Creates an array of all the questions
answers = data.getSheet('B2:AG') #Creates an arry of everyone's answers
qlen = len(questions) #Finds # of questions
alen = len(answers) #Finds the # of people who responded
print("Creating Dataframe... ", end="", flush=True)
df = pd.DataFrame(answers,columns=questions) #Creates a Table
df.set_index(['Email Address']) #Sets the indentifier to email (Chosen because there can not be duplicate emails)
for i in range(alen): #Converts multiple choice questions into arrays
    df.loc[i][QT['GI']] = df.loc[i][QT['GI']].split(', ')
    df.loc[i][QT['AR']] = df.loc[i][QT['AR']].split(', ')
print('DONE!')
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
    if canMatch(p1, p2): #If prefered gender or age group do not match the similarity goes to 0%
        return(int(round((((similarity/qlen)*100)), 0)))
    else:
        return(0)

def bestMatches(p1): #Finds the top 5 matches
    sorted_by_value, add = sorted(p1.items(), key=lambda kv: kv[1]), {} #Sorts the similarity of each person by least to greatest
    sorted_by_value.reverse() #Reveres the order to greatest to least
    for n in sorted_by_value[:5]: #Removes anything after the 5th position
        add[n[0]] = n[1]
    return(add)

def createMatches(): #Finds all matches 
    print("Finding Similarities... ", end="", flush=True)
    df['All'], df['Best'] = [None]*(alen), [None]*(alen)
    for i in range(alen):
        add = {}
        for n in range(alen):
            if n != i:
                add[df.loc[n]['Email Address']] = similarity(df.loc[n], df.loc[i])
        df.loc[i]['All'] = add
        df.loc[i]['Best'] = bestMatches(add)
    print('DONE!')

def sendResults(): #Sends Results via email
    mail.connectSMPT() #Connects to SMPT Server
    if not jsonCollection.loadSent():
        jsonCollection.overwrite(list(df['Email Address'])) #Comment out by default
    while len(jsonCollection.loadSent()) > 0:
        counter, mailing_list = 0, jsonCollection.loadSent()
        mlen = len(mailing_list)
        for email in mailing_list:
            counter += 1
            mail.sendResult(df[df['Email Address'] == email], df) #Sets who the email is sent to and it's contents
            print('Sending mail... '+str(int(round(counter/mlen, 0)))+'%', end="\r") #Usefull print statements
        if mlen == len(jsonCollection.loadSent()): #Sees if the emails can not be sent
            print('ERROR YOU HAVE '+str(len(jsonCollection.loadSent()))+' that can not be sent')
            break
    print('Sending Mail... DONE!')
    mail.disconnectSMPT() #Disconnects from SMPT Server

if __name__ == '__main__': #Functions that run when the file is opened
    createMatches()
    sendResults()