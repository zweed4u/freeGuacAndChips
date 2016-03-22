#21 March 2016
#http://www.guachunter.com/
#http://nrn.com/marketing/chipotle-offers-free-guacamole-and-chips-guac-hunter-game
import requests,json
def freeGuacAndChips(f,l,m,z):
	print f,l,m,z
	reqUrl='http://api.guachunter.com/guac-it-out/reg'
	postHeaders={
		'Accept-Language':'en-US,en;q=0.8',
		'Origin':'http://www.guachunter.com',
		'Referer':'http://www.guachunter.com/',
		'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/37.0.2062.120 Chrome/37.0.2062.120 Safari/537.36'
	}

	payload={"f":f,"l":l,"m":m,"s":"true","z":z}
	session=requests.Session()
	response=session.post(reqUrl,data=json.dumps(payload),headers=postHeaders)
	print response.content

first=raw_input('First Name: ')
last=raw_input('Last Name: ')
mobile=raw_input('Mobile number: ')
zipCode=raw_input('Zip Code: ')

freeGuacAndChips(first,last,mobile,zipCode)
