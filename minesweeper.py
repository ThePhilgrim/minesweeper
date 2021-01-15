import pathlib
import random
import tkinter
from tkinter import ttk
from tkinter import PhotoImage

width = 21
height = width
button_size = 25

how_many_mines_user_wants = 120

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

def clicked_square(event):
    print(event.__dict__)
    x = int(event.x / 25)
    y = int(event.y / 25)
    coordinate = (x, y)

    if len(mine_locations) == 0:
        generate_random_mine_locations(coordinate, how_many_mines_user_wants)

    canvas.create_image(int(event.x / 25)*25, int(event.y / 25)*25, image=button_image_pressed, anchor='nw')
    print(f'x = {int(event.x / 25)} y = {int(event.y / 25)}')

    if coordinate in mine_locations:
        statusbar.config(text=f"BOOOOOOOOOOM! {random.choice(fail_message)}")
        canvas.create_image(int(event.x / 25)*25, int(event.y / 25)*25, image=bomb_image, anchor='nw')

    else:
        statusbar.config(text=f"{random.choice(live_message)}")
        mine_count = mines_around_square(mine_locations, coordinate)

#        canvas.create_text((coordinate[0] * 25 + 12.5),
#        (coordinate[1] * 25 + 12.5), text=(str(mines_around_square(mine_locations, clicked_square))))

        canvas.create_text(coordinate[0] * 25 + 12.5,
        coordinate[1] * 25 + 12.5, text = str(mine_count))

def flagging(event):
    print(event.__dict__)
    #flag_coordinates = []
    #x_flag = int(event.x / 25) * 25
    #y_flag = int(event.y / 25) * 25
    print('RIGHT CLICK')
    #canvas.create_image(int(event.x / 25)*25, int(event.y / 25)*25, image=flag_image, anchor='center')


canvas = tkinter.Canvas(big_frame, width=25*width, height=25*height, highlightthickness=0, bg='black')
canvas.pack(fill='both', expand=True)
canvas.bind('<Button-1>', clicked_square)
canvas.bind('<Button-2>', flagging)
canvas.bind('<Button-3>', flagging)


where_this_file_is = pathlib.Path(__file__).parent
button_image = PhotoImage(file=(where_this_file_is / 'button_small.png'))
button_image_pressed = PhotoImage(file=(where_this_file_is / 'pressed_button_small.png'))
flag_image = PhotoImage(file=(where_this_file_is / 'flag_small.png'))
bomb_image = PhotoImage(file=(where_this_file_is / 'bomb_small.png'))


for x in range(0, button_size*width, button_size):
    for y in (range(0, button_size*height, button_size)):
        canvas.create_image((x, y), image=button_image, anchor='nw')

live_message = ["You're alive.. for now !", "You think you're smart, huh?",
    "Great.. now what?", "There's no mine in the top right corner! Promise!",
    "Wait, why are there even mines everywhere??", "Feeling lucky, punk?"]
fail_message = ["Sorry bud, lost a couple of limbs there ..",
    "Aww, so unlucky! You almost didn't step on it!",
    "Ouch, that must've hurt..", "Dance, bitch!", "Happy birthday!",
    "Hasta la vista.. baby!"]


statusbar=tkinter.Label(root, bd=1, text='***Lets go!***', relief=tkinter.SUNKEN, anchor=tkinter.W)
statusbar.pack(side=tkinter.BOTTOM, fill=tkinter.X)

def mines_around_square(mine_locations, coordinate):
    """ Looks at the squares adjacent to current_square and counts
        how many mines there are """
    adjacent_mines = 0
    for mine in mine_locations:
        if ((mine[0] == coordinate[0] -1 or
             mine[0] == coordinate[0] +1) and
            (mine[1] == coordinate[1] or
             mine[1] == coordinate[1] -1 or
             mine[1] == coordinate[1] +1)):
            adjacent_mines += 1
        elif ((mine[1] == coordinate[1] -1 or
               mine[1] == coordinate[1] +1) and
              (mine[0] == coordinate[0] or
               mine[0] == coordinate[0] -1 or
               mine[0] == coordinate[0] +1)):
            adjacent_mines += 1
    return adjacent_mines

### Test for function mines_around_square
# mine_locations = [(2,3), (3,3), (4,3), (2,4), (4,4), (2,5), (3,5), (4,5)]
# print(mines_around_square(mine_locations, (3,4)))   # should be 8

root.title("Minesweeper – by Arrinao, The Philgrim, and Master Akuli")
root.mainloop()
