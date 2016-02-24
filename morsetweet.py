#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import urllib
from PIL import Image
from rgbmatrix import Adafruit_RGBmatrix
 
import tweepy
# You'll need to set these yourself from:
#
# https://apps.twitter.com/
#
# and see the documentation here:
#
# https://pythonhosted.org/tweepy/auth_tutorial.html
#
auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
auth.set_access_token(auth.request_token.key,
auth.request_token.secret)
api = tweepy.API(auth)
public_tweets = api.home_timeline()
 
 
CODE = {' ': ' ', 
        "'": '.----.', 
        '(': '-.--.-', 
        ')': '-.--.-', 
        ',': '--..--', 
        '-': '-....-', 
        '.': '.-.-.-', 
        '/': '-..-.', 
        '0': '-----', 
        '1': '.----', 
        '2': '..---', 
        '3': '...--', 
        '4': '....-', 
        '5': '.....', 
        '6': '-....', 
        '7': '--...', 
        '8': '---..', 
        '9': '----.', 
        ':': '---...', 
        ';': '-.-.-.', 
        '?': '..--..', 
        'A': '.-', 
        'B': '-...', 
        'C': '-.-.', 
        'D': '-..', 
        'E': '.', 
        'F': '..-.', 
        'G': '--.', 
        'H': '....', 
        'I': '..',
        'J': '.---', 
        'K': '-.-', 
        'L': '.-..', 
        'M': '--', 
        'N': '-.', 
        'O': '---', 
        'P': '.--.', 
        'Q': '--.-', 
        'R': '.-.', 
        'S': '...', 
        'T': '-', 
        'U': '..-', 
        'V': '...-', 
        'W': '.--', 
        'X': '-..-', 
        'Y': '-.--', 
        'Z': '--..', 
        '_': '..--.-',
        '#': '.',
        '%': '.',
        '!': '..'}
 
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
p = GPIO.PWM(18, 161) 
 
def dot():
        p.start(1)
        time.sleep(0.2)
        p.stop()
        time.sleep(0.2)
        #GPIO.cleanup()
 
def dash():
        p.start(1)
        time.sleep(0.5)
        p.stop()
        time.sleep(0.2)
        #GPIO.cleanup()
 
 
 
response = api.user_timeline(count=1)
matrix = Adafruit_RGBmatrix(32, 1)
status_old = "nil"
# print status_old
for status in response:
        time.sleep(0.5) 
        print "initial status %s" % status.text
while True:
        response = api.user_timeline(count=1)
        if status.text != status_old:
                for status in response:
                        for word in status.text.split():
                                for letter in word:
                                        if letter == "@":
                                                print word
                                                user = word
                tuser = api.get_user(user)
                profileimage = tuser.profile_image_url
                oimage=urllib.URLopener()
                oimage.retrieve(profileimage, "image.png")
                img = Image.open('image.png')
                resize_image = img.resize((32,32))
                matrix.Clear()
                resize_image.load()
                matrix.SetImage(resize_image.im.id)
                for letter in status.text:
                        if letter.upper() in CODE:
                                print CODE[letter.upper()]
                        if letter.upper() in CODE:
                                for symbol in CODE[letter.upper()]:
                                        if symbol == '-':
                                                dash()
                                        elif symbol == '.':
                                                dot()
                                        else:
                                                time.sleep(0.5)
                        time.sleep(0.5)
                status_old = status.text
                matrix.Clear()
                # print "morse old %s" % status_old
                # print "morse stat.t %s" % status.text
        else:
                response = api.user_timeline(count=1)
                for status in response:
                        print "new status %s" % status.text     
                # print "else %s" % status.text
                # print "else old %s" % status_old
                matrix.Clear()
                time.sleep(3600)