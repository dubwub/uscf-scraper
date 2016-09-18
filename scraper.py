# right now just pulling regular data from high level, maybe in the future might go into individual tournaments
# and pull actual internal tournament data too
# requires: pip install BeautifulSoup, lxml (requires msft visual c++ 9.0)

from bs4 import BeautifulSoup
from urllib2 import urlopen, Request

userAgent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7' # i'm totally a real browser
playerFullURL = 'http://www.uschess.org/msa/MbrDtlTnmtHst.php?13034164';
baseURL = 'http://www.uschess.org/msa/'
hdr = {'User-Agent': userAgent,}
pageRange = 5; # http://www.uschess.org/msa/MbrDtlTnmtHst.php?13034164.4 is max page

def pullTournamentsFromPage(index):
	urlToRead = playerFullURL + '.' + str(index)
	req = Request(urlToRead, headers=hdr)
	page = urlopen(req)
	soup = BeautifulSoup(page, "html.parser")
	return soup.findAll('tr', bgcolor=['FFFF80', 'FFFFC0'])[1:]

def parseTournament(tournament):
	date = [text for text in tournament.find('td', width='120').stripped_strings][0]
	link = tournament.find('td', width='350').a.get('href')
	name = tournament.find('td', width='350').a.getText()
	ratings = [text for text in tournament.find('td', width='160').stripped_strings]
	beforeRating = ''
	afterRating = ''
	if len(ratings) == 2:
		beforeRating = ratings[0][:-3]
		afterRating = ratings[1]
	output = {
		'tdate': date,
		'tlink': link,
		'tname': name,
		'tbeforerating': beforeRating,
		'tafterrating': afterRating
	}
	print output
	return output

def scrapeUSCF():
	tournaments = []
	for index in range(1, pageRange):
		t_data = pullTournamentsFromPage(index)
		for t in t_data:
			tournaments.append(parseTournament(t))
	f1=open('./testfile', 'w+')
	for i in range(0, len(tournaments)):
		f1.write(tournaments[i]['tdate'] + ',' + tournaments[i]['tlink'] + ',' + tournaments[i]['tname'] + ',' + 
			tournaments[i]['tbeforerating'] + ',' + tournaments[i]['tafterrating'] + '\n')

scrapeUSCF()