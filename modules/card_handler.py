import requests
import csv
import time
import re
import bs4
import math

def get_card_list(search):
    r = requests.get('https://api.scryfall.com/cards/search?q='+search)
    time.sleep(0.1)
    return r.json()['data']

def get_card_list_full(search):
    r = requests.get('https://api.scryfall.com/cards/search?q='+search)
    time.sleep(0.1)
    full_list = [l['name'] for l in r.json()['data']]
    n_pages = math.ceil(r.json()['total_cards']/175)
    for n in range(0, n_pages):
        if(r.json()['has_more']):
            r = requests.get(r.json()['next_page'])
            time.sleep(0.1)
            for c in r.json()['data']:
                full_list.append(c['name'])
    return full_list

def get_search_page(n_page):
    r = requests.get(n_page)
    time.sleep(0.1)
    return r.json()['data'], r.json()['has_more']

def pretty_list(list):
    for card in list:
        print(("Card: %r, %r, %r, %r, %r") % (list.index(card), card['name'], card['mana_cost'], card['type_line'], card['oracle_text']))

def get_name(list, n):
    return list[n]['name']

def get_set(name):
    set = ""
    n = get_card_list(name)[0]['set_name'].split(' ')
    for s in n:
        set += s+"+"
    return set[:-1]

def get_archetype(deck):
    name = ""
    with open('./decks/'+deck+'.csv') as f:
        reader = csv.reader(f)
        header_row = next(reader)
        name = next(reader)[0]
    n= ""
    pattern = re.compile('[\W_]+')
    for s in name.split(' '):
        n += pattern.sub('', s)+"-"
    r = requests.get('https://www.mtggoldfish.com/archetype/'+n[:-1]+'#paper')
    time.sleep(0.1)
    r.raise_for_status()
    soup = bs4.BeautifulSoup(r.text, 'html.parser')
    creature_arr = []
    planeswalker_arr = []
    spells_arr = []
    artifact_arr = []
    enchantment_arr = []
    land_arr = []
    for title in soup.select('div[class=spoiler-card-container] > h3'):
        for sibling in title.next_siblings:
            temp = [t for t in sibling.getText().split('\n') if not t=='']
            if temp:
                if(title.getText()=='Creatures'):
                    creature_arr.append([temp[0], temp[-1][-12:-10]])
                if(title.getText()=='Planeswalkers'):
                    planeswalker_arr.append([temp[0], temp[-1][-12:-10]])
                if(title.getText()=='Spells'):
                    spells_arr.append([temp[0], temp[-1][-12:-10]])
                if(title.getText()=='Artifacts'):
                    artifact_arr.append([temp[0], temp[-1][-12:-10]])
                if(title.getText()=='Enchantments'):
                    enchantment_arr.append([temp[0], temp[-1][-12:-10]])
                if(title.getText()=='Lands'):
                    land_arr.append([temp[0], temp[-1][-12:-10]])
    return creature_arr[1:], planeswalker_arr, spells_arr, artifact_arr, enchantment_arr, land_arr

def get_archetype_names(deck):
    name = ""
    with open('./decks/'+deck+'.csv') as f:
        reader = csv.reader(f)
        header_row = next(reader)
        name = next(reader)[0]
    n = ""
    pattern = re.compile('[\W_]+')
    for s in name.split(' '):
        n += pattern.sub('', s)+'-'
    r = requests.get('https://www.mtggoldfish.com/archetype/'+n[:-1]+'#paper')
    time.sleep(0.1)
    r.raise_for_status()
    soup = bs4.BeautifulSoup(r.text, 'html.parser')
    full_arr = []
    for title in soup.select('div[class=spoiler-card-container] > h3'):
        for sibling in title.next_siblings:
            temp = [t for t in sibling.getText().split('\n') if not t=='']
            if temp:
                full_arr.append(temp[0])
    return full_arr

def get_card_as_list(name):
    r = requests.get('https://api.scryfall.com/cards/search?q=!"'+name+'"')
    time.sleep(0.1)
    if(r.json()['total_cards']==0):
        return "no cards were found. check spelling and punctuation"
    if (r.json()['total_cards'] > 1):
        return "oops, the chosen name has more than one card. Please refine search and try again"
    if(r.json()['total_cards']==1):
        card = r.json()['data'][0]
        if card['mana_cost']:
            mana_cost = [l[:-1] for l in card['mana_cost'].split('{')]
            return [card['name'], card['type_line'], str(mana_cost[1:]), card['cmc'], str(card['color_identity'])]
        else:
            return "card got no mana cost, gonna fix this at not 4:AM"

def get_effect_text(name):
    r = requests.get('https://api.scryfall.com/cards/search?q=!"'+name+'"')
    time.sleep(0.1)
    return r.json()['data'][0]['oracle_text'].split('\n')

def get_commander_colors(deck):
    with open('./decks/'+deck+'.csv', 'r') as f:
        reader = csv.reader(f)
        header_row = next(reader)
        for row in reader:
            if (row[5]=="Commander"):
                result = ""
                if('W' in row[4]):
                    result += 'W'
                if('U' in row[4]):
                    result += 'U'
                if('B' in row[4]):
                    result += 'B'
                if('R' in row[4]):
                    result += 'R'
                if('G' in row[4]):
                    result += 'G'
                return result

def get_dual_lands(colors):
    results = [pretty_list(get_card_list("commander:"+colors+" (is:dual or is:shockland)"))]
    return results[:-1]

def get_tri_lands(colors):
    results = [pretty_list(get_card_list("commander:"+colors+" type:land o:"+'"cycling {3}"'))]
    return results[:-1]