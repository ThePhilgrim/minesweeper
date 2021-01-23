import pathlib
import random
import tkinter
import datetime
from tkinter import ttk
from tkinter import PhotoImage


class Game:
    def __init__(self, rounded_percentage, width, height):
        self.width = width
        self.height = height
        self.how_many_mines_user_wants = rounded_percentage
        self.mine_locations = []
        self.previously_clicked_square = []
        self.flag_dict = {}
        self.game_over = False

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

    def open_squares(self, x, y):
        if x not in range(self.width) or y not in range(self.height):
            # Happens when auto-opening at edge buttons
            return

        coordinate = (x, y)

        if coordinate in self.previously_clicked_square:
            return

        if coordinate in self.flag_dict:
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
        if (
            count_already_open + count_mine_locations == self.width * self.height
            and coordinate not in self.mine_locations
        ):

            frames = [
                PhotoImage(
                    file=where_this_file_is / "doomguy.gif",
                    format="gif -index %i" % (i),
                )
                for i in range(8)
            ]
            gif_label.place(relx=0.5, rely=0.5, anchor="center")

            def update(index):
                frame = frames[index]
                index += 1
                if index >= 8:
                    index = 0
                gif_label.configure(image=frame)
                if self is current_game:
                    # New game not started yet, can keep animating
                    root.after(100, update, index)

            root.after(0, update, 0)

        if coordinate in self.mine_locations:
            statusbar_action.config(text=f"BOOOOOOOOOOM! {random.choice(fail_message)}")
            self.game_over = True
            canvas.create_image(
                int(x * button_size),
                int(y * button_size),
                image=bomb_image,
                anchor="nw",
            )
        else:
            statusbar_action.config(text=f"{random.choice(live_message)}")
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
        if self is current_game and self.game_over == False:
            statusbar_time.config(text=self.game_time.strftime("%M:%S"))
            self.game_time += datetime.timedelta(seconds=1)
            root.after(1000, self.timer)

    def generate_random_mine_locations(self, where_user_clicked):
        """Generates mine locations across the board after the user
        clicks the first square"""
        while len(self.mine_locations) < self.how_many_mines_user_wants:
            x = random.randrange(self.width)
            y = random.randrange(self.height)
            if (x, y) != where_user_clicked and (x, y) not in self.mine_locations:
                self.mine_locations.append((x, y))


def clicked_square(event):
    """Takes click events and prints number of adjacent mines,
    or generates bomb_image"""
    if not current_game.game_over:
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
    if not current_game.game_over:
        x_flag = int(event.x / button_size)
        y_flag = int(event.y / button_size)
        if (x_flag, y_flag) in current_game.previously_clicked_square:
            return
        elif (x_flag, y_flag) in current_game.flag_dict.keys():
            canvas.delete(current_game.flag_dict[x_flag, y_flag])
            current_game.flag_dict.pop((x_flag, y_flag))
            statusbar_count[
                "text"
            ] = f"{current_game.how_many_mines_user_wants - len(current_game.flag_dict)} mines left"
        else:
            flag_id = canvas.create_image(
                int(event.x / button_size) * button_size + (button_size / 2),
                int(event.y / button_size) * button_size + (button_size / 2),
                image=flag_image,
                anchor="center",
            )
            current_game.flag_dict[(x_flag, y_flag)] = flag_id
            statusbar_count[
                "text"
            ] = f"{current_game.how_many_mines_user_wants - len(current_game.flag_dict)} mines left"


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


