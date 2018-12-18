import urllib2
from bs4 import BeautifulSoup

quote_page = 'http://www.bloomberg.com/quote/SPX:IND%27'
#'https://africanfinancials.com/zimbabwe-stock-exchange-share-prices/'
page = urllib2.urlopen(quote_page)
soup = BeautifulSoup(page, 'html.parser')
name_box = soup.find('h1', attrs={'class': 'name'})
name = name_box.text.strip() # strip() is used to remove starting and trailing
print name