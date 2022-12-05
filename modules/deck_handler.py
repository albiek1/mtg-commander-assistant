from os import listdir
from os.path import isfile, join
import csv, platform, openpyxl
from csv import writer
from modules import card_handler
import requests

def get_decks():
    files = [f for f in listdir('./decks') if isfile(join('./decks', f))]
    return files

def create_deck(name):
    with open("./decks/"+name+".csv", 'w') as f:
        f.seek(0)
        f.write("name, type_line, mana_cost, cmc, color_identity, category\n")

def begin_deck_construction(name, card_name):
    c = card_handler.get_card_as_list(card_name)
    if(type(c)==str):
        return c
    if(type(c)==list):
        create_deck(name)
        write_to_deck(name, c, "Commander")
        return "Success!"

def return_deck(name):
    with open("./decks/"+name+".txt", 'r') as f:
        return f.read()

def edit_deck(deck, command):
    with open("./decks/"+deck+".txt", 'r+') as f:
        lines = f.readlines()
        c = command[1:]
        if command[0] == "-":
            f.seek(0)
            if c in lines:
                for l in lines:
                    if l != c:
                        f.write(l)
            else:
                return print("that card isn't in the deck, are you sure you spelt the name right?")
        if command[0] == "+":
            if c in lines:
                return print("that card is already in the deck")
            else:
                f.write('\n'+c)
        f.truncate()
        return lines

def clean_empty(deck):
    with open("./decks/"+deck+".txt", 'r+') as f:
        lines = f.readlines()
        print(lines)
        f.seek(0)
        for line in lines:
            if not line.isspace():
                f.write(line)
                print(line.strip())

def write_to_deck(deck, card, sType="Core"):
    with open('./decks/'+deck+'.csv', 'r+') as f:
        reader = csv.reader(f)
        f_writer = csv.writer(f)
        header_row = next(reader)
        for row in reader:
            if row:
                if(row[0]==card[0]):
                    return (card[0]+" is already in the deck")
        print(card)
        card.append(sType)
        f_writer.writerow(card)

def get_average_cmc(deck):
    with open('./decks/'+deck+'.csv', 'r') as f:
        reader = csv.reader(f)
        header_row = next(reader)
        t_cmc = []
        t_row = 0
        for row in reader:
            if row:
                t_cmc.append(float(row[3]))
                t_row += 1
            #t_cmc.append(float(row[3]))
        return sum(t_cmc)/len(t_cmc)

def get_color_breakdown(deck):
    total_W = []
    total_U = []
    total_B = []
    total_R = []
    total_G = []
    with open('./decks/'+deck+'.csv') as f:
        reader = csv.reader(f)
        header_row = next(reader)
        for row in reader:
            if row:
                cost_split = row[2][1:-1].split(', ')
                for c in cost_split:
                    if(c=="'W'"):
                        total_W.append(c)
                    if(c=="'U'"):
                        total_U.append(c)
                    if(c=="'B'"):
                        total_B.append(c)
                    if(c=="'R'"):
                        total_R.append(c)
                    if(c=="'G'"):
                        total_G.append(c)
        return "Deck contains: W:%r, U:%r, B:%r, R:%r, G:%r" % (len(total_W), len(total_U), len(total_B), len(total_R), len(total_G))

def get_mana_curve(deck):
    with open('./decks/'+deck+'.csv') as f:
        reader = csv.reader(f)
        header_row = next(reader)
        for row in reader:
            if row:
                print(row[2])
                tc = []
                if 'W' in row[2]:
                    tc.append('W')
                    if not ('U' in row[2] or 'B' in row[2] or 'R' in row[2] or 'G' in row[2]):
                        print(row[0] + " is white with cmc "+ row[3])
                if 'U' in row[2]:
                    tc.append('U')
                    if not ('W' in row[2] or 'B' in row[2] or 'R' in row[2] or 'G' in row[2]):
                        print(row[0] + " is Blue with cmc " + row[3])
                if 'B' in row[2]:
                    tc.append('B')
                    if not ('W' in row[2] or 'U' in row[2] or 'R' in row[2] or 'G' in row[2]):
                        print(row[0] + " is Black with cmc "+ row[3])
                if 'R' in row[2]:
                    tc.append('R')
                    if not ('W' in row[2] or 'U' in row[2] or 'B' in row[2] or 'G' in row[2]):
                        print(row[0] + " is Red with cmc " + row[3])
                if 'G' in row[2]:
                    tc.append('G')
                    if not ('W' in row[2] or 'U' in row[2] or 'B' in row[2] or 'R' in row[2]):
                        print(row[0] + " is Green with cmc " + row[3])
                if len(row[2]) > 2 and not ('W' in row[2] or 'U' in row[2] or 'B' in row[2] or 'R' in row[2] or 'G' in row[2]):
                    print(row[0] + " is Colorless with cmc " + row[3])
                if (len(tc) >= 2):
                    print(row[0] + " is multicolored with cmc " + row[3])

