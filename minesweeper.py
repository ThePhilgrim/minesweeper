import pathlib
import random
import tkinter
from tkinter import ttk
from tkinter import PhotoImage

class Game:

    def __init__(self):
        self.width = 21
        self.height = 21
        self.how_many_mines_user_wants = 50
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

        count_already_open=len(self.previously_clicked_square)
        count_mine_locations=len(self.mine_locations)
        if count_already_open + count_mine_locations == self.width*self.height and coordinate not in self.mine_locations:
            frames = [PhotoImage(file=where_this_file_is / 'doomguy.gif', format = 'gif -index %i' %(i)) for i in range(8)]
            gif_label.place(relx=0.5, rely=0.5, anchor='center')

            def update(index):
                frame = frames[index]
                index += 1
                if index>=8:
                    index = 0                
                gif_label.configure(image=frame)
                if self is current_game:     # TODO: this check is ugly, get rid of it
                    # New game not started yet, can keep animating
                    root.after(100, update, index)
            root.after(0, update, 0)   

        if coordinate in self.mine_locations:
            statusbar_action.config(text=f"BOOOOOOOOOOM! {random.choice(fail_message)}")
            self.game_over = True
            canvas.create_image(
                int(x * button_size), int(y * button_size), image=bomb_image, anchor="nw"
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

    def generate_random_mine_locations(self, where_user_clicked):
        """Generates mine locations across the board after the user
        clicks the first square"""
        while len(self.mine_locations) < self.how_many_mines_user_wants:
            x = random.randrange(self.width)
            y = random.randrange(self.height)
            if (x, y) != where_user_clicked and (x, y) not in self.mine_locations:
                self.mine_locations.append((x, y))
                
        

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

def clicked_square(event):
    """Takes click events and prints number of adjacent mines,
    or generates bomb_image"""
    if  not current_game.game_over:
        x = int(event.x / button_size)
        y = int(event.y / button_size)
        coordinate = (x, y)

        if len(current_game.mine_locations) == 0:
            current_game.generate_random_mine_locations(coordinate)

        current_game.open_squares(x, y)


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
            statusbar_count['text']=(current_game.how_many_mines_user_wants - len(current_game.flag_dict))
        else:
            flag_id = canvas.create_image(
                int(event.x / button_size) * button_size + (button_size / 2),
                int(event.y / button_size) * button_size + (button_size / 2),
                image=flag_image,
                anchor="center",
            )
            current_game.flag_dict[(x_flag, y_flag)] = flag_id
            statusbar_count['text']=(current_game.how_many_mines_user_wants - len(current_game.flag_dict))

canvas = tkinter.Canvas(
    top_frame,
    highlightthickness=0,
    bg="black",
)
canvas.pack(fill="both", expand=True, side='left')
canvas.bind("<Button-1>", clicked_square)
canvas.bind("<Button-2>", flagging)  # Mac
canvas.bind("<Button-3>", flagging)  # Windows, Linux

gif_label = ttk.Label(canvas, background='black', text='Congratulations!', compound='top', font='Helvetica 20', foreground='orange')

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

def quit_game():
    root.destroy()


def new_game():
    canvas.delete('all')
    global current_game
    current_game = Game()

    gif_label.place_forget()
    canvas['width']=button_size * current_game.width
    canvas['height']=button_size * current_game.height

    for x in range(0, button_size * current_game.width, button_size):
        for y in range(0, button_size * current_game.height, button_size):
            canvas.create_image((x, y), image=button_image, anchor="nw")
    statusbar_action['text'] = '***Lets go!***'
    statusbar_count['text'] = current_game.how_many_mines_user_wants



statusbar_action = ttk.Label(
    big_frame, anchor="w", relief="sunken"
)
statusbar_action.pack(side="bottom", fill='x')

statusbar_count = ttk.Label(
    statusbar_action, anchor='s', relief='sunken', width='13' 
    )
statusbar_count.pack(side='right', fill='x')

sidebar = ttk.Frame(
    top_frame, width=100, borderwidth=2,
)
sidebar.pack(side="right", fill="both", anchor="w",)
new_game_button = ttk.Button(sidebar, text='New Game', command=new_game)
options_button = ttk.Button(sidebar, text='Options')
quit_game_button = ttk.Button(sidebar, text="Quit game", command=quit_game)
new_game_button.pack()
options_button.pack()
quit_game_button.pack()

new_game()

root.title("Minesweeper – by Arrinao, The Philgrim, and Master Akuli")
root.mainloop()
