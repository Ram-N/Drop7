
import numpy as np
import random

import cfg
from game_log import _Stats

from grid_utils import apply_gravity_to_column 
from grid_utils import update_grid	




def generate_init_grid(_SIZE):
    '''
    drop-7 starting grid with a few rules.
    
    Explode as needed (vertical)
    Explode as needed (horizontal)
    '''
    grid = np.zeros((_SIZE, _SIZE), dtype=np.int) # Example array
    
    for x in np.nditer(grid, op_flags=['readwrite']):
        #generate a U(0,1). If it is less than _fraction, then get a random integer from 1..7
        if random.random() <= random.uniform(cfg._FRACTION[0], cfg._FRACTION[1]):
            x[...] = random.randint(1, _SIZE) #ellipsis will modify the right element
    
    #apply gravity to each column
    for colnum in range(grid.shape[1]):
        _,_, new = apply_gravity_to_column(grid[:, colnum])
        grid[ :, colnum] = new

    s = _Stats
    update_grid(grid, s)
    s.reset(cfg._outfile)

    return grid



def row(grid, rnum, _string):
    grid[cfg._SIZE-1-rnum, :] = list(_string)
    return grid
    
def zerow(grid, rnum):
    grid[cfg._SIZE-1-rnum,:] = list('0')*cfg._SIZE

def zecol(grid, cnum):
    grid[:, cnum] = list('0')*cfg._SIZE

def grid_of_zeros(size=cfg._SIZE):
    return np.zeros((size,size), dtype=np.int)



def generate_next_ball(size):
    return random.randint(1,size)


def generate_random_row(_size):
    return np.random.randint(low=1, high=_size+1, size=(1, _size))


def generate_fixed_row(_size, fixed_num):
	return np.asarray([fixed_num,]*_size)


def top_row_occupied(grid):
    return np.count_nonzero(grid[0, :])

def level_up(grid):
    '''
    Add a row of balls to the bottom of the grid.
    If the top row has any ball, Game Over

    Note that when the balls are first surfaced, they are all -2. (meaning doubly hidden)
    The first explosion exposes them onnce to -1.
    Second neigboring explosion makes them the Original value.
    '''
    # if top row has something, return grid and gameover
    if(top_row_occupied(grid)):
        return grid, 1 #game over
        
        
    original = grid.copy()
    for i in range(cfg._SIZE - 1):
        grid[i, :] = original[i+1, :] # move the row up
        

    grid[-1, : ] = generate_random_row(cfg._SIZE)
    grid[-1, : ] = generate_fixed_row(cfg._SIZE, -2)

    return grid, 0 #game is not over

