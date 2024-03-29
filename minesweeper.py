import pathlib
import random
import tkinter
import time
import json
import sys
from tkinter import ttk
from enum import Enum
from appdirs import AppDirs

try:
    # When an end user is running the app or exe created with pyinstaller,
    # sys._MEIPASS is the path to where images are, as a string.
    image_dir = pathlib.Path(sys._MEIPASS)
except AttributeError:
    # When a developer runs this program without pyinstaller, there is no
    # sys._MEIPASS attribute, and we need to find the images based on where
    # this file is.
    image_dir = pathlib.Path(__file__).parent / "images"

config_dir = pathlib.Path(AppDirs("Minesweeper").user_config_dir)

# Recursion limit is increased to prevent Recursion error from
# auto-opening open_squares in open_squares ()
sys.setrecursionlimit(2000)

GameStatus = Enum("GameStatus", "in_progress, game_lost, game_won")
try:
    with open(config_dir / "game_data.json", "r") as source:
        json_dict = json.load(source)
except FileNotFoundError:
    json_dict = {
        "width_slider": 15,
        "height_slider": 10,
        "difficulty_slider": 15,
        "high_scores": [],  # list of dicts with keys: 'time', 'width', 'height', 'mine_count'
    }


class Game:
    def __init__(self, mine_count, width, height):
        self.width = width
        self.height = height
        self.mine_count = mine_count
        self.mine_locations = []
        self.previously_clicked_square = set()
        self.flag_dict = {}
        self.game_status = GameStatus.in_progress
        self.start_time = time.time()

    def mines_around_square(self, coordinate):
        """Looks at the squares adjacent to current_square and counts
        how many mines there are"""
        adjacent_mines = 0
        x, y = coordinate
        for mine in self.mine_locations:
            if (
                mine == (x, y - 1)
                or mine == (x, y + 1)
                or mine == (x - 1, y)
                or mine == (x - 1, y - 1)
                or mine == (x - 1, y + 1)
                or mine == (x + 1, y)
                or mine == (x + 1, y - 1)
                or mine == (x + 1, y + 1)
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
                root.after(90, update, index)

        root.after(0, update, 0)

    def open_squares(self, x, y):
        if x not in range(self.width) or y not in range(self.height):
            # Happens when auto-opening at edge buttons
            return

        coordinate = (x, y)

        if coordinate in self.previously_clicked_square or coordinate in self.flag_dict:
            return

        self.previously_clicked_square.add((x, y))

        if coordinate in self.mine_locations:
            draw_image(x, y, red_button_image_pressed)
        else:
            draw_image(x, y, button_image_pressed)

        count_already_open = len(self.previously_clicked_square)
        count_mine_locations = len(self.mine_locations)

        if coordinate in self.mine_locations:
            statusbar_action.config(text=f"BOOOOOOOOOOM! {random.choice(fail_message)}")
            self.game_status = GameStatus.game_lost

            # Shows user all mines when losing
            for x, y in self.mine_locations:
                if (x, y) not in self.flag_dict:
                    if (x, y) not in self.previously_clicked_square:
                        draw_image(x, y, button_image_pressed)
                    draw_image(x, y, bomb_image)
            for x, y in self.flag_dict:
                if (x, y) not in self.mine_locations:
                    draw_image(x, y, wrong_flag_image)

        else:
            if count_already_open + count_mine_locations == self.width * self.height:
                self.game_status = GameStatus.game_won
                json_dict["high_scores"].append(
                    {
                        "time": time.time() - self.start_time,
                        "width": self.width,
                        "height": self.height,
                        "mine_count": self.mine_count,
                    }
                )
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
        if self is current_game and self.game_status == GameStatus.in_progress:
            game_time = time.time() - self.start_time
            statusbar_time.config(text=f"{int(game_time / 60):02d}:{int(game_time % 60):02d}")
            root.after(1000, self.timer)

    def generate_random_mine_locations(self, where_user_clicked):
        """Generates mine locations across the board after the user
        clicks the first square"""
        while len(self.mine_locations) < self.mine_count:
            x = random.randrange(self.width)
            y = random.randrange(self.height)
            if (x, y) != where_user_clicked and (x, y) not in self.mine_locations:
                self.mine_locations.append((x, y))

    def update_statusbar_mines_left(self):
        """Prints out how many mines are left"""
        statusbar_count["text"] = f"{self.mine_count - len(self.flag_dict)} mines left"


def draw_image(x, y, image):
    if image == flag_image or image == wrong_flag_image:
        return canvas.create_image(
            x * button_size + (button_size / 2),
            y * button_size + (button_size / 2),
            image=image,
            anchor="center",
        )
    else:
        return canvas.create_image(x * button_size, y * button_size, image=image, anchor="nw")


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
            canvas.delete(current_game.flag_dict.pop((x_flag, y_flag)))
        else:
            flag_id = draw_image(x_flag, y_flag, flag_image)
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

button_image = tkinter.PhotoImage(file=(image_dir / "button_small.png"))
button_image_pressed = tkinter.PhotoImage(file=(image_dir / "pressed_button_small.png"))
red_button_image_pressed = tkinter.PhotoImage(file=(image_dir / "pressed_red_button_small.png"))
flag_image = tkinter.PhotoImage(file=(image_dir / "flag_small.png"))
wrong_flag_image = tkinter.PhotoImage(file=(image_dir / "wrong_flag_small.png"))
bomb_image = tkinter.PhotoImage(file=(image_dir / "bomb_small.png"))
gif_frames = [
    tkinter.PhotoImage(
        file=image_dir / "doomguy.gif",
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


def save_json_file():
    json_dict["height_slider"] = int(height_slider.scale.get())
    json_dict["width_slider"] = int(width_slider.scale.get())
    json_dict["difficulty_slider"] = int(difficulty_slider.scale.get())
    config_dir.mkdir(exist_ok=True, parents=True)
    with open(config_dir / "game_data.json", "w") as file:
        json.dump(json_dict, file)


def quit_game(event=None):
    save_json_file()
    root.destroy()


highscore_window = None


def create_highscores_window(event=None):
    global highscore_window
    if highscore_window is not None and highscore_window.winfo_exists():
        highscore_window.lift()
        return
    highscore_window = tkinter.Toplevel()
    highscore_window.resizable(False, False)
    highscore_window.title("High Scores")
    frame = ttk.Frame(highscore_window)
    frame.pack(fill="both", expand=True)

    treeview = ttk.Treeview(frame)

    # Define columns
    treeview["columns"] = ("Mine Percentage", "Board Size", "Time per Square", "Total Time")

    # Format columns
    treeview.column("#0", width=0, stretch="NO")
    treeview.column("Mine Percentage", anchor="w", width=140, minwidth=140)
    treeview.column("Board Size", anchor="w", width=140, minwidth=140)
    treeview.column("Time per Square", anchor="w", width=175, minwidth=175)
    treeview.column("Total Time", anchor="w", width=120, minwidth=120)

    # Create headings
    treeview.heading("#0", text="", anchor="w")
    treeview.heading("Mine Percentage", text="Mine Percentage", anchor="w")
    treeview.heading("Board Size", text="Board Size", anchor="w")
    treeview.heading("Time per Square", text="Avg. Time per Square", anchor="w")
    treeview.heading("Total Time", text="Total Time", anchor="w")

    def get_highscore_data(highscore_dict):
        return (-get_mine_percentage(highscore_dict), get_avg_time(highscore_dict))

    def get_mine_percentage(highscore_dict):
        return round(
            highscore_dict["mine_count"]
            / (highscore_dict["width"] * highscore_dict["height"])
            * 100
        )

    def get_board_size(highscore_dict):
        return f"{highscore_dict['width']} x {highscore_dict['height']}"

    def get_avg_time(highscore_dict):
        return round(
            highscore_dict["time"] / (highscore_dict["width"] * highscore_dict["height"]), 2
        )

    for highscore_dict in sorted(json_dict["high_scores"], key=get_highscore_data):
        seconds = int(highscore_dict["time"])
        if seconds >= 60:
            format_time = f"{int(seconds / 60)} min & {seconds % 60} sec"
        else:
            format_time = f"{seconds} sec"
        treeview.insert(
            parent="",
            index="end",
            values=(
                (f"{get_mine_percentage(highscore_dict)} %"),
                get_board_size(highscore_dict),
                (f"{get_avg_time(highscore_dict)} sec"),
                format_time,
            ),
        )

    treeview.pack()


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
    current_game.timer()
    canvas["width"] = button_size * current_game.width
    canvas["height"] = button_size * current_game.height

    for x in range(current_game.width):
        for y in range(current_game.height):
            draw_image(x, y, image=button_image)
    statusbar_action["text"] = "***Lets go!***"
    current_game.update_statusbar_mines_left()


top_menu = tkinter.Menu(root)
root.config(menu=top_menu)

top_menu_game = tkinter.Menu(top_menu)
if root.tk.call("tk", "windowingsystem") == "aqua":
    top_menu.add_cascade(label="Game", menu=top_menu_game)
    top_menu_game.add_command(label="New Game", accelerator="F2", command=new_game)
    top_menu_game.add_command(
        label="High Scores", accelerator="F6", command=create_highscores_window
    )
    top_menu_game.add_command(label="Quit Game", accelerator="F10", command=quit_game)
else:
    top_menu.add_command(label="New Game", accelerator="F2", command=new_game)
    top_menu.add_command(label="High Scores", accelerator="F6", command=create_highscores_window)
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
height_slider.value = json_dict["height_slider"]
height_slider.pack(padx=5)

sidebar_width_text = ttk.Label(sidebar, text="Board Width:")
sidebar_width_text.pack(pady=[5, 0])

width_slider = ttk.LabeledScale(sidebar, from_=10, to=55)
width_slider.value = json_dict["width_slider"]
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
difficulty_slider.value = json_dict["difficulty_slider"]
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
root.bind("<F6>", create_highscores_window)
root.bind("<F10>", quit_game)

new_game()
root.title("Minesweeper – by Arrinao, The Philgrim, and Master Akuli")
root.iconphoto(False, tkinter.PhotoImage(file=image_dir / "bomb.png"))

root.protocol("WM_DELETE_WINDOW", quit_game)
root.mainloop()
