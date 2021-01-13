def generate_random_mine_locations(where_user_clicked, how_many_mines_user_wants):
    mine_locations = []
    while len(mine_locations) < how_many_mines_user_wants:
        x = random.randint(0, WIDTH - 1)
        y = random.randint(0, HEIGHT - 1)
        if (x, y) != where_user_clicked and (x, y) not in mine_locations:
            mine_locations.append((x, y))
    return mine_locations
