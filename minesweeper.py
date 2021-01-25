import pathlib
import random
import tkinter
import datetime
import json
from tkinter import ttk
from tkinter import PhotoImage
from enum import Enum

GameStatus = Enum("GameStatus", "in_progress, game_lost, game_won")
hs_list = []


class Game:
    def __init__(self, mine_count, width, height):
        self.width = width
        self.height = height
        self.how_many_mines_user_wants = mine_count
        self.mine_locations = []
        self.previously_clicked_square = []
        self.flag_dict = {}
        self.game_status = GameStatus.in_progress

    def mines_around_square(self, coordinate):
        """Looks at the squares adjacent to current_square and counts
        how many mines there are"""
        adjacent_mines = 0
        for mine in self.mine_locations:
            if (mine[0] == coordinate[0] - 1 or mine[0] == coordinate[0] + 1) and (
                mine[1] == coordinate[1]
                or mine[1] == coordinate[1] - 1
                or mine[1] == coordinate[1] + 1
            ):
                adjacent_mines += 1
            elif (mine[1] == coordinate[1] - 1 or mine[1] == coordinate[1] + 1) and (
                mine[0] == coordinate[0]
                or mine[0] == coordinate[0] - 1
                or mine[0] == coordinate[0] + 1
            ):
                adjacent_mines += 1
        return adjacent_mines

    def win_animation(self):
        gif_label.place(relx=0.5, rely=0.5, anchor="center")

        def update(index):
            frame = gif_frames[index]
            index += 1
            index %= len(gif_frames)
            gif_label.configure(image=frame)
            if self is current_game:
                # New game not started yet, can keep animating
                root.after(100, update, index)

        root.after(0, update, 0)

    def open_squares(self, x, y):
        if x not in range(self.width) or y not in range(self.height):
            # Happens when auto-opening at edge buttons
            return

        coordinate = (x, y)

        if coordinate in self.previously_clicked_square or coordinate in self.flag_dict:
            return

        self.previously_clicked_square.append((x, y))
        canvas.create_image(
            int(x * button_size),
            int(y * button_size),
            image=button_image_pressed,
            anchor="nw",
        )

        count_already_open = len(self.previously_clicked_square)
        count_mine_locations = len(self.mine_locations)

        if coordinate in self.mine_locations:
            statusbar_action.config(text=f"BOOOOOOOOOOM! {random.choice(fail_message)}")
            self.game_status = GameStatus.game_lost
            canvas.create_image(
                int(x * button_size),
                int(y * button_size),
                image=bomb_image,
                anchor="nw",
            )
        else:
            if count_already_open + count_mine_locations == self.width * self.height:
                self.game_status = GameStatus.game_won
                statusbar_action.config(text=random.choice(win_message))
                self.win_animation()
            else:
                statusbar_action.config(text=random.choice(live_message))
            mine_count = self.mines_around_square(coordinate)
            if mine_count == 0:
                self.open_squares(x - 1, y - 1)
                self.open_squares(x - 1, y)
                self.open_squares(x - 1, y + 1)
                self.open_squares(x, y - 1)
                self.open_squares(x, y + 1)
                self.open_squares(x + 1, y - 1)
                self.open_squares(x + 1, y)
                self.open_squares(x + 1, y + 1)

            if mine_count > 0:
                canvas.create_text(
                    coordinate[0] * button_size + (button_size / 2),
                    coordinate[1] * button_size + (button_size / 2),
                    text=str(mine_count),
                    font=("helvetica", 17, "bold"),
                    fill=color_chart[mine_count],
                )

    def timer(self):
        if self is current_game:
            if self.game_status == GameStatus.in_progress:
                statusbar_time.config(text=self.game_time.strftime("%M:%S"))
                self.game_time += datetime.timedelta(seconds=1)
                root.after(1000, self.timer)
            elif self.game_status == GameStatus.game_won:
                with open("high_scores.json", "w") as high_scores:
                    json.dump(self.game_time.strftime("%M:%S"), high_scores)

    def generate_random_mine_locations(self, where_user_clicked):
        """Generates mine locations across the board after the user
        clicks the first square"""
        while len(self.mine_locations) < self.how_many_mines_user_wants:
            x = random.randrange(self.width)
            y = random.randrange(self.height)
            if (x, y) != where_user_clicked and (x, y) not in self.mine_locations:
                self.mine_locations.append((x, y))

    def update_statusbar_mines_left(self):
        statusbar_count[
            "text"
        ] = f"{self.how_many_mines_user_wants - len(self.flag_dict)} mines left"


