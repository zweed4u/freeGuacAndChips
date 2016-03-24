#Parses user's DM and enters them for free quac and chips
#DM format: 
#                  FIRST_NAME LAST_NAME MOBILE_NUMBER ZIPCODE 
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy import API
from tweepy.streaming import StreamListener
import json,requests,urllib2

#enter the corresponding information from your Twitter application:
#make sure to set proper permissions for application (DMs included)
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

class StdOutListener( StreamListener ):
	#@staticmethod <- use if StdOutListener.freeGuacAndChips wanted rather than self
	def freeGuacAndChips(self,f,l,m,z):
		global response
		reqUrl='http://api.guachunter.com/guac-it-out/reg'
		postHeaders={
			'Accept-Language':'en-US,en;q=0.8',
			'Origin':'http//www.guachunter.com',
			'Referer':'http://www.guachunter.com/',
			'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/37.0.2062.120 Chrome/37.0.2062.120 Safari/537.36'
		}

		payload={"f":f,"l":l,"m":m,"s":"true","z":z}
		session=requests.Session()
		response=session.post(reqUrl,data=json.dumps(payload),headers=postHeaders)
		#want {"status":"success","is_repeat":false}
		print response.content

    	def __init__( self ):
        	self.tweetCount = 0

    	def on_connect( self ):
        	print("Connection established!!")

    	def on_disconnect( self, notice ):
        	print("Connection lost!! : ", notice)

    	def on_data( self, status ):
		global message,first,last,mobile,zipCode
		#unicode to string
		status = str(status)
		try:
			json_acceptable_string = status.replace('\\','')
			#string to dict
			status=json.loads(json_acceptable_string)
			#conditional for wanted message stream
			if 'direct_message' in status.keys():
				print '\n'
				print status[u'direct_message'][u'sender_screen_name'] +' sent: '+ status[u'direct_message'][u'text']
				message=str(status[u'direct_message'][u'text'])
				#makes sure the message is 4 words
				if len(message.split(' '))==4:
					first=message.split(' ')[0]
					last=message.split(' ')[1]
					mobile=message.split(' ')[2]
					zipCode=message.split(' ')[3]
					self.freeGuacAndChips(first,last,mobile,zipCode)
					print '\n'
				else:
					#message is not in designed format
					print 'Message ill formed'
			else:
				#not direct message flow
				pass
		except:
			#not important flows - couldn't convert to json/not correct flow in stream
			pass
		return True

   	def on_direct_message( self, status ):
		print("Entered on_direct_message()")
		try:
		    print(status)#, flush = True)
		    return True

		except BaseException as e:
		    print("Failed on_direct_message()", str(e))

    	def on_error( self, status ):
		#Verbose error code
		if status==200:
			print str(status)+' :: OK - Success!'
		elif status==304:
			print str(status)+' :: Not modified'
		elif status==400:
			print str(status)+' :: Bad request'
		elif status==401:
			print str(status)+' :: Unauthorized'
		elif status==403:
			print str(status)+' :: Forbidden'
		elif status==404:
			print str(status)+' :: Not found'
		elif status==406:
			print str(status)+' :: Not acceptable'
		elif status==410:
			print str(status)+' :: Gone'
		elif status==420:
			print str(status)+' :: Enhance your Calm - rate limited'
		elif status==422:
			print str(status)+' :: Unprocessable entity'
		elif status==429:
			print str(status)+' :: Too many requests'
		elif status==500:
			print str(status)+' :: Internal server error'
		elif status==502:
			print str(status)+' :: Bad gateway'
		elif status==503:
			print str(status)+' :: Service unavailable'
		elif status==504:
			print str(status)+' :: Gateway timeout'
		else:
			print str(status)+' :: Unknown'

def main():
   	try:
		auth = OAuthHandler(consumer_key, consumer_secret)
		auth.secure = True
		auth.set_access_token(access_token, access_token_secret)
		api = API(auth)
		print(api.me().name)
		stream = Stream(auth, StdOutListener())
		stream.userstream()

    	except BaseException as e:
        	print("Error in main()", e)


if __name__ == '__main__':
	main()
