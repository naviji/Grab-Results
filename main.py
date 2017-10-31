import urllib.request
from urllib.request import urlopen
from bs4 import BeautifulSoup
from pdftotext import convert_pdf_to_txt
from data_extract import extractor
import os
import sys


def get_html( str ):
	# returns html string from url
	fp = urllib.request.urlopen(str)
	mybytes = fp.read()
	mystr = mybytes.decode("utf8")
	fp.close()
	return mystr

def download_file(download_url,save_path):
	#download binary files like pdf (not text)
	response = urlopen(download_url)
	file = open(save_path, 'wb+')
	file.write(response.read())
	file.close()



def convert_file(src,des):
	# convert pdf in desc path to txt file and store in src path
	raw_text = convert_pdf_to_txt(src)
	text_file = open(des,"w")
	text_file.write(raw_text)
	text_file.close()



download_links = [] # list to store the download urls
count = 0 # initialize number of colleges to zero

#result_url = input("Enter the url of result page: ")
# format should be https://www.example.com


#reevaluation
result_url = """https://www.ktu.edu.in/eu/res/viewExamResults.htm?examDefIdEnr=%2FXYPj2s32s%2FOZ6t84s7EhlO3S%2FGQX6qT%2B2qyVwPNFM8%3D&type=Yhr4byAdiTiOWpqU3YUF9v6SoVXPa7y64sg52hGYouw%3D&publishId=l8lJgrFygKWKuU72PEFgt41gTZvupO%2F%2F6CYuvI6GCCU%3D"""

html_doc = get_html(result_url)

# creates a ordered grouping from raw html string
soup = BeautifulSoup(html_doc, 'html.parser')


for link in soup.find_all('a'):
	temp = link.get('href')
	if("attachment" in temp):
		if("https://www.ktu.edu.in" not in temp):
			download_links.append("https://www.ktu.edu.in"+temp)
		else:
			download_links.append(temp)


print("Started downloading files...")
print("Please wait!")
for url in download_links:
	count = count + 1
	download_file(url,"./pdf/{}.pdf".format(count))
	print("Downloaded {}-".format(count))
print("Download completed")


num_college = count # Set number of colleges to count

print("Started conversion of files...")
print("Please wait!")
for i in range(1,num_college+1):
	convert_file("./pdf/{}.pdf".format(i),"./text/{}.txt".format(i))
	os.remove("./pdf/{}.pdf".format(i))
	extractor("./text/{}.txt".format(i),"./extracted_data")
	os.remove("./text/{}.txt".format(i))
	print("Converted {}-".format(i))
print("Conversion completed and data extracted")


