#!/usr/bin/env python2

"""
yes i know py3 blah blah blah

very simple irc bot for ack by okabe

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

c = httplib.HTTPSConnection("acktic.github.io")
c.request("GET", "/js/xmlAssets.js")
response = c.getresponse()
print response.status, response.reason
data = response.read()

#some variables
server = "irc.blackcatz.org"
port = 6697
blackcatz = "#blackcatz"
malgroup = "#malgroup"
nick = "r"

#function definitions
def run_leafly( channel ):
    result = 'https://www.leafly.com/feed'
    title = []
    ext = []
    feed = feedparser.parse(result)
    for key in feed["entries"]:
        title.append(unidecode.unidecode(key["title"]))
        ext.append(unidecode.unidecode(key["link"]))

    sock.send( "PRIVMSG {} :{} {}\r\n".format( channel , title[0], ext[0] ) )

def run_rss( channel ):
    result = re.findall("(category:\`Technology\`.+uri:\`([A-Za-z]+:\/\/[A-Za-z0-9\-_]+\.[A-Za-z0-9\-_:%&;\?\#\/.=]+)\`)", data)
    ran = random.choice (result)
    title = []
    ext = []
    feed = feedparser.parse(ran[1])
    for key in feed["entries"]:
         title.append(unidecode.unidecode(key["title"]))
         ext.append(unidecode.unidecode(key["link"]))

    print ran
    sock.send( "PRIVMSG {} :{} {}\r\n".format( channel , title[0], ext[0] ) )

def run_media( channel ):
    result = re.findall("(category:\`Media\`.+uri:\`([A-Za-z]+:\/\/[A-Za-z0-9\-_]+\.[A-Za-z0-9\-_:%&;\?\#\/.=]+)\`)", data)
    ran = random.choice (result)
    title = []
    ext = []
    feed = feedparser.parse(ran[1])
    for key in feed["entries"]:
         title.append(unidecode.unidecode(key["title"]))
         ext.append(unidecode.unidecode(key["link"]))

    print ran
    sock.send( "PRIVMSG {} :{} {}\r\n".format( channel , title[0], ext[0] ) )

def run_sports( channel ):
    result = re.findall("(category:\`Sports\`.+uri:\`([A-Za-z]+:\/\/[A-Za-z0-9\-_]+\.[A-Za-z0-9\-_:%&;\?\#\/.=]+)\`)", data)
    ran = random.choice (result)
    title = []
    ext = []
    feed = feedparser.parse(ran[1])
    for key in feed["entries"]:
         title.append(unidecode.unidecode(key["title"]))
         ext.append(unidecode.unidecode(key["link"]))

    print ran
    sock.send( "PRIVMSG {} :{} {}\r\n".format( channel , title[0], ext[0] ) )

def run_world( channel ):
    result = re.findall("(category:\`World\`.+uri:\`([A-Za-z]+:\/\/[A-Za-z0-9\-_]+\.[A-Za-z0-9\-_:%&;\?\#\/.=]+)\`)", data)
    ran = random.choice (result)
    title = []
    ext = []
    feed = feedparser.parse(ran[1])
    for key in feed["entries"]:
         title.append(unidecode.unidecode(key["title"]))
         ext.append(unidecode.unidecode(key["link"]))

    print ext[0]
    sock.send( "PRIVMSG {} :{} {}\r\n".format( channel , title[0], ext[0] ) )

def run_news( channel ):
    result = re.findall("(category:\`News\`.+uri:\`([A-Za-z]+:\/\/[A-Za-z0-9\-_]+\.[A-Za-z0-9\-_:%&;\?\#\/.=]+)\`)", data)
    ran = random.choice (result)
    title = []
    ext = []
    feed = feedparser.parse(ran[1])
    for key in feed["entries"]:
         title.append(unidecode.unidecode(key["title"]))
         ext.append(unidecode.unidecode(key["link"]))

    print ext[0]
    sock.send( "PRIVMSG {} :{} {}\r\n".format( channel , title[0], ext[0] ) )

def run_youtube( channel ):
    result = re.findall("(category:`Youtube`.+uri:\`([A-Za-z]+:\/\/[A-Za-z0-9\-_]+\.[A-Za-z0-9\-_:%&;\?\#\/.=]+)\`)", data)
    ran = random.choice (result)
    title = []
    ext = []
    feed = feedparser.parse(ran[1])
    for key in feed["entries"]:
         title.append(unidecode.unidecode(key["title"]))
         ext.append(unidecode.unidecode(key["link"]))

    print ext[0]
    sock.send( "PRIVMSG {} :{} {}\r\n".format( channel , title[0], ext[0] ) )

#some state variables
authed = False
inchan = False

#make our socket - check `man socket`
sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )

#connect to blackcatz
sock.connect(( server, port ))

#once socket has connected, we need to force all communication over SSL, we can do this by reassigning the value of sock
sock = ssl.wrap_socket( sock )

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
                    sock.send( "JOIN {}\r\n".format( blackcatz ) )
                    print "\n[SENT] JOIN {}\n".format( blackcatz )
                    sock.send( "JOIN {}\r\n".format( malgroup ) )
                    print "\n[SENT] JOIN {}\n".format( malgroup )
                    inchan = True

            #dont forget to pong
            if line.startswith( "PING" ):
                sock.send( "PONG {}\r\n".format( line.split( ":" )[1] ) )
                print "\n[SENT] PONG {}\n".format( line.split( ":" )[1] )

            #handle messages sent to our channel

        if "PRIVMSG {}".format( blackcatz ) in line:
                msg = line.split( " :" )[1] #strip off protocol bits
                if msg.startswith ( "!help" ):
                    sock.send( "PRIVMSG {} :commands are !erb !cve !db !sports !media !world !tech !yt !news \r\n".format( blackcatz ) )

        if "PRIVMSG {}".format( blackcatz ) in line:
                msg = line.split( " :" )[1] #strip off protocol bits
                if msg.startswith ( "!erb" ):
            		run_leafly( blackcatz )

        if "PRIVMSG {}".format( blackcatz ) in line:
                msg = line.split( " :" )[1] #strip off protocol bits
                if msg.startswith ( "!world" ):
            		run_world( blackcatz )

        if "PRIVMSG {}".format( blackcatz ) in line:
                msg = line.split( " :" )[1] #strip off protocol bits
                if msg.startswith ( "!media" ):
            		run_media( blackcatz )

        if "PRIVMSG {}".format( blackcatz ) in line:
                msg = line.split( " :" )[1] #strip off protocol bits
                if msg.startswith ( "!sports" ):
            		run_sports( blackcatz )

        if "PRIVMSG {}".format( blackcatz ) in line:
                msg = line.split( " :" )[1] #strip off protocol bits
                if msg.startswith ( "!yt" ):
            		run_youtube( blackcatz )

        if "PRIVMSG {}".format( blackcatz ) in line:
                msg = line.split( " :" )[1] #strip off protocol bits
                if msg.startswith ( "!news" ):
            		run_news( blackcatz )

        if "PRIVMSG {}".format( blackcatz ) in line:
                msg = line.split( " :" )[1] #strip off protocol bits
                if msg.startswith ( "!tech" ):
            		run_rss( blackcatz )

        if "PRIVMSG {}".format( malgroup ) in line:
                msg = line.split( " :" )[1] #strip off protocol bits
                if msg.startswith ( "!help" ):
                    sock.send( "PRIVMSG {} :commands are !erb !cve !db !world !sports !media !tech !yt !news \r\n".format( malgroup ) )

        if "PRIVMSG {}".format( malgroup ) in line:
                msg = line.split( " :" )[1] #strip off protocol bits
                if msg.startswith ( "!erb" ):
            		run_leafly( malgroup )

        if "PRIVMSG {}".format( malgroup ) in line:
                msg = line.split( " :" )[1] #strip off protocol bits
                if msg.startswith ( "!news" ):
            		run_news( malgroup )

        if "PRIVMSG {}".format( malgroup ) in line:
                msg = line.split( " :" )[1] #strip off protocol bits
                if msg.startswith ( "!tech" ):
            		run_rss( malgroup )

        if "PRIVMSG {}".format( malgroup ) in line:
                msg = line.split( " :" )[1] #strip off protocol bits
                if msg.startswith ( "!yt" ):
            		run_youtube( malgroup )

        if "PRIVMSG {}".format( malgroup ) in line:
                msg = line.split( " :" )[1] #strip off protocol bits
                if msg.startswith ( "!sports" ):
            		run_sports( malgroup )

        if "PRIVMSG {}".format( malgroup ) in line:
                msg = line.split( " :" )[1] #strip off protocol bits
                if msg.startswith ( "!media" ):
            		run_media( malgroup )

        if "PRIVMSG {}".format( malgroup ) in line:
        	title = []
        	ext = []
                msg = line.split( " :" )[1] #strip off protocol bits
                if msg.startswith( "!db" ): #check for our command trigger
            	    feed = feedparser.parse("https://www.exploit-db.com/rss.xml")
            	    for key in feed["items"]:
                	title.append(unidecode.unidecode(key["title"]))
             		ext.append(unidecode.unidecode(key["link"]))
            	    sock.send( "PRIVMSG {} :{} {}\r\n".format( malgroup , title[0], ext[0] ) )

        if "PRIVMSG {}".format( malgroup ) in line:
        	title = []
        	ext = []
                msg = line.split( " :" )[1] #strip off protocol bits
                if msg.startswith( "!cve" ): #check for our command trigger
            	    feed = feedparser.parse("https://nvd.nist.gov/feeds/xml/cve/misc/nvd-rss.xml")
            	    for key in feed["items"]:
                	title.append(unidecode.unidecode(key["title"]))
             		ext.append(unidecode.unidecode(key["link"]))
            	    sock.send( "PRIVMSG {} :{} {}\r\n".format( malgroup , title[-1], ext[-1] ) )

        if "PRIVMSG {}".format( blackcatz ) in line:
        	title = []
        	ext = []
                msg = line.split( " :" )[1] #strip off protocol bits
                if msg.startswith( "!db" ): #check for our command trigger
            	    feed = feedparser.parse("https://www.exploit-db.com/rss.xml")
            	    for key in feed["items"]:
                        title.append(unidecode.unidecode(key["title"]))
             	        ext.append(unidecode.unidecode(key["link"]))
            	    sock.send( "PRIVMSG {} :{} {}\r\n".format( blackcatz , title[0], ext[0] ) )

        if "PRIVMSG {}".format( blackcatz ) in line:
        	title = []
        	ext = []
                msg = line.split( " :" )[1] #strip off protocol bits
                if msg.startswith( "!cve" ): #check for our command trigger
            	    feed = feedparser.parse("https://nvd.nist.gov/feeds/xml/cve/misc/nvd-rss.xml")
            	    for key in feed["items"]:
                	title.append(unidecode.unidecode(key["title"]))
             		ext.append(unidecode.unidecode(key["link"]))
            	    sock.send( "PRIVMSG {} :{} {}\r\n".format( blackcatz , title[-1], ext[-1] ) )
