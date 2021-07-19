#!/usr/bin/env python2
"""
yes i know py3 blah blah blah

very simple irc bot for ack by okabe
slighly modified by fuckoo

rss done by ack
"""
import socket
import ssl
import select
import httplib
import re
import random
import feedparser
import unidecode
import logging
import inspect

c = httplib.HTTPSConnection("acktic.github.io")
c.request("GET", "site/js/main/Assets.js")
response = c.getresponse()
print response.status, response.reason
data = response.read()

# Logging
logger = logging.getLogger( 'root' )
FORMAT = "[ %(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig( format=FORMAT )
logger.setLevel(logging.DEBUG)

#some variables
server = "irc.blackcatz.org"
port = 6697
channels = [ "#blackcatz", "#malgroup" ]
nick = "r"

#some state variables
authed = False
inchan = False

#make our socket - check `man socket`
sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )

#connect to blackcatz
sock.connect(( server, port ))

#once socket has connected, we need to force all communication over SSL, we can do this by reassigning the value of sock
sock = ssl.wrap_socket( sock )


#function definitions
def has_contents( title, ext ):
    """ Returns true if title and ext lists are not empty """
    if title and ext:
        return True
    else:
        prev_func = inspect.stack()[1][3]
        msg = "No content was fetched (title and ext are empty) in function %s()" % prev_func
        logger.debug( msg )
        return False

def run_rss( channel ):
    result = re.findall("(category:\`Technology\`.+uri:\`([A-Za-z]+:\/\/[A-Za-z0-9\-_]+\.[A-Za-z0-9\-_:%&;\?\#\/.=]+)\`)", data)
    if not result:
        logger.debug( 'result is empty - regular expression did not return anything' )
        return

    ran = random.choice( result )
    title = []
    ext = []
    feed = feedparser.parse( ran[1] )
    for key in feed["entries"]:
        title.append(unidecode.unidecode(key["title"]))
        ext.append(unidecode.unidecode(key["link"]))

    if has_contents( title, ext ):
        print ran
        sock.send( "PRIVMSG {} :{} {}\r\n".format( channel , title[0], ext[0] ) )

def run_media( channel ):
    result = re.findall("(category:\`Entertainment\`.+uri:\`([A-Za-z]+:\/\/[A-Za-z0-9\-_]+\.[A-Za-z0-9\-_:%&;\?\#\/.=]+)\`)", data)
    if not result:
        logger.debug( 'result is empty - regular expression did not return anything' )
        return

    ran = random.choice( result )
    title = []
    ext = []
    feed = feedparser.parse(ran[1])
    for key in feed["entries"]:
        title.append(unidecode.unidecode(key["title"]))
        ext.append(unidecode.unidecode(key["link"]))

    if has_contents( title, ext ):
        print ran
        sock.send( "PRIVMSG {} :{} {}\r\n".format( channel , title[0], ext[0] ) )

def run_sports( channel ):
    result = re.findall("(category:\`Sports\`.+uri:\`([A-Za-z]+:\/\/[A-Za-z0-9\-_]+\.[A-Za-z0-9\-_:%&;\?\#\/.=]+)\`)", data)
    if not result:
        logger.debug( 'result is empty - regular expression did not return anything' )
        return

    ran = random.choice( result )
    title = []
    ext = []
    feed = feedparser.parse(ran[1])
    for key in feed["entries"]:
        title.append(unidecode.unidecode(key["title"]))
        ext.append(unidecode.unidecode(key["link"]))

    if has_contents( title, ext ):
        print ran
        sock.send( "PRIVMSG {} :{} {}\r\n".format( channel , title[0], ext[0] ) )

def run_world( channel ):
    result = re.findall("(category:\`World\`.+uri:\`([A-Za-z]+:\/\/[A-Za-z0-9\-_]+\.[A-Za-z0-9\-_:%&;\?\#\/.=]+)\`)", data)
    if not result:
        logger.debug( 'result is empty - regular expression did not return anything' )
        return

    ran = random.choice( result )
    title = []
    ext = []
    feed = feedparser.parse(ran[1])
    for key in feed["entries"]:
        title.append(unidecode.unidecode(key["title"]))
        ext.append(unidecode.unidecode(key["link"]))

    if has_contents( title, ext ):
        print ext[0]
        sock.send( "PRIVMSG {} :{} {}\r\n".format( channel , title[0], ext[0] ) )

def run_news( channel ):
    result = re.findall("(category:\`News\`.+uri:\`([A-Za-z]+:\/\/[A-Za-z0-9\-_]+\.[A-Za-z0-9\-_:%&;\?\#\/.=]+)\`)", data)
    if not result:
        logger.debug( 'result is empty - regular expression did not return anything' )
        return

    ran = random.choice( result )
    title = []
    ext = []
    feed = feedparser.parse(ran[1])
    for key in feed["entries"]:
        title.append(unidecode.unidecode(key["title"]))
        ext.append(unidecode.unidecode(key["link"]))

    if has_contents( title, ext ):
        print ext[0]
        sock.send( "PRIVMSG {} :{} {}\r\n".format( channel , title[0], ext[0] ) )

