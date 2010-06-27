import serial
import tweetstream
import time

#signfile = serial.Serial('/dev/ttyUSB0',baudrate=9600,stopbits=1,xonxoff=1,rtscts=0,timeout=0,parity='N',dsrdtr=0)

styles = {
	"scroll_stuck" : "<FM>",
	"center" : "<FB>",
	"scroll_always" : "<FH>",
}

def tosign(id, topStyle, u, bottomStyle, s):
	signfile.write("\x0D\x0A\x0A")
	signfile.write("  <ID"+str(id)+"><PZ>")
	signfile.write(styles.get(topStyle))
	signfile.write("<L1>")
	signfile.write(u)
	signfile.write("<L2>"+s)
	signfile.write(styles.get(bottomStyle))
	signfile.write("\x0D\x0A")
	signfile.write("  ")
	signfile.write("<ID"+str(id)+"><RPZ>")
	signfile.write("\x0D\x0A")
	signfile.write("  <ID00><L1>")
	signfile.write("\x0D\x0A")
	signfile.write("  <ID00><RPZ>")
	time.sleep(1)
	signfile.write("\x0C")

def formSign(sign, tweet):
  tosign(sign, "center", '@'+tweet['user']['screen_name'].upper(), "scroll_always", tweet['text'])

signfile = serial.Serial('/dev/ttyUSB0',baudrate=9600)
tosign(30, "center", "", "center", "Please tweet at me!")
tosign(40,"center", "", "center", "")
tosign(73,"center", "", "center", "")
words = ["oil","dojosign","hackerdojo","hacker dojo","#dojosign"]
p = ""
pp = ""
with tweetstream.TrackStream("dojosign", "dojo77", words) as stream:
  for tweet in stream:
    if type(tweet['text']) is str:
      print tweet['user']['screen_name']+": "+tweet['text'] 
      print "\n"
      if "oil" in tweet['text']:
        formSign(30, tweet)
        if p:
          formSign(40, p)
        if pp:
          formSign(73, pp)
        if p:
          pp = p
        p = tweet
        time.sleep(10)

signfile.close()



#signfile.write("\n\n<ID40><PZ><FB><L1>BBB<FP5><L2>AAA<FH>\n")
#signfile.write("<ID40><RPZ>")
#signfile.write("\x0C")
#signfile.close()
