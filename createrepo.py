#!/usr/bin/python
__author__ = 'Administrator'

import os
import sys
import urllib
import urllib2
import json

def _download_progress(count, blockSize, totalSize):
      percent = int(count*blockSize*100/totalSize)
      sys.stdout.write("\rdownload...%d%%" % percent)
      sys.stdout.flush()

def _download(url, dir, name):
    donename = '/done'
    if os.path.isdir(dir):
        if os.path.isfile(dir + donename):
            print 'The directory is already existed. Do you want to redownload it?'
            # t = raw_input()
            # if t != 'y' :
            #     return False
            return False
    else:
        os.makedirs(dir)

    print 'Start downloading %s%s' % (dir, name)

    try:
        urllib.urlretrieve(url, dir + name, _download_progress)
        print '\nCompletely finished downloading %s%s.' % (dir, name)
        open(dir + donename, 'w')
    except:
        print 'Fail to download %s%s.' % (dir, name)
        return False

    return True

def main():
    if len(sys.argv) > 1 :
        if sys.argv[1] == 'all': 
            dstversion = 'all'
        else:
            dstversion = sys.argv[1]
    else: 
        print 'Please input the version fo repo you want to create(all of all of the versions):'
        dstversion = raw_input()

    url = 'http://s3.amazonaws.com/Minecraft.Download/versions/%s/minecraft_server.%s.jar'
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
                # if version['type'] != 'old_alpha':
                if version['type'] == 'release':
                    dstdir = 'mcrepo/%s'
                    _download(url % (version['id'], version['id']), dstdir % (version['id']), dstname)
    else :
        dstdir = 'mcrepo/%s' % dstversion
        _download(url % (dstversion, dstversion), dstdir, dstname)

if __name__ == '__main__': 
    main()