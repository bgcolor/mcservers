#!/bin/python
__author__ = 'bgcolor'

import os
import sys
import shutil

# configurations
srcgf = 'mcrepo/%s/minecraft_server.jar' # src game file format
dstgf = '%s/minecraft_server.%s_%s.jar' # dst game file format
# ip = '121.43.155.82'
ip = '127.0.0.1'

# parameter from command line
if len(sys.argv) > 1:
    version = sys.argv[1]
else:
    version = '1.7.2'

maxmemory = '-Xmx512m' # max memory jvm use
# minmemory = '-Xms512m' # min memory jvm use\
minmemory = '-Xincgc' # enable incremental garbage collection

# print 'Please input version:'
# version = raw_input()
#
# print 'Please input IP:'
# ip = raw_input()

def onfailure(mcdir):
    if os.system('cat start.log') == 0:
        shutil.rmtree(os.path.abspath('../' + mcdir))
    else:
        print 'Fatal error occurred please cd %s manually!' % (mcdir)
    print 'Server starting failed !'

ports = []
if os.path.isfile('ports'):
    with open('ports') as fp:
        res = fp.readlines()
        fp.close()
        if res :
            for s in res:
                ports.append(s)
else:
    fp = open('ports','w')
    fp.close()


ports.sort();

if len(ports) == 0 :
    port = 25565
else:
    port = int(ports.pop()) + 1

mcdir = '%s%s_%d' % ('mcserver', version, port)
try:
    os.mkdir(mcdir)
except:
    print 'can not create game directory %s!' % (mcdir)

try:
    shutil.copy(srcgf % (version), dstgf % (mcdir, version, port))
except:
    print 'can not cp game files into specified directory.'

properties = '''#Minecraft server properties
generator-settings=
op-permission-level=4
allow-nether=true
level-name=world
enable-query=false
allow-flight=false
announce-player-achievements=true
server-port=%d
level-type=DEFAULT
enable-rcon=false
force-gamemode=false
level-seed=
server-ip=%s
max-build-height=256
spawn-npcs=true
white-list=false
spawn-animals=true
hardcore=false
snooper-enabled=true
online-mode=false
resource-pack=
pvp=true
difficulty=1
enable-command-block=false
gamemode=0
player-idle-timeout=0
max-players=20
public=false
spawn-monsters=true
generate-structures=true
view-distance=10
spawn-protection=16
motd=A Minecraft Server
''' % (port, ip)

# startscript = '''java -Xmx%s -Xms%s -jar minecraft_server.%s_%s.jar nogui
# ''' % (maxmemory, minmemory, version, port)
startscript = 'nohup java %s %s -jar minecraft_server.%s_%d.jar nogui >start.log 2>&1' % (maxmemory, minmemory, version, port)

f=open('%s/server.properties' % (mcdir), 'w')
f.write(properties);
f.close()

f=open('%s/start.sh' % (mcdir), 'w')
f.write(startscript);
f.close()

# if os.system('%s/start.bat' % (mcdir)) != 1:

# else:
#     os.rmdir(mcdir)
try:
    os.chdir(mcdir)
    os.system(startscript)
    fp = open('ports', 'a')
    fp.write('%s%s' % (str(port), '\n'))
    fp.close()
    print 'Server starts successfully! tail -f %s/start.log for log' % (mcdir)

except:
    onfailure(mcdir)

