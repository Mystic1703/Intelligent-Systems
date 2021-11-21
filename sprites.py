import pygame
import os
import config
import math

class BaseSprite(pygame.sprite.Sprite):
    images = dict()

    def __init__(self, row, col, file_name, transparent_color=None):
        pygame.sprite.Sprite.__init__(self)
        if file_name in BaseSprite.images:
            self.image = BaseSprite.images[file_name]
        else:
            self.image = pygame.image.load(os.path.join(config.IMG_FOLDER, file_name)).convert()
            self.image = pygame.transform.scale(self.image, (config.TILE_SIZE, config.TILE_SIZE))
            BaseSprite.images[file_name] = self.image
        # making the image transparent (if needed)
        if transparent_color:
            self.image.set_colorkey(transparent_color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (col * config.TILE_SIZE, row * config.TILE_SIZE)
        self.row = row
        self.col = col


class Agent(BaseSprite):
    def __init__(self, row, col, file_name):
        super(Agent, self).__init__(row, col, file_name, config.DARK_GREEN)

    def move_towards(self, row, col):
        row = row - self.row
        col = col - self.col
        self.rect.x += col
        self.rect.y += row

    def place_to(self, row, col):
        self.row = row
        self.col = col
        self.rect.x = col * config.TILE_SIZE
        self.rect.y = row * config.TILE_SIZE

    # game_map - list of lists of elements of type Tile
    # goal - (row, col)
    # return value - list of elements of type Tile
    def get_agent_path(self, game_map, goal):
        pass

    def calculate_heuristic(self, current_field, heuristic_map):
        pass

    def reconstruct_path(self, goal_field, field_pair):
        curr_field = goal_field
        path = []
        while curr_field.row != self.row or curr_field.col != self.col:
            path.append(curr_field)
            for f in field_pair:
                if f[0] == curr_field:
                    curr_field = f[1]
                    break
        path.append(curr_field)
        path.reverse()
        return path




class ExampleAgent(Agent):
    def __init__(self, row, col, file_name):
        super().__init__(row, col, file_name)

    def get_agent_path(self, game_map, goal):
        path = [game_map[self.row][self.col]]

        row = self.row
        col = self.col
        while True:
            if row != goal[0]:
                row = row + 1 if row < goal[0] else row - 1
            elif col != goal[1]:
                col = col + 1 if col < goal[1] else col - 1
            else:
                break
            path.append(game_map[row][col])
        return path

class Aki(Agent):

    def __init__(self, row, col, file_name):
        super().__init__(row, col, file_name)

    def get_agent_path(self, game_map, goal):
        row = self.row
        col = self.col
        queue = [(game_map[row][col].cost(), game_map[row][col], None)]
        visited_fields = set()
        field_pair = []

        while len(queue) > 0:
            neighbors = []
            field = queue.pop(0)
            if field[1] in visited_fields:
                continue
            visited_fields.add(field[1])
            field_pair.append((field[1], field[2]))

            if field[1].row == goal[0] and field[1].col == goal[1]:
                curr_field = field[1]
                return self.reconstruct_path(field[1], field_pair)

            row = field[1].row
            col = field[1].col
            if row - 1 >= 0:
                cost = game_map[row - 1][col].cost()
                neighbors.append((cost, game_map[row - 1][col], game_map[row][col]))
            if col + 1 < len(game_map[0]):
                cost = game_map[row][col + 1].cost()
                neighbors.append((cost, game_map[row][col + 1], game_map[row][col]))
            if row + 1 < len(game_map):
                cost = game_map[row + 1][col].cost()
                neighbors.append((cost, game_map[row + 1][col], game_map[row][col]))
            if col - 1 >= 0:
                cost = game_map[row][col - 1].cost()
                neighbors.append((cost, game_map[row][col - 1], game_map[row][col]))
            neighbors = sorted(neighbors, key= lambda x: x[0])
            queue = neighbors + queue



class Jocke(Agent):

    def __init__(self, row, col, file_name):
        super().__init__(row, col, file_name)

    def get_agent_path(self, game_map, goal):
        row = self.row
        col = self.col
        path = []
        visited_fields = set()
        field_pair = []
        queue = [(0, game_map[row][col], None)] # heuristic, order of expansion, field, parent field
        while len(queue) > 0:
            neighbors = []
            field = queue.pop(0)
            if field[1] not in visited_fields:
                visited_fields.add(field[1])
                field_pair.append((field[1], field[2]))
                if field[1].row == goal[0] and field[1].col == goal[1]:
                    return self.reconstruct_path(field[1], field_pair)

                row = field[1].row
                col = field[1].col
                if row - 1 >= 0:
                    if game_map[row - 1][col] not in visited_fields:
                        heuristic = game_map[row - 1][col].calculate_bfs_heuristic(game_map[row][col], game_map)
                        neighbors.append((heuristic, game_map[row - 1][col], game_map[row][col]))
                if col + 1 < len(game_map[0]):
                    if game_map[row][col + 1] not in visited_fields:
                        heuristic = game_map[row][col + 1].calculate_bfs_heuristic(game_map[row][col], game_map)
                        neighbors.append((heuristic, game_map[row][col + 1], game_map[row][col]))
                if row + 1 < len(game_map):
                    if game_map[row + 1][col] not in visited_fields:
                        heuristic = game_map[row + 1][col].calculate_bfs_heuristic(game_map[row][col], game_map)
                        neighbors.append((heuristic, game_map[row + 1][col], game_map[row][col]))
                if col - 1 >= 0:
                    if game_map[row][col - 1] not in visited_fields:
                        heuristic = game_map[row][col - 1].calculate_bfs_heuristic(game_map[row][col], game_map)
                        neighbors.append((heuristic, game_map[row][col - 1], game_map[row][col]))
                neighbors = sorted(neighbors, key= lambda x: x[0])
                for n in neighbors:
                    queue.append(n)

class Bole(Agent):

    def __init__(self, row, col, file_name):
        super().__init__(row, col, file_name)

    def calculate_heuristic(self, cost, current_field, heuristic_map):
        return cost + heuristic_map[current_field[2].row][current_field[2].col]

    def find_neighbors(self, game_map, current_field, checked_fields, heuristic_map):
        neighbors = []
        field = current_field[2]
        row = field.row
        col = field.col
        row_count = len(game_map)
        col_count = len(game_map[0])
        if row - 1 >= 0:
            if game_map[row - 1][col] not in checked_fields:
                cost = current_field[0] + field.cost()
                heuristic = self.calculate_heuristic(cost, current_field, heuristic_map)
                neighbors.append((cost, heuristic, game_map[row - 1][col], game_map[row][col]))
        if row + 1 < row_count:
            if game_map[row + 1][col] not in checked_fields:
                cost = current_field[0] + field.cost()
                heuristic = self.calculate_heuristic(cost, current_field, heuristic_map)
                neighbors.append((cost, heuristic, game_map[row + 1][col], game_map[row][col]))
        if col - 1 >= 0:
            if game_map[row][col - 1] not in checked_fields:
                cost = current_field[0] + field.cost()
                heuristic = self.calculate_heuristic(cost, current_field, heuristic_map)
                neighbors.append((cost, heuristic, game_map[row][col - 1], game_map[row][col]))
        if col + 1 < col_count:
            if game_map[row][col + 1] not in checked_fields:
                cost = current_field[0] + field.cost()
                heuristic = self.calculate_heuristic(cost, current_field, heuristic_map)
                neighbors.append((cost, heuristic, game_map[row][col + 1], game_map[row][col]))
        return neighbors

    def get_agent_path(self, game_map, goal):
        heuristic_map = Bole.form_heuristic_map(game_map, goal)
        row = self.row
        col = self.col
        queue = [(0, heuristic_map[row][col], game_map[row][col], None)] #cost, heuristic_for_field, field, parent
        checked_fields = set()
        field_pairs = []
        path = []
        while len(queue) > 0:
            field = queue.pop(0)
            if field[2] in checked_fields:
                continue
            field_pairs.append((field[2], field[3]))
            checked_fields.add(field[2])
            if field[2].row == goal[0] and field[2].col == goal[1]:
                return self.reconstruct_path(field[2], field_pairs)

            neighbors = self.find_neighbors(game_map, field, checked_fields, heuristic_map)
            for n in neighbors:
                queue.append(n)
            queue.sort(key= lambda x: x[1])
    @staticmethod
    def form_heuristic_map(game_map, goal):
        row = goal[0]
        col = goal[1]
        map = []
        for i in range(0, len(game_map), 1):
            map.append([])
            for j in range(0, len(game_map[0]), 1):
                dist = (row - i) ** 2 + (col - j) ** 2
                map[i].append(math.sqrt(dist))
        return map



class Draza(Agent):

    def __init__(self, row, col, file_name):
        super().__init__(row, col, file_name)

    def calculate_heuristic(self, current_field):
        return current_field[1] + 1

    def find_neighbors(self, game_map, current_field, checked_fields):
        neighbors = []
        field = current_field[2]
        row = field.row
        col = field.col
        row_count = len(game_map)
        col_count = len(game_map[0])
        if row - 1 >= 0:
            if game_map[row - 1][col] not in checked_fields:
                cost = current_field[0] + field.cost()
                heuristic = self.calculate_heuristic(current_field)
                neighbors.append((cost, heuristic, game_map[row - 1][col], game_map[row][col]))
        if row + 1 < row_count:
            if game_map[row + 1][col] not in checked_fields:
                cost = current_field[0] + field.cost()
                heuristic = self.calculate_heuristic(current_field)
                neighbors.append((cost, heuristic, game_map[row + 1][col], game_map[row][col]))
        if col - 1 >= 0:
            if game_map[row][col - 1] not in checked_fields:
                cost = current_field[0] + field.cost()
                heuristic = self.calculate_heuristic(current_field)
                neighbors.append((cost, heuristic, game_map[row][col - 1], game_map[row][col]))
        if col + 1 < col_count:
            if game_map[row][col + 1] not in checked_fields:
                cost = current_field[0] + field.cost()
                heuristic = self.calculate_heuristic(current_field)
                neighbors.append((cost, heuristic, game_map[row][col + 1], game_map[row][col]))
        return neighbors

    def get_agent_path(self, game_map, goal):
        row = self.row
        col = self.col
        path = []
        queue = [(0, 0, game_map[row][col], None)] # current cost - field before - current field - parent field
        checked_fields = set()
        field_pairs = []
        while len(queue) > 0:
            field = queue.pop(0)
            if field[2] in checked_fields:
                continue
            field_pairs.append((field[2], field[3]))
            checked_fields.add(field[2])
            if field[2].row == goal[0] and field[2].col == goal[1]:
                return self.reconstruct_path(field[2], field_pairs)

            neighbors = self.find_neighbors(game_map, field, checked_fields)
            for n in neighbors:
                queue.append(n)
            queue = sorted(queue, key= lambda x: (x[0], x[1]))


class Tile(BaseSprite):
    def __init__(self, row, col, file_name):
        super(Tile, self).__init__(row, col, file_name)

    def position(self):
        return self.row, self.col

    def cost(self):
        pass

    def kind(self):
        pass

    def calculate_bfs_heuristic(self, current_tile, game_map):
        cost = 0
        neighbor_tiles_count = 0
        row_count = len(game_map)
        col_count = len(game_map[0])
        if self.row - 1 >= 0:
            if game_map[self.row - 1][self.col] != current_tile:
                cost += game_map[self.row - 1][self.col].cost()
                neighbor_tiles_count += 1
        if self.row + 1 < row_count:
            if game_map[self.row + 1][self.col] != current_tile:
                cost += game_map[self.row + 1][self.col].cost()
                neighbor_tiles_count += 1
        if self.col - 1 >= 0:
            if game_map[self.row][self.col - 1] != current_tile:
                cost += game_map[self.row][self.col - 1].cost()
                neighbor_tiles_count += 1
        if self.col + 1 < col_count:
            if game_map[self.row][self.col + 1] != current_tile:
                cost += game_map[self.row][self.col + 1].cost()
                neighbor_tiles_count += 1
        if neighbor_tiles_count == 0:
            return -1
        else:
            return cost / neighbor_tiles_count

    @staticmethod
    def check_bounds(row, col, game_map):
        if 0 <= row < len(game_map) and 0 <= col < len(game_map[0]):
            return True
        else:
            return False


class Stone(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'stone.png')

    def cost(self):
        return 1000

    def kind(self):
        return 's'


class Water(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'water.png')

    def cost(self):
        return 500

    def kind(self):
        return 'w'


class Road(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'road.png')

    def cost(self):
        return 2

    def kind(self):
        return 'r'


class Grass(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'grass.png')

    def cost(self):
        return 3

    def kind(self):
        return 'g'


class Mud(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'mud.png')

    def cost(self):
        return 5

    def kind(self):
        return 'm'


class Dune(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'dune.png')

    def cost(self):
        return 7

    def kind(self):
        return 's'


class Goal(BaseSprite):
    def __init__(self, row, col):
        super().__init__(row, col, 'x.png', config.DARK_GREEN)


class Trail(BaseSprite):
    def __init__(self, row, col, num):
        super().__init__(row, col, 'trail.png', config.DARK_GREEN)
        self.num = num

    def draw(self, screen):
        text = config.GAME_FONT.render(f'{self.num}', True, config.WHITE)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)