def run_youtube( channel ):
    result = re.findall("(category:\`Youtube\`.+uri:\`([A-Za-z]+:\/\/[A-Za-z0-9\-_]+\.[A-Za-z0-9\-_:%&;\?\#\/.=]+)\`)", data)
    if not result:
        logger.debug( 'result is empty - regular expression did not return anything' )
        return

    ran = random.choice( result )
    title = []
    ext = []
    feed = feedparser.parse(ran[1])
    for key in feed["entries"]:
        title.append(unidecode.unidecode(key["title"]))
        ext.append(unidecode.unidecode(key["link"]))

    if has_contents( title, ext ):
        print ext[0]
        sock.send( "PRIVMSG {} :{} {}\r\n".format( channel , title[0], ext[0] ) )

def run_cve( channel ):
    title = []
    ext = []
    msg = line.split( " :" )[1] #strip off protocol bits
    feed = feedparser.parse("https://nvd.nist.gov/feeds/xml/cve/misc/nvd-rss.xml")
    for key in feed["items"]:
        title.append(unidecode.unidecode(key["title"]))
        ext.append(unidecode.unidecode(key["link"]))

    if has_contents( title, ext ):
        sock.send( "PRIVMSG {} :{} {}\r\n".format( channel, title[-1], ext[-1] ) )

def run_db( channel ):
    title = []
    ext = []
    feed = feedparser.parse("https://www.exploit-db.com/rss.xml")
    for key in feed["items"]:
        title.append(unidecode.unidecode(key["title"]))
        ext.append(unidecode.unidecode(key["link"]))

    if has_contents( title, ext ):
        sock.send( "PRIVMSG {} :{} {}\r\n".format( channel, title[0], ext[0] ) )

def run_help( channel ):
    sock.send( "PRIVMSG {} :commands are !cve !db !sports !media !world !tech !yt !news \r\n".format( channel ) )

def parse_line( line ):
    # hash table of <cmd>: <function>
    # @TODO: remember to update as new bot commands are added
    supported_commands = { '!cve': run_cve, '!db': run_db, '!world': run_world, '!sports': run_sports, '!media': run_media,
                           '!tech': run_rss, '!yt': run_youtube, '!news': run_news, '!help': run_help }

    #:<sender>!user@hostname PRIVMSG <channel> :<cmd>
    bufparts = line.split( ' ' )
    sender   = bufparts[0].split( '!' )[0][1:]
    irc_cmd  = bufparts[1]
    channel  = bufparts[2]
    cmd      = bufparts[3][1:].rstrip()

    if cmd in supported_commands:
        if channel == nick:
            supported_commands[cmd]( sender )
        else:
            supported_commands[cmd]( channel )

#now handle AUTH to the IRC server and loop forever
buff = b"" #fun lil buffer
while True:
    lines = []
    #check if data has been written to the socket file descriptor
    ready = select.select( [sock], [], [], 1 )
    if ready[0]:
        try:
            #if data is waiting, process it into a list of lines
            raw = sock.recv( 512 )
            buff = buff + raw
            lines = buff.split( "\n" )
            buff = lines.pop()
        except Exception as ERROR: #blindly pass on derpy errors that might happen
            pass

    #now check if we got any lines and process each one
    if len( lines ) > 0:
        for line in lines:
            print line #send to console

            #handle authentication
            if "NOTICE" in line and authed == False:
                sock.send( "USER {} {} {} {}\r\n".format( nick, nick, nick, nick ) )
                print "\n[SENT] USER {} {} {} {}\n".format( nick, nick, nick, nick )
                sock.send( "NICK {}\r\n".format( nick ) )
                print "\n[SENT] NICK {}\n".format( nick )
                authed = True

            #handle MOTD and join channel when server is ready by triggering on OP code
            #https://tools.ietf.org/html/rfc2812 - RPL_ENDOFMOTD
            if "376" in line and inchan == False:
                for channel in channels:
                    sock.send( "JOIN {}\r\n".format( channel ) )
                    print "\n[SENT] JOIN {}\n".format( channel )
                    inchan = True

            #dont forget to pong
            if line.startswith( "PING" ):
                sock.send( "PONG {}\r\n".format( line.split( ":" )[1] ) )
                print "\n[SENT] PONG {}\n".format( line.split( ":" )[1] )

            #handle messages sent to our channel

        if "PRIVMSG" in line:
            parse_line( line )
