import os
import requests
from bs4 import BeautifulSoup
import re
import time
import tldextract
import urllib.request
import random
import subprocess
from multiprocessing.pool import ThreadPool

##V1

name_q=input("Enter Model Name: ")
name=name_q.replace(" " ,"-")

isExist = os.path.exists(f'./{name}')
if not isExist:

   os.makedirs(f'./{name}')
   print("The new directory is created!")

def s3():
	s3=f'https://babes.porn/pics/{name}'
	r=requests.get(s3)
	soup = BeautifulSoup(r.text, 'html.parser')
	urls=[]
	image_url=[]
	

	for tag in soup.findAll('a'  ,href=re.compile('^/photos/')):

		a='https://babes.porn'
		b=tag['href']
		urls.append(a+b)
	
	#print (urls)
	#print (len(urls))

	def download_url(url):
			  print("downloading: ",url)
			  
			  file_name_start_pos = url.rfind("/") + 1
			  file_name = url[file_name_start_pos:]
			 
			  r = requests.get(url, stream=True)
			  if r.status_code == requests.codes.ok:
			    with open(f'./{name}/{file_name}', 'wb') as f:
			      for data in r:
			        f.write(data)
			  return url

	i = 0
	while i < len(urls):
		
		image_html=requests.get(urls[i])
		time.sleep(2)
		soup2 = BeautifulSoup(image_html.text, 'html.parser')

		for tag in soup2.findAll('img', src=re.compile('^//pornhd.vip/pics/') , alt='thumb'):

			a='https:' + tag['src']
			b=a.replace("hd-" , "")
			#print(b)
			image_url.append(b)
		print(f'Finished {i}')

		i=i+1

	image_url = list(set(image_url))
	results = ThreadPool(10).imap_unordered(download_url,image_url)
	for r in results:
		print(r)




def s5():

	first_char=name[0]	
	#print(first_char)
	search=f'https://babesource.com/pornstars/?letter={first_char}'
	rs=requests.get(search)
	soup = BeautifulSoup(rs.text, 'html.parser')
	#print(name)
	for tag in soup.findAll('a' , class_="pornstars-lists__link",  href=re.compile(f'^https://babesource.com/pornstars/{name}')):
		p_page = (tag['href'])

	#print(p_page)
	s5=f'{p_page}page1.html'
	r=requests.get(s5)
	soup = BeautifulSoup(r.text, 'html.parser')
	image_url=[]
	pages=[]

	
	
	for tag in soup.findAll('a' , class_="paginations__link",  href=re.compile('^page')):
		pages.append(tag['href'])
	
	a=pages[-1]
	b=a.replace("page" , "")
	total_pages=b.replace(".html" , "")

	#
	#print(total_pages)

	

	i = 1

	while i <= int(total_pages):
		image_htmlc=requests.get(f'{p_page}page{i}.html')
		urls=[]

		soup2c = BeautifulSoup(image_htmlc.text, 'html.parser')

		for tag in soup2c.findAll('a' , class_="main-content__card-link",  href=re.compile('^https://babesource.com/galleries/')):
			urls.append(tag['href'])

		#print(len(urls))
		k = 0


		while k < len(urls):
		
			image_htmld=requests.get(urls[k])
			name_a=urls[k].replace("https://babesource.com/galleries/" , "")
			full_name=name_a.replace(".html" , "")
			def download_url(url):
			  print("downloading: ",url)

			  file_name_start_pos = url.rfind("/") + 1

			  file_name = url[file_name_start_pos:]
			 
			  r = requests.get(url, stream=True)
			  if r.status_code == requests.codes.ok:
			    with open(f'./{name}/{full_name}{file_name}.jpg', 'wb') as f:
			      for data in r:
			        f.write(data)
			  return url
			
			#print(urls[k])
			
			soup2d = BeautifulSoup(image_htmld.text, 'html.parser')

			for tag in soup2d.findAll('a', class_= "box-massage__card-link" ,href=re.compile('^https://media.babesource.com/galleries/')):


				image_url.append(tag['href'])
				print(image_url)
			
			k=k+1
		image_url = list(set(image_url))
		results = ThreadPool(10).imap_unordered(download_url,image_url)
		for r in results:
			print(r)


				
			
		i=i+1
		urls.clear()
	
s3()
s5()





		
		



