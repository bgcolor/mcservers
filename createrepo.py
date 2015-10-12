#!/usr/bin/python
__author__ = 'Administrator'

import os
import sys
import urllib
import urllib2
import json

def _download_by_chunk(url, dir, name, CHUNK=16 * 1024):
    if os.path.isdir(dir):
        print 'The directory is already existed. Do you want to redownload it?'
        # t = raw_input()
        # if t != 'y' :
        #     return False
    else:
        os.makedirs(dir)

    print 'Start downloading %s%s' % (dir, name)
    
    response = urllib2.urlopen(url)
    total_size = response.info().getheader('Content-Length').strip()
    total_size = int(total_size)

    print 'total size: %d' % (total_size)
    chunk_count = 0;

    with open(dir + name, 'wb') as f:
        while True:
            chunk = response.read(CHUNK)
            if not chunk:
                break
            f.write(chunk)
            chunk_count = chunk_count + 1
            progress = '%s%s downloaded %3.0f%%.' % (dir, name, chunk_count * CHUNK * 100 / total_size)
            # sys.stdout.write(progress)
            # sys.stdout.write('\b'*len(progress))
            if chunk_count % 5 == 0 :
                print progress

    print 'Completely finished downloading %s.' % (name)

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
                # print url % (version['id'], version['id'])
                dstdir = 'mcrepo/%s'
                _download_by_chunk(url % (version['id'], version['id']), dstdir % (version['id']), dstname)
    else :
        dstdir = 'mcrepo/%s' % dstversion
        _download_by_chunk(url % (dstversion, dstversion), dstdir, dstname)

if __name__ == '__main__': 
    main()