def clicked_square(event):
    """Takes click events and prints number of adjacent mines,
    or generates bomb_image"""
    if current_game.game_status == GameStatus.in_progress:
        x = int(event.x / button_size)
        y = int(event.y / button_size)
        coordinate = (x, y)

        if len(current_game.mine_locations) == 0:
            current_game.generate_random_mine_locations(coordinate)
        current_game.open_squares(x, y)


button_size = 23

color_chart = {
    1: "turquoise",
    2: "yellow green",
    3: "yellow",
    4: "gold",
    5: "orange",
    6: "dark orange",
    7: "red2",
    8: "red4",
}

root = tkinter.Tk()
root.resizable(False, False)

big_frame = ttk.Frame(root)
big_frame.pack(fill="both", expand=True)
top_frame = ttk.Frame(big_frame)
top_frame.pack(fill="both", expand=True)


def flagging(event):
    """Takes right click events, and places or removes flag_image.
    Adds placed flag positions with their flag id into a dict."""
    if current_game.game_status == GameStatus.in_progress:
        x_flag = int(event.x / button_size)
        y_flag = int(event.y / button_size)
        if (x_flag, y_flag) in current_game.previously_clicked_square:
            return
        elif (x_flag, y_flag) in current_game.flag_dict.keys():
            canvas.delete(current_game.flag_dict[x_flag, y_flag])
            current_game.flag_dict.pop((x_flag, y_flag))
            current_game.update_statusbar_mines_left()
        else:
            flag_id = canvas.create_image(
                int(event.x / button_size) * button_size + (button_size / 2),
                int(event.y / button_size) * button_size + (button_size / 2),
                image=flag_image,
                anchor="center",
            )
            current_game.flag_dict[(x_flag, y_flag)] = flag_id
            current_game.update_statusbar_mines_left()


canvas = tkinter.Canvas(
    top_frame,
    highlightthickness=0,
    bg="black",
)
canvas.pack(fill="both", expand=True, side="left")
canvas.bind("<Button-1>", clicked_square)
canvas.bind("<Button-2>", flagging)  # Mac
canvas.bind("<Button-3>", flagging)  # Windows, Linux

gif_label = ttk.Label(
    canvas,
    background="black",
    text="Congratulations!",
    compound="top",
    font="Impact 20",
    foreground="sienna3",
)

where_this_file_is = pathlib.Path(__file__).parent
button_image = PhotoImage(file=(where_this_file_is / "button_small.png"))
button_image_pressed = PhotoImage(
    file=(where_this_file_is / "pressed_button_small.png")
)
flag_image = PhotoImage(file=(where_this_file_is / "flag_small.png"))
bomb_image = PhotoImage(file=(where_this_file_is / "bomb_small.png"))
gif_frames = [
    PhotoImage(
        file=where_this_file_is / "doomguy.gif",
        format=f"gif -index {i}",
    )
    for i in range(8)
]


live_message = [
    "You're alive.. for now !",
    "You think you're smart, huh?",
    "Great.. now what?",
    "There's no mine in the top right corner! Promise!",
    "Wait, why are there even mines everywhere??",
    "Feeling lucky, punk?",
    "Why so serious?",
    "Life is like a box of chocolate ...",
    "Nobody puts Baby in a corner.",
]
fail_message = [
    "Sorry bud, lost a couple of limbs there ..",
    "Aww, so unlucky! You almost didn't step on it!",
    "Ouch, that must've hurt..",
    "Dance, bitch!",
    "Happy birthday!",
    "Hasta la vista.. baby!",
    "Houston, we have a problem.",
    "Luca Brasi is sleeping with the fishes.",
    "I love the smell of napalm in the morning.",
    "Say 'hello' to my little friend.",
]
win_message = [
    "I am proud of you, young padawan.",
    "The student has become the master.",
    "The force is strong with this one.",
]

# This is a starting idea of how a high score list could look. For now it only considers time,
# It takes the time, converts it to seconds, and loops through top_10_times to see if the current score
# is lower than a previous time at that index. It will then insert that score to the index of top_10_times.
# # TODO: ADD THE SCORE TO TOP_10_TIMES AS (CONVERTED_TO_SECONDS % 60) TO FORMAT IT IN MINS & SECS.
# # TAKE INTO CONSIDERATION THE DIFFICULTY. EX, 50 MINUTES ON MEDIUM IS HIGHER THAN 10 MINUTES ON EASY.
top_10_times = []


def highscore(mins, secs):
    converted_to_seconds = mins * 60 + secs
    for time in top_10_times:
        if converted_to_seconds < time and len(top_10_times) < 10:
            top_10_times.insert(
                index, converted_to_seconds
            )  # HOW DO I GET THE INDEX OF "TIME" IN FOR LOOP?
        elif converted_to_seconds < time and len(top_10_times >= 10):
            top_10_times.remove(top_10_times[-1])
            top_10_times.insert(index, converted_to_seconds)  # SAME AS ABOVE


