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

def get_lines_between_separator(starting_separator, TheConfigFile, ending_separator=''):
    #Opens config file and returns a list of every line betwix the separators
    starting_separator = str(starting_separator)
    if ending_separator == '':
        ending_separator = starting_separator
    else:
        ending_separator = str(ending_separator)
    spot = 0
    separatorIs = [5, 9]
    logger = open(TheConfigFile, 'r')
    desiredLines = logger.readlines()
    separators = [starting_separator, ending_separator]
    #print(desiredLines)
    for i in range(10, len(desiredLines)): #Finds starting and ending lines with relevant info
        if spot > 1:
            pass
        else:
            if desiredLines[i] == separators[spot]:
                separatorIs[spot] = i
                spot = spot + 1
                if spot == 3:
                    i = 2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2
    i = 0
    stuff_between_separators = []
    for i in range(separatorIs[0]+1, separatorIs[1]):#Checks through each line between first and second separator
        #print(i)
        line_no_space = desiredLines[i].split('\n')[0]
        line_no_space = str(line_no_space.rstrip())
        stuff_between_separators.append(line_no_space)
    return stuff_between_separators

the_file = 'MangaHere.txt'
def write2file(text, file=the_file, mode='a'):
    print(text)
    logger = open(file, mode)
    logger.write(text)
    logger.write('\n')
    logger.close()

def getStatus(string):
    particular_site_status = str(string)
    particular_site_status = particular_site_status.replace(': ', '').strip()
    desiredInfoSeparators = '#########################################################################' + '\n'
    list_of_statuses = get_lines_between_separator(desiredInfoSeparators, TheConfigurationFile)
    #print(list_of_statuses)
    GoNoGo_result = 'fail'
    for i in range(0, len(list_of_statuses)):
        status = list_of_statuses[i].replace(': Go', '')
        status = status.replace(': go', '')
        status = status.replace(': No', '')
        status = status.replace(': no', '')
        status = status.replace(': GO', '')
        status = status.replace(': NO', '')
        status = status.strip()
        #print(status)
        if status == particular_site_status:
            GoNoGo_result = list_of_statuses[i].replace(particular_site_status + ': ', '')
            i = len(list_of_statuses) + 1
    print(GoNoGo_result)
    return GoNoGo_result
    
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

def writeTOlog(x):
    logger = open('MangaHere.txt', 'a')
    now = datetime.now()
    dt_string = now.strftime("%m/%d/%Y %I:%M:%S %p")
    logger.write('\n')
    print(x)
    logger.write(x + '\n')
    logger.close()

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
    #p = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    skip = []
    
    #number of sites now may be more than the previous number of sites
    #Must adjust for that
    if counter <= 0:
        p = []
        for i in url:
            p.append(0)
    else:        
        p = parray
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
                
    if len(truncurl) != len(url):
        print(url)
        print('****')
        print(truncurl)
        write2file('NOT =')
        exit(0)
    
    msg = 'Go to: '
    sendEmail = 0
    print('url '+str(len(url))+'  truncurl '+str(len(truncurl)))
    for site in range(0, len(url), 1):
        # try to download the page
        #if computer is sleep wait six seconds then leave loop
        try:
            if url[site] != '0':
                response = requests.get(url[site])#, headers=headers)
            else:
                writeTOlog('MangaHereSearchChecker:\nurl[{}] = {}'.format(site, url[site]))
        except:
            better_sleep(6)
            #site = "Fucked"
            print('fucked')
        if site != "Fucked":
            # parse the downloaded page
            # Checks whole main instead of tab
            # There were two tabs (shared and serial) and only the first was checked
            data = 'None'
            try:
                data = BeautifulSoup(response.text, "lxml").body.find(class_='manga-list-4-list line')
                data = data.findAll(class_='manga-list-4-item-tip')[1].getText()
                #s.append(data)
            except:
                try:
                    data = BeautifulSoup(response.text, "lxml").body.find(class_='manga-list-4-list line')
                    data = data.findAll(class_='manga-list-4-item-tip')[1]
                except:
                    data = '{} seems to be down'.format(url[site])
            print('pre data {}'.format(data))
            data = data.replace('Latest Chapter:Ch.', '')
            print('post data {}'.format(data))
            #debugging
##            if (site == 1) and (counter % 3 == 0) and (counter > 0):
##                data = '11037'
            starts_with_zero = True
            while starts_with_zero:
                if data.startswith('0'):
                    data = data[1:]
                else:
                    starts_with_zero = False
            write2file('C {}: {} current chapter is {}'.format(counter, url[site], data))
            s.append(data)
            print(s)
            #print(data)
            #print('s['+str(site)+'] had no issues')
            if ((data == None) or (str(data) == 'None') or (response == None)):
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
            print('site = {}'.format(site))
            if s[site] == p[site]:
                print(site)
                print('s:{}'.format(s[site]))
                print('p:{}'.format(p[site]))
                p[site] = s[site]
            else:
                sendEmail = 1
                p[site] = s[site]
                try:
                    msg = (msg +'\n'+truncurl[site] + ' ch ' + s[site])
                    write2file(msg)
                except Exception as xxx:
                    writeTOlog(str(xxx))
                    truncurl.append('0')
                    writeTOlog('truncurl.append(0)')
                    msg = (msg +'\n'+truncurl[site] + ' ch ' + s[site])
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
                    status = getStatus('StatusMH: ')
                    if (getStatus('StatusMH: ') == 'Go') or (getStatus('StatusMH: ') == 'GO') or (getStatus('StatusMH: ') == 'go'):
                        print(count)
                        past_soup = mangaHere(count, past_soup)
                    else:
                        print(status)
                except Exception as errrrrrrrr:
                    error = str(errrrrrrrr)
                    print(errrrrrrrr)
                    msg = error + '\n' + 'There was a main() error in MangaHereSeachChecker. Maybe check mangahere'
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
        better_sleep(secrets.randbelow(int(69)))
##        if count == 4:
##            print(count)
##            exit(0)
        #Get log file size in bytes
        MangaHere_text_file_size = os.path.getsize('MangaHere.txt')
        if MangaHere_text_file_size > 64321:
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








