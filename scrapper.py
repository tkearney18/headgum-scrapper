import requests
from bs4 import BeautifulSoup
import sys
import csv
#functions needed: main, get episode data, write file,paginate, get full description
#URL = sys.argv[0]
def main():
	url = 'http://headgum.com/if-i-were-you'
	request = requests.get(url)
	segments = url.rpartition('/')
	soup = BeautifulSoup(request.content, 'html5lib')

	episodes = soup.find('ul', attrs = {'class':'episode_list'})

	podcastInfo = soup.find('div', attrs = {'class':'hug'})
	podcastTitle = podcastInfo.find('h1').get_text()
	#print podcastTitle
	allEpisodes = getEpisodeData(episodes,segments[0])	
	fileName = podcastTitle + ".csv"
	buildCSV(allEpisodes,fileName)
	#print allEpisodes

def getEpisodeData(episodes,url):
	allEpisodes = []
	for row in episodes.findAll('li', attrs = {'class':'episode_summary'}):
		episodeData = {}
		meta = row.find('div', attrs = {'class':'meta'})
		episodeRow = meta.find('a', attrs = {'class':'episode_row'})
		title = episodeRow.select('span')[1].get_text()
		date = episodeRow.find('span', attrs = {'class':'timestamp'}).get_text()

		descriptionLink = meta.find('p')
		anchor = descriptionLink.find('a')['href']
		descriptionLink = url + anchor	
		description = getDescription(descriptionLink)
		description = getDescription(descriptionLink)

		episodeData["title"] = title.encode('UTF-8')
		episodeData["description"] = description.encode('UTF-8')
		episodeData["date"] = date.encode('UTF-8')
		episodeData["url"] = descriptionLink.encode('UTF-8')
		print episodeData
		allEpisodes.append(episodeData) 

	return allEpisodes

def getDescription(url):	
	request = requests.get(url)
	soup = BeautifulSoup(request.content, 'html5lib')
	center = soup.find('div', attrs = {'class':'center'})
	descHolder = center.select('div')[3]
	description = descHolder.find('p').get_text()
	return description	
def buildCSV(allEpisodes,fileName):
	with open(fileName,'wb') as f:
		w = csv.DictWriter(f,['title', 'description','date','url'],extrasaction='ignore', delimiter=',')
		w.writeheader()
		for episode in allEpisodes:
			w.writerow(episode)
main()
