from tkinter import *
import pandas as pd
import random
import time

# -------------------- CONSTANTS -----------------------
BACKGROUND_COLOR = "#B1DDC6"
TITLE_COR = (400, 150)
WORD_COR = (400, 263)
TITLE_FONT = ("Ariel", 40, "italic")
WORD_FONT = ("Ariel", 60, "bold")
rand_pair = None


# -------------------- APP MECHANISM --------------------
def random_pair():
    canvas.itemconfig(flash_card, image=front_flash_img)
    rand_pair = random.choice(data_dict)
    canvas.itemconfig(title_text, text="French")
    canvas.itemconfig(word_text, text=rand_pair["French"])
    return rand_pair


def flip_card(rand_pair):
    canvas.itemconfig(flash_card, image=back_flash_img)
    canvas.itemconfig(title_text, text="English")
    canvas.itemconfig(word_text, text=rand_pair["English"])


def refresh(side):
    global rand_pair
    if rand_pair is not None:
        if side == "R":
            words_to_learn_list.remove(rand_pair)
        data_dict.remove(rand_pair)

    rand_pair = random_pair()
    window.update()
    time.sleep(3)
    flip_card(rand_pair)


def right_btn_click():
    refresh("R")


def wrong_btn_click():
    refresh("W")


# -------------------- DATA ----------------------------------
try:
    df = pd.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    df = pd.read_csv("data/french_words.csv")
    open("data/words_to_learn.csv", mode="w")

data_dict = df.to_dict(orient="records")
words_to_learn_list = data_dict.copy()

# -------------------- UI SETUP ------------------------------

# Window
window = Tk()
window.title("Flash cards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

window.minsize(width=500, height=500)

# Buttons
right_btn_img = PhotoImage(file="images/right.png")
left_btn_img = PhotoImage(file="images/wrong.png")

right_btn = Button(image=right_btn_img, highlightthickness=0, command=right_btn_click)
left_btn = Button(image=left_btn_img, highlightthickness=0, command=wrong_btn_click)

# Canvas
front_flash_img = PhotoImage(file="images/card_front.png")
back_flash_img = PhotoImage(file="images/card_back.png")
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
flash_card = canvas.create_image(400, 268, image=front_flash_img)
title_text = canvas.create_text(TITLE_COR, text="Title", fill="black", font=TITLE_FONT)
word_text = canvas.create_text(WORD_COR, text="Word", fill="black", font=WORD_FONT)
canvas.grid(row=0, column=0, columnspan=2)

left_btn.grid(row=1, column=0)
right_btn.grid(row=1, column=1)

window.mainloop()

df_words_to_learn = pd.DataFrame.from_records(words_to_learn_list)
df_words_to_learn.to_csv("data/words_to_learn.csv")
