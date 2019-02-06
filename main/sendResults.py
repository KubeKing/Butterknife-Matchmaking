#Developed by Trey Walker for The Butterknife 
import smtplib #For Mailing services
import jsonCollection
from string import Template #Used for templating from an external file
from email.mime.multipart import MIMEMultipart #Email Formatting
from email.mime.text import MIMEText #Email Formatting
EMAIL = 'woodwardmatchmaker@gmail.com'
PASSWORD = ''
POSMOD = {1: 'color:#EBC944;font-size:250%;font-weight:700;margin-left:0px;margin-right:40px;', 2: 'color:#9E9E9E;font-size:225%;font-weight:600;margin-left:0px;margin-right:40px;', 
3: 'color:#6D4C41;font-size:200%;font-weight:575;margin-left:0px;margin-right:40px;', 
4: 'opacity:0.9;font-size:155%;font-weight:475;margin-left:0px;margin-right:40px;', 5: 'opacity:0.9;font-size:155%;font-weight:450;margin-left:0px;margin-right:40px;'}
global repeatEx
repeatEx = 0
smtpObj = smtplib.SMTP('smtp.gmail.com', 587)

def connectSMPT():
    if smtpObj.ehlo()[0] == 250:
        print('Connection Successful!')
    if smtpObj.starttls()[0] == 220:
        print('TLS Encryption Active!')
    if smtpObj.login(EMAIL, PASSWORD)[0] == 235:
        print('Logged in!')

def disconnectSMPT():
    smtpObj.quit()
    print('Closed SMTP Connection')

def simpleSocial(key, df):
    social, output = [list(df.loc[df['Email Address'] == key]['Snapchat Username (Optional)'])[0], list(df.loc[df['Email Address'] == key]['Instagram Username (Optional)'])[0]], ''
    if social[0] != '':
        output += ('Snapchat Username<b>:</b> '+social[0])
        if social[1] != '':
            output += ('<br>Instagram Username<b>:</b> '+social[1])
            return(output)
    elif social[1] != '':
        output += ('Instagram Username<b>:</b> '+social[1])
    return(output)

def read_template(filename):
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)

def sendResult(p1, df):
    try:
        to, name = list(p1['Email Address'])[0], list(p1['Name'])[0]
        text_template = read_template('main\\templates\messsage.txt')
        html_template = read_template('main\\templates\message.html')
        counter, matches = 0, {'text' : '', 'html': ''}
        for key, val in list(p1['Best'])[0].items():
            counter += 1
            social = simpleSocial(key, df)
            matches['text'] += (str(counter)+'. '+list(df.loc[df['Email Address'] == key]['Name'])[0]+': '+str(val)+'%!\n')
            matches['html'] += ('<li style=\"'+POSMOD[counter]+'\"><a href=\"mailto:'+key+'\" target=\"_top\" style=\"color: inherit;\">'+list(df.loc[df['Email Address'] == key]['Name'])[0]+'</a>: '+str(val)+'%!</li>')
            if social != '':
                matches['html'] += ('<dt style=\"opacity: 0.8;font-size: 90%;font-weight:425;margin-left:0px;margin-right:40px;\">'+social+'</dt>')
        text = text_template.substitute(PERSON_NAME=name, BEST_MATCHES=matches['text'])
        html = html_template.substitute(PERSON_NAME=name, BEST_MATCHES=matches['html'])
        #Attatch and Send
        msg = MIMEMultipart('alternative')
        msg['From']=EMAIL
        msg['To']=to
        msg['Subject']="Your Match Results are here!"
        msg.attach(MIMEText(text, 'plain'))
        msg.attach(MIMEText(html, 'html'))
        smtpObj.send_message(msg)
        jsonCollection.sent(to)
    except Exception as e:
        pass

