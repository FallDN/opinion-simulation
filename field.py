import cv2
import numpy as np
from random import randint

class Field():
    def __init__(self, field, shape, opinion_matrix):
        
        self.shape = shape
        if opinion_matrix is not None and opinion_matrix.shape == shape:
            self.opinion_matrix = opinion_matrix
        else:
            self.opinion_matrix = np.ones(shape)

        if field is not None and field.shape == shape:
            self.field = field
        else:
            self.field = np.random.choice([0, 1], size=shape)

    def life_cycle(self, w):
        new_field = self.field.copy()

        for i in range(self.shape[0]):
            for j in range(self.shape[1]):

                if self.opinion_matrix[i,j] == 2:
                    continue

                neighbours = self.get_cell_neighbours((i, j))

                d = randint(1, w)
                if d <= sum(neighbours):
                    if self.opinion_matrix[i, j] == 0:
                        new_field[i, j] = 1
                    else:
                        new_field[i, j] = 0
                else:
                    if self.opinion_matrix[i, j] == 0:
                        new_field[i, j] = 0
                    else:
                        new_field[i, j] = 1

        self.field = new_field

    def plot(self, cell_size):
        
        grid = self.field
        grid_size = self.shape
        image = np.zeros((grid_size[0]*cell_size, grid_size[1]*cell_size, 3), np.uint8)

        for x in range(0, grid_size[1] * cell_size, cell_size):
            cv2.line(image, (x, 0), (x, grid_size[0] * cell_size), (255, 255, 255))
        for y in range(0, grid_size[0] * cell_size, cell_size):
            cv2.line(image, (0, y), (grid_size[1] * cell_size, y), (255, 255, 255))


        for y in range(grid_size[0]):
            for x in range(grid_size[1]):
                if self.opinion_matrix[y, x] != 2:
                    if grid[y, x] == 1:
                        cv2.rectangle(image, (x*cell_size, y*cell_size), ((x+1)*cell_size, (y+1)*cell_size), (255, 255, 255), -1)
                else:
                    
                    if grid[y, x] == 1:
                        cv2.rectangle(image, (x*cell_size, y*cell_size), ((x+1)*cell_size, (y+1)*cell_size), (0, 255, 0), -1)
                    elif grid[y, x] == 0:
                        cv2.rectangle(image, (x*cell_size, y*cell_size), ((x+1)*cell_size, (y+1)*cell_size), (0, 0, 255), -1)

        return image


    def calculate_stat(self):
        n_whites = np.count_nonzero(self.field == 1)
        return n_whites / (self.shape[0]**2)
    

class Ring(Field):
    def __init__(self, field, shape, opinion_matrix):
        super().__init__(field, shape, opinion_matrix)
        
    def get_cell_neighbours(self, pos):
        neighbours = []
        for i in np.array((pos[0] - 1, pos[0], pos[0] + 1)):
            for j in np.array((pos[1] - 1, pos[1], pos[1] + 1)):
                neighbours.append(self.field[i % self.shape[0], j%self.shape[1]])
        return neighbours

    def life_cycle(self):
        super().life_cycle(8)


class Cross(Field):
    def __init__(self, field, shape, opinion_matrix):
        super().__init__(field, shape, opinion_matrix)
        
    def get_cell_neighbours(self, pos: tuple) -> list:
        neighbours = []
        neighbour_rows = np.array((pos[0] - 1, pos[0] + 1))
        neighbour_columns = np.array((pos[1] - 1, pos[1] + 1))
        for row in neighbour_rows:
            neighbours.append(self.field[row % self.shape[0], pos[1]])
        for col in neighbour_columns:
            neighbours.append(self.field[pos[0], col  % self.shape[1]])
        return neighbours

    def life_cycle(self):
        super().life_cycle(4)


        
