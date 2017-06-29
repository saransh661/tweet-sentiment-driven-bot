
from textblob import TextBlob as tb
import tweepy
import bluetooth
import time

print("\nStart")

## Functions
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
    

##To find mac_address of the bluetooth device
"""
def find_mac():
    target_name = input('Input device name\n')
    target_addr = None

    nearby_devices = bluetooth.discover_devices()
    for btaddr in nearby_devices:
        if target_name == bluetooth.lookup_name(btaddr):
            target_addr = btaddr
            break

    if target_addr is not None :
         print("Matching device found", target_name)
    else:
         print("No required device found")
    return target_addr
"""


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
"""
def try_port(mac):

    while True:
        p=bluetooth.PORT_ANY
        s=bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        s.bind((mac,p))
        s.close
        if p != 0 :
            return p 
            break

"""
def conv(x):
    if x > 0:
        return ("Positive","Forward",'F')
    elif x < 0:
        return ("Negative", "Backward", 'B')
    else :
        return ("Neutral","Nowhere", 'N')

mac = inquiry() #find_mac()
port =  find_port(mac) #try_port(mac)
print("port found", port)
s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
s.connect(( mac ,port))
print("\n Port Connected\n")


## SENTIMENT MODULE  
cons_key = 'ABkhGSqsTjrkXJx0ODZlEjHvi'
cons_secret = 'YsPyhMOZfGLOpNjTAHpq8z0RyTLuYIftDQ7NwN0lBp8zID1THf'


access_token ='192923260-kvYRRIvP0JskbKDgF9rKBTritiCYnIsom746P7ZU'
access_token_secret ='uC89Dg3gEIJIKPGWBbkl7ZYvMSbsDgawYB0TeLKNaDOOX'

auth = tweepy.OAuthHandler(cons_key, cons_secret)
auth.set_access_token(access_token, access_token_secret)

print("\nTwitter Authorization Success!\n")


api = tweepy.API(auth)

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
