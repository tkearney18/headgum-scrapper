import requests
from bs4 impoer BeautifulSoup

URL = sys.argv(0)
request = requests.get(URL)
soup = BeautifulSoup(request.content, 'html5lib')

episodes = soup.findAll('ul', attrs = {'class':'episode_list'})

for row in episodes.findAll('li', atts = {'class':'episode_summary'}):
	
