import requests
from bs4 import BeautifulSoup as bs 

def read(Sid):
	soup = bs(requests.get(f'https://any-more.ru/manga/?manga=1-{Sid}').text,'html5lib')
	img = soup.text.split('nimation:animation-demon 4s ease;position:absolute;top:0;left:0;background-image:url(')[1].split(')')[0]
	name = soup.find('div',class_='anime__details__title').find('h3').text
	return f'<a href="https://any-more.ru/manga/?manga=1-{Sid}" alt="{name}" title="Нажмите для перехода на сайт манги {name}"><img src="{img}"><tizle><h1>{name}</h1></tizle></a>'

def take(Sid,Mid):
	soup = bs(requests.get(f'https://any-more.ru/manga/1-{Sid}/{Mid}_index.php').text,'html5lib')
	imgs = [img.find('img').get('src') for img in soup.find('div',class_='demo').find('div',class_="grid").find_all('center')]
	endl = ''
	for i in imgs:
		endl+=f'<li><img src="{i}" width="83%"></li>'
	endl+='<li>Актуальные ссылки для доната: <a href="/payment?from=/">Донат нужен для поддержания работы всех проектов GEXEM</a></li>'

	return (
			endl,
			f'<a href="https://any-more.ru/manga/1-{Sid}/{Mid}_index.php">'+\
				soup.find('div',class_='demo').find('div',class_="grid").find_all('center')[1].find('img').get('alt')\
			+'</a>')

if __name__ == '__main__':
	print(take(input('ID: '),1))