"""
Webs scraping functions used to gather information about publications, web
pages and categories from Wikipedia.
"""

import requests
import bs4
from collections import deque

def pub_info(pub_id):
    """
    Return the title of a publication with a given pub_id
    
    Parameters
    ----------
    pub_id: tuple (str, str)
            publication id type (doi, isbn, ...) and number

    Returns
    -------
    link: str
          link to a web page with publication information
    title: str
           publication title or 'N/A' if not available
    """

    # urls for publications with different types of ids
    urls = {'doi':'https://doi.org/',
            'doi2':'https://doi.org/',
            'arxiv':'https://arxiv.org/abs/',
            #'isbn':'https://isbnsearch.org/isbn/',
            'isbn2':'https://www.google.com/search?tbm=bks&q=isbn+',
            'isbn': 'https://books.google.com/books?isbn=', #0195154797
            'pmid':'https://www.ncbi.nlm.nih.gov/pubmed/',
            'pmc':'https://'
           }
    
    link = urls[pub_id[0]] + pub_id[1]

    selector = {'doi':'header h1',#[itemprop="name headline"]',
                'doi2':'header h1',
                'arxiv':'h1', 
                #'isbn':'#search > .g > .rc > h3',
                'isbn':'h1',
                'isbn2':'h3 > a[href=]',
                'pmid':'.rprt_all h1',
                'pmc':'h1'
               }

    # try to find the title of a publication; if not successful, return N/A.
    title = ''
    try:
        #print('link', link)
        r = requests.get(link, allow_redirects=True)
        try:
            soup = bs4.BeautifulSoup(r.text, 'html.parser')
            if pub_id[0] == 'arxiv':
                title = soup.select(selector[pub_id[0]])[-1].get_text()
            elif pub_id[0] == 'isbn':
                title = soup.select(selector[pub_id[0]])[0].get_text()
            elif pub_id[0] == 'doi':
                title = soup.select(selector[pub_id[0]])[0].get_text()
            elif pub_id[0] == 'pmid':
                title = soup.select(selector[pub_id[0]])[0].get_text()
            else:
                title = soup.select(selector[pub_id[0]])[0].get_text()
        except:
            if pub_id[0] == 'isbn':
                # another try for ISBN directly search google
                link = urls[pub_id[0]+'2'] + pub_id[1]
                try:
                    r = requests.get(link, allow_redirects=True)
                    soup = bs4.BeautifulSoup(r.text, 'html.parser')
                    tags = soup.select('h3.r > a[href*="books.google.com"]')
                    title = tags[0].get_text()
                    links_new = tags[0].get('href')
                    if len(lings_new) > 0:
                        link = lins_new[0]
                except:
                    title = 'N/A'
            elif pub_id[0] == 'doi':
                # another try for DOI
                link = urls[pub_id[0]+'2'] + pub_id[1]
                try:
                    r = requests.get(link, allow_redirects=True)
                    soup = bs4.BeautifulSoup(r.text, 'html.parser')
                    tags = soup.select('h1')
                    #print('h1 tags num (doi)', len(tags))
                    #print("LINK TAGS", link, tags)
                    title = tags[0].get_text()
                    #link = tags[0].get('href')
                except:
                    title = 'N/A'
            else:
                    title = 'N/A'

    except requests.exceptions.RequestException:
        title = 'N/A'

    title = title.replace('Title:', '').lstrip()
    
    return link, title

def get_cats(address):
    """
    Accept a wiki page element and return a list of category elements found on the page.
    Parameters
    ----------
    address: str
             Address of a wikipedia web page (without the wiki_url base)
    Returns
    -------
    cats: List of BeautifulSoup tag objects
          Contains (not-hidden) category information for subsequent processing   
    """

    wiki_url = 'http://en.wikipedia.org'

    r = requests.get(wiki_url+address)

    soup = bs4.BeautifulSoup(r.text, 'html.parser')
    
    cats = soup.select('#mw-normal-catlinks ul li a')

    return cats 

def get_cat_children(cat_name):
    """
    Obtains wikipedia articles that are children of a given category
    
    Parameters
    ----------
    cat_name: str
              Category name
              
    Returns
    -------
    article_list: list of Beautiful tag objects
    """
    
    cat_tree = 'https://en.wikipedia.org/wiki/Special:CategoryTree'
    cat_name = cat_name.replace(' ','+')
    query = '?target=' + cat_name + '&mode=all&namespaces=0&title=Special%3ACategoryTree'
    
    r = requests.get(cat_tree+query)
    
    soup = bs4.BeautifulSoup(r.text, 'html.parser')
    
    article_list = soup.find_all('a', {'class':'CategoryTreeLabelPage'})
    
    return article_list

