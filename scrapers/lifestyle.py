import requests
import json
import googlesearch
import google
from googlesearch import search
import bs4
from bs4 import BeautifulSoup
import pandas as pd

def coffee_bot(term):
	url = google_search('yelp.com', term.replace('_',' ') + 'best coffee shop list')
	page_response = requests.get(url, timeout=10, headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate',
    'accept-language': 'en-US,en;q=0.9,fr;q=0.8,ro;q=0.7,ru;q=0.6,la;q=0.5,pt;q=0.4,de;q=0.3',
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'})
	page_content = BeautifulSoup(page_response.content, "html.parser")
	#get the title
	
	#send the link - and wait for "yes", then put into "database"
	navigate_name = page_content.findAll('h4', class_="css-1l5lt1i")[2:7]
	names = [i.find('a').text for i in navigate_name]
	navigate_address = page_content.findAll('p', class_="css-8jxw1i")
	#print(navigate_address)
	address, counter = [], 0
	for i in navigate_address:
		try:
			if counter<7:
				address += [i.find('span').text]
				counter += 1
			else:
				continue
		except:
			continue
	address = address[2:]
	#the weird list comp ust puts them in the same list with a new line
	table = str(pd.DataFrame({'Name and Address':[names[i]+'\n'+address[i] for i in range(len(address))]}).to_markdown())
	response = '```'+table + '```'
	return response

def nykr_article(articel_string):
	url = google_search('The New Yorker: ', articel_string)
	return url



# _________________  worker functions _________________________
def google_search(query, term):
    httpsLink = [j for j in search(query+term, num=1, stop=1, pause=1)][0]
    return httpsLink
