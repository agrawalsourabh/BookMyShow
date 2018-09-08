

from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup 
from bs4 import BeautifulSoup as b_soup 
import os

print("Enter your City")
city = input()

def openSite(myUrl):
	# myUrl = 'https://in.bookmyshow.com'
	# myUrl_ext = '/pune/movies'

	# open connection 
	uClient = uReq(myUrl)

	# get html web page
	page_html = uClient.read()

	# close connection
	uClient.close()

	return page_html

myUrl = 'https://in.bookmyshow.com'
myUrlExt = '/' + city +'/movies'
page_html = openSite(myUrl+myUrlExt)

# #open file
fileName  = 'bms_'+city+'.csv'
OUTPUT_DIR = 'city'
f = open( fileName, 'w')
header = 'SNo, Movie_Title, Language, Release_Date, Duration \n'

f.write(header)

page_soup = soup(page_html)
print(page_soup.title.text)

containers = page_soup.findAll('div', {'class': 'card-container wow fadeIn movie-card-container'})
print(str(len(containers)))
sno = 0

#for container in containers: for all available movies

for i in range(10): # First - 10 movies 
	try:
		movies_details = containers[i].findAll('div', {'class': 'card-details'})

	except IndexError:
		break
	# movies_details_name = movies_details[0].find('div', {'class':'card-right'})
	
	movies_details_name = movies_details[0].find('div', {'class':'card-right'})
	movie_title = movies_details_name.div.h4.text

	movies_details_lang = movies_details[0].find('li', {'class':'__language'})
	movie_lang = movies_details_lang.text

	
	# print('sno' + str(sno))
	# movies_pages = container.find('div', {'class' : 'card-container wow fadeIn movie-card-container'})

	movie_page_html = openSite(myUrl + str(containers[i].a['href']))
	# print(movie_page_html)
	movie_page_soup = b_soup(movie_page_html)
	# print(movie_page_soup.title.text)
	# print(myUrl +  str(container.a['href']))

	# movie_page_container = movie_page_soup.findAll('div', {'class' : 'date-time'})

	movie_page_container_date = movie_page_soup.find('span', {'class': '__release-date'})
	release_date = movie_page_container_date.text
	# print(str(movie_page_container_date.text))

	try:
		movie_page_container_dur = movie_page_soup.find('span', {'class':'__time'})
		movie_dur = movie_page_container_dur.text
	except AttributeError:
		movie_dur = '-'

	sno = sno + 1

	f.write(str(sno) + ',' + movie_title.replace(',', ' ') + ',' + movie_lang.replace(',', '') + ',' +release_date.replace(',', '') +', ' + movie_dur.replace(',', '') +'\n')



	

f.close()