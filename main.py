import urllib.request as ul
from bs4 import BeautifulSoup
import urllib.parse
import re
import os

baseUrl = 'https://uva.onlinejudge.org/'

def downloadFile(fileUrl, direc):
    filename = ''.join(fileUrl.split('/')[-1])
    req = ul.Request(fileUrl)
    resp = ul.urlopen(req)
    with open(direc+'/'+filename, 'wb') as out_file:
        out_file.write(resp.read())

def scraper(url, direc):
    data = ul.urlopen(url).read()
    soup = BeautifulSoup(data, 'html.parser')
    all_links = soup.select('td > a')
    fileTag = soup.find('iframe')

    if fileTag!=None:
        fileUrl = soup.select('a[href^="external"]')
        fileUrl = baseUrl+fileUrl[0].get('href')
        print(direc)
        downloadFile(fileUrl,direc)
        return

    for i in all_links:
        if i.get('class') == None and 'udebug' not in i.get('href'):
            print(i.string)
            if not os.path.exists(direc+'/'+i.string):
                os.makedirs(direc+'/'+i.string)
            scraper(baseUrl+re.sub("&amp;","&",i.get('href')),direc+'/'+i.string)


if __name__ == "__main__":
    the_url = 'https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&category=604'
    scraper(the_url, '.')
