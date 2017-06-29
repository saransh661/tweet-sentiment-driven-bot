
#!/usr/bin/env python3

#Start
#Importing Modules
from textblob import TextBlob as tb
import tweepy
import serial
import time

print("\nStart")

## Functions

#Usb uses serial communication which only needs listening port address
def port() :
   port0 = input("\nEnter Serial Port\n")
   check = input("\nConfirm Port ?\n(y/n)\n")
   if check != "y":
        port()
   return port0

#To convert NLTK Output into Sensible form
def conv(x):
    if x > 0:
        return ("Positive","Forward",'F')
    elif x < 0:
        return ("Negative", "Backward", 'B')
    else :
        return ("Neutral","Nowhere", 'N')
#Calling functions
sport = port()
comm = serial.Serial(sport,9600)
print("\n Port Connected\n")

## SENTIMENT MODULE 
#Twitter Authorization keys
cons_key = 'ABkhGSqsTjrkXJx0ODZlEjHvi'
cons_secret = 'YsPyhMOZfGLOpNjTAHpq8z0RyTLuYIftDQ7NwN0lBp8zID1THf'


access_token ='192923260-kvYRRIvP0JskbKDgF9rKBTritiCYnIsom746P7ZU'
access_token_secret ='uC89Dg3gEIJIKPGWBbkl7ZYvMSbsDgawYB0TeLKNaDOOX'

#Getting Twitter Access
auth = tweepy.OAuthHandler(cons_key, cons_secret)
auth.set_access_token(access_token, access_token_secret)

print("\nTwitter Authorization Success!\n")


api = tweepy.API(auth)

#Search and retrieve the relevant tweets
while True:
    term = input("\nEnter Tweet Search Term, To exit enter 'stopcode' \n")
    if term == "stopcode":
        break
    public_tweets = api.search(term)
    
    if len(public_tweets) > 0 :
        print("\nTweets found! Initiating Sentiment Analysis\n")
        sleep(0.5)
        break
    else :
        print("\nNo tweets found, Enter another term\n")

sent_dict = {}

# Analysing tweets
for tweet in public_tweets:
    analysis = tb(tweet.text)
    sent_dict.update({tweet.text:analysis.sentiment.polarity})
    
#Serial buffer reset

comm.flushInput()

#Passing the analysis output to usb serial port withing specific time intervals
for tweets in sent_dict:
    sentiment = conv(sent_dict[tweets])
    print("\nThe tweet we are going to analyse is : \n\n", tweets, 
            "\n\n Whose sentiment is :\n", sentiment[0],
            "\n Therefore preparing bot to move\n",sentiment[1] )
                ## Serial Communication
    comm.write(str.encode(sentiment[2]))
    time.sleep(5)


print("\nProcess complete. Exiting.\n") 



    

