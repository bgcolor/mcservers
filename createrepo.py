#!/usr/bin/python
__author__ = 'Administrator'

import os
import urllib
import urllib2
import json

def download(dstversion):
    url = 'http://s3.amazonaws.com/Minecraft.Download/versions/%s/minecraft_server.%s.jar'
    dstdir = 'mcrepo/%s' % dstversion
    dstname = '/minecraft_server.jar'

    if dstversion == 'all' :
        versionsurl = 'http://s3.amazonaws.com/Minecraft.Download/versions/versions.json'

        if os.path.isfile('versions.json') == False :
            # download versions info from amazon s3
            try:
                urllib.urlretrieve(versionsurl, 'versions.json')
            except:
                print 'Failed to download versions info'
                return False

        with open('versions.json') as f :
            versions = json.loads(f.read())
            versions = versions['versions']
            for version in versions :
                response = urllib2.urlopen(url % (version['id'], version['id']))
                total_size = response.info().getheader('Content-Length').strip()
                total_size = int(total_size)
                CHUNK = 16 * 1024

                print 'Start downloading total: %d' % (total_size)
                cchunk = 0;
                os.mkdir(dstdir)
                with open(dstdir + dstname, 'wb') as f:
                   while True:
                      chunk = response.read(CHUNK)
                      if not chunk: break
                      f.write(chunk)
                      print 'Finished %f%.' % (++cchunk * CHUNK / total_size)

                print 'Completely finished.'
    else :
        if os.path.isdir(dstdir) :
            print 'This version is already existed. Do you want to redownload it?'
            t = raw_input()
            if t != 'y' :
                return False
        else :
            os.makedirs(dstdir)

        response = urllib2.urlopen(url % (dstversion, dstversion))
        total_size = response.info().getheader('Content-Length').strip()
        total_size = int(total_size)
        CHUNK = 16 * 1024

        print 'Start downloading total: %d' % (total_size)
        cchunk = 0;

        with open(dstdir + dstname, 'wb') as f:
            while True :
                chunk = response.read(CHUNK)
                if not chunk :
                    break
                f.write(chunk)
                cchunk = cchunk + 1
                print 'Finished %3.0f%%.' % (cchunk * CHUNK * 100 / total_size)


        print 'Completely finished.'

def __main__():
    print 'Please input the version fo repo you want to create(all of all of the versions):'
    dstversion = raw_input()
    download(dstversion)

__main__()