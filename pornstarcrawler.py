import os
import requests
from bs4 import BeautifulSoup
import re
import concurrent.futures

modelName = input("Enter Model Name: ").replace(" ", "-")

downloaded_unique_links = set()


def download_link(link, folder):
    response = requests.get(link)
    filename = link.split('/')[-1]
    filepath = os.path.join(folder, filename)
    with open(filepath, 'wb') as file:
        file.write(response.content)
        print(f'Downloaded {filename}')


def babesPornExtractor(name):
    set_urls = []
    site_url = 'https://babes.porn'
    url = f'{site_url}/pics/{name}'
    html_response = requests.get(url)

    for tag in BeautifulSoup(html_response.text, 'html.parser').findAll('a', href=re.compile('^/photos/')):
        half_link = tag['href']
        set_urls.append(site_url + half_link)

    for urls in set_urls:
        image_url = []
        set_html = requests.get(urls)
        for tag in BeautifulSoup(set_html.text, 'html.parser').findAll('img',
                                                                       src=re.compile('^//pics.jjgirls.com/pictures/'),
                                                                       alt='thumb'):
            if tag:
                image_url.append(('https:' + tag['src']).replace("hd-", ""))
            else:
                print("No Image Found")
        print(f'Image Links Fetched: {urls}')
        sub_dir_name = urls.split('/')[-1]

        if len(image_url) == 0:
            print("No Images Found")
        else:
            if not os.path.exists(f'./{name}/{sub_dir_name}'):
                print("No Existing Directory Found.")
                print(f'Creating New Directory for {name}/{sub_dir_name}')
                os.makedirs(f'./{name}/{sub_dir_name}')

            with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
                executor.map(lambda link: download_link(link, f'./{name}/{sub_dir_name}'), list(set(image_url)))


def babesSourceExtractor(name):
    model_html_page = ""
    site_url = 'https://babesource.com'
    first_char = name[0]
    search = f'{site_url}/pornstars/?letter={first_char}'
    html_response = requests.get(search)
    for tag in BeautifulSoup(html_response.text, 'html.parser').findAll('a', class_="pornstars-lists__link",
                                                                        href=re.compile(
                                                                            f'^{site_url}/pornstars/{name}')):
        model_html_page = tag['href']

    if model_html_page == "":
        print("Model Not Found")
    else:
        s5 = f'{model_html_page}page1.html'
        r = requests.get(s5)
        pages = []
        for tag in BeautifulSoup(r.text, 'html.parser').findAll('a', class_="paginations__link",
                                                                href=re.compile('^page')):
            pages.append(tag['href'])
        try:
            total_pages = (pages[-1].replace("page", "")).replace(".html", "")
        except:
            total_pages = 1

        gallery_urls = []
        for i in range(1, int(total_pages) + 1):
            model_gallery_html = requests.get(f'{model_html_page}page{i}.html')
            for tag in BeautifulSoup(model_gallery_html.text, 'html.parser').findAll('a',
                                                                                     class_="main-content__card-link",
                                                                                     href=re.compile(
                                                                                         '^https://babesource.com/galleries/')):
                gallery_urls.append(tag['href'])

        for url in gallery_urls:
            image_url = []
            gallery_html_response = requests.get(url)
            for tag in BeautifulSoup(gallery_html_response.text, 'html.parser').findAll('a',
                                                                                        class_="box-massage__card-link",
                                                                                        href=re.compile(
                                                                                            '^https://media.babesource.com/galleries/')):
                image_url.append(tag['href'])
            print(f'Image Links Fetched: {url}')
            sub_dir_name = url.split('/')[-1].replace('.html', '')
            if not os.path.exists(f'./{name}/{sub_dir_name}'):
                print("No Existing Directory Found.")
                print(f'Creating New Directory for {name}/{sub_dir_name}')
                os.makedirs(f'./{name}/{sub_dir_name}')
            with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
                executor.map(lambda link: download_link(link, f'./{name}/{sub_dir_name}'), list(set(image_url)))

def pornPicturesHqExtractor():
    site_url='https://www.pornpictureshq.com'
    

def main(name):
    try:
        babesPornExtractor(name)
    except:
        print("Error While Fetching Links from Babes Porn")

    try:
        babesSourceExtractor(name)
    except:
        print("Error While Fetching Links from Babes Source")


if __name__ == "__main__":
    main(modelName)
