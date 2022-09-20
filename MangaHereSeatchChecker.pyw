import time
import smtplib
import requests
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
from datetime import datetime
import os
import secrets
from email.message import EmailMessage


#cd F:\Users\dudeo\AppData\Local\Programs\Python\Python39
#pyinstaller --onefile MangaHereChecker.pyw
TheConfigurationFile = 'F:\\Users\\dudeo\\AppData\\Local\\Programs\\Python\\Python39\\dist\\Config.txt'

def better_sleep(time2wait):
    start = time.time()
    while((time.time()-start)<time2wait-.005):
        time.sleep(1)

def getStatus(string):
    configurationFile = open(TheConfigurationFile, 'r')
    config = str(configurationFile.read())
    configurationFile.close()
    status = config.split('#########################################################################')[1]
    status = status.split('#########################################################################')[0]
    #print(status)
    string = str(string)
    status = str(status.split(string)[1])
    #at this point if particular_site_status is MStatus int stus will not contain a :
    try:
        returnStatus = status.split('Status')[0].strip()
    except:
        pass
    if status.__contains__('\n'):
        returnStatus = status.split('\n')[0].strip()
    if status.__contains__(' '):
        returnStatus = status.split(' ')[0].strip()
    if status.__contains__('Status'):
        returnStatus = status.split('Status')[0].strip()
    #print(returnStatus)
    return returnStatus
    
#Get email and password
def login_info():
    configFile = open(TheConfigurationFile, 'r')
    config = str(configFile.read())
    email = config.split('Email: ')
    email = email[1].split('Password: ')
    password = str(email[1].strip())
    email = str(email[0].strip()).strip()
    try:
        server = config.split('Server: ')[1]
        server = str(server.split('Email: ')[0].strip())
    except:
        print('its the server')
    try:
        port = config.split('Port: ')[1]
        port = port.split('Server: ')[0].strip()
        port = int(str(port))
    except:
        print('port also fucked up')
    try:
        app = config.split('App Pass: ')[1]
        app = app.split('Port: ')[0].strip()
        app = str(app)
    except:
        print('port also fucked up')
    configFile.close()
    return email, password, server, port, app


#email function
def email(sites):
    myEmail, myPass, theServer, thePort, theAppPassword = login_info()
    configFile = open(TheConfigurationFile, 'r')
    raw_emails = configFile.readlines()
    configFile.close()
    notDone = 1
    x = 0
##    while notDone > 0:
##        bad = 0
##        for line in range(0, len(raw_emails)-x, 1):
##            if ((str(raw_emails[line]).__contains__('@')) and ((str(raw_emails[line]).__contains__('.')))):
##                if (str(raw_emails[line]).__contains__('Email')):
##                    try:
##                        raw_emails[line] = raw_emails[line+1]
##                        raw_emails[line+1] = 0
##                    except:
##                        raw_emails[line] = 0
##                else:                    
##                    raw_emails[line] = str(raw_emails[line]).strip()
##            else:
##                try:
##                    raw_emails[line] = raw_emails[line+1]
##                    raw_emails[line+1] = 0
##                except:
##                    raw_emails[line] = 0
##                bad = 1
##        x=x+1
##        if bad == 0:
##            notDone = 0
##        #print(raw_emails)
##    #initialize array of emails for others
##    the_emails = []
##    for i in range(0, len(raw_emails), 1):
##        if raw_emails[i] != 0:
##            the_emails.append(raw_emails[i])
##            print(the_emails[i])
    #email myself
    try:
        server = smtplib.SMTP_SSL(theServer, thePort)
        server.ehlo()
        server.login(myEmail, theAppPassword)
        msge = EmailMessage()
        msge.set_content(sites)
        server.send_message(msge, from_addr=myEmail, to_addrs=myEmail)
        server.quit()
    except:
        better_sleep(1)
        logger = open('Pokemon.txt', 'a')
        now = datetime.now()
        dt_string = now.strftime("%m/%d/%Y %I:%M:%S %p")
        logger.write('\n')
        logger.write(dt_string + '\n')
        logger.write(str('Failed to send email to me!'))
        logger.close()
