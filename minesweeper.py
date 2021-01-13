import random

width = 10
height = width

def generate_random_mine_locations(where_user_clicked, how_many_mines_user_wants):
    mine_locations = []
    while len(mine_locations) < how_many_mines_user_wants:
        x = random.randrange(WIDTH)
        y = random.randrange(HEIGHT)
        if (x, y) != where_user_clicked and (x, y) not in mine_locations:
            mine_locations.append((x, y))
    return mine_locations
