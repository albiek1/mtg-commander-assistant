import customtkinter as ctk
from os import listdir
from modules import deck_handler, card_handler

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

decklist = []
#if(len(decklist)==0):
#    print("decklist is empty")

class App(ctk.CTk):
    def __init__(self):
        decklist = [f for f in listdir('./decks/') if f.endswith('.csv')]
        super().__init__()
        self.title("MTG Commander Assistant")
        self.geometry(f"{1100}x{580}")

        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.tabbox = ctk.CTkFrame(self, width=250)
        self.tabbox.grid(row=0, column=1, sticky='nswe')
        self.tabview = ctk.CTkTabview(self.tabbox)
        self.tabview.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky='nsew')
        self.tabview.add("Deck Tab")
        self.tabview.add("Get Recomendations")

        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky='nsew')
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.option_menu = ctk.CTkOptionMenu(self.sidebar_frame, dynamic_resizing=False, values=decklist, command=self.deck_text)
        self.option_menu.grid(row=1, column=0, padx=20, pady=10)
        self.create_deck_button = ctk.CTkButton(self.sidebar_frame, text="Add new deck", command=self.button_pressed_event)
        self.create_deck_button.grid(row=2, column=0, padx=20, pady=10)

        self.midframe = ctk.CTkFrame(self.tabview.tab("Deck Tab"), width=400)
        self.midframe.grid(row=0, column=1)
        self.textbox = ctk.CTkTextbox(self.midframe, width=400)
        self.textbox.grid(row=0, column=1, padx=(20, 20), pady=(20, 0), sticky='nsew')
        
        self.resframe = ctk.CTkFrame(self.tabview.tab("Deck Tab"), width=400)
        self.resframe.grid(row=0, column=2)

        self.subframe = ctk.CTkFrame(self.resframe, width=400)
        self.subframe.grid(row=0, column=2)
        self.search_button = ctk.CTkButton(self.subframe, text="search", command=self.search_button_event)
        self.search_button.grid(row=0, column=2)
        self.cardsearch = ctk.CTkEntry(self.subframe, placeholder_text="Please enter full name")
        self.cardsearch.grid(row=0, column=1)

        self.resbox = ctk.CTkTextbox(self.resframe, width=400)
        self.resbox.grid(row=1, column=2)

        self.btn_box = ctk.CTkFrame(self.resframe, width=400)
        self.btn_box.grid(row=2, column=2)
        self.add_btn = ctk.CTkButton(self.btn_box, text="Hell yeah!", command=self.add_card_button)
        self.add_btn.grid(row=0, column=0)

        self.recFrame = ctk.CTkFrame(self.tabview.tab("Get Recomendations"))
        self.recFrame.grid(row=1, column=2, sticky='nswe')
        self.rec_text = ctk.CTkTextbox(self.recFrame, width=500)
        self.rec_text.grid(row=0, column=0)

        self.rec_select = ctk.CTkFrame(self.tabview.tab("Get Recomendations"))
        self.rec_select.grid(row=1, column=1)

        self.rec_ramp = ctk.CTkButton(self.rec_select, text="rec ramp", command=self.get_rec_ramp)
        self.rec_ramp.grid(row=0, column=0)
        self.rec_draw = ctk.CTkButton(self.rec_select, text="rec draw", command=self.get_rec_draw)
        self.rec_draw.grid(row=1, column=0)
        self.rec_removal = ctk.CTkButton(self.rec_select,  text="rec removal", command=self.get_rec_removal)
        self.rec_removal.grid(row=2, column=0)
        self.rec_wipe = ctk.CTkButton(self.rec_select, text="rec boardwipe", command=self.get_rec_wipe)
        self.rec_wipe.grid(row=3, column=0)
        self.rec_tutor = ctk.CTkButton(self.rec_select, text="rec tutor", command=self.get_rec_tutor)
        self.rec_tutor.grid(row=4, column=0)
        self.rec_recursion = ctk.CTkButton(self.rec_select, text="rec recursion", command=self.get_rec_recursion)
        self.rec_recursion.grid(row=5, column=0)

        self.warn_label = ctk.CTkLabel(self.tabview.tab("Get Recomendations"), text="These actions may take up to 30sec for big opperations, please be patient!")
        self.warn_label.grid(row=2, column=2)
        
        #self.tabview.add("Tab 3")

        #self.label_tab1 = ctk.CTkLabel(self.tabview.tab("Tab 1"), text="This is tab 1")
        #self.label_tab1.grid(column=0, row=0, padx=20, pady=(10, 10))
        #self.label_tab2 = ctk.CTkLabel(self.tabview.tab("Tab 2"), text="This is tab 2")
        #self.label_tab2.grid(column=0, row=0, padx=20, pady=(10, 10))
        #self.label_tab3 = ctk.CTkLabel(self.tabview.tab("Tab 3"), text="This is tab 3")
        #self.label_tab3.grid(column=0, row=0, padx=20, pady=(10, 10))

        self.textbox.insert("0.0", deck_handler.return_deck(self.option_menu.get()))

    def button_pressed_event(self):
        dialog = ctk.CTkInputDialog(text="Enter Deck Name", title="Create new deck")
        if(dialog.get()!=""):
            deck_handler.create_deck(dialog.get_input())
            self.option_menu.configure(values=[f for f in listdir('./decks/') if f.endswith('.csv')])
    
    def deck_text(self, dummy): #the dummy value does nothing but prevent an error :/
        self.textbox.delete("0.0", "end")
        self.textbox.insert("0.0", deck_handler.return_deck(self.option_menu.get()))

    def search_button_event(self):
        if(self.cardsearch.get()==""):
            self.resbox.delete("0.0", "end")
            self.resbox.insert("0.0", "oops, looks like the search box is empty!")
        else:
            self.resbox.delete("0.0", "end")
            self.resbox.insert("0.0", str(card_handler.get_card_as_list(self.cardsearch.get()))+"\n\n"+str(card_handler.get_effect_text(self.cardsearch.get())))
            self.resbox.insert("end", "\n\nThis look good?")

    def add_card_button(self):
        if(self.resbox.get("0.0", "end") == ""):
            self.resbox.insert("end", "\n\nTheres no card to add :/")
        else: #yeah this is probs super buggy, gonna fix this later :/
            deck_handler.write_to_deck(self.option_menu.get(), card_handler.get_card_as_list(self.cardsearch.get()))
            self.textbox.delete("0.0", "end")
            self.textbox.insert("0.0", deck_handler.return_deck(self.option_menu.get()))
    
    def get_rec_ramp(self):
        self.rec_text.delete("0.0", "end")
        self.rec_text.insert("0.0", deck_handler.get_meta_ramp(self.option_menu.get()))
    
    def get_rec_draw(self):
        self.rec_text.delete("0.0", "end")
        self.rec_text.insert("0.0", deck_handler.get_card_draw(self.option_menu.get()))

    def get_rec_removal(self):
        self.rec_text.delete("0.0", "end")
        self.rec_text.insert("0.0", deck_handler.get_targeted_removal(self.option_menu.get()))

    def get_rec_wipe(self):
        self.rec_text.delete("0.0", "end")
        self.rec_text.insert("0.0", deck_handler.get_boardwipe(self.option_menu.get()))

    def get_rec_tutor(self):
        self.rec_text.delete("0.0", "end")
        self.rec_text.insert("0.0", deck_handler.get_tutor(self.option_menu.get()))

    def get_rec_recursion(self):
        self.rec_text.delete("0.0", "end")
        self.rec_text.insert("0.0", deck_handler.get_graveyard_recursion(self.option_menu.get()))

if __name__ == "__main__":
    app = App()
    app.mainloop()