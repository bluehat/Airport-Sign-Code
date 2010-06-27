import serial
import tweetstream
import time

#signfile = serial.Serial('/dev/ttyUSB0',baudrate=9600,stopbits=1,xonxoff=1,rtscts=0,timeout=0,parity='N',dsrdtr=0)

def tosign(id,u,s):
	#print signfile
	signfile.write("\x0D\x0A\x0A")
	signfile.write("  <ID"+str(id)+"><PZ><FB><L1>")
	signfile.write(u)
	signfile.write("<L2>               "+s+"<FH>")
	signfile.write("\x0D\x0A")
	signfile.write("  ")
	signfile.write("<ID"+str(id)+"><RPZ>")
	signfile.write("\x0D\x0A")
	signfile.write("  <ID00><L1>")
	signfile.write("\x0D\x0A")
	signfile.write("  <ID00><RPZ>")
	time.sleep(1)
	signfile.write("\x0C")

signfile = serial.Serial('/dev/ttyUSB0',baudrate=9600)
tosign(30,"","Hello world I am testing some shit")
tosign(40,"","")
tosign(73,"","")
words = ["oil","dojosign","hackerdojo","hacker dojo","#dojosign"]
p = ""
pp = ""
with tweetstream.TrackStream("dojosign", "dojo77", words) as stream:
  for tweet in stream:
    if type(tweet['text']) is str:
      print tweet['user']['screen_name']+": "+tweet['text'] 
      print "\n"
      if "dojo" in tweet['text']:
        tosign(30,"@"+tweet['user']['screen_name'].upper(),tweet['text'])
        if p:
          tosign(40,"@"+p['user']['screen_name'].upper(),p['text'])
        if pp:
          tosign(73,"@"+pp['user']['screen_name'].upper(),pp['text'])
        if p:
          pp = p
        p = tweet
        time.sleep(10)

signfile.close()



#signfile.write("\n\n<ID40><PZ><FB><L1>BBB<FP5><L2>AAA<FH>\n")
#signfile.write("<ID40><RPZ>")
#signfile.write("\x0C")
#signfile.close()