live_message = [
    "You're alive.. for now !",
    "You think you're smart, huh?",
    "Great.. now what?",
    "There's no mine in the top right corner! Promise!",
    "Wait, why are there even mines everywhere??",
    "Feeling lucky, punk?",
]
fail_message = [
    "Sorry bud, lost a couple of limbs there ..",
    "Aww, so unlucky! You almost didn't step on it!",
    "Ouch, that must've hurt..",
    "Dance, bitch!",
    "Happy birthday!",
    "Hasta la vista.. baby!",
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
            top_10_times.insert(index, converted_to_seconds) # HOW DO I GET THE INDEX OF "TIME" IN FOR LOOP?
        elif converted_to_seconds < time and len(top_10_times >= 10):
            top_10_times.remove(top_10_times[-1])
            top_10_times.insert(index, converted_to_seconds) # SAME AS ABOVE

def quit_game():
    root.destroy()


def new_game():
    canvas.delete("all")

    height = int(height_slider.scale.get())
    width = int(width_slider.scale.get())

    slider_value = difficulty_slider_callback()
    percentage = (width * height / 100) * slider_value
    rounded_percentage = round(percentage)

    global current_game
    current_game = Game(rounded_percentage, width, height)

    gif_label.place_forget()
    current_game.game_time = datetime.datetime(2021, 1, 1)
    current_game.timer()
    canvas["width"] = button_size * current_game.width
    canvas["height"] = button_size * current_game.height

    for x in range(0, button_size * current_game.width, button_size):
        for y in range(0, button_size * current_game.height, button_size):
            canvas.create_image((x, y), image=button_image, anchor="nw")
    statusbar_action["text"] = "***Lets go!***"
    statusbar_count["text"] = f"{current_game.how_many_mines_user_wants} mines left"

statusbar_frame = ttk.Frame(big_frame, padding=2, relief='sunken')
statusbar_frame.pack(side="bottom", fill='x')

statusbar_time = ttk.Label(statusbar_frame, anchor='w', width='15')
statusbar_time.pack(padx='5', side='left')

statusbar_action = ttk.Label(statusbar_frame, anchor='center')
statusbar_action.pack(side='left', fill='x', expand=True)

statusbar_count = ttk.Label(statusbar_frame, anchor='e', width='15')
statusbar_count.pack(padx='15', side='left', fill='x')

sidebar = ttk.Frame(top_frame, borderwidth=2)
sidebar.pack(side="right", fill="both", anchor="w")

new_game_button = ttk.Button(sidebar, text="New Game", command=new_game)
new_game_button.pack(fill="x", pady=10)

sidebar_height_text = ttk.Label(sidebar, text="Board Height:")
sidebar_height_text.pack(pady=[40, 0])

height_slider = ttk.LabeledScale(sidebar, from_=5, to=35)
height_slider.value = 10
height_slider.pack(padx=5)

sidebar_width_text = ttk.Label(sidebar, text="Board Width:")
sidebar_width_text.pack(pady=[10, 0])

width_slider = ttk.LabeledScale(sidebar, from_=5, to=55)
width_slider.value = 15
width_slider.pack(padx=5)

sidebar_percentage_text = ttk.Label(sidebar, text="Mine Percentage:")
sidebar_percentage_text.pack(pady=[40, 0])

sidebar_difficulty_text = ttk.Label(sidebar, text="Easy")
sidebar_difficulty_text.pack()

def difficulty_slider_callback(*args):
    if int(slider_variable.get()) <= 10:
        sidebar_difficulty_text["text"]="Easy"
    elif int(slider_variable.get()) <= 20:
        sidebar_difficulty_text["text"]="Medium"
    elif int(slider_variable.get()) <= 35:
        sidebar_difficulty_text["text"]="Hard"
    else:
        sidebar_difficulty_text["text"]="HELL!"
    return slider_variable.get()

slider_variable = tkinter.IntVar()
slider_variable.trace_variable('w', difficulty_slider_callback)

difficulty_slider = ttk.LabeledScale(sidebar, from_=5, to=50, variable=slider_variable)
difficulty_slider.value = 15
difficulty_slider.pack(padx=5)








quit_game_button = ttk.Button(sidebar, text="Quit game", command=quit_game)
quit_game_button.pack(fill="x", side="bottom", pady=10)

new_game()
print(ttk)
root.title("Minesweeper – by Arrinao, The Philgrim, and Master Akuli")
root.mainloop()