def quit_game(event=None):
    root.destroy()


def new_game(event=None):
    canvas.delete("all")

    height = int(height_slider.scale.get())
    width = int(width_slider.scale.get())

    slider_value = slider_variable.get()
    percentage_to_mine_count = (width * height / 100) * slider_value
    mine_count = round(percentage_to_mine_count)

    global current_game
    current_game = Game(mine_count, width, height)

    gif_label.place_forget()
    current_game.game_time = datetime.datetime(2021, 1, 1)
    current_game.timer()
    canvas["width"] = button_size * current_game.width
    canvas["height"] = button_size * current_game.height

    for x in range(0, button_size * current_game.width, button_size):
        for y in range(0, button_size * current_game.height, button_size):
            canvas.create_image((x, y), image=button_image, anchor="nw")
    statusbar_action["text"] = "***Lets go!***"
    current_game.update_statusbar_mines_left()


top_menu = tkinter.Menu(root)
root.config(menu=top_menu)


top_menu_game = tkinter.Menu(top_menu)
if root.tk.call("tk", "windowingsystem") == "aqua":
    top_menu.add_cascade(label="Game", menu=top_menu_game)
    top_menu_game.add_command(label="New Game", accelerator="F2", command=new_game)
    top_menu_game.add_command(label="Quit Game", accelerator="F10", command=quit_game)
else:
    top_menu.add_command(label="New Game", accelerator="F2", command=new_game)
    top_menu.add_command(label="Quit Game", accelerator="F10", command=quit_game)


statusbar_frame = ttk.Frame(big_frame, padding=2, relief="sunken")
statusbar_frame.pack(side="bottom", fill="x")

# Make sure that statusbar is always 2 lines tall
ttk.Label(statusbar_frame, text="\n").pack(side="left")

statusbar_time = ttk.Label(statusbar_frame)
statusbar_time.pack(side="left")

statusbar_action = ttk.Label(statusbar_frame, anchor="center", justify="center")
statusbar_action.pack(side="left", fill="x", expand=True)

statusbar_count = ttk.Label(statusbar_frame)
statusbar_count.pack(side="left", fill="x")

sidebar = ttk.Frame(top_frame, borderwidth=2)
sidebar.pack(side="right", fill="both", anchor="w")

sidebar_height_text = ttk.Label(sidebar, text="Board Height:")
sidebar_height_text.pack(pady=[5, 0])

height_slider = ttk.LabeledScale(sidebar, from_=10, to=35)
height_slider.value = 10
height_slider.pack(padx=5)

sidebar_width_text = ttk.Label(sidebar, text="Board Width:")
sidebar_width_text.pack(pady=[5, 0])

width_slider = ttk.LabeledScale(sidebar, from_=10, to=55)
width_slider.value = 15
width_slider.pack(padx=5)

sidebar_percentage_text = ttk.Label(sidebar, text="Mine Percentage:")
sidebar_percentage_text.pack(pady=[5, 0])

sidebar_difficulty_text = ttk.Label(sidebar, text="Easy")
sidebar_difficulty_text.pack()


def difficulty_slider_callback(*args):
    if slider_variable.get() <= 10:
        sidebar_difficulty_text["text"] = "Easy"
    elif slider_variable.get() <= 20:
        sidebar_difficulty_text["text"] = "Medium"
    elif slider_variable.get() <= 35:
        sidebar_difficulty_text["text"] = "Hard"
    else:
        sidebar_difficulty_text["text"] = "HELL!"


slider_variable = tkinter.IntVar()
slider_variable.trace_variable("w", difficulty_slider_callback)

difficulty_slider = ttk.LabeledScale(sidebar, from_=5, to=50, variable=slider_variable)
difficulty_slider.value = 15
difficulty_slider.pack(padx=5)

# Tkinter's LabeledScale is broken: https://bugs.python.org/issue40219
height_slider.label.lift()
width_slider.label.lift()
difficulty_slider.label.lift()

# Make sure that text in status bar is wrapped correctly
def update_statusbar_wraplength(event):
    statusbar_action["wraplength"] = (
        top_frame.winfo_reqwidth()
        - statusbar_time.winfo_reqwidth()
        - statusbar_count.winfo_reqwidth()
        - 15  # Leave gaps between the status bar labels
    )


root.bind("<Configure>", update_statusbar_wraplength)
root.bind("<F2>", new_game)
root.bind("<F10>", quit_game)

new_game()
root.title("Minesweeper – by Arrinao, The Philgrim, and Master Akuli")
root.iconphoto(False, tkinter.PhotoImage(file=where_this_file_is / "bomb.png"))
root.mainloop()
