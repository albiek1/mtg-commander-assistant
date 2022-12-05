import bs4
import requests

def get_card_list(search):
    r = requests.get('https://api.scryfall.com/cards/search?q='+search)
    return r.json()

def get_commander_colors(search):
    r = requests.get('https://api.scryfall.com/cards/search?q='+search)
    if(r.json()['total_cards']!=1):
        return "more than one card found, please refine search"
    return r.json()['data'][0]['colors']

def get_commander_name(search):
    r = requests.get('https://api.scryfall.com/cards/search?q='+search)
    if(r.json()['total_cards']!=1):
        return "more than one card found, please refine search"
    return r.json()['data'][0]['name']

def get_card_text(url):
    r = requests.get(url)
    soup = bs4.BeautifulSoup(r.text, 'html.parser')
    return soup

def card_to_obj(url):
    r = get_card_text(url)  
    name = r.select('span[class="card-text-card-name"]')[0].getText()
    return name

#def get_card_by_name(name):