##    #email others
##    for i in range(0, len(the_emails), 1):
##        try:
##            server = smtplib.SMTP_SSL(theServer, thePort)
##            server.ehlo()
##            server.login(myEmail, theAppPassword)
##            msge = EmailMessage()
##            msge.set_content(sites)
##            server.send_message(msge, from_addr=myEmail, to_addrs=str(the_emails[i]))
##            server.quit()
##        except:
##            better_sleep(1)
##            logger = open('Pokemon.txt', 'a')
##            now = datetime.now()
##            dt_string = now.strftime("%m/%d/%Y %I:%M:%S %p")
##            logger.write('\n')
##            logger.write(dt_string + '\n')
##            logger.write(str('Failed to send email to ' + str(the_emails[i]) + '!'))
##            logger.close()



#pokemon checker
def mangaHere(counter, parray):
    #get the sites from the configuration file
    print('openConfig')
    mangaConfig = open(TheConfigurationFile, 'r')
    print('raw')
    raw = mangaConfig.readlines()
    print('closer')
    mangaConfig.close()
    #remove the not links
    notDone = 1
    x = 0
    while notDone > 0:
        bad = 0
        for line in range(0, len(raw)-x, 1):
            if str(raw[line]).__contains__('https') and str(raw[line]).__contains__('mangahere') and str(raw[line]).__contains__('search'):
                raw[line] = str(raw[line]).strip()
            else:
                try:
                    raw[line] = raw[line+1]
                    raw[line+1] = 0
                except:
                    raw[line] = 0
                bad = 1
        x=x+1
        if bad == 0:
            notDone = 0
    #The not links were removed but there are zeros at the end
    url = []
    for i in range(0, len(raw), 1):
        if raw[i] != 0:
            url.append(raw[i])
            print(url[i])
    # The url list is set but now the truncurl list needs to be made
    #for some reason the code doesnt like having https:// so it must be removed

    truncurl = []
    for i in range(0, len(url), 1):
        x = str(url[i]).split('www.')
        truncurl.append(x[1])
        print(truncurl[i])
        
    s = []
    p = parray
    #p = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    skip = []
    
    #number of sites now may be more than the previous number of sites
    #Must adjust for that
    if len(p) < len(url):
        difference = len(url) - len(p)
        for i in range(len(p), len(p)+difference, 1):
            p.append('0')
            truncurl.append('0')
        print('less '+str(len(p)))
        print(len(url))

    #number of sites now may be less than the previous number of sites
    #Must adjust for that
    if len(p) > len(url):
        difference = len(p) - len(url)
        for i in range(len(url), len(url)+difference, 1):
            url.append('0')
            truncurl.append('0')
        print('more '+str(len(p)))
        print(len(url))
                
    
    
    msg = 'Go to: '
    sendEmail = 0
    print('url '+str(len(url))+'  truncurl '+str(len(truncurl)))
    for site in range(0, len(url), 1):
        # try to download the page
        #if computer is sleep wait six seconds then leave loop
        try:
            if url[site] != '0':
                response = requests.get(url[site])#, headers=headers)
        except:
            better_sleep(6)
            site = "Fucked"
            print('fucked')
        if site != "Fucked":
            # parse the downloaded page
            # Checks whole main instead of tab
            # There were two tabs (shared and serial) and only the first was checked
            data = 'None'
            try:
                data = BeautifulSoup(response.text, "lxml").body.find(class_='manga-list-4-list line')
                data = data.findAll(class_='manga-list-4-item-tip')[1].getText()
                s.append(data)
            except:
                data = BeautifulSoup(response.text, "lxml").body.find(class_='manga-list-4-list line')
                data = data.findAll(class_='manga-list-4-item-tip')[1]
                s.append(data)
            #print(data)
            #print('s['+str(site)+'] had no issues')
            if ((data == None) or (str(data) == 'None')):
                print(str(url[site])+' is None')
                logger = open('MangaHere.txt', 'a')
                now = datetime.now()
                dt_string = now.strftime("%m/%d/%Y %I:%M:%S %p")
                logger.write('\n')
                logger.write(dt_string + '\n')
                try:
                    logger.write(str(url[site])+' is None' + '\n')
                except:
                    pass
                logger.close()
            if s[site] == p[site]:
                p[site] = s[site]
            else:
                sendEmail = 1
                p[site] = s[site]
                try:
                    msg = (msg +'\n'+truncurl[site])
                except:
                    truncurl.append('0')
                    msg = (msg +'\n'+truncurl[site])
    print('finished for site in range(0, len(url), 1)')
    #sendEmail = 1
    if site != "Fucked":
        logger = open('MangaHere.txt', 'a')
        now = datetime.now()
        dt_string = now.strftime("%m/%d/%Y %I:%M:%S %p")
        logger.write('\n')
        logger.write(dt_string + '\n')
        logger.write(str('MangaHere got response'))
        logger.close()
    if counter > 0:
        if sendEmail == 1:
            email(str(msg))
            logger = open('MangaHere.txt', 'a')
            now = datetime.now()
            dt_string = now.strftime("%m/%d/%Y %I:%M:%S %p")
            logger.write('\n')
            logger.write(dt_string + '\n')
            try:
                logger.write(str(msg) + '\n')
            except:
                pass
            logger.write('New chapter!\n')
            logger.close()
        else:
            logger = open('MangaHere.txt', 'a')
            now = datetime.now()
            dt_string = now.strftime("%m/%d/%Y %I:%M:%S %p")
            logger.write('\n')
            logger.write(dt_string + '\n')
            logger.write('No new chapters\n')
            logger.close()
    else:
        logger = open('MangaHere.txt', 'a')
        now = datetime.now()
        dt_string = now.strftime("%m/%d/%Y %I:%M:%S %p")
        logger.write('\n')
        logger.write(dt_string + '\n')
        logger.write('Just started.  Not sending email. \n')
        logger.close()
        pastsoup = s
    msg = 'Go to: '
    sendEmail = 0
    return p


