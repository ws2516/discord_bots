import requests
import json
import googlesearch
import google
from googlesearch import search
import bs4
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime


def libor():
	# Chatham Financial Curve
	url = 'https://www.chathamfinancial.com/getrates/24955'
	# Connect to the URL
	page_response = requests.get(url, timeout=10, headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate',
    'accept-language': 'en-US,en;q=0.9,fr;q=0.8,ro;q=0.7,ru;q=0.6,la;q=0.5,pt;q=0.4,de;q=0.3',
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'})
	curve_results, counter, steps = [], 0, 5
	text_decode = page_response.content
	rates = json.loads(text_decode)['Rates']
	for i in range(len(rates)):
		if i%12 and counter < steps:
			curve_results += [float(rates[i]['Rate'])]
			counter += 1
	date = datetime.now().strftime('%Y')
	dates = [i+int(date) for i in range(steps)]
	table = str(pd.DataFrame({'Date':dates, 'Curve Results':curve_results}).to_markdown())
	response = '```'+table + '```'
	return response

def investopedia_definitions(term):
	url = google_search('investopedia.com', term.replace('_',' '))
	page_response = requests.get(url, timeout=10, headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate',
    'accept-language': 'en-US,en;q=0.9,fr;q=0.8,ro;q=0.7,ru;q=0.6,la;q=0.5,pt;q=0.4,de;q=0.3',
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'})
	page_content = BeautifulSoup(page_response.content, "html.parser")
	navigate = page_content.findAll('p', class_="comp mntl-sc-block finance-sc-block-html mntl-sc-block-html")[0]
	return navigate.text + '\n See more here: ' + url


# _________________  worker functions _________________________
def google_search(query, term):
    httpsLink = [j for j in search(query+term, num=1, stop=1, pause=1)][0]
    return httpsLink