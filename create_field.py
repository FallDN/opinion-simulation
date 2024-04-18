import cv2
import numpy as np
import json
import os

def custom_callback(clicked_points, image, cell_size, window_name):
    def mouse_callback(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            cell_x = x // cell_size
            cell_y = y // cell_size
            clicked_points.append((cell_x, cell_y))
            cv2.rectangle(image, (cell_x*cell_size, cell_y*cell_size), ((cell_x+1)*cell_size, (cell_y+1)*cell_size), (255, 255, 255), -1)
            cv2.imshow(window_name, image)
    return mouse_callback

def create_fixed_cells(
        grid_size,
        lower_n_positive=2,
        upper_n_positive=10,
        lower_n_negative=2,
        upper_n_negative=10
        ):
    
    num_pairs1 = np.random.randint(lower_n_positive, upper_n_positive)

    random_indices1 = set()

    while len(random_indices1) < num_pairs1:
        inds = tuple([int(x) for x in np.random.choice(grid_size[0], 2, replace=False).astype(int)])
        random_indices1.add(inds)

    num_pairs2 = np.random.randint(lower_n_negative, upper_n_negative)
    random_indices2 = set()

    while len(random_indices2) < num_pairs2:
        inds = tuple([int(x) for x in np.random.choice(grid_size[0], 2, replace=False).astype(int)])
        random_indices2.add(inds)
    
    fixed_cells = {
        1: [list(i) for i in random_indices1],
        0: [list(i) for i in random_indices2]
        }
    return fixed_cells

def create_field(
        grid_size,
        cell_size,
        window_name='my game'
        ):

    clicked_points = []

    image = np.zeros((grid_size[0]*cell_size, grid_size[1]*cell_size, 3), np.uint8) * 255

    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    for x in range(0, grid_size[1] * cell_size, cell_size):
        cv2.line(image, (x, 0), (x, grid_size[0] * cell_size), (255, 255, 255))
    for y in range(0, grid_size[0] * cell_size, cell_size):
        cv2.line(image, (0, y), (grid_size[1] * cell_size, y), (255, 255, 255))

    grid = np.zeros(grid_size, dtype=int)

    for y in range(grid_size[0]):
        for x in range(grid_size[1]):
            if grid[y, x] == 1:
                cv2.rectangle(image, (x*cell_size, y*cell_size), ((x+1)*cell_size, (y+1)*cell_size), (255, 255, 255), -1)
    
    cv2.namedWindow(window_name)
    cv2.setMouseCallback(window_name, custom_callback(
        clicked_points=clicked_points,
        image=image,
        cell_size=cell_size,
        window_name=window_name
        ))

    cv2.imshow(window_name, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    for point in clicked_points:
        grid[point[1], point[0]] = 1

    return grid