def main():
    #email('This is a test.  Current BDSP events are Shayman.  Connect to Mystery Gift internet.  Starting April 1st to April 30th connect to MG internet and get Darkrai.  I love you a ton and once I finish school I promis Ill have more game time for you <3')
    z = 0
    count = 0
    daycount = count
    past = 0
    if(os.path.exists('MangaHere.txt')):
        pass
    else:
        logger = open('MangaHere.txt', 'w')
        logger.write('This is the log of stuff:' + '\n')
        logger.close()
    while z < 30:
        # should do the initializing
        # wont send email.  Just doing set up
        if count == 0:
            past_soup = mangaHere(count,  [])
        #now the set up is done do the check for real
        if count > 0:
            now = datetime.now()
            today = now.strftime("%I") #check once each hour
            if today == past:
                past = today
            else:
                try:
                    if (getStatus('StatusMH: ') == 'Go') or (getStatus('StatusMH: ') == 'GO') or (getStatus('StatusMH: ') == 'go'):
                        past_soup = mangaHere(count, past_soup)
                except Exception as errrrrrrrr:
                    error = str(errrrrrrrr)
                    print(errrrrrrrr)
                    msg = error + '\n' + 'There was a main() error. Maybe check mangahere'
                    email(msg)
                    logger = open('MangaHere.txt', 'a')
                    now = datetime.now()
                    dt_string = now.strftime("%m/%d/%Y %I:%M:%S %p")
                    logger.write('\n')
                    logger.write(dt_string + '\n')
                    logger.write('There was a main() error. \n' + '\n')
                    logger.close()
                past = today
                daycount = daycount + 1
        better_sleep(secrets.randbelow(69))
        #Get log file size in bytes
        MangaHere_text_file_size = os.path.getsize('MangaHere.txt')
        if MangaHere_text_file_size > 54321:
            # clear out the log file if it gets too big (1MB)
            logger_lines = []
            logger = open('MangaHere.txt', 'r')
            logger_lines = logger.readlines()
            logger.close()
            logger = open('MangaHere.txt', 'w')
            for number, line in enumerate(logger_lines):
                if number > (len(logger_lines)/6) or number == 0:
                    logger.write(line)
            logger.close()
            daycount = count
        count = count + 1
        
if __name__ == '__main__':
    main()








