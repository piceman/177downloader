#!/usr/local/bin/python3.4
# -*- coding: utf-8 -*-
__author__ = 'piceman'

import requests
from bs4 import BeautifulSoup
from io import BytesIO
import os
import re


def dlog(s):
    """Debug log, easy to toggle in debug or product environment

    Arguments:
        s {str} -- [string for print]
    """
    # return
    print(s)


def getImgLink(page):
    """Extrace image source from page

    Arguments:
        page {url} -- per page of comic

    Returns:
        array -- array of images
    """
    img_list = []
    p = requests.get(page)
    img_soup = BeautifulSoup(p.text,'lxml')
    img_link = img_soup.findAll('img')
    for img in img_link:
        # print(img_link)
        if 'data-lazy-src' in img.attrs:
            print(img['data-lazy-src'])
            img_list.append(img['data-lazy-src'])
    return  img_list


def downloadComic(comic_link):
    """Main method to download comic

    Arguments:
        comic_link {url} -- the comic main url
    """
    p = requests.get(comic_link)
    pagesoup = BeautifulSoup(p.text,'lxml')
    title=pagesoup.title.text
    dlog(title)
    sub_pages = pagesoup.find(attrs={'class':'page-links'}).find_all('a')
    # print(sub_pages)
    max_page = 0
    for x in sub_pages:
        if len(x.text.strip()) == 0:
            continue
        k = int(x.text.strip())
        if max_page < int(x.text.strip()):
            max_page = int(x.text)

    if max_page==0:
        print('fail to parse pages')
        exit()

    imglist = []
    print('get {} pages'.format(max_page))

    i=1
    for x in range(1,max_page+1):
        page_link = comic_link + '/{}/'.format(x)
        # print(page_link)
        tmp = getImgLink(page_link)
        for y in tmp:
            imglist.append(y)
    os.mkdir(title)
    os.chdir(title)

    for z in range(len(imglist)):      # 用range是因为要重命名图片为后面打包做准备
        # print('ready to download')
        img = requests.get(imglist[z-1])
        img_name = "{}.jpg".format(str(i).zfill(4))
        dlog('{} downloaded'.format(img_name))
        i = i + 1
        if img.status_code == 200:
            with open(img_name, 'wb') as f:
                f.write(img.content)
        else:
            dlog(img.status_code)
    os.chdir('..')


def main():
    urls= []
    urls.append('http://www.177pic.info/html/2019/09/3114081.html')
    urls.append('http://www.177pic.info/html/2019/09/3114108.html')
    urls.append('http://www.177pic.info/html/2019/09/3114110.html')
    urls.append('http://www.177pic.info/html/2019/09/3114107.html')
    for u in urls:
        downloadComic(u)

if __name__ == '__main__':
    main()
