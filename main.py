import json, feedparser
from qbittorrent import Client
from requests_html import HTMLSession

session = HTMLSession()
#Headers to mimic Humanly Request
headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
    'referer': 'https://ww3.7movierulz.es/'
}

qb = Client('http://127.0.0.1:6969/')
url = 'https://ww3.7movierulz.es/category/telugu-movie/feed/'
feed = feedparser.parse(url)
movies = feed.entries
hd_movies = []
#Function to download movie
def download(movie):
    url = movie.link
    r = session.get(url, headers=headers)
    uri = r.html.find('.mv_button_css',first=True)
    uri = uri.xpath('//a/@href',first=True)
    qb.download_from_link(uri, category='telugu')

for movie in movies:
    title = movie.title
    if 'HDRip' in title:
        title = title[:title.find(')')+1]
        hd_movies.append(title)
        with open('movies.json','r') as fp:
            dump = json.load(fp)
        if title not in dump:
            download(movie)
with open('movies.json','w') as fp:
    json.dump(hd_movies, fp, indent=2)