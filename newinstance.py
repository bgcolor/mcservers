#!/usr/bin/python
__author__ = 'bgcolor'

import os
import shutil

# configurations
srcgf = 'mcrepo/%s/minecraft_server.jar' # src game file format
dstgf = '%s/minecraft_server.jar' # dst game file format
maxmemory = '512m' # max memory jvm use
minmemory = '512m' # min memory jvm use

print 'Please input version:'
version = raw_input()

print 'Please input IP:'
ip = raw_input()


fp = open('ports', 'w+')
ports = []

res = fp.readlines()

if res :
    for s in res:
        ports.append(s)

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
    shutil.copy(srcgf % (version), dstgf % (mcdir))
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

startscript = '''java -Xmx%s -Xms%s -jar minecraft_server.jar nogui
''' % (maxmemory, minmemory)

f=open('%s/server.properties' % (mcdir), 'w')
f.write(properties);
f.close()

f=open('%s/start.sh' % (mcdir), 'w')
f.write(startscript);
f.close()

# if os.system('%s/start.bat' % (mcdir)) != 1:
#     fp = open('ports', 'a')
#     fp.write('%s%s' % (str(port), '\n'))
#     fp.close()
# else:
#     os.rmdir(mcdir)
os.chdir(mcdir)
os.system(startscript)
