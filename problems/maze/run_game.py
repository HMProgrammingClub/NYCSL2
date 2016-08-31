import socket, json

# Directions
NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

# Tile states
UNKNOWN = 0
EMPTY = 1 # transparent
WALL = 2 # opaque
GLASS = 3 # transparent
GOAL = 4 # transparent
PLAYER = 5

class Point:
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y

class Map:
    def __init__(self, width, height, seed):
        self.contents = []
        self.visibility = []
        for y in range(0, height):
            contents_row = []
            visibility_row = []
            for x in range(0, width):
                contents_row.append(EMPTY) # Full of empty squares to start.
                visibility_row.append(True)
            self.contents.append(contents_row)
            self.visibility.append(visibility_row)
        self.contents[0][0] = PLAYER

    def make_move(self, dir):
        player_loc = None
        for y in range(0, len(self.contents)):
            for x in range(0, len(self.contents[0])):
                if self.contents[y][x] == PLAYER:
                    player_loc = (x, y)
                    self.contents[y][x] = EMPTY
        if dir == NORTH and player_loc[1] != 0 and (self.contents[player_loc[1]-1][player_loc[0]] == EMPTY or self.contents[player_loc[1]-1][player_loc[0]] == GOAL):
            player_loc = (player_loc[0], player_loc[1]-1)
        elif dir == EAST and player_loc[0] != len(self.contents[0])-1 and (self.contents[player_loc[1]][player_loc[0]+1] == EMPTY or self.contents[player_loc[1]][player_loc[0]+1] == GOAL):
            player_loc = (player_loc[0]+1, player_loc[1])
        elif dir == SOUTH and player_loc[1] != len(self.contents)-1 and (self.contents[player_loc[1]+1][player_loc[0]] == EMPTY or self.contents[player_loc[1]+1][player_loc[0]] == GOAL):
            player_loc = (player_loc[0], player_loc[1]+1)
        elif dir == WEST and player_loc[0] != 0 and (self.contents[player_loc[1]][player_loc[0]-1] == EMPTY or self.contents[player_loc[1]][player_loc[0]-1] == GOAL):
            player_loc = (player_loc[0]-1, player_loc[1])
        if self.contents[player_loc[1]][player_loc[0]] == GOAL:
            return True
        self.contents[player_loc[1]][player_loc[0]] = PLAYER
        return False

    def update_visibility(self):
        x=0

    def serialize(self):
        grid = []
        for y in range(0, len(self.contents)):
            row = []
            for x in range(0, len(self.contents[0])):
                if self.visibility[y][x]:
                    row.append(self.contents[y][x])
                else:
                    row.append(UNKNOWN)
            grid.append(row)
        return json.dumps(grid)

m = Map(5, 5, 0)
m.make_move(SOUTH)
print(m.serialize())
