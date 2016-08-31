import socket, json

UNKNOWN = 0
EMPTY = 1
WALL = 2
GOAL = 3
PLAYER = 4

class Map:
    def __init__(self, width, height, seed):
        self.contents = []
        for y in range(0, height):
            row = []
            for x in range(0, width):
                row.append((EMPTY, False)) # Full of empty yet unseen squares.
            self.contents.append(row)
    def serialize(self):
        grid = []
        for y in range(0, len(self.contents)):
            row = []
            for x in range(0, len(self.contents[0])):
                if self.contents[y][x][1]:
                    row.append(self.contents[y][x][0])
                else:
                    row.append(UNKNOWN)
            grid.append(row)
        return json.dumps(grid)

m = Map(5, 5, 0)
print(m.serialize())
