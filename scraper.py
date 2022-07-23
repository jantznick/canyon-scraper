import requests
import bs4
import os
import time
from twilio.rest import Client

# run in crontab from a folder called 'canyon' in home directory
# Change URL to URL of bike product page and size you want
url = ''
bikeSize = 'M' # Should be like: 'S' 'M' 'L' or 'XL'
# Add twilio secret and Sid
twilioSecret = ''
twilioSid = ''

res = requests.get(url)
canyonSoup = bs4.BeautifulSoup(res.text, 'html.parser')

# all bike selection icons on the site have a data-product-size selector used to select a size
myBike = canyonSoup.select('[data-product-size="' + bikeSize + '"]')

classes = myBike[0].get('class')

# canyon's site uses a class called 'js-nonSelectableVariation' to change the style of the sizing buttons for unavailable bikes
bikeInStock = not 'js-nonSelectableVariation' in classes

if bikeInStock:
	if not 'bikeAvailable' in os.listdir('canyon'):
		# send twilio message
		client = Client(twilioSid, twilioSecret)
		message = client.messages.create(to="", from_="", body="ALERT! Canyon Speedmax CF SLX size " + bikeSize + " is in stock! Order Now!\n" + url)
		# create a file called bikeAvailable when the text is sent so that it doesn't overrun your phone with texts
		f = open("canyon/bikeAvailable", "w")
		f.close()
else:
	# log times to bikeCheck.txt just so you can check the script is working
	f = open('canyon/bikeCheck.txt', "a")
	f.write("Bike not available at " + time.strftime("%m-%d-%Y, %H:%M", time.localtime()) + "\n")
	f.close()
