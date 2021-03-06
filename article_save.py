import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime
from datetime import datetime
import requests
import bs4
import pandas as pd
from bs4 import BeautifulSoup
import os

def write_to_sheet(article_title, article_url):
	credentials = os.environ['GOOGLE_APPLICATION_CREDENTIALS']
	creds = ServiceAccountCredentials.from_json_keyfile_name(credentials)
	client = gspread.authorize(creds)
	sheet = client.open("SavedArticles").sheet1
	row = [article_title,str(article_url)]
	sheet.append_row(row)
	return 'Done'

#open timesheet
def write_to_sheet_times(timed, typed):
	credentials = os.environ['GOOGLE_APPLICATION_CREDENTIALS']
	creds = ServiceAccountCredentials.from_json_keyfile_name(credentials)
	client = gspread.authorize(creds)
	sheet = client.open("TimeSheet").sheet1
	row = [timed,typed]
	sheet.append_row(row)
	return 'Done'

def get_last_time():
	credentials = os.environ['GOOGLE_APPLICATION_CREDENTIALS']
	creds = ServiceAccountCredentials.from_json_keyfile_name(credentials)
	client = gspread.authorize(creds)
	sheet = client.open("TimeSheet").sheet1
	last_time = sheet.col_values(0)[-1]
	return last_time


#helper functions
def next_available_row():
    str_list = list(filter(None, worksheet.col_values(1)))
    return str(len(str_list)-2)

def on_sheet_grab(string_url):
    page_sourced = requests.get(string_url).content
    html_content = BeautifulSoup(page_sourced, "html.parser")
    titled = html_content.find('h1')
    return titled.text