# mtg-commander-assistant
 Project name: MTG Commander Assistant

 Project Description:
 This is a program to help new Magic players to get into commander format. Utilizing both scryfall for card data and mtggoldfish for meta picks, this is designed to help you skip the boring card picks so you can get to trying out the fun cards.

List of used technologies:
customtkinter / tkinter, requests, csv and math

Installation Guide:
I think just customtkinter?
So run "pip install customtkinter" in the terminal?

User guide:
There is an unfinished and slightly broken tutorial with examples in "main_file.ipynb", however running "mtg_guiMain.py" will open a seperate window with interactable GUI. Theres also some more unfinished guide in "Introduction.txt"

Status:
Getting cards from mtggoldfish and scryfall all work, as well as getting the full list as scryfall caps the length of card lists to 175. Various analysis functions work as well as the hypergeometric formula for getting mana and ramp ratios.
The aformentioned formula could do with improving as it currently does not optimize towards a goal and will just give an answer.
The functions in the GUI all work and buttons update correctly (as far as I know).

Many functions work however have not been implimented into the GUI, such as the deck breakdown functions. Honestly, some of these would not take too long to add, however I have simply not had the time.
Some functions need fixing since I changed to using .csv instead of .txt. This is a mostly quick fix.
Needs much, much more exception handling, however it has been mostly done and there shouldn't be many errors during runtime.
Some webscraping functions are not optimized as best as they can be, however I did try to make minimal use of requests for speed.

Challenges:
I wanted to make extensive use of webscraping for different sites and implement a GUI solution for best user interactivity.
I then wanted to use and process the data into something easier for a human to read and be able to give recomendations based on data collected from other people.