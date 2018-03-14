#!/usr/bin/env python3


#Begin


#Importing the libraries

from textblob import TextBlob as tb
import tweepy
import bluetooth
import time

print("\nStart")

## Function Definitio

## Searches for nearby devices and asks the user to select one, On selection, returns it's MAC ADDRESS
def inquiry():
    
    print("performing inquiry...")

    nearby_devices = bluetooth.discover_devices(
        duration=8, lookup_names=True, flush_cache=True, lookup_class=False)

    print("found %d devices" % len(nearby_devices))
    i=1
    list0=[]
    for addr, name in nearby_devices:
        print("[%d]  %s - %s" % (i, addr, name))
        list0.append((addr,name))
        i += 1
    i = input("Enter Device no\n")
    addr , name = list0[int(i)-1]
    print("device ",name , "selected\n")
    return addr
    


#To find listening port of the bluetooth module

def find_port(mac):
    for port in range(1,31):
        s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        try:
            
            print("trying port no", port)
            s.bind((mac, port))
            s.close()
            return port
        except:
            s.close()
            break



# To convert NLTK Output into Sensible form

def conv(x):
    if x > 0:
        return ("Positive","Forward",'F')
    elif x < 0:
        return ("Negative", "Backward", 'B')
    else :
        return ("Neutral","Nowhere", 'N')



#Calling the functions

mac = inquiry() # Getting a Mac
port =  find_port(mac) #Getting a Listening PORT
print("port found", port)
s = bluetooth.BluetoothSocket(bluetooth.RFCOMM) #Creating a bluetooth socket for connection
s.connect(( mac ,port)) # Connecting the socket to the other device using MAC and PORT
print("\n Port Connected\n")


## SENTIMENT MODULE  

# Twitter Authenication Keys
cons_key = '\# Put Your own cons key'
cons_secret = '\# Put Your own cons_secret'


access_token ='\# your access token'
access_token_secret ='\# you know what to put'

#Getting Twitter Access
auth = tweepy.OAuthHandler(cons_key, cons_secret)
auth.set_access_token(access_token, access_token_secret)

print("\nTwitter Authorization Success!\n")


api = tweepy.API(auth)

#Asking to search for a tweet term
while True:

    term = input("\nEnter Tweet Search Term, To exit enter 'stopcode' \n")
    if term == "stopcode":
        break
    public_tweets = api.search(term)
    
    if len(public_tweets) > 0 :
        print("\nTweets found! Initiating Sentiment Analysis\n")
        time.sleep(0.5)
        break
    else :
        print("\nNo tweets found, Enter another term\n")

sent_dict = {}

#Analysing tweets one by one and sending it over bluetooth within a specific time interval
for tweet in public_tweets:
    analysis = tb(tweet.text)
    sent_dict.update({tweet.text:analysis.sentiment.polarity})
    


for tweets in sent_dict:
    sentiment = conv(sent_dict[tweets])
    print("\nThe tweet we are going to analyse is : \n\n", tweets, 
            "\n\n Whose sentiment is :\n", sentiment[0],
            "\n Therefore preparing bot to move\n",sentiment[1] )
               
    s.send(str.encode(sentiment[2]))
    time.sleep(5)

s.close()
print("\nProcess complete. Exiting.\n") 
