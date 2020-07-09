import requests
from time import sleep
from tqdm import tqdm
import json

base_url = f'https://api.nytimes.com/svc/search/v2/articlesearch.json?q=election&api-key={api_key}=section_name:("SECTION_NAME")&page=PAGE' 

section_names = ['Arts', 'Business', 'Sports', 'World', 'Paid Death Notices']

def main():
    articles = []
    for section_name in section_names:
        for i in tqdm(range(50)):
            url = base_url.replace('SECTION_NAME', section_name).replace('PAGE', str(i + 1))
            sleep(5)
            res =  requests.get(url)
            if not res.ok:
                print(res.text)
                continue
            articles += res.json()['response']['docs']

    with open('articles.json', 'w') as f:
        f.write(json.dumps(articles, indent=4))


if __name__ == '__main__':
    main()
