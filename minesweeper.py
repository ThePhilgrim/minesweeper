import pathlib
import random
import tkinter
from tkinter import ttk
from tkinter import PhotoImage

width = 21
height = width

how_many_mines_user_wants = 150

mine_locations = []


def generate_random_mine_locations(where_user_clicked, how_many_mines_user_wants):
    """ Generates mine locations across the board after the user
    clicks the first square """
    while len(mine_locations) < how_many_mines_user_wants:
        x = random.randrange(width)
        y = random.randrange(height)
        if (x, y) != where_user_clicked and (x, y) not in mine_locations:
            mine_locations.append((x, y))


root = tkinter.Tk()
root.resizable(False, False)
big_frame = ttk.Frame(root)
big_frame.pack(fill = 'both', expand = True)


canvas = tkinter.Canvas(big_frame, width=25*width, height=25*height, bg='black')
canvas.pack(fill='both', expand=True)

where_this_file_is = pathlib.Path(__file__).parent
button_image = PhotoImage(file=(where_this_file_is / 'button_small.png'))

for x in (range(0, 21*25, 25)):
    for y in (range(0, 21*25, 25)):
        canvas.create_image((x, y), image=button_image)

root.title("Minesweeper – by Arrinao, The Philgrim, and Master Akuli")
root.mainloop()

def mines_around_square(mine_locations, clicked_square):
    """ Looks at the squares adjacent to current_square and counts
        how many mines there are """
    adjacent_mines = 0
    for mine in mine_locations:
        if ((mine[0] == clicked_square[0] -1 or
             mine[0] == clicked_square[0] +1) and
            (mine[1] == clicked_square[1] or
             mine[1] == clicked_square[1] -1 or
             mine[1] == clicked_square[1] +1)):
            adjacent_mines += 1
        elif ((mine[1] == clicked_square[1] -1 or
               mine[1] == clicked_square[1] +1) and
              (mine[0] == clicked_square[0] or
               mine[0] == clicked_square[0] -1 or
               mine[0] == clicked_square[0] +1)):
            adjacent_mines += 1
    return adjacent_mines

### Test for function mines_around_square
# mine_locations = [(2,3), (3,3), (4,3), (2,4), (4,4), (2,5), (3,5), (4,5)]
# print(mines_around_square(mine_locations, (3,4)))   # should be 8

def user_clicked_square(x, y):
    """ Defines what happens when the user clicks on a square. """
    if len(mine_locations) == 0:
        generate_random_mine_locations((0,0), how_many_mines_user_wants)
    clicked_square = (x, y)
    live_message = ["You're alive.. for now !", "You think you're smart, huh?",
    "Great.. now what?", "There's no mine in the top right corner! Promise!",
    "Wait, why are there even mines everywhere??", "Feeling lucky, punk?"]
    fail_message = ["Sorry bud, lost a couple of limbs there ..",
    "Aww, so unlucky! You almost didn't step on it!",
    "Ouch, that must've hurt..", "Dance, bitch!", "Happy birthday!",
    "Hasta la vista.. baby!"]
    if clicked_square in mine_locations:
        print("BOOOOOOOOOOOOOOOOOOOOOM\n")
        print(random.choice(fail_message))
    else:
        # TODO: add code to make button look like it's pressed down
        # TODO: show mines_around_square number in the button
        mines_around_square(mine_locations, clicked_square)
        print(random.choice(live_message))
# Should return adjacent_mines, but it's not defined (scope error). Need help
# to solve it. Would like to keep adjacent_mines inside mines_around_square function.

user_clicked_square(3, 8)
