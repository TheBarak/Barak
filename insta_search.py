import requests
from  urllib import urlopen
import urllib3.request
#import urllib.parse
#import urllib.error
from bs4 import BeautifulSoup
import ssl
import json
import os
import re

OPTIONS = ['{}_{}','{}__{}', '{}{}','{}-{}']
URL_CONTS = r'https://www.instagram.com/{}/'
NAME = raw_input("Enter user name to find info: ")
first_last = NAME.split()
username_url = ''

def find_user_names():
    user_url = {}
    all_users_url = []
    users = []
    for option in OPTIONS:
        users.append(option.format(first_last[0],first_last[1]))
        users.append(option.format(first_last[1],first_last[0]))
        
    for username in users:
        try:
            user_url[username] = URL_CONTS.format(username)
        except:
            pass
    return user_url
    
class Insta_Info_Scraper:

    def get_image(self, url, path, username):
        image = requests.get(url).content
        pic_name = 'ProfilePic.png'
        dest_path = '{}\\{}\\{}'.format(path,NAME,username)
        
        if not os.path.exists(dest_path):
            os.makedirs(dest_path)

        with open('{}\\{}'.format(dest_path,pic_name), 'wb') as my_image:
            my_image.write(image)
  
    def getinfo(self, url, username):
        try:
            html = urlopen(url, context=self.ctx).read()
            soup = BeautifulSoup(html, 'html.parser')
            data = soup.find_all('meta', attrs={'property': 'og:description'})
            text = data[0].get('content').split()
            user = '%s %s %s' % (text[-3], text[-2], text[-1])
            followers = text[0]
            following = text[2]
            posts = text[4]
            print ('User:', user)
            print ('Followers:', followers)
            print ('Following:', following)
            print ('Posts:', posts)
            print ('---------------------------\n')

            pic = soup.find_all('meta' , attrs={'property': 'og:image'})
            pic2 = pic[0].get('content').split()[0]
            path = r'\images'
            self.get_image(pic2,path,username)
        except:
            print ("{} not found!\n".format(username))
        
    def main(self):
        self.ctx = ssl.create_default_context()
        self.ctx.check_hostname = False
        self.ctx.verify_mode = ssl.CERT_NONE

        all_users = find_user_names()
        for user, url in all_users.items():
            self.getinfo(url, user)

if __name__ == '__main__':
    obj = Insta_Info_Scraper()
    obj.main()

