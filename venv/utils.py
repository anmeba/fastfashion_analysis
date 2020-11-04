import requests
import pandas as pd
from bs4 import BeautifulSoup
import time
from io import BytesIO
import gzip
import json
import re


def decompressRequestSoup(url):
    """Given an url perform a get request,
    decompress content and inject in soup
    object.

    Args:
    :param url: an url wich returnes compressed
    content

    Return: soup object of the response contents

    """
    r_comp = requests.get(url)
    decomp = gzip.GzipFile(fileobj=BytesIO(r_comp.content))
    soup = BeautifulSoup(decomp.read(), features="html.parser")
    return soup


# decompressRequestSoup(url)

def requestSoup(url):
    """Given an url perform a get request and
    set response in a soup object.

    Args:
    :param url: an url to soup, string.

    Return: soup object of get response

    """
    r = requests.get(url)
    soup = BeautifulSoup(r.content, features="html.parser")
    return soup


# links = soup.find('body').findAll('loc')

def getGeneralLinks(url, country, gender):
    """


    """
    """Get all general clothing urls from web sitemap

    Args:
    :param url: sitemap, string. 
    :param country: pattern string.
    :param gender: pattern string, language depends on
    country pattern.
    
    Return: list of general clothing types urls

    """
    soup = decompressRequestSoup(url)
    links = soup.findAll('loc')
    for link in links:
        href = link.text
        if re.search(country, href) != None:
            time_1 = time.time()
            es_url = href
            es_soup = decompressRequestSoup(es_url)
            es_links = es_soup.findAll('loc')
            es_links_mujer = [link.text for link in es_links
                              if re.search(gender, link.text) != None]
            time_2 = time.time()
            resp_time = time_2 - time_1
            time.sleep(resp_time)

    return es_links_mujer


# getAllLinks(url,country, gender)

# https://stackoverflow.com/questions/33406313/how-to-match-any-string-from-a-list-of-strings-in-regular-expressions-in-python


def selectGeneralType(url, country, gender, item_types):
    """Get general types of clothing filtered url list from
    web sitemap.

    Args:
    ;url: (sitemap)
    ;country: (pattern string)
    ;gender: (pattern string, language depends on
    coutry pattern)
    ;item_types: (list of types of clothing to
    filter).

    Returns: list of general clothing sections urls.

    """
    link_list = getGeneralLinks(url, country, gender)
    pattern = '|'.join(item_types)
    type_links = [link for link in link_list
                  if re.search(pattern, link) != None]
    return type_links


#selectGeneralType(url, country, gender, item_types)


def getItemUrl(url, country, gender, item_types):
    """Given a list of general cloth sections it
     gets the url of each item in each.

    Args:
    :param url: (sitemap)
    :param country: (pattern string)
    :param gender: (pattern string, language depends on
    :param coutry pattern)
    :param item_types: (list of types of clothing to
    filter).

    Retturns: list of items urls.

    """
    gen_urls = selectGeneralType(url, country, gender, item_types)
    for gen_url in gen_urls:
        time_1 = time.time()
        gen_soup = requestSoup(gen_url)
        gen_soup
        time_2 = time.time()
        resp_time = time_2 - time_1
        item_cont = gen_soup.find_all('a', class_="name _item")
        item_urls = [cont.get('href') + '#' for cont in item_cont]  # adding hash to access app content page
        time.sleep(resp_time + 2)

        return item_urls


#len(getItemUrl(url, country, gender, item_types))


def getItemsDataframe(url, country, gender, item_types, keyword_script, output):
    """Given the list of items urls, extract key features (price, composition,
    description) and build a dataset
    :param url: (sitemap)
    :param country: (pattern string)
    :param gender: (pattern string, language depends on
    :param coutry pattern)
    :param item_types: (list of types of clothing to
    filter).
    :param keyword_script: string to match right script
    :param output: limit of items that we want to get
    :return: a dataset with key informaition of every item (price, composition,
    description)
    """
    df_items = pd.DataFrame(columns=['item_code',
                                     'item_name',
                                     'item_desc',
                                     'item_composition_ext',
                                     'item_composition_int',
                                     'item_price'])
    item_urls = getItemUrl(url, country, gender, item_types)
    # hi ha 1091 items de camiseta, aquí treuré nomès els 100 primers items
    i = 0
    while i < output:
        time_1 = time.time()
        item_url = item_urls[i]
        item_code = 100000 + i
        i += 1
        item_script_all = requestSoup(item_url).find_all('script',
                                                         type="text/javascript")  # language-and-stores #"product-detail-others-container _product-detail-others-container"
        time_2 = time.time()
        resp_time = time_2 - time_1
        item_script = [scrpt.text for scrpt in item_script_all if re.search(keyword_script, str(scrpt)) != None]
        for item_app in item_script:
            item_info = item_app[item_app.find(';window.zara.dataLayer ='):].replace(
                ';window.zara.viewPayload = window.zara.dataLayer;', '').replace(';window.zara.dataLayer =', '')
            parsed = json.loads(item_info)
            # print(json.dumps(parsed, indent=4, sort_keys=True))

            ##name
            name = parsed['product']['name']

            ## Descripció
            desc = parsed['product']['detail']['rawDescription']

            ## Preu
            preu = parsed['product']['detail']['colors'][0]['price']

            ## Composició
            compo_ext = parsed['product']['detail']['detailedComposition']['parts'][0]['components']
            try:
                compo_int = parsed['product']['detail']['detailedComposition']['parts'][1]['components']
                new_row = {'item_code': item_code,
                           'item_name': name,
                           'item_desc': desc,
                           'item_composition_ext': compo_ext,
                           'item_composition_int': compo_int,
                           'item_price': preu}
                # append row to the dataframe
                df_items = df_items.append(new_row, ignore_index=True)
                items_json = df_items.to_json(orient='table')
            except IndexError:
                new_row = {'item_code': item_code,
                           'item_name': name,
                           'item_desc': desc,
                           'item_composition_ext': compo_ext,
                           'item_composition_int': "",
                           'item_price': preu}
                # append row to the dataframe
                df_items = df_items.append(new_row, ignore_index=True)
                items_json = df_items.to_json(orient='table')

            '''
            intento separar el que es el material i el que es el percentatge
            compo_int = parsed['product']['detail']['detailedComposition']['parts'][1]['components'][0]['material']
            '''

            # append row to the dataframe
            # df_items = df_items.append(new_row, ignore_index=True)
            # items_json = df_items.to_json(orient='table')

    return df_items