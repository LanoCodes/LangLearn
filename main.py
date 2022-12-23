from tkinter import *
import pandas as pd
import random
from os.path import exists

BACKGROUND_COLOR = "#B1DDC6"
CURRENT_IDX = 0

if exists("data/words_to_learn.csv"):
    ES_WORDS_DF = pd.read_csv("data/words_to_learn.csv")
else:
    ES_WORDS_DF = pd.read_csv("data/spanish_words.csv")

def gen_card():
    """Generates a new card with Spanish word facing you"""
    lang_change_dict = {
        "text": "Spanish",
        "fill": "black"
    }
    eng_word_change_dict = {
        "text": generate_word(),
        "fill": "black"
    }
    front_card_canv.itemconfig("lang", lang_change_dict)
    front_card_canv.itemconfig("es_word", eng_word_change_dict)
    front_card_canv.itemconfig(card_bg, image=front_card_img)

    window.after(4000, flip_card)


def understood():
    """Removes card from the deck and denerates new card"""
    global ES_WORDS_DF
    test_df = ES_WORDS_DF.drop(CURRENT_IDX)
    ES_WORDS_DF = test_df
    test_df.to_csv("data/words_to_learn.csv", index=False)
    gen_card()


def generate_word():
    """Returns a randomly selected Spanish word"""
    global CURRENT_IDX
    global ES_WORDS_DF

    # Index for a random word from the dataframe
    es_word_idx = random.randint(0, len(ES_WORDS_DF.index))
    CURRENT_IDX = es_word_idx

    # Random spanish word
    rand_es_word = ES_WORDS_DF["Spanish"][es_word_idx]
    return rand_es_word

def flip_card():
    """Shows the translation for the current word to English"""
    front_card_canv.itemconfig(card_bg, image=back_card_img)
    lang_change_dict = {
        "text": "English",
        "fill": "white"
    }
    es_word_change_dict = {
        "text": ES_WORDS_DF["English"][CURRENT_IDX],
        "fill": "white"
    }
    front_card_canv.itemconfig("lang", lang_change_dict)
    front_card_canv.itemconfig("es_word", es_word_change_dict)

# UI Setup
window = Tk()
window.title("LangLearn")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

# Delay timer for execution of card flip
window.after(4000, flip_card)

# Card setup
front_card_canv = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
front_card_img = PhotoImage(file="images/card_front.png")
back_card_img = PhotoImage(file="images/card_back.png")
card_bg = front_card_canv.create_image(400, 263, image=front_card_img)
front_card_canv.grid(row=0, column=0, columnspan=2)
front_card_canv.create_text(400, 150, text="Spanish", font=("Ariel", 40, "italic"),  fill="black", tags="lang")
front_card_canv.create_text(400, 263, text=generate_word(), font=("Ariel", 60, "bold"), fill="black", tags= "es_word")

# wrong button
wrong_img = PhotoImage(file="images/wrong.png")
wrong_btn = Button(image=wrong_img, highlightthickness=0, bd=0, command=gen_card)
wrong_btn.grid(row=1, column=0)
# right button
right_img = PhotoImage(file="images/right.png")
correct_btn = Button(image=right_img, highlightthickness=0, bd=0, command=understood)
correct_btn.grid(row=1, column=1)

window.mainloop()