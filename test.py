import requests
import re

from bs4 import BeautifulSoup
from word2number import w2n


response = requests.get('https://www.gov.mb.ca/health/newsreleases/index.html')
soup = BeautifulSoup(response.text, 'html.parser');
news = soup.findAll('p')

for i in reversed(range(len(news)-2)):
	link_news = news[i]
	covid_cases = link_news.contents[0].text
	date = link_news.em.text
	if("COVID-19 Bulletin" in covid_cases):
		link = requests.get(link_news.a['href'])
		soup_link = BeautifulSoup(link.text, 'html.parser')
		for paragraph in soup_link.select('.content-section'):
			announcement = paragraph.div.text
			match = re.search(r'(\S+) new', announcement)
			additional_case = re.search(r'(\S+) additional case', announcement)
			
			if match:
				cases = match.w2n.word_to_num(group(1))
			elif(additional_case):
				cases = additional_case.w2n.word_to_num(group(1))

sms_body = date + ", Manitoba has " + cases + " new cases"

# message = client.messages.create(
#     to="+12049156184", 
#     from_="+12058989300",
#     body="Hello, on " + sms_body)

print(sms_body)