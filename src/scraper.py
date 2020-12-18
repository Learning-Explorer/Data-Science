import requests
import lxml.html as html
import os
import json
import csv



HOME_URL = 'https://gist.github.com/teffcode'

XPATH_LINK_TO_RETO = '//div/a/@href'
XPATH_TITLE_LINK = '//div/h1/strong//text()'
XPATH_IMG = '//kbd//img/@data-canonical-src'


def parse_home(url):

    try:
        r = requests.get(url)
        if r.status_code == 200:
            home = r.content.decode('utf-8')
            parsed = html.fromstring(home)

            return parsed

        else:
            raise ValueError(f'Error: {r.status_code}')
    except ValueError as ve:
        print(ve)


def parse_links(parsed):

    try:
        links_to_reto = parsed.xpath(XPATH_LINK_TO_RETO)
        
        return links_to_reto

    except:
        pass

def links():

    parsed = parse_home(HOME_URL)
    list1 = parse_links(parsed)
    parsed2 = parse_home(list1[37])
    list2 = parse_links(parsed2)
    all_list = list1[18:37]+list2[18:37]
    all_list = [item for item in all_list if item not in ('/teffcode')]
     
    with open('challenge.csv', 'w+', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['topic', 'challenge', 'answer'])

        for link in all_list:
            retos = parse_tags(link)
            row = [elements for elements in retos]
            writer.writerow(row)



def parse_tags(link):

    try:
        response = requests.get(link)
        if response.status_code == 200:
            quiz = response.content.decode('utf-8')
            parsed = html.fromstring(quiz)
            title = parsed.xpath(XPATH_TITLE_LINK)[0]
            title = _transform_title(title)
            resolved = parsed.xpath('//tbody//td/text()')[0]
            
            try:
                img = parsed.xpath(XPATH_IMG)[0]
            except:
                img = parsed.xpath('//p//img/@data-canonical-src')[0]

            topic, challenge, answer = (title, img, resolved)

        return (topic, challenge, answer)


    except ValueError as ve:
        print(ve)
        


def _transform_title(title):
    transform_title = title.split('-')
    transform_title = transform_title[0]

    return transform_title




if __name__ == "__main__":
    links()