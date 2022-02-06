from bs4 import BeautifulSoup as bs
import requests
import json


project_info = []
project_urls=[]
headers = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'}
url = 'https://www.wildberries.ru/catalog/sport/velosport/komplektuyushchie?sort=popular&page='

def get_data(url):
	
	for i in range(1,26):
		
		req = requests.get(url+str(i), headers=headers) #делаем запрос к основному сайт, используя фильтр
		
		with open(f'project{str(i)}.html', 'w', encoding='utf-8') as file:
			file.write(req.text) #делаем запись в файл, чтобы постоянно не нагружать сайт своими запросами, а то еще не дай бог бан дадут)
			
		with open(f'project{str(i)}.html', encoding='utf-8') as file:
			src = file.read()
			
			soup = bs(src, 'lxml')
			bicycle_parts = soup.find_all('div', class_='product-card j-card-item') #переходим к основным ссылкам - ссылкам на нужные нам товары
			for bicycle_part in bicycle_parts:	
				
				project_url = bicycle_part.find('a').get('href')
				if ('http' or 'https') not in project_url:
					project_url = 'https://www.wildberries.ru' + project_url
					
				project_urls.append(project_url)
				req = requests.get(project_url, headers)
				soup = bs(req.text, 'lxml')
				
				
				#ниже мы получаем цену искомого продукта и записываем в переменнную
				try:
					price = soup.find('div', class_='price-block__content').find('span', class_='price-block__final-price').get_text()
				except:
					print('Oops, sth went wrong')
					price = f'на странице со ссылкой "{project_url}" цены нет'
					
					
				#ниже мы получаем название искомого продукта и записываем в переменнную
				try:
					name_of_product = soup.find('div', class_='same-part-kt__header-wrap hide-mobile').find_all('span')[0].text + ' / ' + soup.find('div', class_='same-part-kt__header-wrap hide-mobile').find_all('span')[1].text
				except:
					print('Oops, sth went wrong')
					name_of_product = f'на странице со ссылкой "{project_url}" названия нет'
					
					
				#ниже мы получаем ссылку на картинку искомого продукта и записываем в переменнную	
				try:
					picture = soup.find('div', class_='photo-zoom__img-plug img-plug').find('img').get('src')
					picture = 'https:' + picture
				except:
					print('Oops, sth went wrong')
					picture = f'на странице со ссылкой "{project_url}" картинки нет'

					
				#ниже мы получаем описание искомого продукта и записываем в переменнную
				try:
					description = soup.find('div', class_='collapsable__content j-description').find('p').get_text()
				except:
					print('Oops, sth went wrong')
					description = f'на странице со ссылкой "{project_url}" описания нет'

				
				#делаем словарь с полученной информацией и добавляем в список, который будет записан в json файл
				project_info.append(
					{
						'Название': name_of_product.strip(),
						'Цена': price.strip(),
						'описание': description.strip(),
						'ссылка к картинке': picture.strip()
					}
				)
				
				#записываем все в файл
				with open('data/bicycle_info.json', 'w', encoding='utf-8') as filename:
					json.dump(project_info, filename, indent=4, ensure_ascii=False)


get_data(url)
