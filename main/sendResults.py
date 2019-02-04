#Developed by Trey Walker for The Butterknife 
import smtplib
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
EMAIL = 'woodwardmatchmaker@gmail.com'
PASSWORD = ''
smtpObj = smtplib.SMTP('smtp.gmail.com', 587)

def connectSMPT():
    if smtpObj.ehlo()[0] == 250:
        print('Connection Successful!')
    if smtpObj.starttls()[0] == 220:
        print('TLS Encryption Active!')
    if smtpObj.login(EMAIL, PASSWORD)[0] == 235:
        print('Logged in!')
    print()

def disconnectSMPT():
    smtpObj.quit()
    print('Closed SMTP Connection')

def read_template(filename):
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)

def sendResult(p1, df):
    to, name = p1['Email Address'], p1['Name']
    text_template = read_template('main\\templates\messsage.txt')
    html_template = read_template('main\\templates\message.html')
    counter, matches = 0, {'text' : '', 'html': ''}
    for key, val in p1['Best'].items():
        counter += 1
        if counter == 1:
            holder = list(df.loc[df['Email Address'] == key]['Snapchat and/or Instagram'])[0]
        matches['text'] += (str(counter)+'. '+df.loc[df['Email Address'] == key]['Name']+': '+str(val)+'%!\n')
        matches['html'] += ('<li><a href=\"mailto:'+key+'\" target=\"_top\">'+list(df.loc[df['Email Address'] == key]['Name'])[0]+'</a>: '+str(val)+'%!</li>')
    text = text_template.substitute(PERSON_NAME=name, BEST_MATCHES=matches['text'])
    html = html_template.substitute(PERSON_NAME=name, BEST_MATCHES=matches['html'], CONTACT=holder)
    #Attatch and Send
    msg = MIMEMultipart('alternative')
    msg['From']=EMAIL
    msg['To']=to
    msg['Subject']="Your Match Results are here!"
    msg.attach(MIMEText(text, 'plain'))
    msg.attach(MIMEText(html, 'html'))
    print(str(msg))
    smtpObj.send_message(msg)

