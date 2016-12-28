import requests
from bs4 import BeautifulSoup
from django.shortcuts import render



# Create your views here.

def home(request):

	messsage = 'Django Web Scraper - Choose Your Site: '
	
	app_name = ['Gumtree Python Jobs', 'Luxury Cars Collection']
	
	app_link = ['gumtree', 'cars']
	
	app_list = zip(app_name, app_link)

	context = {
		'messsage': messsage,
		'app_list': app_list,
	}

	return render(request, 'scraper/home.html', context)
	
	
def scrapGumtree(request):
	
	url_to_scrape = 'https://www.gumtree.co.za/s-jobs/western-cape/python/v1c8l3100001q0p1'
	
	r = requests.get(url_to_scrape)
	
	soup = BeautifulSoup(r.text, "html.parser")
	#for encoding error - type in the cmd: 
	#chcp 65001
	#set PYTHONIOENCODING=utf-8
	
	inmates_links = []
	
	inmates_names = []
	
	inmates_general = []
	
	scrap_message = 'No content scraped'
		
	#scraping title of the website
	title_name = soup.title.string
	
	#scraping span keyword on the website for content
	content_info = soup.select_one('span.keyword').string
	
	#scraping image from site
	content_logo_link = soup.select_one('img.logo')['src']
	
	#scraps the content of the entire img tag
	content_logo = soup.select(".logo img")
	
	
	#scraping job titles
	job_title_list = []
	job_counter = 0
	
	for link in soup.findAll('a', {'class': 'href-link'}):
	
		try:
			#print(link['href'])
			job_title_list.append(link.string)
			scrap_message = 'Job titles scraped'
			job_counter += 1
			
		except KeyError:
	
			pass
	
	
	#scraping job title links
	job_title_list_links = []
	
	job_phone_number = []
	
	job_full_description = []
	
	base_url_for_scraped_links = "https://www.gumtree.co.za"

	for link in soup.findAll('a', {'class': 'href-link'}):
	
		try:
			#print(link['href'])
			job_title_list_links.append(base_url_for_scraped_links + link['href'])
			scrap_message = 'Job links scraped'
			
			##########################################
			#scraping phone numbers from full ad 
	
			url_to_scrape_for_details = base_url_for_scraped_links + link['href']
	
			r2 = requests.get(url_to_scrape_for_details)
	
			soup_details = BeautifulSoup(r2.text, "html.parser")
	
			for link in soup_details.findAll('span', {'id': 'phone-number'}):
	
				try:
					#print(link['href'])
					job_phone_number.append(link.string)
					scrap_message = 'Job Phone numbers scraped'
			
				except KeyError:
	
					pass
			###########################################
			
			###########################################
			#scraping full description from full ad
			
			for link in soup_details.findAll('span', {'class': 'pre'}):
	
				try:
					#print(link['href'])
					#job_full_description.append(link.string)
					job_full_description.append(link.prettify())
					scrap_message = 'Job Full description scraped'
			
				except KeyError:
	
					pass
			###########################################
			
		except KeyError:
	
			pass
			
			
	#scraping job descriptions
	job_description = []
	
	for link in soup.findAll('div', {'class': 'description hidden'}):
	
		try:
			#print(link['href'])
			job_description.append(link.string)
			scrap_message = 'Job descriptions scraped'
			
		except KeyError:
	
			pass
	
	
	#scraping job locations
	job_location = []
	
	#scraping child without class of parent with class
	for link in soup.findAll('div', {'class': 'category-location'}):
	
		for childSpan in link.findAll('span'):
	
			try:
				#print(link['href'])
				job_location.append(childSpan.string)
				scrap_message = 'Job locations scraped'
			
			except KeyError:
	
				pass
	
	
	#zipping lists scraped together
	jobs_general = zip(job_title_list, job_title_list_links, job_description, job_location, job_phone_number, job_full_description)
	
	messsage = 'This is the Scraper Index for Gumtree.'
	
	messsage_2 = 'Jobs'
	
	context={
	'messsage': messsage,
	'messsage_2': messsage_2,
	'scrap_message': scrap_message,
	'title_name': title_name,
	'content_logo': content_logo,
	'content_logo_link': content_logo_link,
	'content_info': content_info,
	'job_title_list': job_title_list,
	'job_title_list_links': job_title_list_links,
	'job_description': job_description,
	'job_counter': job_counter,
	'job_location': job_location,
	'jobs_general': jobs_general,
	'job_phone_number': job_phone_number,
	'job_full_description': job_full_description,
	}

	return render(request, 'scraper/scrap_gumtree.html', context)

	
def scrapCars(request):

	url_to_scrape = 'http://www.hdwallpapers.in/cars-desktop-wallpapers.html'
	
	r = requests.get(url_to_scrape)

	soup = BeautifulSoup(r.text, "html.parser")
	
	#scraping title of the website
	title_name = soup.title.string
		
	#scraping span keyword on the website for content
	content_info = soup.h1.string
	
	base_url_for_scraped_links = "http://www.hdwallpapers.in/"
		
	cars_pics = []
			
	cars_names = []
	
	cars_list = []
	
	car_counter = 0
	
	#scraping links img children
	for link in soup.findAll('div', {'class': 'thumb'}):
		for child1 in link.findAll('a'):
			for child2 in child1.findAll('img'):
				cars_pics.append(base_url_for_scraped_links + child2['src'])
				car_counter += 1
				
	for link in soup.findAll('div', {'class': 'thumb'}):
		for child1 in link.findAll('a'):
			for child2 in child1.findAll('p'):
				cars_names.append(child2.string)
	
	cars_list = zip(cars_pics, cars_names)
	
	messsage = 'Luxury Cars Collection'
	
	messsage_2 = 'Cars'
	
	context = {
		'title_name': title_name,
		'content_info': content_info,		
		'cars_pics': cars_pics,
		'cars_list': cars_list,
		'car_counter': car_counter,
		'messsage': messsage,
		'messsage_2': messsage_2,
	}

	return render(request, 'scraper/index_cars.html', context)

	
def about(request):

	author_dict = {
		"Sun Tzu": "The supreme art of war is to subdue the enemy without fighting.", 
		"Mandela": "I learned that courage was not the absence of fear, but the triumph over it. The brave man is not he who does not feel afraid, but he who conquers that fear.", 
		"Gandhi": "Strength does not come from physical capacity. It comes from an indomitable will."}
		
	author_pics_dict = {
		"Sun Tzu": "http://larrygeorges-productions.co.nf/Website%20Experience/image/sun%20tzu.jpg", 
		"Mandela": "http://larrygeorges-productions.co.nf/Website%20Experience/image/mandela.png", 
		"Gandhi": "http://larrygeorges-productions.co.nf/Website%20Experience/image/gandhi_2.jpg"}
	
	context = {
		'author_dict': author_dict,
		'author_pics_dict': author_pics_dict
	}

	return render(request, 'scraper/about.html', context)