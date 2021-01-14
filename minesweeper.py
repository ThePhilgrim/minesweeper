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
