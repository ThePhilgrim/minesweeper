import random

width = 5
height = width

def generate_random_mine_locations(where_user_clicked, how_many_mines_user_wants):
    mine_locations = []
    while len(mine_locations) < how_many_mines_user_wants:
        x = random.randrange(WIDTH)
        y = random.randrange(HEIGHT)
        if (x, y) != where_user_clicked and (x, y) not in mine_locations:
            mine_locations.append((x, y))
    return mine_locations

import tkinter
from tkinter import ttk


root = tkinter.Tk()
root.resizable(False, False)
big_frame = ttk.Frame(root)
big_frame.pack(fill='both', expand=True)

# None means that we'll create the button later

for y, row in enumerate(range(0, 21)):
    for x, character in enumerate(range(0, 21)):
        if character is not None:
            # try this without width=3 so you'll know why i put it there
            button = ttk.Button(big_frame, text=character, width=3)
            button.grid(row=y, column=x, sticky='nswe')

# the widths of these buttons are set to smallest possible values because grid
# will make sure that they are wide enough, e.g. zerobutton is below '1' and
# '2', and it will have the same width as the '1' and '2' buttons together


# let's make everything stretch when the window is resized
for x in range(20):
    big_frame.grid_columnconfigure(x, weight=1)
for y in range(20):
    big_frame.grid_rowconfigure(y, weight=1)

root.title("Calculator")
root.mainloop()

def mines_around_square(mine_locations, current_square):
    """ Looks at the squares adjacent to current_square and counts
        how many mines there are """
    adjacent_mines = 0
    for mine in mine_locations:
        if ((mine[0] == current_square[0] -1 or
             mine[0] == current_square[0] +1) and
            (mine[1] == current_square[1] or
             mine[1] == current_square[1] -1 or
             mine[1] == current_square[1] +1)):
            adjacent_mines += 1
        elif ((mine[1] == current_square[1] -1 or
               mine[1] == current_square[1] +1) and
              (mine[0] == current_square[0] or
               mine[0] == current_square[0] -1 or
               mine[0] == current_square[0] +1)):
            adjacent_mines += 1
    return adjacent_mines

### Test for function mines_around_square
# mine_locations = [(2,3), (3,3), (4,3), (2,4), (4,4), (2,5), (3,5), (4,5)]
# print(mines_around_square(mine_locations, (3,4)))   # should be 8
