import socket, json, collections, time, sys

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

# The following class and functions are for testing visibility.
class Point:
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y
    def __repr__(self):
        return '(' + str(self.x) + ', ' + str(self.y) + ')'
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    def __key(self):
        return (self.x, self.y)
    def __hash__(self):
        return hash(self.__key())
def get_orientation(p1, p2, p3):
    val = (p2.y - p1.y) * (p3.x - p2.x) - (p2.x - p1.x) * (p3.y - p2.y)
    if val == 0: return 0
    if val > 0: return 1
    return -1
def col_is_on_seg(p1, p2, test):
    return test.x >= min(p1.x, p2.x) and test.x <= max(p1.x, p2.x) and test.y >= min(p1.y, p2.y) and test.y <= max(p1.y, p2.y)
def does_intersect(l1, l2):
    o1 = get_orientation(l1[0], l1[1], l2[0])
    o2 = get_orientation(l1[0], l1[1], l2[1])
    o3 = get_orientation(l2[0], l2[1], l1[0])
    o4 = get_orientation(l2[0], l2[1], l1[1])
    if o1 != o2 and o3 != o4: return True
    if o1 == 0 and col_is_on_seg(l1[0], l1[1], l2[0]): return True
    if o2 == 0 and col_is_on_seg(l1[0], l1[1], l2[1]): return True
    if o3 == 0 and col_is_on_seg(l2[0], l2[1], l1[0]): return True
    if o4 == 0 and col_is_on_seg(l2[0], l2[1], l1[1]): return True
    return False

class Map:
    def __init__(self, width, height, seed):
        self.height = height
        self.width = width
        self.contents = []
        self.visibility = []
        for y in range(0, self.height):
            contents_row = []
            visibility_row = []
            for x in range(0, self.width):
                contents_row.append(EMPTY) # Full of empty squares to start.
                visibility_row.append(False)
            self.contents.append(contents_row)
            self.visibility.append(visibility_row)
        self.contents[0][0] = PLAYER
        self.player_loc = (0, 0)
        self.opaque_walls = [] # We'll use these for finding what walls are opaque.
        # We'll also assume that every square is 1x1, as it doesn't matter.
        self.contents[2][2] = WALL # for testing
        self.contents[2][3] = WALL # for testing
        for y in range(0, self.height):
            for x in range(0, self.width):
                if self.contents[y][x] == WALL:
                    self.opaque_walls.append((Point(x, y), Point(x, y+1)))
                    self.opaque_walls.append((Point(x, y), Point(x+1, y)))
                    self.opaque_walls.append((Point(x+1, y), Point(x+1, y+1)))
                    self.opaque_walls.append((Point(x, y+1), Point(x+1, y+1)))
        self.opaque_walls = set(self.opaque_walls)
    def make_move(self, dir):
        self.contents[self.player_loc[1]][self.player_loc[0]] = EMPTY
        if dir == NORTH and self.player_loc[1] != 0 and (self.contents[self.player_loc[1]-1][self.player_loc[0]] == EMPTY or self.contents[self.player_loc[1]-1][self.player_loc[0]] == GOAL):
            self.player_loc = (self.player_loc[0], self.player_loc[1]-1)
        elif dir == EAST and self.player_loc[0] != self.width-1 and (self.contents[self.player_loc[1]][self.player_loc[0]+1] == EMPTY or self.contents[self.player_loc[1]][self.player_loc[0]+1] == GOAL):
            self.player_loc = (self.player_loc[0]+1, self.player_loc[1])
        elif dir == SOUTH and self.player_loc[1] != self.height-1 and (self.contents[self.player_loc[1]+1][self.player_loc[0]] == EMPTY or self.contents[self.player_loc[1]+1][self.player_loc[0]] == GOAL):
            self.player_loc = (self.player_loc[0], self.player_loc[1]+1)
        elif dir == WEST and self.player_loc[0] != 0 and (self.contents[self.player_loc[1]][self.player_loc[0]-1] == EMPTY or self.contents[self.player_loc[1]][self.player_loc[0]-1] == GOAL):
            self.player_loc = (self.player_loc[0]-1, self.player_loc[1])
        if self.contents[self.player_loc[1]][self.player_loc[0]] == GOAL: return True
        self.contents[self.player_loc[1]][self.player_loc[0]] = PLAYER
        return False
    def get_neighbors(self, loc):
        neighbors = []
        if loc[1] != 0: neighbors.append((loc[0], loc[1]-1))
        if loc[0] != self.width-1: neighbors.append((loc[0]+1, loc[1]))
        if loc[1] != self.height-1: neighbors.append((loc[0], loc[1]+1))
        if loc[0] != 0: neighbors.append((loc[0]-1, loc[1]))
        return neighbors
    def test_visible(self, loc):
        corners = [ Point(loc[0], loc[1]),Point(loc[0]+1, loc[1]),Point(loc[0], loc[1]+1),Point(loc[0]+1, loc[1]+1) ]
        center = Point(self.player_loc[0]+0.5, self.player_loc[1]+0.5)
        for p in corners:
            is_good = True
            for wall in self.opaque_walls:
                if wall[0] == p or wall[1] == p:
                    continue
                if does_intersect(wall, (p, center)):
                    is_good = False
                    break
            if is_good:
                return True
        return False
    def update_visibility(self):
        # Ensure that the squares directly adjacent to the player are visible.
        for loc in self.get_neighbors(self.player_loc):
            self.visibility[loc[1]][loc[0]] = True
        bfs = collections.deque()
        for y in range(0, self.height):
            for x in range(0, self.width):
                if self.visibility[y][x]:
                    bfs.appendleft((x, y))
        while len(bfs) > 0:
            # We're going to use an additional value, -1, to mark tiles we've visited and confirmed are invisible this turn.
            loc = bfs.pop()
            for n in self.get_neighbors(loc):
                if self.visibility[n[1]][n[0]] == False:
                    if self.test_visible(n):
                        self.visibility[n[1]][n[0]] = True
                        bfs.appendleft(n)
                    else:
                        self.visibility[n[1]][n[0]] = -1
        for y in range(0, self.height):
            for x in range(0, self.width):
                if self.visibility[y][x] == -1:
                    self.visibility[y][x] = False
    def serialize(self):
        grid = []
        for y in range(0, self.height):
            row = []
            for x in range(0, self.width):
                if self.visibility[y][x]:
                    row.append(self.contents[y][x])
                else:
                    row.append(UNKNOWN)
            grid.append(row)
        return json.dumps(grid)

MAX_SEC = 60

m = Map(5, 5, 0)
start_time = time.time();
game_over = False
while not game_over:
    m.update_visibility()
    send_string(m.serialize())
    try:
        move = get_move(MAX_SEC + start_time - time.time())
        game_over = m.make_move(move)
    except Exception:
        print(-1)
        sys.exit(0)
print(time.time() - start_time)