def get_type_breakdown(deck):
    with open('./decks/'+deck+'.csv') as f:
        reader = csv.reader(f)
        header_row = next(reader)
        land = 0
        instant = 0
        sorcery = 0
        enchantment = 0
        artifact = 0
        planeswalker = 0
        creature = 0
        for row in reader:
            if row:
                if 'Land' in row[1]:
                    land += 1
                if 'Creature' in row[1] and not 'Land' in row[1]:
                    creature += 1
                if 'Planeswalker' in row[1]:
                    planeswalker += 1
                if 'Enchantment' in row[1] and not 'Creature' in row[1]:
                    enchantment += 1
                if 'Artifact' in row[1] and not 'Creature' in row[1]:
                    artifact += 1
                if 'Sorcery' in row[1]:
                    sorcery += 1
                if 'Instant' in row[1]:
                    instant += 1
        print("Land: %r, Creature: %r, Instant: %r, Sorcery: %r, Artifact: %r, Enchantment: %r, Planeswalker: %r" % (land, creature, instant, sorcery, artifact, enchantment, planeswalker))

def get_multi_lands(deck):
    colors = "commander:"+card_handler.get_commander_colors(deck)
    lands = []
    search_str = "-type:snow ("
    if('W' in colors):
        lands.append('type:Plains')
    if('U' in colors):
        lands.append('type:Island')
    if('B' in colors):
        lands.append('type:Swamp')
    if('R' in colors):
        lands.append('type:Mountain')
    if('G' in colors):
        lands.append('type:Forest')
    for land in lands:
        search_str += land+" or "
    search_str = search_str[:-4] + ")"
    legal = "legal:commander"
    return card_handler.pretty_list(card_handler.get_card_list(colors+" "+search_str+" "+legal))

def get_staple_lands(deck):
    colors = card_handler.get_commander_colors(deck)
    results = []
    if (len(colors) >= 2):
        for d in card_handler.get_dual_lands(colors):
            if d:
                results.append(d)
        if (len(colors) >= 3):
            for t in card_handler.get_tri_lands(colors):
                if t:
                    results.append(t)
    return results

def get_avg_ramp(deck):
    with open('./decks/'+deck+'.csv') as f:
        reader = csv.reader(f)
        header_row = next(reader)

def get_meta_ramp(deck):
    colors = card_handler.get_commander_colors(deck)
    ramp_list = card_handler.get_card_list_full("function:ramp legal:commander commander:"+colors)
    meta_list = card_handler.get_archetype_names(deck)
    return [l for l in meta_list if l in ramp_list]

def get_card_draw(deck):
    colors = card_handler.get_commander_colors(deck)
    draw_list = card_handler.get_card_list_full("function:draw legal:commander commander:"+colors)
    meta_list = card_handler.get_archetype_names(deck)
    return [l for l in meta_list if l in draw_list]

def get_targeted_removal(deck):
    colors = card_handler.get_commander_colors(deck)
    removal_list = card_handler.get_card_list_full("function:removal o:target legal:commander commander:"+colors)
    meta_list = card_handler.get_archetype_names(deck)
    return [l for l in meta_list if l in removal_list]

def get_boardwipe(deck):
    colors = card_handler.get_commander_colors(deck)
    wipe_list = card_handler.get_card_list_full('function"board wipe" legal:commander commander:'+colors)
    meta_list = card_handler.get_archetype_names(deck)
    return [l for l in meta_list if l in wipe_list]

def get_tutor(deck):
    colors = card_handler.get_commander_colors(deck)
    tutor_list = card_handler.get_card_list_full("function:tutor legal:commander commander:"+colors)
    meta_list = card_handler.get_archetype_names(deck)
    return [l for l in meta_list if l in tutor_list]

def get_graveyard_recursion(deck):
    colors = card_handler.get_commander_colors(deck)
    return_list = card_handler.get_card_list_full('o:"return target" o:"from your graveyard" legal:commander commander:'+colors)
    meta_list = card_handler.get_archetype_names(deck)
    return [l for l in meta_list if l in return_list]

def convert_to_txt(deck):
    with open('./decks/'+ deck + '.csv') as f:
        reader = csv.reader(f)
        header_row = next(reader)