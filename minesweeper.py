import random
import tkinter
from tkinter import ttk

width = 21
height = width

def generate_random_mine_locations(where_user_clicked, how_many_mines_user_wants):
    """ Generates mine locations across the board after the user
    clicks the first square """
    mine_locations = []
    while len(mine_locations) < how_many_mines_user_wants:
        x = random.randrange(width)
        y = random.randrange(height)
        if (x, y) != where_user_clicked and (x, y) not in mine_locations:
            mine_locations.append((x, y))
    return mine_locations

root = tkinter.Tk()
root.resizable(False, False)
big_frame = ttk.Frame(root)
big_frame.pack(fill = 'both', expand = True)

def check_if_theres_mine():
    if mine == True:
        print('BOOOOM!')
    elif mine == False:
        mines_around_square()
    

for x in (range(width)):
    for y in (range(height)):
        button = ttk.Button(big_frame, width = 3)
        button.state(['pressed'])
        button.grid(row = y, column = x, sticky = 'nswe')

root.title("Minesweeper – by Arrinao, The Philgrim, and Master Akuli")
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


